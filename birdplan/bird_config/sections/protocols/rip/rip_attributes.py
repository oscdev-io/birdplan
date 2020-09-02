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

"""BIRD RIP protocol attributes."""

from typing import Dict


class RIPRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    RIP route policy for acceptance of routes from RIP peers into the main RIP table.

    Attributes
    ----------
    default : bool
        Accept default route. Defaults to `False`.

    """

    default: bool

    def __init__(self):
        """Initialize object."""
        self.default = False


class RIPRoutePolicyRedistribute:  # pylint: disable=too-few-public-methods
    """
    RIP route policy for redistributing of routes.

    Attributes
    ----------
    connected : Dict[str, bool]
        Redistribute connected routes to the main RIP table. This attribute is indexed by interface name with a boolean option.
        The interface name can be an exact interface match, or a wildcard with a *.
    default: Dict[str, Bool]
        Redistribute the default to the main RIP table. Defaults to `False`.
    kernel : bool
        Redistribute kernel routes to the main RIP table. Defaults to `False`.
    rip : bool
        Redistribute rip routes to the main RIP table. Defaults to `False`.
    static : bool
        Redistribute static routes to the main RIP table. Defaults to `False`.

    """

    connected: Dict[str, bool]
    default: bool
    kernel: bool
    static: bool

    def __init__(self):
        """Initialize object."""
        self.connected = {}
        self.default = False
        self.kernel = False
        self.rip = True
        self.static = False


class RIPAttributes:  # pylint: disable=too-few-public-methods
    """
    RIP attributes.

    Attributes
    ----------
    route_policy_accept : RIPRoutePolicyAccept
        Route policy for acceptance of routes from RIP peers into our main RIP table.
    route_policy_redistribute : RIPRoutePolicyRedistribute
        Route policy for importing of routes from internal tables into our main RIP table.

    """

    route_policy_accept: RIPRoutePolicyAccept
    route_policy_redistribute: RIPRoutePolicyRedistribute

    def __init__(self):
        """Initialize object."""

        self.route_policy_accept = RIPRoutePolicyAccept()
        self.route_policy_redistribute = RIPRoutePolicyRedistribute()
