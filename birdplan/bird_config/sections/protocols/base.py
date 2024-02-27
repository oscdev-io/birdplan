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

"""BIRD protocol base class."""

from ...globals import BirdConfigGlobals
from ..base import SectionBase
from ..constants import SectionConstants
from ..functions import SectionFunctions
from ..tables import SectionTables

__all__ = ["SectionProtocolBase"]


class SectionProtocolBase(SectionBase):
    """BIRD protocol base class."""

    # Global objects to inject configuration
    _constants: SectionConstants
    _functions: SectionFunctions
    _tables: SectionTables

    def __init__(
        self,
        birdconfig_globals: BirdConfigGlobals,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        self._constants = constants
        self._functions = functions
        self._tables = tables

    @property
    def constants(self) -> SectionConstants:
        """Return the global constants section."""
        return self._constants

    @property
    def functions(self) -> SectionFunctions:
        """Return the global functions section."""
        return self._functions

    @property
    def tables(self) -> SectionTables:
        """Return the global tables section."""
        return self._tables
