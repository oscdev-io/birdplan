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

"""BIRD OSPF area interface attributes."""

from typing import Optional

from .......exceptions import BirdPlanError

__all__ = ["OSPFAreaInterfaceAttributes"]


class OSPFAreaInterfaceAttributes:  # pylint: disable=too-few-public-methods
    """
    OSPF area interface attributes.

    Attributes
    ----------
    name : Optional[str]
        Interface name.

    cost : int
        Interface output cost, defaults to 10.

    ecmp_weight : int
        ECMP weight, defaults to 1.

    hello : Optional[int]
        Helo message interface, defaults to 10 in BIRD.

    wait : Optional[int]
        Wait time between election and building adjacency. Defaults to 4*hello in BIRD.

    stub : bool
        Indicats that this interface is a stub or not, defaults to False.

    """

    _name: Optional[str]

    cost: int
    ecmp_weight: int

    hello: Optional[int]
    wait: Optional[int]

    stub: bool

    def __init__(self) -> None:
        """Initialize object."""

        self._name = None

        self.cost = 10
        self.ecmp_weight = 1

        self.hello = None
        self.wait = None

        self.stub = False

    @property
    def name(self) -> str:
        """Area interface name."""
        if self._name is None:
            raise BirdPlanError("OSPF area interface name must be set")
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Area interface name."""
        self._name = name
