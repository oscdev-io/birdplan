#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

from ....globals import BirdConfigGlobals
from ...base import SectionBase
from ...protocols.pipe import ProtocolPipe, ProtocolPipeFilterType
from .master_attributes import MasterTableAttributes, MasterTableRoutePolicyExport

__all__ = ["TableMaster"]


class TableMaster(SectionBase):
    """BIRD master table configuration."""

    _master_attributes: MasterTableAttributes

    def __init__(self, birdconfig_globals: BirdConfigGlobals) -> None:
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        # Set section header
        self._section = "Master Table"

        self._master_attributes = MasterTableAttributes()

    def configure(self) -> None:
        """Configure the master tables."""
        super().configure()

        # Setup filters
        self._master_to_kernel_export_filter("4")
        self._master_to_kernel_export_filter("6")

        self._master_to_kernel_import_filter("4")
        self._master_to_kernel_import_filter("6")

        # Configure pipe from kernel table to master table
        kernel_master_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from="master",
            table_to="kernel",
            export_filter_type=ProtocolPipeFilterType.VERSIONED,
            import_filter_type=ProtocolPipeFilterType.VERSIONED,
        )
        self.conf.add(kernel_master_pipe)

    def _master_to_kernel_import_filter(self, ipv: str) -> None:
        """Master to kernel import filter setup."""
        # Configure import filter to master table
        self.conf.add(f"filter f_master{ipv}_kernel{ipv}_import {{")
        self.conf.add("  # Accept all routes from the kernel, always")
        self.conf.add("  if (source = RTS_INHERIT) then {")
        self.conf.add("    accept;")
        self.conf.add("  }")
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _master_to_kernel_export_filter(self, ipv: str) -> None:
        """Master to kernel export filter setup."""
        # Configure export filter to master table
        self.conf.add(f"filter f_master{ipv}_kernel{ipv}_export {{")

        if self.route_policy_export.kernel.static:
            self.conf.add("  # Export static routes to kernel")
            self.conf.add("  if (source = RTS_STATIC) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")

        if self.route_policy_export.kernel.rip:
            self.conf.add("  # Export RIP routes to kernel")
            self.conf.add("  if (source = RTS_RIP) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")

        if self.route_policy_export.kernel.ospf:
            self.conf.add("  # Export OSPF routes to kernel")
            # NK: We cannot seem to filter out the device routes
            self.conf.add("  if (source ~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2]) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")

        if self.route_policy_export.kernel.bgp:
            self.conf.add("  # Export BGP routes to kernel")
            self.conf.add("  if (source = RTS_BGP) then {")
            self.conf.add("    accept;")
            self.conf.add("  }")

        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    @property
    def master_attributes(self) -> MasterTableAttributes:
        """Return our table attributes."""
        return self._master_attributes

    @property
    def route_policy_export(self) -> MasterTableRoutePolicyExport:
        """Return our route policy for exporting routes from the master table."""
        return self.master_attributes.route_policy_export
