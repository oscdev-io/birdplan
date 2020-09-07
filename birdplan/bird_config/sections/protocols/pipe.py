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

"""BIRD pipe protocol configuration."""

from typing import Callable, List, Union
from ..base import SectionBase
from ...globals import BirdConfigGlobals


PipeTableNameType = Union[str, Callable[[str], str]]


# This class cannot be a decendant of the SectionProtocolBase class or we'll have circular imports
class ProtocolPipe(SectionBase):  # pylint: disable=too-many-instance-attributes
    """BIRD pipe protocol configuration."""

    _name_suffix: str

    _table_from: PipeTableNameType
    _table_to: PipeTableNameType
    _table_export: str
    _table_import: str
    _table_export_filtered: bool
    _table_import_filtered: bool

    # IP versions we're creating a pipe for
    _ipversions: List[str]

    def __init__(
        self,
        birdconfig_globals: BirdConfigGlobals,
        table_from: PipeTableNameType,
        table_to: PipeTableNameType,
        name: str = "",
        table_export: str = "none",
        table_import: str = "none",
        table_export_filtered: bool = False,
        table_import_filtered: bool = False,
        has_ipv4: bool = True,
        has_ipv6: bool = True,
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        # Add a suffix if we have a name
        self._name_suffix = ""
        if name:
            self._name_suffix = f"_{name}"

        # Grab table information
        self._table_from = table_from
        self._table_to = table_to
        self._table_export = table_export
        self._table_import = table_import
        self._table_export_filtered = table_export_filtered
        self._table_import_filtered = table_import_filtered

        # Are we excluding anything?
        self._ipversions = []
        if has_ipv4:
            self._ipversions.append("4")
        if has_ipv6:
            self._ipversions.append("6")

    def configure(self) -> None:
        """Create a pipe protocol."""
        super().configure()

        for ipv in self._ipversions:
            self.conf.add(f"protocol pipe p_{self.table_from(ipv)}_to_{self.table_to(ipv)}{self.name_suffix} {{")
            self.conf.add(f'  description "Pipe from {self.t_table_from(ipv)} to {self.t_table_to(ipv)}{self.name_suffix}";')
            self.conf.add("")
            self.conf.add(f"  table {self.t_table_from(ipv)};")
            self.conf.add(f"  peer table {self.t_table_to(ipv)}{self.name_suffix};")
            self.conf.add("")

            # Check if we're doing export filtering
            if self.table_export_filtered:
                self.conf.add(f"  export filter f_{self.table_from(ipv)}_{self.table_to(ipv)}_export;")
            # If not add per normal
            else:
                self.conf.add(f"  export {self.table_export};")

            # Check if we're doing import filtering
            if self.table_import_filtered:
                self.conf.add(f"  import filter f_{self.table_from(ipv)}_{self.table_to(ipv)}_import;")
            # If not add per normal
            else:
                self.conf.add(f"  import {self.table_import};")

            self.conf.add("};")
            self.conf.add("")

    def table_from(self, ipv: str) -> str:
        """Return table_from with IP version included."""

        # If the table is callable, call it and get the name
        if callable(self._table_from):
            table_from = self._table_from(ipv)
        # Else just use it as a string
        else:
            table_from = f"{self._table_from}{ipv}"

        # If it starts with t_, we need to remove t_ for now
        if table_from.startswith("t_"):
            table_from = table_from[2:]

        return table_from

    def table_to(self, ipv: str) -> str:
        """Return table_to with IP version included."""

        # If the table is callable, call it and get the name
        if callable(self._table_to):
            table_to = self._table_to(ipv)
        # Else just use it as a string
        else:
            table_to = f"{self._table_to}{ipv}"

        # If it starts with t_, we need to remove t_ for now
        if table_to.startswith("t_"):
            table_to = table_to[2:]

        return table_to

    def t_table_from(self, ipv: str) -> str:
        """Return table_from, some tables don't have t_ prefixes."""
        table_name = self.table_from(ipv)
        # If it is not a master table, add t_
        if not table_name.startswith("master"):
            table_name = "t_" + table_name
        return table_name

    def t_table_to(self, ipv: str) -> str:
        """Return table_to, some tables don't have t_ prefixes."""
        table_name = self.table_to(ipv)
        # If it is not a master table, add t_
        if not table_name.startswith("master"):
            table_name = "t_" + table_name
        return table_name

    @property
    def name_suffix(self) -> str:
        """Return our name suffix."""
        return self._name_suffix

    @property
    def table_export(self) -> str:
        """Return that state of us exporting the table."""
        return self._table_export

    @property
    def table_import(self) -> str:
        """Return that state of us importing the table."""
        return self._table_import

    @property
    def table_export_filtered(self) -> bool:
        """Return that state of us exporting the table filtered."""
        return self._table_export_filtered

    @property
    def table_import_filtered(self) -> bool:
        """Return that state of us importing the table filtered."""
        return self._table_import_filtered
