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

"""BIRD OSPF protocol attributes."""

from typing import List, Union


class OSPFRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    OSPF route policy for acceptance of routes from OSPF peers into the main OSPF table.

    Attributes
    ----------
    default : bool
        Accept default route. Defaults to `False`.

    """

    default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.default = False


class OSPFRoutePolicyRedistribute:  # pylint: disable=too-few-public-methods
    """
    OSPF route policy for redistributing of routes.

    Attributes
    ----------
    connected : Union[bool, List[str]]
        Redistribute connected routes to the main OSPF table. This attribute is indexed by interface name with a boolean option.
        The interface name can be an exact interface match, or a wildcard with a *.
    kernel : bool
        Redistribute kernel routes to the main OSPF table. Defaults to `False`.
    kernel_default : bool
        Redistribute kernel default routes to the main OSPF table. Defaults to `False`.
    static : bool
        Redistribute static routes to the main OSPF table. Defaults to `False`.
    static_default : bool
        Redistribute static default routes to the main OSPF table. Defaults to `False`.

    """

    connected: Union[bool, List[str]]
    kernel: bool
    kernel_default: bool
    static: bool
    static_default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = False
        self.kernel = False
        self.kernel_default = False
        self.static = False
        self.static_default = False


class OSPFAttributes:  # pylint: disable=too-few-public-methods
    """
    OSPF attributes.

    Attributes
    ----------
    route_policy_accept : OSPFRoutePolicyAccept
        Route policy for acceptance of routes from OSPF peers into our main OSPF table.
    route_policy_redistribute : OSPFRoutePolicyRedistribute
        Route policy for importing of routes from internal tables into our main OSPF table.

    """

    route_policy_accept: OSPFRoutePolicyAccept
    route_policy_redistribute: OSPFRoutePolicyRedistribute

    def __init__(self) -> None:
        """Initialize object."""

        self.route_policy_accept = OSPFRoutePolicyAccept()
        self.route_policy_redistribute = OSPFRoutePolicyRedistribute()
