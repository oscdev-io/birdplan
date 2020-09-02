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

"""BIRD protocol base class."""

from ..base import SectionBase
from ..constants import SectionConstants
from ..functions import SectionFunctions
from ..tables import SectionTables


class SectionProtocolBase(SectionBase):
    """BIRD protocol base class."""

    _section = "BGP Protocol"

    # Global objects to inject configuration
    _constants: SectionConstants
    _functions: SectionFunctions
    _tables: SectionTables

    def __init__(self, **kwargs):
        """Initialize the object."""
        super().__init__(**kwargs)

        # Make sure we have constants passed to us
        if "constants" not in kwargs:
            raise RuntimeError("Protocols require 'constants' to be passed")
        self._constants = kwargs.get("constants")

        # Make sure we have functions passed to us
        if "functions" not in kwargs:
            raise RuntimeError("Protocols require 'functions' to be passed")
        self._functions = kwargs.get("functions")

        # Make sure we have tables passed to us
        if "tables" not in kwargs:
            raise RuntimeError("Protocols require 'tables' to be passed")
        self._tables = kwargs.get("tables")

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
