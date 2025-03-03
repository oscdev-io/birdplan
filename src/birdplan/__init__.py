#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2024, AllWorldIT
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""BirdPlan package."""

# pylint: disable=too-many-lines

import grp
import json
import os
import pathlib
import pwd
from typing import Any, Dict, Optional

import birdclient
import jinja2
import packaging.version

from .bird_config import BirdConfig
from .bird_config.sections.protocols.bgp.bgp_config_parser import BGPConfigParser
from .bird_config.sections.protocols.ospf.ospf_config_parser import OSPFConfigParser
from .bird_config.sections.protocols.rip.rip_config_parser import RIPConfigParser
from .exceptions import BirdPlanError
from .version import __version__
from .yaml import YAML, YAMLError

__all__ = [
    "BirdPlan",
    "__version__",
]

# Some types we need
BirdPlanBGPPeerSummary = dict[str, dict[str, Any]]
BirdPlanBGPPeerShow = dict[str, Any]
BirdPlanBGPPeerGracefulShutdownStatus = dict[str, dict[str, bool]]
BirdPlanBGPPeerQuarantineStatus = dict[str, dict[str, bool]]
BirdPlanOSPFInterfaceStatus = dict[str, dict[str, dict[str, Any]]]
BirdPlanOSPFSummary = dict[str, dict[str, Any]]

# Check we have a sufficiently new version of birdclient
if packaging.version.parse(birdclient.__version__) < packaging.version.parse("0.0.11"):
    raise BirdPlanError("BirdPlan requires birdclient version 0.0.11 or newer")


class BirdPlan:  # pylint: disable=too-many-public-methods
    """Main BirdPlan class."""

    _birdconf: BirdConfig
    _config: dict[str, Any]
    _state_file: str | None
    _yaml: YAML

    def __init__(self, test_mode: bool = False) -> None:
        """Initialize object."""

        self._birdconf = BirdConfig(test_mode=test_mode)
        self._config = {}
        self._state_file = None
        self._yaml = YAML()

    def load(self, **kwargs: Any) -> None:  # pylint: disable=too-many-locals
        """
        Initialize object.

        Parameters
        ----------
        plan_file : str
            Source plan file to generate configuration from.

        state_file : Optional[str]
            Optional state file, used for commands like BGP graceful shutdown.

        ignore_irr_changes : bool
            Optional parameter to ignore IRR lookups during configuration load.

        ignore_peeringdb_changes : bool
            Optional parameter to ignore peering DB lookups during configuraiton load.

        use_cached : bool
            Optional parameter to use cached values from state during configuration load.

        """

        # Grab parameters
        plan_file: str | None = kwargs.get("plan_file")
        state_file: str | None = kwargs.get("state_file")
        ignore_irr_changes: bool = kwargs.get("ignore_irr_changes", False)
        ignore_peeringdb_changes: bool = kwargs.get("ignore_peeringdb_changes", False)
        use_cached: bool = kwargs.get("use_cached", False)

        # Make sure we have the parameters we need
        if not plan_file:
            raise BirdPlanError("Required parameter 'plan_file' not found")

        # Create search paths for Jinja2
        search_paths = [os.path.dirname(plan_file)]
        # We need to pass Jinja2 our filename, as it is in the search path
        plan_file_fname = os.path.basename(plan_file)

        # Render first with jinja
        template_env = jinja2.Environment(  # nosec
            loader=jinja2.FileSystemLoader(searchpath=search_paths),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Check if we can load the configuration
        try:
            raw_config = template_env.get_template(plan_file_fname).render()
        except jinja2.TemplateError as err:
            raise BirdPlanError(f"Failed to template BirdPlan configuration file '{plan_file}': {err}") from None

        # Load configuration using YAML
        try:
            self.config = self.yaml.load(raw_config)
        except YAMLError as err:  # pragma: no cover
            raise BirdPlanError(f" Failed to parse BirdPlan configuration in '{plan_file}': {err}") from None

        # Set our state file and load state
        self.state_file = state_file
        self.load_state()

        # Make sure we have configuration...
        if not self.config:
            raise BirdPlanError("No configuration found")

        # Check configuration options are supported
        for config_item in self.config:
            if config_item not in ("router_id", "kernel", "log_file", "debug", "static", "export_kernel", "bgp", "rip", "ospf"):
                raise BirdPlanError(f"The config item '{config_item}' is not supported")

        # Setup globals we need
        self.birdconf.birdconfig_globals.ignore_irr_changes = ignore_irr_changes
        self.birdconf.birdconfig_globals.ignore_peeringdb_changes = ignore_peeringdb_changes
        self.birdconf.birdconfig_globals.use_cached = use_cached

        # Configure sections
        self._config_global()
        self._config_kernel()
        self._config_static()
        self._config_export_kernel()

        rip_parser = RIPConfigParser(self.birdconf)
        rip_parser.parse(self.config)

        ospf_parser = OSPFConfigParser(self.birdconf)
        ospf_parser.parse(self.config)

        bgp_parser = BGPConfigParser(self.birdconf)
        bgp_parser.parse(self.config)

    def configure(self) -> str:
        """
        Create BIRD configuration.

        Returns
        -------
            str : Bird configuration as a string.

        """
        return "\n".join(self.birdconf.get_config())

    def commit_state(self) -> None:
        """Commit our current state."""

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Commit of BirdPlan state requires a state file, none loaded")

        # Try get user and group ID's
        try:
            birdplan_uid = pwd.getpwnam("birdplan").pw_uid
        except KeyError:
            birdplan_uid = None
        try:
            birdplan_gid = grp.getgrnam("birdplan").gr_gid
        except KeyError:
            birdplan_gid = None

        # Write out state file
        try:
            fd = os.open(self.state_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o640)
            # Chown the file if we have the user and group ID's
            if birdplan_uid and birdplan_gid:
                os.fchown(fd, birdplan_uid, birdplan_gid)
            # Open for writing
            with os.fdopen(fd, "w") as file:
                file.write(json.dumps(self.state))
        except OSError as err:  # pragma: no cover
            raise BirdPlanError(f"Failed to open '{self.state_file}' for writing: {err}") from None

    def load_state(self) -> None:
        """Load our state."""

        # Clear state
        self.state = {}

        # Skip if we don't have a state file
        if not self.state_file:
            return

        # Check if the state file exists...
        if os.path.isfile(self.state_file):
            # Read in state file
            try:
                self.state = json.loads(pathlib.Path(self.state_file).read_text(encoding="UTF-8"))
            except OSError as err:
                raise BirdPlanError(f"Failed to read BirdPlan state file '{self.state_file}': {err}") from None
            except json.JSONDecodeError as err:  # pragma: no cover
                # We use the state_file here because the size of raw_state may be larger than 100MiB
                raise BirdPlanError(f" Failed to parse BirdPlan state file '{self.state_file}': {err}") from None

    def state_ospf_summary(self, bird_socket: str | None = None) -> BirdPlanOSPFSummary:
        """
        Return OSPF summary.

        Returns
        -------
        BirdPlanOSPFSummary
            Dictionary containing the OSPF summary.

            eg.
            {
                'name1': {
                    'channel': ...,
                    'info': ...,
                    'input_filter': ...,
                    'name': ...,
                    'output_filter': ...,
                    'preference': ...,
                    'proto': ...,
                    'routes_exported': ...,
                    'routes_imported': ...,
                    'since': ...,
                    'state': ...
                    'table': ...,
                }
                'name2': {
                    ...,
                }
            }

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of OSPF summary requires a state file, none loaded")

        # Initialize our return structure
        ret: BirdPlanOSPFSummary = {}

        # Return if we don't have any BGP state
        if "ospf" not in self.state:
            return ret

        # Query bird client for the current protocols
        birdc = birdclient.BirdClient(control_socket=bird_socket)
        bird_protocols = birdc.show_protocols()

        for name, data in bird_protocols.items():
            if data["proto"] != "OSPF":
                continue
            ret[name] = data

        return ret

    def state_bgp_peer_summary(self, bird_socket: str | None = None) -> BirdPlanBGPPeerSummary:
        """
        Return BGP peer summary.

        Returns
        -------
        BirdPlanBGPPeerStatus
            Dictionary containing the BGP peer summary.

            eg.
            {
                'peer1': {
                    'name': ...,
                    'asn': ...,
                    'description': ...,
                    'protocols': {
                        'ipv4': ...,
                        'ipv6': ...,
                    }
                }
                'peer2': {
                    ...,
                }
            }

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP peer summary requires a state file, none loaded")

        # Initialize our return structure
        ret: BirdPlanBGPPeerSummary = {}

        # Return if we don't have any BGP state
        if "bgp" not in self.state:
            return ret

        # Query bird client for the current protocols
        birdc = birdclient.BirdClient(control_socket=bird_socket)
        bird_protocols = birdc.show_protocols()

        # Check if we have any peers in our state
        if "peers" in self.state["bgp"]:
            # If we do loop with them
            for peer, peer_state in self.state["bgp"]["peers"].items():
                # Start with a clear status
                ret[peer] = {
                    "name": peer,
                    "asn": peer_state["asn"],
                    "description": peer_state["description"],
                    "protocols": peer_state["protocols"],
                }

                # Next loop through each protocol
                for ipv, peer_state_protocol in peer_state["protocols"].items():
                    # If we don't have a live session, skip adding it
                    if peer_state_protocol["name"] not in bird_protocols:
                        continue
                    # Set protocol name
                    ret[peer]["protocols"][ipv]["protocol"] = ipv
                    # But if we do, add it
                    ret[peer]["protocols"][ipv]["status"] = bird_protocols[peer_state_protocol["name"]]

        return ret

    def state_bgp_peer_show(self, peer: str, bird_socket: str | None = None) -> BirdPlanBGPPeerShow:
        """
        Return the status of a specific BGP peer.

        Returns
        -------
        BirdPlanBGPPeerShow
            Dictionary containing the status of a BGP peer.

            eg.
            {
                'asn': ...,
                'description': ...,
                'protocols': {
                    'ipv4': {
                        ...,
                        'status': ...,
                    }
                    'ipv6': ...,
                },
            }

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP peer show requires a state file, none loaded")

        # Return if we don't have any BGP state
        if "bgp" not in self.state:
            raise BirdPlanError("No BGP state found")
        # Check if the configured state has this peer, if not return
        if peer not in self.state["bgp"]["peers"]:
            raise BirdPlanError(f"BGP peer '{peer}' not found in configured state")

        # Make things easier below
        configured = self.state["bgp"]["peers"][peer]

        # Set our peer info to the configured state
        ret: BirdPlanBGPPeerShow = configured

        # Add peer name
        ret["name"] = peer

        # Query bird client for the current protocols
        birdc = birdclient.BirdClient(control_socket=bird_socket)

        # Loop with protocols and grab live bird status
        for ipv, protocol_info in configured["protocols"].items():
            bird_state = birdc.show_protocol(protocol_info["name"])
            # Skip if we have no bird state
            if not bird_state:
                continue
            # Set the protocol status
            ret["protocols"][ipv]["status"] = bird_state

        return ret

    def state_bgp_peer_graceful_shutdown_set(self, peer: str, value: bool) -> None:
        """
        Set the BGP graceful shutdown override state for a peer.

        Parameters
        ----------
        peer : str
            Peer name to set to BGP graceful shutdown state for.
            Pattern matches can be specified with '*'.

        value : bool
            State of the graceful shutdown option for this peer.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP graceful shutdown override requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state:
            self.state["bgp"] = {}

        # Make sure we have the global setting
        if "+graceful_shutdown" not in self.state["bgp"]:
            self.state["bgp"]["+graceful_shutdown"] = {}
        # Set the global setting for this pattern
        self.state["bgp"]["+graceful_shutdown"][peer] = value

    def state_bgp_peer_graceful_shutdown_remove(self, peer: str) -> None:
        """
        Remove a BGP graceful shutdown override flag from a peer or pattern.

        Parameters
        ----------
        peer : str
            Peer name or pattern to remove the BGP graceful shutdown override flag from.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP graceful shutdown override requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state:
            return

        # Remove from the global settings
        if "+graceful_shutdown" in self.state["bgp"]:
            # Check it exists first, if not raise an exception
            if peer not in self.state["bgp"]["+graceful_shutdown"]:
                raise BirdPlanError(f"BGP peer '{peer}' graceful shutdown override not found")
            # Remove peer from graceful shutdown list
            del self.state["bgp"]["+graceful_shutdown"][peer]
            # If the result is an empty dict, just delete it too
            if not self.state["bgp"]["+graceful_shutdown"]:
                del self.state["bgp"]["+graceful_shutdown"]

    def state_bgp_peer_graceful_shutdown_status(self) -> BirdPlanBGPPeerGracefulShutdownStatus:
        """
        Return the status of BGP peer graceful shutdown.

        Returns
        -------
        BirdPlanBGPPeerGracefulShutdownStatus
            Dictionary containing the status of overrides and peers.

            eg.
            {
                'overrides': {
                    'p*': True,
                    'peer1': False,
                }
                'current': {
                    'peer1': False,
                }
                'pending': {
                    'peer1': False,
                }
            }

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP graceful shutdown override requires a state file, none loaded")

        # Initialize our return structure
        ret: BirdPlanBGPPeerGracefulShutdownStatus = {
            "overrides": {},
            "current": {},
            "pending": {},
        }

        # Return if we don't have any BGP state
        if "bgp" not in self.state:
            return ret

        # Pull in any overrides we may have
        if "+graceful_shutdown" in self.state["bgp"]:
            ret["overrides"] = self.state["bgp"]["+graceful_shutdown"]

        # Check if we have any peers in our state
        if "peers" in self.state["bgp"]:
            # If we do loop with them
            for peer, peer_state in self.state["bgp"]["peers"].items():
                # And check if they have a graceful shutdown state or not
                ret["current"][peer] = peer_state.get("graceful_shutdown", False)

        # Generate the override status as if we were doing a configure
        for peer in self.birdconf.protocols.bgp.peers:
            ret["pending"][peer] = self.birdconf.protocols.bgp.peer(peer).graceful_shutdown

        return ret

    def state_bgp_peer_quarantine_set(self, peer: str, value: bool) -> None:
        """
        Set the BGP quarantine override state for a peer.

        Parameters
        ----------
        peer : str
            Peer name to set to BGP quarantine state for.
            Pattern matches can be specified with '*'.

        value : bool
            State of the quarantine option for this peer.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP quarantine override requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state:
            self.state["bgp"] = {}

        # Make sure we have the global setting
        if "+quarantine" not in self.state["bgp"]:
            self.state["bgp"]["+quarantine"] = {}
        # Set the global setting for this pattern
        self.state["bgp"]["+quarantine"][peer] = value

    def state_bgp_peer_quarantine_remove(self, peer: str) -> None:
        """
        Remove a BGP quarantine override flag from a peer or pattern.

        Parameters
        ----------
        peer : str
            Peer name or pattern to remove the BGP quarantine override flag from.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP quarantine override requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state:
            return

        # Remove from the global settings
        if ("+quarantine" not in self.state["bgp"]) or (peer not in self.state["bgp"]["+quarantine"]):
            raise BirdPlanError(f"BGP peer '{peer}' quarantine override not found")

        # Remove peer from quarantine list
        del self.state["bgp"]["+quarantine"][peer]
        # If the result is an empty dict, just delete it too
        if not self.state["bgp"]["+quarantine"]:
            del self.state["bgp"]["+quarantine"]

    def state_bgp_peer_quarantine_status(self) -> BirdPlanBGPPeerQuarantineStatus:
        """
        Return the status of BGP peer quarantine.

        Returns
        -------
        BirdPlanBGPPeerQuarantineStatus
            Dictionary containing the status of overrides and peers.

            eg.
            {
                'overrides': {
                    'p*': True,
                    'peer1': False,
                }
                'current': {
                    'peer1': False,
                }
                'pending': {
                    'peer1': False,
                }
            }

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of BGP quarantine override requires a state file, none loaded")

        # Initialize our return structure
        ret: BirdPlanBGPPeerQuarantineStatus = {
            "overrides": {},
            "current": {},
            "pending": {},
        }

        # Return if we don't have any BGP state
        if "bgp" not in self.state:
            return ret

        # Pull in any overrides we may have
        if "+quarantine" in self.state["bgp"]:
            ret["overrides"] = self.state["bgp"]["+quarantine"]

        # Check if we have any peers in our state
        if "peers" in self.state["bgp"]:
            # If we do loop with them
            for peer, peer_state in self.state["bgp"]["peers"].items():
                # And check if they have a quarantine state or not
                ret["current"][peer] = peer_state.get("quarantine", False)

        # Generate the override status as if we were doing a configure
        for peer in self.birdconf.protocols.bgp.peers:
            ret["pending"][peer] = self.birdconf.protocols.bgp.peer(peer).quarantine

        return ret

    def state_ospf_set_interface_cost(self, area: str, interface: str, cost: int) -> None:
        """
        Set an OSPF interface cost override.

        Parameters
        ----------
        area : str
            Interface to set the OSPF cost for.

        interface : str
            Interface to set the OSPF cost for.

        cost : int
            OSPF interface cost.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of OSPF interface cost override requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "ospf" not in self.state:
            self.state["ospf"] = {}
        if "areas" not in self.state["ospf"]:
            self.state["ospf"]["areas"] = {}
        if area not in self.state["ospf"]["areas"]:
            self.state["ospf"]["areas"][area] = {}
        if "+interfaces" not in self.state["ospf"]["areas"][area]:
            self.state["ospf"]["areas"][area]["+interfaces"] = {}
        if interface not in self.state["ospf"]["areas"][area]["+interfaces"]:
            self.state["ospf"]["areas"][area]["+interfaces"][interface] = {}

        # Set the interface cost value
        self.state["ospf"]["areas"][area]["+interfaces"][interface]["cost"] = cost

    def state_ospf_remove_interface_cost(self, area: str, interface: str) -> None:
        """
        Remove an OSPF interface cost override.

        Parameters
        ----------
        area : str
            OSPF area which contains the interface.

        interface : str
            Interface to remove the OSPF cost for.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of OSPF interface cost override requires a state file, none loaded")

        # Check if this cost override exists
        if (  # pylint: disable=too-many-boolean-expressions
            "ospf" not in self.state
            or "areas" not in self.state["ospf"]
            or area not in self.state["ospf"]["areas"]
            or "+interfaces" not in self.state["ospf"]["areas"][area]
            or interface not in self.state["ospf"]["areas"][area]["+interfaces"]
            or "cost" not in self.state["ospf"]["areas"][area]["+interfaces"][interface]
        ):
            raise BirdPlanError(f"OSPF area '{area}' interface '{interface}' cost override not found")

        # Remove OSPF interface cost from state
        del self.state["ospf"]["areas"][area]["+interfaces"][interface]["cost"]
        # Remove hanging data structure endpoint
        if not self.state["ospf"]["areas"][area]["+interfaces"][interface]:
            del self.state["ospf"]["areas"][area]["+interfaces"][interface]
        if not self.state["ospf"]["areas"][area]["+interfaces"]:
            del self.state["ospf"]["areas"][area]["+interfaces"]

    def state_ospf_set_interface_ecmp_weight(self, area: str, interface: str, ecmp_weight: int) -> None:
        """
        Set an OSPF interface ECMP weight override.

        Parameters
        ----------
        area : str
            OSPF area which contains the interface.

        interface : str
            Interface to set the OSPF ECMP weight for.

        ecmp_weight : int
            OSPF interface ECMP weight.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of OSPF interface ECMP weight override requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "ospf" not in self.state:
            self.state["ospf"] = {}
        if "areas" not in self.state["ospf"]:
            self.state["ospf"]["areas"] = {}
        if area not in self.state["ospf"]["areas"]:
            self.state["ospf"]["areas"][area] = {}
        if "+interfaces" not in self.state["ospf"]["areas"][area]:
            self.state["ospf"]["areas"][area]["+interfaces"] = {}
        if interface not in self.state["ospf"]["areas"][area]["+interfaces"]:
            self.state["ospf"]["areas"][area]["+interfaces"][interface] = {}

        # Set the interface ecmp_weight value
        self.state["ospf"]["areas"][area]["+interfaces"][interface]["ecmp_weight"] = ecmp_weight

    def state_ospf_remove_interface_ecmp_weight(self, area: str, interface: str) -> None:
        """
        Remove an OSPF interface ECMP weight override.

        Parameters
        ----------
        area : str
            OSPF area which contains the interface.

        interface : str
            Interface to remove the OSPF ECMP weight for.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of OSPF interface ECMP weight override requires a state file, none loaded")

        # Check if this ECMP weight override exists
        if (  # pylint: disable=too-many-boolean-expressions
            "ospf" not in self.state
            or "areas" not in self.state["ospf"]
            or area not in self.state["ospf"]["areas"]
            or "+interfaces" not in self.state["ospf"]["areas"][area]
            or interface not in self.state["ospf"]["areas"][area]["+interfaces"]
            or "ecmp_weight" not in self.state["ospf"]["areas"][area]["+interfaces"][interface]
        ):
            raise BirdPlanError(f"OSPF area '{area}' interface '{interface}' ECMP weight override not found")

        # Remove OSPF interface ECMP weight from state
        del self.state["ospf"]["areas"][area]["+interfaces"][interface]["ecmp_weight"]
        # Remove hanging data structure endpoint
        if not self.state["ospf"]["areas"][area]["+interfaces"][interface]:
            del self.state["ospf"]["areas"][area]["+interfaces"][interface]
        if not self.state["ospf"]["areas"][area]["+interfaces"]:
            del self.state["ospf"]["areas"][area]["+interfaces"]

    def state_ospf_interface_status(self) -> BirdPlanOSPFInterfaceStatus:  # pylint: disable=too-many-branches
        """
        Return the status of OSPF interfaces.

        Returns
        -------
        BirdPlanOSPFInterfaceStatus
            Dictionary containing the status of overrides and peers.

            eg.
            {
                'overrides': {
                    'areas': {
                        '0': {
                            'interfaces': {
                                'eth0': {
                                    'cost': 10,
                                    'ecmp_weight': 100,
                                }
                            }
                        }
                    }
                },
                'current': {
                    'areas': {
                        '0': {
                            'interfaces': {
                                'eth0': {
                                    'cost': 10,
                                    'ecmp_weight': 100,
                                }
                            }
                        }
                    }
                },
                'pending': {
                    'areas': {
                        '0': {
                            'interfaces': {
                                'eth0': {
                                    'cost': 10,
                                    'ecmp_weight': 100,
                                }
                            }
                        }
                    }
                }
            }

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("The use of OSPF interface override requires a state file, none loaded")

        # Initialize our return structure
        ret: BirdPlanOSPFInterfaceStatus = {
            "overrides": {},
            "current": {},
            "pending": {},
        }

        # Return if we don't have any OSPF state
        if "ospf" not in self.state or "areas" not in self.state["ospf"]:
            return ret

        # Process overrides
        for area_name, area in self.state["ospf"]["areas"].items():
            # Make sure we have interfaces in the area
            if "+interfaces" not in area:
                continue
            # Loop with interfaces
            for interface_name, interface in area["+interfaces"].items():
                # Check our structure is setup
                if "areas" not in ret["overrides"]:
                    ret["overrides"]["areas"] = {}
                if area_name not in ret["overrides"]["areas"]:
                    ret["overrides"]["areas"][area_name] = {}
                if "interfaces" not in ret["overrides"]["areas"][area_name]:
                    ret["overrides"]["areas"][area_name]["interfaces"] = {}
                # Link interface
                ret["overrides"]["areas"][area_name]["interfaces"][interface_name] = interface

        # Process current state
        for area_name, area in self.state["ospf"]["areas"].items():
            # Make sure we have interfaces in the area
            if "interfaces" not in area:
                continue
            # Loop with interfaces
            for interface_name, interface in area["interfaces"].items():
                # Check our structure is setup
                if "areas" not in ret["current"]:
                    ret["current"]["areas"] = {}
                if area_name not in ret["current"]["areas"]:
                    ret["current"]["areas"][area_name] = {}
                if "interfaces" not in ret["current"]["areas"][area_name]:
                    ret["current"]["areas"][area_name]["interfaces"] = {}
                # Link interface
                ret["current"]["areas"][area_name]["interfaces"][interface_name] = interface

        # Generate the override status as if we were doing a configure
        for area_name, area in self.birdconf.protocols.ospf.areas.items():
            for interface_name, interface in area.interfaces.items():
                # Check our structure is setup
                if "areas" not in ret["pending"]:
                    ret["pending"]["areas"] = {}
                if area_name not in ret["pending"]["areas"]:
                    ret["pending"]["areas"][area_name] = {}
                if "interfaces" not in ret["pending"]["areas"][area_name]:
                    ret["pending"]["areas"][area_name]["interfaces"] = {}
                if interface_name not in ret["pending"]["areas"][area_name]["interfaces"]:
                    ret["pending"]["areas"][area_name]["interfaces"][interface_name] = {}
                # Add attributes we need
                ret["pending"]["areas"][area_name]["interfaces"][interface_name]["cost"] = interface.cost
                ret["pending"]["areas"][area_name]["interfaces"][interface_name]["ecmp_weight"] = interface.ecmp_weight

        return ret

    def _config_global(self) -> None:
        """Configure global options."""

        # Check that a router ID was specified
        if "router_id" not in self.config:
            raise BirdPlanError("The 'router_id' attribute must be specified")
        self.birdconf.router_id = self.config["router_id"]

        # Check if we have a log_file specified to use
        if "log_file" in self.config:
            self.birdconf.log_file = self.config["log_file"]

        # Check if we're in debugging mode or not
        if "debug" in self.config:
            self.birdconf.debug = self.config["debug"]

    def _config_kernel(self) -> None:
        """Configure kernel section."""

        # If we have no rip section, just return
        if "kernel" not in self.config:
            return

        # Check configuration options are supported
        for config_item in self.config["kernel"]:
            if config_item not in ("vrf", "routing_table"):
                raise BirdPlanError(f"The 'kernel' config item '{config_item}' is not supported")

        # Check if we have a VRF to use
        if "vrf" in self.config["kernel"]:
            self.birdconf.vrf = '"' + self.config["kernel"]["vrf"] + '"'
            # Make sure we also have a routing talbe
            if "routing_table" not in self.config["kernel"]:
                raise BirdPlanError("The 'kernel' config item 'vrf' requires that 'routing_table' is also specified")

        if "routing_table" in self.config["kernel"]:
            self.birdconf.routing_table = self.config["kernel"]["routing_table"]

    def _config_static(self) -> None:
        """Configure static section."""
        # Static routes
        if "static" in self.config:
            for route in self.config["static"]:
                self.birdconf.protocols.static.add_route(route)

    def _config_export_kernel(self) -> None:
        """Configure export_kernel section."""

        # Check if we're exporting routes from the master tables to the kernel tables
        if "export_kernel" in self.config:
            # Loop with export_kernel items
            for export, export_config in self.config["export_kernel"].items():
                # Static routes
                if export == "static":
                    self.birdconf.tables.master.route_policy_export.kernel.static = export_config
                # RIP routes
                elif export == "rip":
                    self.birdconf.tables.master.route_policy_export.kernel.rip = export_config
                # OSPF routes
                elif export == "ospf":
                    self.birdconf.tables.master.route_policy_export.kernel.ospf = export_config
                # BGP routes
                elif export == "bgp":
                    self.birdconf.tables.master.route_policy_export.kernel.bgp = export_config
                # If we don't understand this 'accept' entry, throw an error
                else:
                    raise BirdPlanError(f"Configuration item '{export}' not understood in 'export_kernel'")

    @property
    def birdconf(self) -> BirdConfig:
        """Return the BirdConfig object."""
        return self._birdconf

    @property
    def config(self) -> dict[str, Any]:
        """Return our config."""
        return self._config

    @config.setter
    def config(self, config: dict[str, Any]) -> None:
        """Set our configuration."""
        self._config = config

    @property
    def state(self) -> dict[str, Any]:
        """Return our state."""
        return self.birdconf.state

    @state.setter
    def state(self, state: dict[str, Any]) -> None:
        """Set our state."""
        self.birdconf.state = state

    @property
    def state_file(self) -> str | None:
        """State file we're using."""
        return self._state_file

    @state_file.setter
    def state_file(self, state_file: str | None) -> None:
        """Set our state file."""
        self._state_file = state_file

    @property
    def yaml(self) -> YAML:
        """Return our YAML parser."""
        return self._yaml
