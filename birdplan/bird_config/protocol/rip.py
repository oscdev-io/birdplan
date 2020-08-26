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

from ..base import BirdConfigBase
from .direct import BirdConfigProtocolDirect
from .pipe import BirdConfigProtocolPipe


class BirdConfigProtocolRIP(BirdConfigBase):
    """BIRD RIP protocol configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

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

    def _interface_config(self):
        """Generate interface configuration."""

        interface_lines = []
        # Loop with interfaces
        for interface_name in sorted(self.interfaces.keys()):
            interface = self.interfaces[interface_name]
            interface_lines.append('\tinterface "%s" {' % interface_name)
            # Loop with config items
            for config_item in interface:
                # Loop with key-value pairs
                for key, value in config_item.items():
                    if (key == "update-time") and value:
                        interface_lines.append("\t\tupdate time %s;" % value)
                    else:
                        interface_lines.append("\t\t%s %s;" % (key, value))
            interface_lines.append("\t};")

        return interface_lines

    def _setup_protocol(self, ipv):
        """Set up RIP protocol."""
        if ipv == 4:
            self._addline("protocol rip rip%s {" % ipv)
        elif ipv == 6:
            self._addline("protocol rip ng rip%s {" % ipv)
        self._addline('\tdescription "RIP protocol for IPv%s";' % ipv)
        self._addline("")
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_rip%s;" % ipv)
        self._addline("")
        self._addline("\t\texport filter f_rip_export%s;" % ipv)
        self._addline("\t\timport filter f_rip_import%s;" % ipv)
        self._addline("")
        self._addline("\t};")
        self._addline("")
        self._addlines(self._interface_config())
        self._addline("};")

    def _rip_export_filter(self, ipv):
        """RIP export filter setup."""
        self._addline("filter f_rip_export%s {" % ipv)
        # Redistribute the default route
        if not self.redistribute_default:
            self._addline("\t# Reject redistribution of the default route")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute connected
        if self.redistribute_connected:
            self._addline("\t# Redistribute connected")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute_static:
            self._addline("\t# Redistribute static routes")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self._addline("\t# Redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute RIP routes
        if self.redistribute_rip:
            self._addline("\t# Redistribute RIP routes")
            self._addline("\tif (source = RTS_RIP) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else reject
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _rip_import_filter(self, ipv):
        """RIP import filter setup."""
        # Configure import filter
        self._addline("filter f_rip_import%s {" % ipv)
        # Accept all inbound routes into the table
        self._addline("\t# Import all RIP routes by default")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

    def _rip_to_master_export_filter(self, ipv):
        """RIP to master export filter setup."""
        # Configure export filter to master4
        self._addline("filter f_rip_master%s_export {" % ipv)
        # Check if we accept the default route, if not block it
        if not self.accept_default:
            self._addline("\t# Do not export default route to master (no accept:default)")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Accept only RIP routes into the master table
        self._addline("\t# Only export RIP routes to the master table")
        self._addline("\tif (source = RTS_RIP) then {")
        self._addline("\t\taccept;")
        self._addline("\t}")
        # Default to reject
        self._addline("\t# Reject everything else;")
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _rip_to_master_import_filter(self, ipv):
        """RIP to master import filter setup."""
        # Configure import filter to master table
        self._addline("filter f_rip_master%s_import {" % ipv)
        # Redistribute the default route
        if not self.redistribute_default:
            self._addline("\t# Deny import of default route into RIP (no redistribute_default)")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute connected
        if self.redistribute_connected:
            self._addline("\t# Import RTS_DEVICE routes into RIP (redistribute_connected)")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute_static:
            self._addline("\t# Import RTS_STATIC routes into RIP (redistribute_static)")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self._addline("\t# Import RTS_INHERIT routes (kernel routes) into RIP (redistribute_kernel)")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else accept
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def configure(self):
        """Configure the RIP protocol."""

        # If we don't have any configuration, just abort
        if not self.interfaces:
            return

        self._addtitle("RIP Protocol")
        self._addline("# RIP Tables")
        self._addline("ipv4 table t_rip4;")
        self._addline("ipv6 table t_rip6;")
        self._addline("")

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
        rip_master_pipe = BirdConfigProtocolPipe(
            self, table_from="rip", table_to="master", table_export_filtered=True, table_import_filtered=True
        )
        rip_master_pipe.configure()

        # Check if we're redistributing connected routes, if we are, create the protocol and pipe
        if self.redistribute_connected:
            if "interfaces" not in self.redistribute_connected:
                raise RuntimeError('RIP redistribute connected requires a list in item "interfaces" to match interface names')
            # Add direct protocol for redistribution of connected routes
            rip_direct_protocol = BirdConfigProtocolDirect(self, name="rip", interfaces=self.redistribute_connected["interfaces"])
            rip_direct_protocol.configure()
            # Add pipe
            rip_direct_pipe = BirdConfigProtocolPipe(
                self, name="rip", description="RIP", table_from="rip", table_to="direct", table_export="none", table_import="all"
            )
            rip_direct_pipe.configure()

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
                    raise RuntimeError(
                        'The RIP config for interface "%s" item "%s" hasnt been added to Salt yet' % (interface_name, key)
                    )

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