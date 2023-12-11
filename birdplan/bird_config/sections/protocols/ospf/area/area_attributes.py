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

"""BIRD OSPF area attributes."""

from typing import Optional

from ......exceptions import BirdPlanError

__all__ = ["OSPFAreaAttributes"]


class OSPFAreaAttributes:  # pylint: disable=too-few-public-methods
    """
    OSPF area attributes.

    Attributes
    ----------
    name : Optional[str]
        Area name.

    """

    _name: Optional[str]

    def __init__(self) -> None:
        """Initialize object."""

        self._name = None

    @property
    def name(self) -> str:
        """Area name."""
        if self._name is None:
            raise BirdPlanError("OSPF area name must be set")
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Area name."""
        self._name = name
