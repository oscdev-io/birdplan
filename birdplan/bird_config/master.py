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

"""BIRD master table configuration."""

from .base import BirdConfigBase
from .protocol.pipe import BirdConfigProtocolPipe


class BirdConfigMaster(BirdConfigBase):
    """BIRD master table configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Are we going to export routes to the kernel
        self._export_kernel = {
            "static": True,
            "rip": True,
            "ospf": True,
            "bgp": True,
        }

    def configure(self):
        """Configure the master tables."""
        self._addtitle("Master Tables")

        # Setup filters
        self._master_to_kernel_export_filter(4)
        self._master_to_kernel_export_filter(6)

        self._master_to_kernel_import_filter(4)
        self._master_to_kernel_import_filter(6)

        # Configure pipe from kernel table to master table
        kernel_master_pipe = BirdConfigProtocolPipe(
            self, table_from="master", table_to="kernel", table_export_filtered=True, table_import_filtered=True
        )
        kernel_master_pipe.configure()
        self._addline("")

    def _master_to_kernel_import_filter(self, ipv):
        """Master to kernel import filter setup."""
        # Configure import filter to master table
        self._addline(f"filter f_master_kernel{ipv}_import {{")
        self._addline("\t# Accept all routes from the kernel, always")
        self._addline("\tif (source = RTS_INHERIT) then {")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _master_to_kernel_export_filter(self, ipv):
        """Master to kernel export filter setup."""
        # Configure export filter to master table
        self._addline(f"filter f_master_kernel{ipv}_export {{")

        if self.export_kernel_static:
            self._addline("\t# Export static routes to kernel")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        if self.export_kernel_rip:
            self._addline("\t# Export RIP routes to kernel")
            self._addline("\tif (source = RTS_RIP) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        if self.export_kernel_ospf:
            self._addline("\t# Export OSPF routes to kernel")
            # NK: We cannot seem to filter out the device routes
            self._addline("\tif (source ~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2]) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        if self.export_kernel_bgp:
            self._addline("\t# Export BGP routes to kernel")
            self._addline("\tif (source = RTS_BGP) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    @property
    def export_kernel_static(self):
        """Return if we're exporting static to kernel."""
        return self._export_kernel["static"]

    @export_kernel_static.setter
    def export_kernel_static(self, value):
        """Set if we're exporting static routes to kernel."""
        self._export_kernel["static"] = value

    @property
    def export_kernel_rip(self):
        """Return if we're exporting RIP to kernel."""
        return self._export_kernel["rip"]

    @export_kernel_rip.setter
    def export_kernel_rip(self, value):
        """Set if we're exporting RIP routes to kernel."""
        self._export_kernel["rip"] = value

    @property
    def export_kernel_ospf(self):
        """Return if we're exporting OSPF to kernel."""
        return self._export_kernel["ospf"]

    @export_kernel_ospf.setter
    def export_kernel_ospf(self, value):
        """Set if we're exporting OSPF routes to kernel."""
        self._export_kernel["ospf"] = value

    @property
    def export_kernel_bgp(self):
        """Return if we're exporting BGP to kernel."""
        return self._export_kernel["bgp"]

    @export_kernel_bgp.setter
    def export_kernel_bgp(self, value):
        """Set if we're exporting BGP routes to kernel."""
        self._export_kernel["bgp"] = value
