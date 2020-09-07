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

"""Bird configuration package."""

from typing import List, Optional

from .globals import BirdConfigGlobals
from .sections import Sections
from .sections.constants import SectionConstants
from .sections.protocols import SectionProtocols
from .sections.tables import SectionTables


class BirdConfig:
    """BirdConfig is responsible for configuring Bird."""

    _birdconfig_globals: BirdConfigGlobals

    _sections: Sections

    def __init__(self) -> None:
        """Initialize the object."""
        super().__init__()

        self._birdconfig_globals = BirdConfigGlobals()
        self._sections = Sections(self.birdconfig_globals)

    def get_config(self) -> List[str]:
        """Return the Bird configuration."""

        self.sections.configure()

        return self.sections.conf.lines

    @property
    def birdconfig_globals(self) -> BirdConfigGlobals:
        """Return our global configuration options."""
        return self._birdconfig_globals

    # HELPERS

    @property
    def log_file(self) -> Optional[str]:
        """Return the log file to use."""
        return self.birdconfig_globals.log_file

    @log_file.setter
    def log_file(self, log_file: str) -> None:
        """Set the log file to use."""
        self.birdconfig_globals.log_file = log_file

    @property
    def debug(self) -> bool:
        """Return debugging mode."""
        return self.birdconfig_globals.debug

    @debug.setter
    def debug(self, debug: bool) -> None:
        """Set debugging mode."""
        self.birdconfig_globals.debug = debug

    @property
    def test_mode(self) -> bool:
        """Return if we're running in test mode."""
        return self.birdconfig_globals.test_mode

    @test_mode.setter
    def test_mode(self, test_mode: bool) -> None:
        """Set test mode."""
        self.birdconfig_globals.test_mode = test_mode

    @property
    def router_id(self) -> str:
        """Return our router_id."""
        return self.sections.router_id.router_id

    @router_id.setter
    def router_id(self, router_id: str) -> None:
        """Set router_id."""
        self.sections.router_id.router_id = router_id

    @property
    def sections(self) -> Sections:
        """Return our sections."""
        return self._sections

    @property
    def constants(self) -> SectionConstants:
        """Return our constants."""
        return self.sections.constants

    @property
    def tables(self) -> SectionTables:
        """Return our master config."""
        return self.sections.tables

    @property
    def protocols(self) -> SectionProtocols:
        """Return our protocols."""
        return self.sections.protocols
