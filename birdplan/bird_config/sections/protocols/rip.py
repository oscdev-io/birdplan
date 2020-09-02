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

"""BIRD RIP protocol configuration."""

from .direct import ProtocolDirect
from .pipe import ProtocolPipe
from .base import SectionProtocolBase
from ....exceptions import BirdPlanError


class ProtocolRIP(SectionProtocolBase):
    """BIRD RIP protocol configuration."""

    _section = "RIP Protocol"

    def __init__(self, **kwargs):
        """Initialize the object."""
        super().__init__(**kwargs)

        # Interfaces
        self._rip_interfaces = {}

        # Some tunables...
        self._rip_accept = {
            "default": False,
        }

        # RIP route redistribution
        self._rip_redistribute = {
            "connected": {},
            "static": False,
            "kernel": False,
            "default": False,
            "rip": True,
        }

    def configure(self):
        """Configure the RIP protocol."""
        super().configure()

        # If we don't have any configuration, just abort
        if not self.interfaces:
            return

        self.tables.conf.append("# RIP Tables")
        self.tables.conf.append("ipv4 table t_rip4;")
        self.tables.conf.append("ipv6 table t_rip6;")
        self.tables.conf.append("")

        # RIP export filters
        self._rip_export_filter(4)
        self._rip_export_filter(6)

        # RIP import filters
        self._rip_import_filter(4)
        self._rip_import_filter(6)

        # RIP to master export filters
        self._rip_to_master_export_filter(4)
        self._rip_to_master_export_filter(6)

        # RIP to master import filters
        self._rip_to_master_import_filter(4)
        self._rip_to_master_import_filter(6)

        # Setup the protocol
        self._setup_protocol(4)
        self._setup_protocol(6)

        # Configure pipe from RIP to the master routing table
        rip_master_pipe = ProtocolPipe(
            birdconf_globals=self.birdconf_globals,
            table_from="rip",
            table_to="master",
            table_export_filtered=True,
            table_import_filtered=True,
        )
        self.conf.add(rip_master_pipe)

        # Check if we're redistributing connected routes, if we are, create the protocol and pipe
        if self.redistribute_connected:
            if "interfaces" not in self.redistribute_connected:
                raise BirdPlanError("RIP redistribute connected requires a list in item 'interfaces' to match interface names")
            # Add direct protocol for redistribution of connected routes
            rip_direct_protocol = ProtocolDirect(
                constants=self.constants,
                functions=self.functions,
                tables=self.tables,
                birdconf_globals=self.birdconf_globals,
                name="rip",
                interfaces=self.redistribute_connected["interfaces"],
            )
            self.conf.add(rip_direct_protocol)
            # Add pipe
            rip_direct_pipe = ProtocolPipe(
                birdconf_globals=self.birdconf_globals,
                name="rip",
                description="RIP",
                table_from="rip",
                table_to="direct",
                table_export="none",
                table_import="all",
            )
            self.conf.add(rip_direct_pipe)

    def add_interface(self, interface_name, interface_config):
        """Add interface to RIP."""
        # Make sure the interface exists
        if interface_name not in self.interfaces:
            self._rip_interfaces[interface_name] = []
        # Grab the config so its easier to work with below
        config = self.interfaces[interface_name]
        # Work through supported configuration
        for item in interface_config:
            for key, value in item.items():
                if key in ("metric", "update-time"):
                    config.append({key: value})
                else:
                    raise BirdPlanError(f"The RIP config for interface '{interface_name}' item '{key}' hasnt been added")

    def _interface_config(self):
        """Generate interface configuration."""

        interface_lines = []
        # Loop with interfaces
        for interface_name in sorted(self.interfaces.keys()):
            interface = self.interfaces[interface_name]
            interface_lines.append(f'  interface "{interface_name}" {{')
            # Loop with config items
            for config_item in interface:
                # Loop with key-value pairs
                for key, value in config_item.items():
                    if (key == "update-time") and value:
                        interface_lines.append(f"    update time {value};")
                    else:
                        interface_lines.append(f"    {key} {value};")
            interface_lines.append("  };")

        return interface_lines

    def _setup_protocol(self, ipv: int):
        """Set up RIP protocol."""
        if ipv == 4:
            self.conf.add(f"protocol rip rip{ipv} {{")
        elif ipv == 6:
            self.conf.add(f"protocol rip ng rip{ipv} {{")
        self.conf.add(f'  description "RIP protocol for IPv{ipv}";')
        self.conf.add("")
        self.conf.add(f"  ipv{ipv} {{")
        self.conf.add(f"    table t_rip{ipv};")
        self.conf.add("")
        self.conf.add(f"    export filter f_rip_export{ipv};")
        self.conf.add(f"    import filter f_rip_import{ipv};")
        self.conf.add("")
        self.conf.add("  };")
        self.conf.add("")
        self.conf.add(self._interface_config())
        self.conf.add("};")

    def _rip_export_filter(self, ipv: int):
        """RIP export filter setup."""
        self.conf.add(f"filter f_rip_export{ipv} {{")
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
        # Redistribute RIP routes
        if self.redistribute_rip:
            self.conf.add("  # Redistribute RIP routes")
            self.conf.add("  if (source = RTS_RIP) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Else reject
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _rip_import_filter(self, ipv: int):
        """RIP import filter setup."""
        # Configure import filter
        self.conf.add(f"filter f_rip_import{ipv} {{")
        # Accept all inbound routes into the table
        self.conf.add("  # Import all RIP routes by default")
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _rip_to_master_export_filter(self, ipv: int):
        """RIP to master export filter setup."""
        # Configure export filter to master4
        self.conf.add(f"filter f_rip{ipv}_master{ipv}_export {{")
        # Check if we accept the default route, if not block it
        if not self.accept_default:
            self.conf.add("  # Do not export default route to master (no accept:default)")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Accept only RIP routes into the master table
        self.conf.add("  # Only export RIP routes to the master table")
        self.conf.add("  if (source = RTS_RIP) then {")
        self.conf.add("    accept;")
        self.conf.add("  }")
        # Default to reject
        self.conf.add("  # Reject everything else;")
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _rip_to_master_import_filter(self, ipv: int):
        """RIP to master import filter setup."""
        # Configure import filter to master table
        self.conf.add(f"filter f_rip{ipv}_master{ipv}_import {{")
        # Redistribute the default route
        if not self.redistribute_default:
            self.conf.add("  # Deny import of default route into RIP (no redistribute_default)")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Redistribute connected
        if self.redistribute_connected:
            self.conf.add("  # Import RTS_DEVICE routes into RIP (redistribute_connected)")
            self.conf.add("  if (source = RTS_DEVICE) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute static routes
        if self.redistribute_static:
            self.conf.add("  # Import RTS_STATIC routes into RIP (redistribute_static)")
            self.conf.add("  if (source = RTS_STATIC) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self.conf.add("  # Import RTS_INHERIT routes (kernel routes) into RIP (redistribute_kernel)")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Else accept
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    @property
    def accept_default(self):
        """Return if we will accept the default route if we get it via RIP."""
        return self._rip_accept["default"]

    @accept_default.setter
    def accept_default(self, value):
        """Set we will accept the default route if we get it via RIP."""
        self._rip_accept["default"] = value

    @property
    def redistribute_connected(self):
        """Return if we redistribute connected routes."""
        return self._rip_redistribute["connected"]

    @redistribute_connected.setter
    def redistribute_connected(self, value):
        """Set redistribute connected routes."""
        self._rip_redistribute["connected"] = value

    @property
    def redistribute_static(self):
        """Return if we redistribute static routes."""
        return self._rip_redistribute["static"]

    @redistribute_static.setter
    def redistribute_static(self, value):
        """Set redistribute static routes."""
        self._rip_redistribute["static"] = value

    @property
    def redistribute_kernel(self):
        """Return if we redistribute kernel routes."""
        return self._rip_redistribute["kernel"]

    @redistribute_kernel.setter
    def redistribute_kernel(self, value):
        """Set redistribute kernel routes."""
        self._rip_redistribute["kernel"] = value

    @property
    def redistribute_default(self):
        """Return if we redistribute the default route."""
        return self._rip_redistribute["default"]

    @redistribute_default.setter
    def redistribute_default(self, value):
        """Set redistribute the default route."""
        self._rip_redistribute["default"] = value

    @property
    def redistribute_rip(self):
        """Return if we redistribute RIP routes."""
        return self._rip_redistribute["rip"]

    @redistribute_rip.setter
    def redistribute_rip(self, value):
        """Set redistribute RIP routes."""
        self._rip_redistribute["rip"] = value

    @property
    def interfaces(self):
        """Return RIP interfaces."""
        return self._rip_interfaces
