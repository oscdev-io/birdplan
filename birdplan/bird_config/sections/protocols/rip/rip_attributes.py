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

"""BIRD RIP protocol attributes."""


__all__ = ["RIPAttributes", "RIPRoutePolicyAccept", "RIPRoutePolicyRedistribute"]


class RIPRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    RIP route policy for acceptance of routes from RIP peers into the main RIP table.

    Attributes
    ----------
    default : bool
        Accept default route. Defaults to `False`.

    """

    default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.default = False


class RIPRoutePolicyRedistribute:  # pylint: disable=too-few-public-methods
    r"""
    RIP route policy for redistributing of routes.

    Attributes
    ----------
    connected : Union[bool, List[str]]
        Redistribute connected routes to the main RIP table. This attribute is indexed by interface name with a boolean option.
        The interface name can be an exact interface match, or a wildcard with a \*.
    kernel : bool
        Redistribute kernel routes to the main RIP table. Defaults to `False`.
    kernel_default : bool
        Redistribute kernel default routes to the main RIP table. Defaults to `False`.
    rip : bool
        Redistribute RIP routes. Defaults to `True`.
    rip_default : bool
        Redistribute RIP default routes. Defaults to `False`.
    static : bool
        Redistribute static routes to the main RIP table. Defaults to `False`.
    static_default : bool
        Redistribute static default routes to the main RIP table. Defaults to `False`.

    """

    connected: bool | list[str]
    kernel: bool
    kernel_default: bool
    rip: bool
    rip_default: bool
    static: bool
    static_default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = False
        self.kernel = False
        self.kernel_default = False
        self.rip = True
        self.rip_default = False
        self.static = False
        self.static_default = False


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

    def __init__(self) -> None:
        """Initialize object."""

        self.route_policy_accept = RIPRoutePolicyAccept()
        self.route_policy_redistribute = RIPRoutePolicyRedistribute()
