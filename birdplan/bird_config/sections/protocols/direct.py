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

"""BIRD direct protocol configuration."""

from typing import List, Optional
from .base import SectionProtocolBase
from ..constants import SectionConstants
from ..functions import SectionFunctions
from ..tables import SectionTables
from ...globals import BirdConfigGlobals


class ProtocolDirect(SectionProtocolBase):
    """BIRD direct protocol configuration."""

    _name_suffix: str
    _interfaces: List[str]

    def __init__(
        self,
        birdconfig_globals: BirdConfigGlobals,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
        name: str = "",
        interfaces: Optional[List[str]] = None,
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals, constants, functions, tables)

        # Add a suffix if we have a name
        if name:
            self._name_suffix = f"_{name}"
        else:
            self._section = "Direct Protocol"
            self._name_suffix = ""

        # Grab the list of interfaces we need
        if interfaces:
            self._interfaces = interfaces
        else:
            self._interfaces = []

    def configure(self) -> None:
        """Configure the direct protocol."""
        super().configure()

        # If we have a list of interfaces, create the config lines
        interface_lines = []
        if self.interfaces:
            # Create list of quoted interfaces
            interface_list = []
            for interface in self.interfaces:
                interface_list.append(f'"{interface}"')
            # Drop in a comma between them
            interface_str = ", ".join(interface_list)
            interface_lines.append("")
            interface_lines.append(f"  interface {interface_str};")

        self.tables.conf.append(f"# Direct Tables: {self.name_suffix}")
        self.tables.conf.append(f"ipv4 table t_direct4{self.name_suffix};")
        self.tables.conf.append(f"ipv6 table t_direct6{self.name_suffix};")
        self.tables.conf.append("")

        self._setup_protocol("4", interface_lines)
        self._setup_protocol("6", interface_lines)

    def _setup_protocol(self, ipv: str, lines: List[str]) -> None:

        protocol_name = f"direct{ipv}{self.name_suffix}"

        self.conf.add(f"protocol direct {protocol_name} {{")
        self.conf.add('  description "Direct protocol for IPv%s";' % ipv)
        self.conf.add("")
        self.conf.add("  ipv%s {" % ipv)
        self.conf.add(f"    table t_{protocol_name};")
        self.conf.add("")
        self.conf.add("    export none;")
        self.conf.add("    import all;")
        self.conf.add("  };")
        self.conf.add(lines)
        self.conf.add("};")
        self.conf.add("")

    @property
    def name_suffix(self) -> str:
        """Return our name suffix."""
        return self._name_suffix

    @property
    def interfaces(self) -> List[str]:
        """Return our interfaces."""
        return self._interfaces
