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

"""BIRD master table attributes."""


class MasterTableRoutePolicyExportKernel:  # pylint: disable=too-few-public-methods
    """
    Master table route policy for exporting of routes to the kernel.

    Attributes
    ----------
    bgp : bool
        Export BGP routes to the kernel table. Defaults to `False`.
    ospf : bool
        Export OSPF routes to the kernel table. Defaults to `False`.
    rip : bool
        Export RIP routes to the kernel table. Defaults to `False`.
    static : bool
        Export static routes to the kernel table. Defaults to `False`.

    """

    bgp: bool
    ospf: bool
    rip: bool
    static: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.bgp = True
        self.ospf = True
        self.rip = True
        self.static = True


class MasterTableRoutePolicyExport:  # pylint: disable=too-few-public-methods
    """
    Master table route policy for exporting of routes to the kernel.

    Attributes
    ----------
    kernel : MasterTableRoutePolicyExportKernel
        Route policies for exporting routes to the kernel table.

    """

    kernel: MasterTableRoutePolicyExportKernel

    def __init__(self) -> None:
        """Initialize object."""
        self.kernel = MasterTableRoutePolicyExportKernel()


class MasterTableAttributes:  # pylint: disable=too-few-public-methods
    """
    RIP attributes.

    Attributes
    ----------
    route_policy_export : MasterTableRoutePolicyExport
        Route policy for exporting of routes from the master table.

    """

    route_policy_export: MasterTableRoutePolicyExport

    def __init__(self) -> None:
        """Initialize object."""

        self.route_policy_export = MasterTableRoutePolicyExport()
