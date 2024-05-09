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

"""BIRD configuration parser base class."""

from typing import Any, Dict

from . import BirdConfig

__all__ = ["ConfigParser"]


class ConfigParser:
    """Configuration parser base class."""

    _birdconf: BirdConfig

    def __init__(self, birdconf: BirdConfig) -> None:
        """Initialize configuration parser."""
        self._birdconf = birdconf

    def parse(self, config: Dict[str, Any]) -> None:
        """Configure BGP protocol."""
        raise NotImplementedError("This method must be implemented in a subclass")

    @property
    def birdconf(self) -> BirdConfig:
        """Return the BirdConfig object."""
        return self._birdconf
