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

"""BIRD configuration sections."""

from .base import SectionBase
from .constants import SectionConstants
from .functions import SectionFunctions
from .logging import SectionLogging
from .main import SectionMain
from .protocols import SectionProtocols
from .router_id import SectionRouterID
from .tables import SectionTables


class Sections(SectionBase):
    """BIRD configuration sections."""

    _logging: SectionLogging
    _main: SectionMain
    _router_id: SectionRouterID
    _constants: SectionConstants
    _functions: SectionFunctions
    _tables: SectionTables
    _protocols: SectionProtocols

    def __init__(self, **kwargs):
        """Initialize object."""
        super().__init__(**kwargs)

        self._logging = SectionLogging(**kwargs)
        self._main = SectionMain(**kwargs)
        self._router_id = SectionRouterID(**kwargs)
        self._constants = SectionConstants(**kwargs)
        self._functions = SectionFunctions(**kwargs)
        self._tables = SectionTables(**kwargs)
        self._protocols = SectionProtocols(constants=self.constants, functions=self.functions, tables=self.tables, **kwargs)

    def configure(self):
        """Configure all sections."""
        self.conf.add(self.logging)
        self.conf.add(self.main)
        self.conf.add(self.router_id)
        self.conf.add(self.constants, deferred=True)
        self.conf.add(self.functions, deferred=True)
        self.conf.add(self.tables, deferred=True)
        self.conf.add(self.protocols)

    @property
    def constants(self) -> SectionConstants:
        """Return the constants section."""
        return self._constants

    @property
    def functions(self) -> SectionFunctions:
        """Return the functions section."""
        return self._functions

    @property
    def logging(self) -> SectionLogging:
        """Return the logging section."""
        return self._logging

    @property
    def main(self) -> SectionMain:
        """Return the main section."""
        return self._main

    @property
    def router_id(self) -> SectionRouterID:
        """Return the router_id section."""
        return self._router_id

    @property
    def tables(self) -> SectionTables:
        """Return the tables section."""
        return self._tables

    @property
    def protocols(self) -> SectionProtocols:
        """Return the protocols section."""
        return self._protocols