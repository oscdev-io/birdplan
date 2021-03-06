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

from typing import Any, Dict, List, Optional, Union
import os
import re
import jinja2
import yaml
from .bird_config import BirdConfig
from .exceptions import BirdPlanError


__VERSION__ = "0.0.1"


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

    def load(self, plan_file: str, state_file: Optional[str] = None) -> None:
        """
        Initialize object.

        Parameters
        ----------
        plan_file : str
            Source plan file to generate configuration from.
        state_file : Optional[str]
            Optional state file, used for commands like BGP graceful shutdown

        """

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
                    with open(self.state_file, "r") as file:
                        raw_state = file.read()
                except OSError as err:
                    raise BirdPlanError(f"Failed to read BirdPlan state file '{state_file}': {err}") from None
                # Load state using YAML
                try:
                    self.state = yaml.safe_load(raw_state)
                except ImportError as err:  # pragma: no cover
                    raise BirdPlanError(f" Failed to load BirdPlan state '{state_file}': {err}") from None

    def configure(self, output_filename: Optional[str] = None) -> str:
        """
        Create configuration for BIRD.

        Parameters
        ----------
        output_filename : Optional[str]
            Optional filename to write the configuration to. If this is not specified we'll just return the
            configuration.

        """

        # Make sure we have configuration...
        if not self.config:
            raise BirdPlanError("No configuration found")

        # Check configuration options are supported
        for config_item in self.config:
            if config_item not in ("router_id", "log_file", "debug", "static", "export_kernel", "bgp", "rip", "ospf"):
                raise BirdPlanError(f"The config item '{config_item}' is not supported")

        # Configure sections
        self._config_global()
        self._config_static()
        self._config_export_kernel()
        self._config_rip()
        self._config_ospf()
        self._config_bgp()

        # Generate the configuration
        config_str = "\n".join(self.birdconf.get_config())

        # If we have a filename, write out
        if output_filename:
            if output_filename == "-":
                print(config_str)
            else:
                try:
                    with open(output_filename, "w") as config_file:
                        config_file.write(config_str)
                except OSError as err:  # pragma: no cover
                    raise BirdPlanError(f"Failed to open '{output_filename}' for writing: {err}") from None

        return config_str

    def commit_state(self) -> None:
        """Commit our current state."""

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Commit of BirdPlan state requires a state file, none loaded")

        # Dump the state in pretty YAML
        raw_state = yaml.dump(self.state, default_flow_style=False)

        # Write out state file
        try:
            with open(self.state_file, "w") as file:
                file.write(raw_state)
        except OSError as err:  # pragma: no cover
            raise BirdPlanError(f"Failed to open '{self.state_file}' for writing: {err}") from None

    def bgp_graceful_shutdown_add_peer(self, peer: str) -> None:
        """
        Add a peer to the BGP graceful shutdown list.

        Parameters
        ----------
        peer : str
            Peer name to add to BGP graceful shutdown list.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Using of BGP graceful shutdown requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state:
            self.state["bgp"] = {}
        if "graceful_shutdown" not in self.state["bgp"]:
            self.state["bgp"]["graceful_shutdown"] = []

        # If the peer is not in the list, then add it
        if peer not in self.state["bgp"]["graceful_shutdown"]:
            self.state["bgp"]["graceful_shutdown"].append(peer)
        else:
            raise BirdPlanError("BGP peer already in graceful_shutdown list")

    def bgp_graceful_shutdown_remove_peer(self, peer: str) -> None:
        """
        Remove a peer from the BGP graceful shutdown list.

        Parameters
        ----------
        peer : str
            Peer name to remove from BGP graceful shutdown list.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Using of BGP graceful shutdown requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if (
            "bgp" not in self.state
            or "graceful_shutdown" not in self.state["bgp"]
            or peer not in self.state["bgp"]["graceful_shutdown"]
        ):
            raise BirdPlanError("BGP peer not in graceful_shutdown list")

        # Remove peer from graceful_shutdown list
        self.state["bgp"]["graceful_shutdown"].remove(peer)

    def bgp_graceful_shutdown_peer_list(self) -> List[str]:
        """
        Return the list of peers that are currently set for graceful shutdown.

        Returns
        -------
        List[str]
            List of BGP peers set for graceful shutdown.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Using of BGP graceful shutdown requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state or "graceful_shutdown" not in self.state["bgp"]:
            return []

        return [f"{x}" for x in self.state["bgp"]["graceful_shutdown"]]

    def bgp_quarantine_add_peer(self, peer: str) -> None:
        """
        Add a peer to the BGP quarantine list.

        Parameters
        ----------
        peer : str
            Peer name to add to BGP quarantine list.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Using of BGP quarantine requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state:
            self.state["bgp"] = {}
        if "quarantine" not in self.state["bgp"]:
            self.state["bgp"]["quarantine"] = []

        # If the peer is not in the list, then add it
        if peer not in self.state["bgp"]["quarantine"]:
            self.state["bgp"]["quarantine"].append(peer)
        else:
            raise BirdPlanError("BGP peer already in quarantine list")

    def bgp_quarantine_remove_peer(self, peer: str) -> None:
        """
        Remove a peer from the BGP quarantine list.

        Parameters
        ----------
        peer : str
            Peer name to remove from BGP quarantine list.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Using of BGP quarantine requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state or "quarantine" not in self.state["bgp"] or peer not in self.state["bgp"]["quarantine"]:
            raise BirdPlanError("BGP peer not in quarantine list")

        # Remove peer from quarantine list
        self.state["bgp"]["quarantine"].remove(peer)

    def bgp_quarantine_peer_list(self) -> List[str]:
        """
        Return the list of peers that are currently set for quarantine.

        Returns
        -------
        List[str]
            List of BGP peers set for quarantine.

        """

        # Raise an exception if we don't have a state file loaded
        if self.state_file is None:
            raise BirdPlanError("Using of BGP quarantine requires a state file, none loaded")

        # Prepare the state structure if its not got what we need
        if "bgp" not in self.state or "quarantine" not in self.state["bgp"]:
            return []

        return [f"{x}" for x in self.state["bgp"]["quarantine"]]

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

    def _config_rip_redistribute(self) -> None:
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
            if config_item not in ("accept", "redistribute", "areas"):
                raise BirdPlanError(f"The 'ospf' config item '{config_item}' is not supported")

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

    def _config_ospf_redistribute(self) -> None:
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

    def _config_ospf_areas(self) -> None:
        """Configure ospf:interfaces section."""

        # If we don't have areas in our ospf section, just return
        if "areas" not in self.config["ospf"]:
            return

        # Loop with each area and its config
        for area_name, area in self.config["ospf"]["areas"].items():
            # Make sure we have an interface for the area
            if "interfaces" not in area:
                raise BirdPlanError(f"OSPF area '{area_name}' must contain 'interfaces'")
            # Loop with each config item
            for config_item, config_value in area.items():
                # Make sure this item is supported
                if config_item not in ("config", "interfaces"):
                    raise BirdPlanError(
                        f"Configuration item '{config_item}' with value '{config_value}' not understood in ospf:areas"
                    )
            # See if we have area config
            area_config = {}
            if "config" in area:
                # Loop with each config item in the peer
                for config_item, config_value in area["config"].items():
                    # No items supported atm
                    if config_item in ("xxxxx", "yyyy"):
                        area_config[config_item] = config_value
                    # If we don't understand this 'redistribute' entry, throw an error
                    else:
                        raise BirdPlanError("Configuration item '{config_item}' not understood in OSPF area")
            # Add area
            self.birdconf.protocols.ospf.add_area(area_name, area_config)
            # Loop with interfaces in area
            for interface_name, interface_config in area["interfaces"].items():
                # Add interface to area
                self.birdconf.protocols.ospf.add_interface(area_name, interface_name, interface_config)

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
                "asn",
                "graceful_shutdown",
                "peertype_constraints",
                "originate",  # Origination
                "accept",
                "import",
                "rr_cluster_id",
                "peers",
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
                if constraint_name.startswith("blackhole_import_"):
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
                if constraint_name.startswith("blackhole_export_"):
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
                if "import" in constraint_name:
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

    def _config_bgp_import(self) -> None:
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

    def _config_bgp_peers_peer(
        self, peer_name: str, peer_config: Dict[str, Any]
    ) -> None:  # pylint: disable=too-many-branches # noqa: C901
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

        # Check if we have a graceful shutdown state
        if "bgp" in self.state and "graceful_shutdown" in self.state["bgp"]:
            # If we do, then check if this peer is in it
            if peer_name in self.state["bgp"]["graceful_shutdown"] or "*" in self.state["bgp"]["graceful_shutdown"]:
                peer["graceful_shutdown"] = self.state["bgp"]["graceful_shutdown"]

        # Check if we have a quarantine state
        if "bgp" in self.state and "quarantine" in self.state["bgp"]:
            # If we do, then check if this peer is in it
            if peer_name in self.state["bgp"]["quarantine"]:
                peer["quarantine"] = self.state["bgp"]["quarantine"]

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
