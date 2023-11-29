#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
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

"""BIRD protocol specific functions base class."""

import textwrap
from collections import OrderedDict
from typing import Dict

from ....bird_config.globals import BirdConfigGlobals
from ..base import SectionBase
from ..functions import SectionFunctions


class ProtocolFunctionsBase(SectionBase):  # pylint: disable=too-many-public-methods
    """BIRD protocol specific functions base class."""

    _functions: SectionFunctions

    bird_functions: Dict[str, str]

    def __init__(self, birdconfig_globals: BirdConfigGlobals, functions: SectionFunctions):
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        self._functions = functions
        self.bird_functions = OrderedDict()

    def configure(self) -> None:
        """Configure global constants."""
        super().configure()

        # Check if we're adding functions
        for _, content in self.bird_functions.items():
            self.conf.add(textwrap.dedent(content))
            self.conf.add("")

    @property
    def functions(self) -> SectionFunctions:
        """Return the functions section."""
        return self._functions
