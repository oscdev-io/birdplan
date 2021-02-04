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

"""BIRD OSPF protocol configuration."""

from typing import Any, Dict, List
from .ospf_attributes import OSPFAttributes, OSPFRoutePolicyAccept, OSPFRoutePolicyRedistribute
from .ospf_functions import OSPFFunctions
from ..direct import ProtocolDirect
from ..pipe import ProtocolPipe, ProtocolPipeFilterType
from ..base import SectionProtocolBase
from ...constants import SectionConstants
from ...functions import SectionFunctions
from ...tables import SectionTables
from ....globals import BirdConfigGlobals
from .....exceptions import BirdPlanError

OSPFAreaConfig = Dict[str, str]
OSPFAreas = Dict[str, OSPFAreaConfig]

OSPFInterfaceConfig = Dict[str, Any]
OSPFInterfaces = Dict[str, OSPFInterfaceConfig]


class ProtocolOSPF(SectionProtocolBase):
    """BIRD OSPF protocol configuration."""

    _areas: OSPFAreas
    _interfaces: OSPFInterfaces

    _ospf_attributes: OSPFAttributes
    # OSPF functions
    _ospf_functions: OSPFFunctions

    def __init__(
        self, birdconfig_globals: BirdConfigGlobals, constants: SectionConstants, functions: SectionFunctions, tables: SectionTables
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals, constants, functions, tables)

        # Set section name
        self._section = "OSPF Protocol"

        # OSPF areas
        self._areas = {}
        self._interfaces = {}

        self._ospf_attributes = OSPFAttributes()
        # Setup OSPF functions
        self._ospf_functions = OSPFFunctions(self.birdconfig_globals, self.functions)

    def configure(self) -> None:
        """Configure the OSPF protocol."""
        super().configure()

        # If we don't have any configuration, just abort
        if not self.areas:
            return

        self.functions.conf.append(self.ospf_functions, deferred=True)

        self.tables.conf.append("# OSPF Tables")
        self.tables.conf.append("ipv4 table t_ospf4;")
        self.tables.conf.append("ipv6 table t_ospf6;")
        self.tables.conf.append("")

        self._ospf_export_filter()
        self._ospf_import_filter()
        self._ospf_to_master_export_filter()
        self._ospf_to_master_import_filter()

        # OSPF protocol configuration
        self._setup_protocol("4")
        self._setup_protocol("6")

        # Configure pipe from OSPF to the master routing table
        ospf_master_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from="ospf",
            table_to="master",
            export_filter_type=ProtocolPipeFilterType.UNVERSIONED,
            import_filter_type=ProtocolPipeFilterType.UNVERSIONED,
        )
        self.conf.add(ospf_master_pipe)

        # Check if we're redistributing connected routes, if we are, create the protocol and pipe
        if self.route_policy_redistribute.connected:
            # Create an interface list to feed to our routing table
            interfaces: List[str] = []
            if isinstance(self.route_policy_redistribute.connected, list):
                interfaces = self.route_policy_redistribute.connected
            # Add direct protocol for redistribution of connected routes
            ospf_direct_protocol = ProtocolDirect(
                self.birdconfig_globals,
                self.constants,
                self.functions,
                self.tables,
                name="ospf",
                interfaces=interfaces,
            )
            self.conf.add(ospf_direct_protocol)
            # Add pipe
            ospf_direct_pipe = ProtocolPipe(
                self.birdconfig_globals,
                name="ospf",
                table_from="ospf",
                table_to="direct",
                table_export="none",
                table_import="all",
            )
            self.conf.add(ospf_direct_pipe)

    def add_area(self, area_name: str, area_config: OSPFAreaConfig) -> None:
        """Add area to OSPF."""
        # Make sure the area exists
        if area_name not in self.areas:
            self._areas[area_name] = area_config

    def add_interface(self, area_name: str, interface_name: str, interface_config: OSPFInterfaceConfig) -> None:
        """Add interface to OSPF."""
        # Make sure the area exists
        if area_name not in self.interfaces:
            self._interfaces[area_name] = {}
        # Make sure the interface exists
        if interface_name not in self.interfaces[area_name]:
            self._interfaces[area_name][interface_name] = []
        # Grab the config so its easier to work with below
        config = self.interfaces[area_name][interface_name]
        # Work through supported configuration
        for key, value in interface_config.items():
            if key in ("hello", "wait"):
                config.append({key: value})
            elif key == "stub":
                if not value:
                    BirdPlanError(f"The OSPF default config for interface '{interface_name}' item 'stub' is 'false'")
                config.append({key: value})
            else:
                raise BirdPlanError(f"The OSPF config for interface '{interface_name}' item '{key}' isn't supported")

    def _area_config(self) -> List[str]:
        """Generate area configuration."""

        area_lines = []
        for area_name in self.interfaces:
            area_lines.append(f"  area {area_name} {{")
            # Loop with area config items
            # NK: NOT USED ATM
            #            for key, value in self.areas[area_name].items():
            #                area_lines.append(f"    {key} {value};")
            # Loop with interfaces
            for interface_name in sorted(self.interfaces[area_name].keys()):
                interface = self.interfaces[area_name][interface_name]
                area_lines.append(f'    interface "{interface_name}" {{')
                # Loop with config items
                for config_item in interface:
                    # Loop with key-value pairs
                    for key, value in config_item.items():
                        if (key == "stub") and value:
                            area_lines.append(f"      {key};")
                        else:
                            area_lines.append(f"      {key} {value};")
                area_lines.append("    };")
            # End off area
            area_lines.append("  };")

        return area_lines

    def _setup_protocol(self, ipv: str) -> None:
        self.conf.add(f"protocol ospf v3 ospf{ipv} {{")
        self.conf.add(f'  description "OSPF protocol for IPv{ipv}";')
        self.conf.add("")
        self.conf.add(f"  ipv{ipv} {{")
        self.conf.add(f"    table t_ospf{ipv};")
        self.conf.add("")
        self.conf.add("    export filter f_ospf_export;")
        self.conf.add("    import filter f_ospf_import;")
        self.conf.add("")
        self.conf.add("  };")
        self.conf.add("")
        self.conf.add(self._area_config())
        self.conf.add("};")
        self.conf.add("")

    def _ospf_export_filter(self) -> None:
        """OSPF export filter setup."""
        # Set our filter name
        filter_name = "f_ospf_export"

        # Configure OSPF export filter
        self.conf.add("# OSPF export filter")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Redistribute connected
        if self.route_policy_redistribute.connected:
            self.conf.add(f"  {self.ospf_functions.redistribute_connected()};")
        # Redistribute kernel routes
        if self.route_policy_redistribute.kernel:
            self.conf.add(f"  {self.functions.redistribute_kernel()};")
        # Redistribute kernel routes
        if self.route_policy_redistribute.kernel_default:
            self.conf.add(f"  {self.functions.redistribute_kernel_default()};")
        # NK: May affect inter-area routes???? removed for now
        # # Redistribute OSPF routes
        # self.conf.add(f"  {self.functions.redistribute_ospf()};")
        # Redistribute static routes
        if self.route_policy_redistribute.static:
            self.conf.add(f"  {self.functions.redistribute_static()};")
        # Redistribute static default routes
        if self.route_policy_redistribute.static_default:
            self.conf.add(f"  {self.functions.redistribute_static_default()};")
        # Else reject
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from t_ospf export (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _ospf_import_filter(self) -> None:
        """OSPF import filter setup."""
        # Set our filter name
        filter_name = "f_ospf_import"

        # Configure OSPF import filter
        self.conf.add("# OSPF import filter")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        # Accept all inbound routes into the table
        self.conf.add("  # Import all OSPF routes by default")
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Accepting ", net, " from t_ospf import (fallthrough)";')
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _ospf_to_master_export_filter(self) -> None:
        """OSPF to master export filter setup."""
        # Set our filter name
        filter_name = "f_ospf_master_export"

        # Configure export filter to master table
        self.conf.add("# OSPF export filter to master table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Accept only OSPF routes into the master table
        self.conf.add("  # Export OSPF routes to the master table by default")
        self.conf.add(f"  {self.ospf_functions.accept_ospf()};")
        # Check if we accept the default route
        if self.route_policy_accept.default:
            self.conf.add("  # Export default route to master (accept:ospf_default is set)")
            self.conf.add(f"  {self.ospf_functions.accept_ospf_default()};")
        # Default to reject
        self.conf.add("  # Reject everything else;")
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from t_ospf to master (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _ospf_to_master_import_filter(self) -> None:
        """OSPF to master import filter setup."""
        # Set our filter name
        filter_name = "f_ospf_master_import"

        # Configure import filter from master table
        self.conf.add("# OSPF import filter from master table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Redistribute connected
        if self.route_policy_redistribute.connected:
            self.conf.add(f"  {self.ospf_functions.accept_connected()};")
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
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from master to t_ospf (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    @property
    def areas(self) -> OSPFAreas:
        """Return OSPF areas."""
        return self._areas

    @property
    def interfaces(self) -> OSPFInterfaces:
        """Return OSPF interfaces."""
        return self._interfaces

    @property
    def ospf_attributes(self) -> OSPFAttributes:
        """Return our OSPF protocol attributes."""
        return self._ospf_attributes

    @property
    def ospf_functions(self) -> OSPFFunctions:
        """Return our OSPF protocol functions."""
        return self._ospf_functions

    @property
    def route_policy_accept(self) -> OSPFRoutePolicyAccept:
        """Return our route policy for accepting of routes from peers into the master table."""
        return self.ospf_attributes.route_policy_accept

    @property
    def route_policy_redistribute(self) -> OSPFRoutePolicyRedistribute:
        """Return our route policy for redistributing of routes to the main OSPF table."""
        return self.ospf_attributes.route_policy_redistribute
