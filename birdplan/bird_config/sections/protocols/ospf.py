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

from .direct import ProtocolDirect
from .pipe import ProtocolPipe
from .base import SectionProtocolBase
from ....exceptions import BirdPlanError


class ProtocolOSPF(SectionProtocolBase):
    """BIRD OSPF protocol configuration."""

    _section = "OSPF Protocol"

    def __init__(self, **kwargs):
        """Initialize the object."""
        super().__init__(**kwargs)

        # Areas and interfaces
        self._ospf_areas = {}
        self._ospf_interfaces = {}

        # Some tunables...
        self._ospf_accept = {
            "default": False,
        }

        # OSPF route redistribution
        self._ospf_redistribute = {
            "connected": {},
            "static": False,
            "kernel": False,
            "default": False,
        }

    def configure(self):
        """Configure the OSPF protocol."""
        super().configure()

        # If we don't have any configuration, just abort
        if not self.areas:
            return

        self.tables.conf.append("# OSPF Tables")
        self.tables.conf.append("ipv4 table t_ospf4;")
        self.tables.conf.append("ipv6 table t_ospf6;")
        self.tables.conf.append("")

        # OSPF export filters
        self._ospf_export_filter(4)
        self._ospf_export_filter(6)

        # OSPF import filters
        self._ospf_import_filter(4)
        self._ospf_import_filter(6)

        # OSPF to master export filters
        self._ospf_to_master_export_filter(4)
        self._ospf_to_master_export_filter(6)

        # OSPF to master import filters
        self._ospf_to_master_import_filter(4)
        self._ospf_to_master_import_filter(6)

        # OSPF protocol configuration
        # FIXME - assigned but not used?  # pylint:disable=fixme
        # area_lines = self._area_config()
        self._setup_protocol(4)
        self._setup_protocol(6)

        # Configure pipe from OSPF to the master routing table
        ospf_master_pipe = ProtocolPipe(
            birdconf_globals=self.birdconf_globals,
            table_from="ospf",
            table_to="master",
            table_export_filtered=True,
            table_import_filtered=True,
        )
        self.conf.add(ospf_master_pipe)

        # Check if we're redistributing connected routes, if we are, create the protocol and pipe
        if self.redistribute_connected:
            if "interfaces" not in self.redistribute_connected:
                raise BirdPlanError("OSPF redistribute connected requires a list in item 'interfaces' to match interface names")
            # Add direct protocol for redistribution of connected routes
            ospf_direct_protocol = ProtocolDirect(
                constants=self.constants,
                functions=self.functions,
                tables=self.tables,
                birdconf_globals=self.birdconf_globals,
                name="ospf",
                interfaces=self.redistribute_connected["interfaces"],
            )
            self.conf.add(ospf_direct_protocol)
            # Add pipe
            ospf_direct_pipe = ProtocolPipe(
                birdconf_globals=self.birdconf_globals,
                name="ospf",
                descospftion="ospf",
                table_from="ospf",
                table_to="direct",
                table_export="none",
                table_import="all",
            )
            self.conf.add(ospf_direct_pipe)

    def add_area(self, area_name, area_config=None):
        """Add area to OSPF."""
        # Make sure the area exists
        if area_name not in self.areas:
            self._ospf_areas[area_name] = area_config

    def add_interface(self, area_name, interface_name, interface_config):
        """Add interface to OSPF."""
        # Make sure the area exists
        if area_name not in self.interfaces:
            self._ospf_interfaces[area_name] = {}
        # Make sure the interface exists
        if interface_name not in self.interfaces[area_name]:
            self._ospf_interfaces[area_name][interface_name] = []
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
                raise BirdPlanError(f"The OSPF config for interface '{interface_name}' item '{key}' hasnt been added to Salt yet")

    def _area_config(self):
        """Generate area configuration."""

        area_lines = []
        for area_name in self.interfaces:
            area_lines.append(f"  area {area_name} {{")
            # Loop with area config items
            for config_item in self.areas[area_name]:
                # Loop with key-value pairs
                for key, value in config_item.items():
                    area_lines.append(f"    {key} {value};")
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

    def _setup_protocol(self, ipv: int):
        self.conf.add(f"protocol ospf v3 ospf{ipv} {{")
        self.conf.add(f'  description "OSPF protocol for IPv{ipv}";')
        self.conf.add("")
        self.conf.add(f"  ipv{ipv} {{")
        self.conf.add(f"    table t_ospf{ipv};")
        self.conf.add("")
        self.conf.add(f"    export filter f_ospf_export{ipv};")
        self.conf.add(f"    import filter f_ospf_import{ipv};")
        self.conf.add("")
        self.conf.add("  };")
        self.conf.add("")
        self.conf.add(self._area_config())
        self.conf.add("};")
        self.conf.add("")

    def _ospf_export_filter(self, ipv: int):
        """OSPF export filter setup."""

        self.conf.add(f"filter f_ospf_export{ipv} {{")
        # Redistribute the default route
        if not self.redistribute_default:
            self.conf.add("  # Reject redistribution of the default route")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Redistribute connected
        if self.redistribute_connected:
            self.conf.add("  # Redistribute connected")
            self.conf.add("  if (source = RTS_DEVICE) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute static routes
        if self.redistribute_static:
            self.conf.add("  # Redistribute static routes")
            self.conf.add("  if (source = RTS_STATIC) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self.conf.add("  # Redistribute kernel routes")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Else reject
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _ospf_import_filter(self, ipv: int):
        """OSPF import filter setup."""
        # Configure import4 filter
        self.conf.add(f"filter f_ospf_import{ipv} {{")
        # Accept all inbound routes into the t_ospf4 table
        self.conf.add("  # Import all OSPF routes by default")
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _ospf_to_master_export_filter(self, ipv: int):
        """OSPF to master export filter setup."""
        # Configure export filter to master table
        self.conf.add(f"filter f_ospf{ipv}_master{ipv}_export {{")
        # Check if we accept the default route, if not block it
        if not self.accept_default:
            self.conf.add("  # Do not export default route to master (no accept:default)")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Accept only OSPF routes into the master table
        self.conf.add("  # Only export OSPF routes to the master table")
        # NK: We cannot seem to filter out the device routes
        self.conf.add("  if (source ~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2]) then {")
        self.conf.add("    accept;")
        self.conf.add("  }")
        # Default to reject
        self.conf.add("  # Reject everything else;")
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _ospf_to_master_import_filter(self, ipv: int):
        """OSPF to master import filter setup."""
        # Configure import filter to master table
        self.conf.add(f"filter f_ospf{ipv}_master{ipv}_import {{")
        # Redistribute the default route
        if not self.redistribute_default:
            self.conf.add("  # Deny import of default route into OSPF (no redistribute_default)")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Redistribute connected
        if self.redistribute_connected:
            self.conf.add("  # Import RTS_DEVICE routes into OSPF (redistribute_connected)")
            self.conf.add("  if (source = RTS_DEVICE) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute static routes
        if self.redistribute_static:
            self.conf.add("  # Import RTS_STATIC routes into OSPF (redistribute_static)")
            self.conf.add("  if (source = RTS_STATIC) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self.conf.add("  # Import RTS_INHERIT routes (kernel routes) into OSPF (redistribute_kernel)")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Else accept
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    @property
    def accept_default(self):
        """Return if we accept the default route if we get it via OSPF."""
        return self._ospf_accept["default"]

    @accept_default.setter
    def accept_default(self, value):
        """Set if we accept the default route if we get it via OSPF."""
        self._ospf_accept["default"] = value

    @property
    def redistribute_connected(self):
        """Return if we redistribute connected routes."""
        return self._ospf_redistribute["connected"]

    @redistribute_connected.setter
    def redistribute_connected(self, value):
        """Set redistribute connected routes."""
        self._ospf_redistribute["connected"] = value

    @property
    def redistribute_static(self):
        """Return if we redistribute static routes."""
        return self._ospf_redistribute["static"]

    @redistribute_static.setter
    def redistribute_static(self, value):
        """Set if we redistribute static routes."""
        self._ospf_redistribute["static"] = value

    @property
    def redistribute_kernel(self):
        """Return if we redistribute kernel routes."""
        return self._ospf_redistribute["kernel"]

    @redistribute_kernel.setter
    def redistribute_kernel(self, value):
        """Set if we redistribute kernel routes."""
        self._ospf_redistribute["kernel"] = value

    @property
    def redistribute_default(self):
        """Return if we redistribute the default route."""
        return self._ospf_redistribute["default"]

    @redistribute_default.setter
    def redistribute_default(self, value):
        """Set if we redistribute the default route."""
        self._ospf_redistribute["default"] = value

    @property
    def areas(self):
        """Return OSPF areas."""
        return self._ospf_areas

    @property
    def interfaces(self):
        """Return OSPF interfaces."""
        return self._ospf_interfaces
