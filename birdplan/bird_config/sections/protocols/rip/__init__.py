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

"""BIRD RIP protocol configuration."""

from typing import Dict, List, Union

from .....exceptions import BirdPlanError
from ....globals import BirdConfigGlobals
from ...bird_attributes import SectionBirdAttributes
from ...constants import SectionConstants
from ...functions import SectionFunctions
from ...tables import SectionTables
from ..base import SectionProtocolBase
from ..direct import ProtocolDirect
from ..pipe import ProtocolPipe, ProtocolPipeFilterType
from .rip_attributes import RIPAttributes, RIPRoutePolicyAccept, RIPRoutePolicyRedistribute
from .rip_functions import RIPFunctions

__all__ = ["ProtocolRIP"]


RIPInterfaceConfig = Union[bool, Dict[str, str]]
RIPInterfaces = Dict[str, RIPInterfaceConfig]


class ProtocolRIP(SectionProtocolBase):
    """BIRD RIP protocol configuration."""

    _rip_interfaces: RIPInterfaces

    _rip_attributes: RIPAttributes
    # RIP functions
    _rip_functions: RIPFunctions

    def __init__(  # pylint: disable=too-many-arguments
        self,
        birdconfig_globals: BirdConfigGlobals,
        birdattributes: SectionBirdAttributes,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
    ) -> None:
        """Initialize the object."""
        super().__init__(birdconfig_globals, birdattributes, constants, functions, tables)

        # Set section header
        self._section = "RIP Protocol"

        # Interfaces
        self._rip_interfaces = {}

        self._rip_attributes = RIPAttributes()
        # Setup RIP functions
        self._rip_functions = RIPFunctions(self.birdconfig_globals, self.functions)

    def configure(self) -> None:
        """Configure the RIP protocol."""
        super().configure()

        # If we don't have any configuration, just abort
        if not self.interfaces:
            return

        self.functions.conf.append(self.rip_functions, deferred=True)

        self.tables.conf.append("# RIP Tables")
        self.tables.conf.append("ipv4 table t_rip4;")
        self.tables.conf.append("ipv6 table t_rip6;")
        self.tables.conf.append("")

        self._rip_export_filter()
        self._rip_import_filter()
        self._rip_to_master_export_filter()
        self._rip_to_master_import_filter()

        # Setup the protocol
        self._setup_protocol("4")
        self._setup_protocol("6")

        # Configure pipe from RIP to the master routing table
        rip_master_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from="rip",
            table_to="master",
            export_filter_type=ProtocolPipeFilterType.UNVERSIONED,
            import_filter_type=ProtocolPipeFilterType.UNVERSIONED,
        )
        self.conf.add(rip_master_pipe)

        # Check if we're redistributing connected routes, if we are, create the protocol and pipe
        if self.route_policy_redistribute.connected:
            # Create an interface list to feed to our routing table
            interfaces: List[str] = []
            if isinstance(self.route_policy_redistribute.connected, list):
                interfaces = self.route_policy_redistribute.connected
            # Add direct protocol for redistribution of connected routes
            rip_direct_protocol = ProtocolDirect(
                constants=self.constants,
                functions=self.functions,
                tables=self.tables,
                birdconfig_globals=self.birdconfig_globals,
                birdattributes=self.birdattributes,
                name="rip",
                interfaces=interfaces,
            )
            self.conf.add(rip_direct_protocol)
            # Add pipe
            rip_direct_pipe = ProtocolPipe(
                birdconfig_globals=self.birdconfig_globals,
                name="rip",
                table_from="rip",
                table_to="direct",
                table_export="none",
                table_import="all",
            )
            self.conf.add(rip_direct_pipe)

    def add_interface(self, interface_name: str, interface_config: RIPInterfaceConfig) -> None:
        """Add interface to RIP."""
        # Make sure the interface exists
        if interface_name not in self.interfaces:
            self.interfaces[interface_name] = {}
        # Grab the config so its easier to work with below
        config = self.interfaces[interface_name]
        # If the interface is just a boolean, we can return...
        if isinstance(interface_config, bool):
            config = interface_config
            return
        if not isinstance(config, dict):
            raise BirdPlanError(f"Conflict RIP config for interface '{interface_name}'")
        # Work through supported configuration
        for key, value in interface_config.items():
            # Make sure key is valid
            if key not in ("metric", "update-time"):
                raise BirdPlanError(f"The RIP config for interface '{interface_name}' item '{key}' hasnt been added")
            # Set the config item
            config[key] = value

    def _interface_config(self) -> List[str]:
        """Generate interface configuration."""

        interface_lines = []
        # Loop with interfaces
        for interface_name in sorted(self.interfaces.keys()):
            # Set "interface" so things are easier to work with below
            interface = self.interfaces[interface_name]
            # If the config is a boolean and its false, skip
            if isinstance(interface, bool) and not interface:
                continue
            # Output interface
            interface_lines.append(f'  interface "{interface_name}" {{')
            # If its not a bollean we have additional configuration to write out
            if isinstance(interface, dict):
                # Loop with config items
                for key, value in interface.items():
                    if (key == "update-time") and value:
                        interface_lines.append(f"    update time {value};")
                    else:
                        interface_lines.append(f"    {key} {value};")
            interface_lines.append("  };")

        return interface_lines

    def _setup_protocol(self, ipv: str) -> None:
        """Set up RIP protocol."""
        if ipv == "4":
            self.conf.add(f"protocol rip rip{ipv} {{")
        elif ipv == "6":
            self.conf.add(f"protocol rip ng rip{ipv} {{")
        self.conf.add(f'  description "RIP protocol for IPv{ipv}";')
        self.conf.add("")
        self.conf.add(f"  vrf {self.birdconfig_globals.vrf};")
        self.conf.add("")
        self.conf.add(f"  ipv{ipv} {{")
        self.conf.add(f"    table t_rip{ipv};")
        self.conf.add("")
        self.conf.add("    export filter f_rip_export;")
        self.conf.add("    import filter f_rip_import;")
        self.conf.add("")
        self.conf.add("  };")
        self.conf.add("")
        self.conf.add(self._interface_config())
        self.conf.add("};")

    def _rip_export_filter(self) -> None:
        """RIP export filter setup."""

        # Set our filter name
        filter_name = "f_rip_export"

        # Configure RIP export filter
        self.conf.add("# RIP export filter")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Redistribute connected
        if self.route_policy_redistribute.connected:
            self.conf.add(f"  {self.rip_functions.redistribute_connected()};")
        # Redistribute kernel routes
        if self.route_policy_redistribute.kernel:
            self.conf.add(f"  {self.functions.redistribute_kernel()};")
        # Redistribute kernel routes
        if self.route_policy_redistribute.kernel_default:
            self.conf.add(f"  {self.functions.redistribute_kernel_default()};")
        # Redistribute RIP routes
        if self.route_policy_redistribute.rip:
            self.conf.add(f"  {self.rip_functions.redistribute_rip()};")
        # Redistribute RIP default routes
        if self.route_policy_redistribute.rip_default:
            self.conf.add(f"  {self.rip_functions.redistribute_rip_default()};")
        # Redistribute static routes
        if self.route_policy_redistribute.static:
            self.conf.add(f"  {self.functions.redistribute_static()};")
        # Redistribute static default routes
        if self.route_policy_redistribute.static_default:
            self.conf.add(f"  {self.functions.redistribute_static_default()};")
        # Else reject
        self.conf.add("  # Reject by default")
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from t_rip export (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _rip_import_filter(self) -> None:
        """RIP import filter setup."""
        # Set our filter name
        filter_name = "f_rip_import"

        # Configure RIP import filter
        self.conf.add("# RIP import filter")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Accept all inbound routes into the table
        self.conf.add("  # Import all RIP routes by default")
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Accepting ", net, " from t_rip import (fallthrough)";')
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _rip_to_master_export_filter(self) -> None:
        """RIP to master export filter setup."""
        # Set our filter name
        filter_name = "f_rip_master_export"

        # Configure export filter to master table
        self.conf.add("# RIP export filter to master table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Accept only RIP routes into the master table
        self.conf.add("  # Export RIP routes to the master table by default")
        self.conf.add(f"  {self.rip_functions.accept_rip()};")
        # Check if we accept the default route
        if self.route_policy_accept.default:
            self.conf.add("  # Export default route to master (accept:rip_default is set)")
            self.conf.add(f"  {self.rip_functions.accept_rip_default()};")
        # Default to reject
        self.conf.add("  # Reject by default")
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from t_rip to master (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _rip_to_master_import_filter(self) -> None:
        """RIP import filter from master table."""
        # Set our filter name
        filter_name = "f_rip_master_import"

        # Configure import filter from master table
        self.conf.add("# RIP import filter from master table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Redistribute connected
        if self.route_policy_redistribute.connected:
            self.conf.add(f"  {self.rip_functions.accept_connected()};")
        # Redistribute static routes
        if self.route_policy_redistribute.static:
            self.conf.add(f"  {self.functions.accept_static()};")
        # Redistribute static default routes
        if self.route_policy_redistribute.static_default:
            self.conf.add(f"  {self.functions.accept_static_default()};")
        # Redistribute kernel routes
        if self.route_policy_redistribute.kernel:
            self.conf.add(f"  {self.functions.accept_kernel()};")
        # Redistribute kernel default routes
        if self.route_policy_redistribute.kernel_default:
            self.conf.add(f"  {self.functions.accept_kernel_default()};")
        # Else accept
        self.conf.add("  # Reject by default")
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from master to t_rip (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    @property
    def interfaces(self) -> RIPInterfaces:
        """Return RIP interfaces."""
        return self._rip_interfaces

    @property
    def rip_attributes(self) -> RIPAttributes:
        """Return our RIP protocol attributes."""
        return self._rip_attributes

    @property
    def rip_functions(self) -> RIPFunctions:
        """Return our RIP protocol functions."""
        return self._rip_functions

    @property
    def route_policy_accept(self) -> RIPRoutePolicyAccept:
        """Return our route policy for accepting of routes from peers into the master table."""
        return self.rip_attributes.route_policy_accept

    @property
    def route_policy_redistribute(self) -> RIPRoutePolicyRedistribute:
        """Return our route policy for redistributing of routes to the main RIP table."""
        return self.rip_attributes.route_policy_redistribute
