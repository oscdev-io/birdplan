#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2020, AllWorldIT
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

import os
import re
from typing import Any, Dict, List, Optional, Union

import jinja2
import yaml

from .bird_config import BirdConfig
from .exceptions import BirdPlanError
from .version import __version__

__all__ = [
    "BirdConfig",
    "__version__",
]

# Some types we need
BirdPlanBGPPeerGracefulShutdownStatus = Dict[str, Dict[str, bool]]
BirdPlanBGPPeerQuarantineStatus = Dict[str, Dict[str, bool]]
BirdPlanOSPFInterfaceStatus = Dict[str, Dict[str, Dict[str, Any]]]


class BirdPlan:
    """Main BirdPlan class."""

    _birdconf: BirdConfig
    _config: Dict[str, Any]
    _state_file: Optional[str]

    def __init__(self, test_mode: bool = False) -> None:
        """Initialize object."""

        self._birdconf = BirdConfig(test_mode=test_mode)
        self._config = {}
        self._state_file = None

    def load(self, **kwargs: Any) -> None:
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
        plan_file: Optional[str] = kwargs.get("plan_file")
        state_file: Optional[str] = kwargs.get("state_file")
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
            raise BirdPlanError(f"Failed to read BirdPlan file '{plan_file}': {err}") from None

        # Load configuration using YAML
        try:
            self.config = yaml.safe_load(raw_config)
        except ImportError as err:  # pragma: no cover
            raise BirdPlanError(f" Failed to import BirdPlan file '{plan_file}': {err}") from None

        # Load state using YAML
        if state_file:
            # Set our state file
            self.state_file = state_file

            # Check if the state file exists...
            if os.path.isfile(self.state_file):
                # Read in state file
                try:
                    with open(self.state_file, "r", encoding="UTF-8") as file:
                        raw_state = file.read()
                except OSError as err:
                    raise BirdPlanError(f"Failed to read BirdPlan state file '{state_file}': {err}") from None
                # Load state using YAML
                try:
                    self.state = yaml.safe_load(raw_state)
                except ImportError as err:  # pragma: no cover
                    # We use the state_file here because the size of raw_state may be larger than 100MiB
                    raise BirdPlanError(f" Failed to load BirdPlan state '{state_file}': {err}") from None

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
        self._config_static()
        self._config_export_kernel()
        self._config_rip()
        self._config_ospf()
        self._config_bgp()

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

        # Dump the state in pretty YAML
        yaml_output = yaml.dump(self.state, default_flow_style=False)

        # Write out state file
        try:
            with open(self.state_file, "w", encoding="UTF-8") as file:
                file.write(yaml_output)
        except OSError as err:  # pragma: no cover
            raise BirdPlanError(f"Failed to open '{self.state_file}' for writing: {err}") from None

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

        """  # noqa: RST201,RST203,RST301

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

        """  # noqa: RST201,RST203,RST301

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

        """  # noqa: RST201,RST203,RST301

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
            if "routing_talbe" not in self.config["kernel"]:
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

    def _config_rip(self) -> None:
        """Configure rip section."""

        # If we have no rip section, just return
        if "rip" not in self.config:
            return

        # Check configuration options are supported
        for config_item in self.config["rip"]:
            if config_item not in ("accept", "redistribute", "interfaces"):
                raise BirdPlanError(f"The 'rip' config item '{config_item}' is not supported")

        self._config_rip_accept()
        self._config_rip_redistribute()
        self._config_rip_interfaces()

    def _config_rip_accept(self) -> None:
        """Configure rip:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in self.config["rip"]:
            return

        # Loop with accept items
        for accept, accept_config in self.config["rip"]["accept"].items():
            # Allow accept of the default route
            if accept == "default":
                self.birdconf.protocols.rip.route_policy_accept.default = accept_config
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{accept}' not understood in RIP accept")

    def _config_rip_redistribute(self) -> None:  # pylint: disable=too-many-branches
        """Configure rip:redistribute section."""

        # If we don't have a redistribute section just return
        if "redistribute" not in self.config["rip"]:
            return

        # Loop with redistribution items
        for redistribute, redistribute_config in self.config["rip"]["redistribute"].items():
            # Add connected route redistribution
            if redistribute == "connected":
                # Set type
                redistribute_connected: Union[bool, List[str]]
                # Check what kind of config we go...
                if isinstance(redistribute_config, bool):
                    redistribute_connected = redistribute_config
                # Else if its a dict, we need to treat it a bit differently
                elif isinstance(redistribute_config, dict):
                    # Check it has an "interfaces" key
                    if "interfaces" not in redistribute_config:
                        raise BirdPlanError(f"Configurion item '{redistribute}' has no 'interfaces' option in rip:redistribute")
                    # If it does, check that it is a list
                    if not isinstance(redistribute_config["interfaces"], list):
                        raise BirdPlanError(f"Configurion item '{redistribute}:interfaces' has an invalid type in rip:redistribute")
                    # Set redistribute_connected as the interface list
                    redistribute_connected = redistribute_config["interfaces"]
                else:
                    raise BirdPlanError(f"Configurion item '{redistribute}' has an unsupported value")
                # Add configuration
                self.birdconf.protocols.rip.route_policy_redistribute.connected = redistribute_connected
            # Add kernel route redistribution
            elif redistribute == "kernel":
                self.birdconf.protocols.rip.route_policy_redistribute.kernel = redistribute_config
            # Add kernel default route redistribution
            elif redistribute == "kernel_default":
                self.birdconf.protocols.rip.route_policy_redistribute.kernel_default = redistribute_config
            # Allow redistribution of RIP routes
            elif redistribute == "rip":
                self.birdconf.protocols.rip.route_policy_redistribute.rip = redistribute_config
            # Allow redistribution of RIP default routes
            elif redistribute == "rip_default":
                self.birdconf.protocols.rip.route_policy_redistribute.rip_default = redistribute_config
            # Add static route redistribution
            elif redistribute == "static":
                self.birdconf.protocols.rip.route_policy_redistribute.static = redistribute_config
            # Add static default route redistribution
            elif redistribute == "static_default":
                self.birdconf.protocols.rip.route_policy_redistribute.static_default = redistribute_config
            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{redistribute}' not understood in rip:redistribute")

    def _config_rip_interfaces(self) -> None:
        """Configure rip:interfaces section."""

        # If we don't have interfaces in our rip section, just return
        if "interfaces" not in self.config["rip"]:
            return

        # Loop with each interface and its config
        for interface_name, interface in self.config["rip"]["interfaces"].items():
            # See if we have interface config
            interface_config = {}
            # Loop with each config item in the peer
            for config_item, config_value in interface.items():
                if config_item in ("update-time", "metric"):
                    interface_config[config_item] = config_value
                # If we don't understand this 'redistribute' entry, throw an error
                else:
                    raise BirdPlanError(f"Configuration item '{config_item}' not understood in RIP area")
            # Add interface
            self.birdconf.protocols.rip.add_interface(interface_name, interface_config)

    def _config_ospf(self) -> None:
        """Configure OSPF section."""

        # If we have no ospf section, just return
        if "ospf" not in self.config:
            return

        # Check configuration options are supported
        for config_item in self.config["ospf"]:
            if config_item not in ("accept", "redistribute", "areas", "v4version"):
                raise BirdPlanError(f"The 'ospf' config item '{config_item}' is not supported")

        # Check what version of OSPF we're using for IPv4
        if "v4version" in self.config["ospf"]:
            if isinstance(self.config["ospf"]["v4version"], (int, str)):
                v4version = f"{self.config['ospf']['v4version']}"
                if v4version in ("2", "3"):
                    self.birdconf.protocols.ospf.v4version = v4version
                else:
                    raise BirdPlanError("The 'ospf' config item 'v4version' has unsupported value")
            else:
                raise BirdPlanError("The 'ospf' config item 'v4version' has unsupported type")

        self._config_ospf_accept()
        self._config_ospf_redistribute()
        self._config_ospf_areas()

    def _config_ospf_accept(self) -> None:
        """Configure ospf:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in self.config["ospf"]:
            return

        # Loop with accept items
        for accept, accept_config in self.config["ospf"]["accept"].items():
            # Allow accept of the default route
            if accept == "default":
                self.birdconf.protocols.ospf.route_policy_accept.default = accept_config
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{accept}' not understood in ospf:accept")

    def _config_ospf_redistribute(self) -> None:  # pylint: disable=too-many-branches
        """Configure ospf:redistribute section."""

        # If we don't have a redistribute section just return
        if "redistribute" not in self.config["ospf"]:
            return

        # Loop with redistribution items
        for redistribute, redistribute_config in self.config["ospf"]["redistribute"].items():
            # Add static route redistribution
            if redistribute == "static":
                self.birdconf.protocols.ospf.route_policy_redistribute.static = redistribute_config
            # Add connected route redistribution
            elif redistribute == "connected":
                # Set type
                redistribute_connected: Union[bool, List[str]]
                # Check what kind of config we go...
                if isinstance(redistribute_config, bool):
                    redistribute_connected = redistribute_config
                # Else if its a dict, we need to treat it a bit differently
                elif isinstance(redistribute_config, dict):
                    # Check it has an "interfaces" key
                    if "interfaces" not in redistribute_config:
                        raise BirdPlanError(f"Configurion item '{redistribute}' has no 'interfaces' option in ospf:redistribute")
                    # If it does, check that it is a list
                    if not isinstance(redistribute_config["interfaces"], list):
                        raise BirdPlanError(
                            f"Configurion item '{redistribute}:interfaces' has an invalid type in ospf:redistribute"
                        )
                    # Set redistribute_connected as the interface list
                    redistribute_connected = redistribute_config["interfaces"]
                else:
                    raise BirdPlanError(f"Configurion item '{redistribute}' has an unsupported value")
                # Add configuration
                self.birdconf.protocols.ospf.route_policy_redistribute.connected = redistribute_connected
            # Add kernel route redistribution
            elif redistribute == "kernel":
                self.birdconf.protocols.ospf.route_policy_redistribute.kernel = redistribute_config
            # Add kernel default route redistribution
            elif redistribute == "kernel_default":
                self.birdconf.protocols.ospf.route_policy_redistribute.kernel_default = redistribute_config
            # Add static route redistribution
            elif redistribute == "static":
                self.birdconf.protocols.ospf.route_policy_redistribute.static = redistribute_config
            # Add static default route redistribution
            elif redistribute == "static_default":
                self.birdconf.protocols.ospf.route_policy_redistribute.static_default = redistribute_config
            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{redistribute}' not understood in ospf:redistribute")

    def _config_ospf_areas(self) -> None:  # pylint: disable=too-many-branches
        """Configure ospf:interfaces section."""

        # If we don't have areas in our ospf section, just return
        if "areas" not in self.config["ospf"]:
            return

        # Loop with each area and its config
        for area_name, raw_area_config in self.config["ospf"]["areas"].items():
            # Make sure we have an interface for the area
            if "interfaces" not in raw_area_config:
                raise BirdPlanError(f"OSPF area '{area_name}' must contain 'interfaces'")
            # Loop with each config item
            area_config = {}
            for config_item, raw_config in raw_area_config.items():
                # Make sure this item is supported
                if config_item not in ("xxxxxxx", "interfaces"):
                    raise BirdPlanError(
                        f"Configuration item '{config_item}' with value '{raw_config}' not understood in ospf:areas"
                    )
                # Skip over interfaces
                if config_item == "interfaces":
                    continue
                # Check for supported config options
                if config_item in ("xxxxx", "yyyy"):
                    area_config[config_item] = raw_config
                # If we don't understand this 'redistribute' entry, throw an error
                else:
                    raise BirdPlanError(f"Configuration item '{config_item}' not understood in ospf:areas")

            # Add area
            area = self.birdconf.protocols.ospf.add_area(area_name, area_config)

            # Loop with interfaces in area
            for interface_name, raw_config in raw_area_config["interfaces"].items():
                # Start with no special interface configuration
                interface_config: Dict[str, Any] = {}
                # Check what kind of config we've got...
                add_ospf_interface = False
                if isinstance(raw_config, bool):
                    add_ospf_interface = raw_config
                # Else if its a dict, we need to treat it a bit differently
                elif isinstance(raw_config, dict):
                    add_ospf_interface = True
                    for raw_item, raw_value in raw_config.items():
                        if raw_item in ("cost", "ecmp_weight", "hello", "stub", "wait"):
                            interface_config[raw_item] = raw_value
                        else:
                            raise BirdPlanError(
                                f"Configuration item '{raw_item}' not understood in OSPF interface '{interface_name}'"
                            )
                else:
                    raise BirdPlanError(
                        f"Configurion for OSPF interface name '{interface_name}' has an unsupported type: '{type(interface_name)}'"
                    )

                # Add interface to area
                if add_ospf_interface:
                    area.add_interface(interface_name, interface_config)

    def _config_bgp(self) -> None:
        """Configure bgp section."""

        # If we have no rip section, just return
        if "bgp" not in self.config:
            return

        # Set our ASN
        if "asn" not in self.config["bgp"]:
            raise BirdPlanError('BGP configuration must have an "asn" item defined')
        self.birdconf.protocols.bgp.asn = self.config["bgp"]["asn"]

        # Check configuration options are supported
        for config_item in self.config["bgp"]:
            if config_item not in (
                # Globals
                "accept",
                "asn",
                "graceful_shutdown",
                "import",
                "originate",  # Origination
                "peers",
                "peertype_constraints",
                "quarantine",
                "rr_cluster_id",
            ):
                raise BirdPlanError(f"The 'bgp' config item '{config_item}' is not supported")

        self._config_bgp_accept()
        self._config_bgp_globals()
        self._config_bgp_peertype_constraints()
        self._config_bgp_originate()

        self._config_bgp_import()
        self._config_bgp_peers()

    def _config_bgp_accept(self) -> None:
        """Configure bgp:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in self.config["bgp"]:
            return

        # Loop with accept items
        for accept, accept_config in self.config["bgp"]["accept"].items():
            # Check if we need to accept some kinds of routes
            if accept in (
                "bgp_customer_blackhole",
                "bgp_own_blackhole",
                "bgp_own_default",
                "bgp_transit_default",
                "originated",
                "originated_default",
            ):
                setattr(self.birdconf.protocols.bgp.route_policy_accept, accept, accept_config)
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{accept}' not understood in bgp:accept")

    def _config_bgp_globals(self) -> None:
        """Configure bgp globals."""

        # Setup graceful shutdown if specified
        if "graceful_shutdown" in self.config["bgp"]:
            self.birdconf.protocols.bgp.graceful_shutdown = self.config["bgp"]["graceful_shutdown"]

        # Setup graceful shutdown if specified
        if "quarantine" in self.config["bgp"]:
            self.birdconf.protocols.bgp.quarantine = self.config["bgp"]["quarantine"]

        # Set our route reflector cluster id
        if "rr_cluster_id" in self.config["bgp"]:
            self.birdconf.protocols.bgp.rr_cluster_id = self.config["bgp"]["rr_cluster_id"]

    def _config_bgp_peertype_constraints(self) -> None:
        """Configure bgp:peertype_constraints section."""

        # If we don't have a peertype_constraints section, just return
        if "peertype_constraints" not in self.config["bgp"]:
            return

        for peer_type in self.config["bgp"]["peertype_constraints"]:
            # Make sure we have a valid peer type
            if peer_type not in (
                "customer",
                "customer.private",
                "internal",
                "peer",
                "routecollector",
                "routeserver",
                "rrclient",
                "rrserver",
                "rrserver-rrserver",
                "transit",
            ):
                raise BirdPlanError(f"The 'bgp:peertype_constraints' config item '{peer_type}' is not supported")
            # Loop with constraint items
            for constraint_name in self.config["bgp"]["peertype_constraints"][peer_type]:
                # Make sure we have a valid constraint to set
                if constraint_name not in (
                    "blackhole_import_maxlen4",
                    "blackhole_import_minlen4",
                    "blackhole_export_maxlen4",
                    "blackhole_export_minlen4",
                    "blackhole_import_maxlen6",
                    "blackhole_import_minlen6",
                    "blackhole_export_maxlen6",
                    "blackhole_export_minlen6",
                    "import_maxlen4",
                    "export_maxlen4",
                    "import_minlen4",
                    "export_minlen4",
                    "import_maxlen6",
                    "export_maxlen6",
                    "import_minlen6",
                    "export_minlen6",
                    "aspath_import_maxlen",
                    "aspath_import_minlen",
                    "community_import_maxlen",
                    "extended_community_import_maxlen",
                    "large_community_import_maxlen",
                ):
                    raise BirdPlanError(
                        f"The 'bgp:peertype_constraints:{peer_type}' config item '{constraint_name}' is not supported"
                    )
                # Make sure this peer supports blackhole imports
                if constraint_name.startswith("blackhole_import_"):  # noqa: SIM102
                    if peer_type not in (
                        "customer",
                        "internal",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                    ):
                        raise BirdPlanError(
                            f"Having 'peertype_constraints:{constraint_name}' specified for peer type '{peer_type}' "
                            "makes no sense"
                        )
                # Make sure this peer accepts blackhole exports
                if constraint_name.startswith("blackhole_export_"):  # noqa: SIM102
                    if peer_type not in (
                        "internal",
                        "routeserver",
                        "routecollector",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        raise BirdPlanError(
                            f"Having 'peertype_constraints:{constraint_name}' specified for peer type '{peer_type}' "
                            "makes no sense"
                        )
                # Make sure this peer supports imports
                if "import" in constraint_name:  # noqa: SIM102
                    if peer_type not in (
                        "customer",
                        "customer.private",
                        "internal",
                        "peer",
                        "routeserver",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        raise BirdPlanError(
                            f"Having 'peertype_constraints:{constraint_name}' specified for peer type '{peer_type}' "
                            "makes no sense"
                        )
                # Finally set the constraint item
                setattr(
                    self.birdconf.protocols.bgp.constraints(peer_type),
                    constraint_name,
                    self.config["bgp"]["peertype_constraints"][peer_type][constraint_name],
                )

    def _config_bgp_originate(self) -> None:
        """Configure bgp:originate section."""

        # If we don't have an accept section, just return
        if "originate" not in self.config["bgp"]:
            return

        # Add origination routes
        for route in self.config["bgp"]["originate"]:
            self.birdconf.protocols.bgp.add_originated_route(route)

    def _config_bgp_import(self) -> None:  # pylint: disable=too-many-branches
        """Configure bgp:import section."""

        # If we don't have the option then just return
        if "import" not in self.config["bgp"]:
            return

        # Loop with redistribution items
        for import_type, import_config in self.config["bgp"]["import"].items():
            # Import connected routes into the main BGP table
            if import_type == "connected":
                # Set type
                import_connected: Union[bool, List[str]]
                # Check what kind of config we go...
                if isinstance(import_config, bool):
                    import_connected = import_config
                # Else if its a dict, we need to treat it a bit differently
                elif isinstance(import_config, dict):
                    # Check it has an "interfaces" key
                    if "interfaces" not in import_config:
                        raise BirdPlanError(f"Configurion item '{import_type}' has no 'interfaces' option in bgp:import")
                    # If it does, check that it is a list
                    if not isinstance(import_config["interfaces"], list):
                        raise BirdPlanError(f"Configurion item '{import_type}:interfaces' has an invalid type in bgp:import")
                    # Set import_connected as the interface list
                    import_connected = import_config["interfaces"]
                else:
                    raise BirdPlanError(f"Configurion item '{import_type}' has an unsupported value")
                # Add configuration
                self.birdconf.protocols.bgp.route_policy_import.connected = import_connected

            # Import kernel routes into the main BGP table
            elif import_type == "kernel":
                self.birdconf.protocols.bgp.route_policy_import.kernel = import_config
            # Import kernel blackhole routes into the main BGP table
            elif import_type == "kernel_blackhole":
                self.birdconf.protocols.bgp.route_policy_import.kernel_blackhole = import_config
            # Import kernel default routes into the main BGP table
            elif import_type == "kernel_default":
                self.birdconf.protocols.bgp.route_policy_import.kernel_default = import_config

            # Import static routes into the main BGP table
            elif import_type == "static":
                self.birdconf.protocols.bgp.route_policy_import.static = import_config
            # Import static blackhole routes into the main BGP table
            elif import_type == "static_blackhole":
                self.birdconf.protocols.bgp.route_policy_import.static_blackhole = import_config
            # Import static default routes into the main BGP table
            elif import_type == "static_default":
                self.birdconf.protocols.bgp.route_policy_import.static_default = import_config

            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{import_type}' not understood in bgp:import")

    def _config_bgp_peers(self) -> None:
        """Configure bgp:peers section."""

        if "peers" not in self.config["bgp"]:
            return

        # Loop with peer ASN and config
        for peer_name, peer_config in self.config["bgp"]["peers"].items():
            # Make sure peer name is valid
            if not re.match(r"^[a-z0-9]+$", peer_name):
                raise BirdPlanError(f"The peer name '{peer_name}' specified in 'bgp:peers' is not valid, use [a-z0-9]")
            # Configure peer
            self._config_bgp_peers_peer(peer_name, peer_config)

    def _config_bgp_peers_peer(  # noqa: CFQ001 # pylint: disable=too-many-branches,too-many-locals,too-many-statements
        self, peer_name: str, peer_config: Dict[str, Any]
    ) -> None:
        """Configure bgp:peers single peer."""

        # Start with no peer config
        peer = {}

        # Loop with each config item in the peer
        for config_item, config_value in peer_config.items():
            if config_item in (
                "asn",
                "description",
                "type",
                "neighbor4",
                "neighbor6",
                "source_address4",
                "source_address6",
                "connect_retry_time",
                "connect_delay_time",
                "error_wait_time",
                "multihop",
                "passive",
                "password",
                "prefix_limit4",
                "prefix_limit6",
                "quarantine",
                "replace_aspath",
                "incoming_large_communities",
                "cost",
                "graceful_shutdown",
                "blackhole_community",
            ):
                peer[config_item] = config_value
            # Peer add_paths configuration
            elif config_item == "add_paths":
                peer["add_paths"] = None
                if isinstance(config_value, bool):
                    if config_value:
                        peer["add_paths"] = "on"
                elif isinstance(config_value, str):
                    if config_value not in ("tx", "rx", "on"):
                        raise BirdPlanError(
                            f"Configuration value '{config_value}' not understood in bgp:peers:{peer_name}:add_paths, valid values"
                            "are 'tx', 'rx', 'on'"
                        )
                    peer["add_paths"] = config_value
                else:
                    raise BirdPlanError(
                        f"Configuration item has invalid type '{type(config_value)}' in bgp:peers:{peer_name}:add_paths"
                    )
            # Peer location configuration
            elif config_item == "location":
                peer["location"] = {}
                # Loop with location configuration items
                for location_type, location_config in config_value.items():
                    if location_type not in ("iso3166", "unm49"):
                        raise BirdPlanError(
                            f"Configuration item '{location_type}' not understood in bgp:peers:{peer_name}:location"
                        )
                    peer["location"][location_type] = location_config
            # Work out redistribution
            elif config_item == "redistribute":
                peer["redistribute"] = {}
                # Loop with redistribution items
                for redistribute_type, redistribute_config in config_value.items():
                    if redistribute_type not in (
                        "connected",
                        "kernel",
                        "kernel_blackhole",
                        "kernel_default",
                        "static",
                        "static_blackhole",
                        "static_default",
                        "originated",
                        "originated_default",
                        "bgp",
                        "bgp_customer",
                        "bgp_customer_blackhole",
                        "bgp_own",
                        "bgp_own_blackhole",
                        "bgp_own_default",
                        "bgp_peering",
                        "bgp_transit",
                        "bgp_transit_default",
                    ):
                        raise BirdPlanError(
                            f"Configuration item '{redistribute_type}' not understood in bgp:peers:{peer_name} redistribute"
                        )
                    peer["redistribute"][redistribute_type] = redistribute_config

            # Work out acceptance of routes
            elif config_item == "accept":
                peer["accept"] = {}
                # Loop with acceptance items
                for accept, accept_config in config_value.items():
                    if accept not in (
                        "bgp_customer_blackhole",
                        "bgp_own_blackhole",
                        "bgp_own_default",
                        "bgp_transit_default",
                    ):
                        raise BirdPlanError(f"Configuration item '{accept}' not understood in bgp:peers:{peer_name}:accept")
                    peer["accept"][accept] = accept_config
            # Work out filters
            elif config_item == "filter":
                peer["filter"] = {}
                # Loop with filter configuration items
                for filter_type, filter_config in config_value.items():
                    if filter_type not in ("as_sets", "aspath_asns", "origin_asns", "peer_asns", "prefixes"):
                        raise BirdPlanError(f"Configuration item '{filter_type}' not understood in bgp:peers:{peer_name}:filter")
                    peer["filter"][filter_type] = filter_config

            # Work out outgoing large community options
            elif config_item == "outgoing_large_communities":
                if isinstance(config_value, dict):
                    # Loop with outgoing large community configuration items
                    for lc_type, lc_config in config_value.items():
                        if lc_type not in (
                            "blackhole",
                            "default",
                            "connected",
                            "kernel",
                            "kernel_blackhole",
                            "kernel_default",
                            "static",
                            "static_blackhole",
                            "static_default",
                            "originated",
                            "originated_default",
                            "bgp",
                            "bgp_own",
                            "bgp_own_blackhole",
                            "bgp_own_default",
                            "bgp_customer",
                            "bgp_customer_blackhole",
                            "bgp_peering",
                            "bgp_transit",
                            "bgp_transit_default",
                            "bgp_blackhole",
                            "bgp_default",
                        ):
                            raise BirdPlanError(
                                f"Configuration item '{lc_type}' not understood in bgp:peers:{peer_name}:outgoing_large_communities"
                            )
                        # Make sure we have a prepend key
                        if "outgoing_large_communities" not in peer:
                            peer["outgoing_large_communities"] = {}
                        # Then add the config...
                        peer["outgoing_large_communities"][lc_type] = lc_config

                # Check in the case it is a list
                elif isinstance(config_value, list):
                    peer["outgoing_large_communities"] = config_value

                # Else if we don't know what it is, then throw an exception
                else:
                    raise BirdPlanError(f"Configuration item bgp:peers:{peer_name}:outgoing_large_communities has incorrect type")

            # Work out prepending options
            elif config_item == "prepend":
                if isinstance(config_value, dict):
                    # Loop with prepend configuration items
                    for prepend_type, prepend_config in config_value.items():
                        if prepend_type not in (
                            "blackhole",
                            "default",
                            "connected",
                            "kernel",
                            "kernel_blackhole",
                            "kernel_default",
                            "static",
                            "static_blackhole",
                            "static_default",
                            "originated",
                            "originated_default",
                            "bgp",
                            "bgp_own",
                            "bgp_own_blackhole",
                            "bgp_own_default",
                            "bgp_customer",
                            "bgp_customer_blackhole",
                            "bgp_peering",
                            "bgp_transit",
                            "bgp_transit_default",
                            "bgp_blackhole",
                            "bgp_default",
                        ):
                            raise BirdPlanError(
                                f"Configuration item '{prepend_type}' not understood in bgp:peers:{peer_name}:prepend"
                            )
                        # Make sure we have a prepend key
                        if "prepend" not in peer:
                            peer["prepend"] = {}
                        # Then add the config...
                        peer["prepend"][prepend_type] = prepend_config
                else:
                    peer["prepend"] = config_value

            # Work out our constraints
            elif config_item == "constraints":
                # Loop with constraint configuration items
                for constraint_name, constraint_value in config_value.items():
                    if constraint_name not in (
                        "blackhole_import_maxlen4",
                        "blackhole_import_minlen4",
                        "blackhole_export_maxlen4",
                        "blackhole_export_minlen4",
                        "blackhole_import_maxlen6",
                        "blackhole_import_minlen6",
                        "blackhole_export_maxlen6",
                        "blackhole_export_minlen6",
                        "import_maxlen4",
                        "export_maxlen4",
                        "import_minlen4",
                        "export_minlen4",
                        "import_maxlen6",
                        "export_maxlen6",
                        "import_minlen6",
                        "export_minlen6",
                        "aspath_import_maxlen",
                        "aspath_import_minlen",
                        "community_import_maxlen",
                        "extended_community_import_maxlen",
                        "large_community_import_maxlen",
                    ):
                        raise BirdPlanError(
                            f"Configuration item '{constraint_name}' not understood in bgp:peers:{peer_name}:prepend"
                        )
                    # Make sure we have a prepend key
                    if "constraints" not in peer:
                        peer["constraints"] = {}
                    # Then add the config...
                    peer["constraints"][constraint_name] = constraint_value

            else:
                raise BirdPlanError(f"Configuration item '{config_item}' not understood in bgp:peers:{peer_name}")

        # Check items we need
        for required_item in ["asn", "description", "type"]:
            if required_item not in peer:
                raise BirdPlanError(f"Configuration item '{required_item}' missing in bgp:peers:{peer_name}")

        # Check the peer type is valid
        if peer["type"] not in (
            "customer",
            "internal",
            "peer",
            "routecollector",
            "routeserver",
            "rrclient",
            "rrserver",
            "rrserver-rrserver",
            "transit",
        ):
            raise BirdPlanError(f"Configuration item 'type' for BGP peer '{peer_name}' has invalid value '%s'" % peer["type"])

        # Check that if we have a peer type of rrclient, that we have rr_cluster_id too...
        if (peer["type"] == "rrclient") and ("rr_cluster_id" not in self.config["bgp"]):
            raise BirdPlanError(f"Configuration for BGP peer '{peer_name}' is missing 'rr_cluster_id' when having 'rrclient' peers")
        # If we are a customer type, we must have filters defined
        if (peer["type"] == "customer") and ("filter" not in peer):
            raise BirdPlanError(f"Configuration for BGP peer '{peer_name}' is missing 'filter' when type is 'customer'")
        # We must have a neighbor4 or neighbor6
        if ("neighbor4" not in peer) and ("neighbor6" not in peer):
            raise BirdPlanError(f"Configuration for BGP peer '{peer_name}' is missing 'neighbor4' or 'neighbor6' config")
        # We must have a source_address4 for neighbor4
        if ("neighbor4" in peer) and ("source_address4" not in peer):
            raise BirdPlanError(f"Configuration for BGP peer '{peer_name}' must have a 'source_address4'")
        # We must have a source_address6 for neighbor6
        if ("neighbor6" in peer) and ("source_address6" not in peer):
            raise BirdPlanError(f"Configuration for BGP peer '{peer_name}' must have a 'source_address6'")

        # Make sure we have items we need
        self.birdconf.protocols.bgp.add_peer(peer_name, peer)

    @property
    def birdconf(self) -> BirdConfig:
        """Return the BirdConfig object."""
        return self._birdconf

    @property
    def config(self) -> Dict[str, Any]:
        """Return our config."""
        return self._config

    @config.setter
    def config(self, config: Dict[str, Any]) -> None:
        """Set our configuration."""
        self._config = config

    @property
    def state(self) -> Dict[str, Any]:
        """Return our state."""
        return self.birdconf.state

    @state.setter
    def state(self, state: Dict[str, Any]) -> None:
        """Set our state."""
        self.birdconf.state = state

    @property
    def state_file(self) -> Optional[str]:
        """State file we're using."""
        return self._state_file

    @state_file.setter
    def state_file(self, state_file: str) -> None:
        """Set our state file."""
        self._state_file = state_file
