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

"""OSPF protocol specific functions class."""

from typing import Any

from ....globals import BirdConfigGlobals
from ...functions import SectionFunctions, bird_function
from ..base_protocol_functions import ProtocolFunctionsBase


class OSPFFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """OSPF protocol specific functions class."""

    def __init__(self, birdconfig_globals: BirdConfigGlobals, functions: SectionFunctions):
        """Initialize the object."""
        super().__init__(birdconfig_globals, functions)

        self._section = "OSPF Functions"

    @bird_function("ospf_accept_connected")
    def accept_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD ospf_accept_connected function."""

        return f"""\
            # Accept OSPF connected routes
            function ospf_accept_connected(string filter_name) {{
                if (proto != "direct4_ospf" && proto != "direct6_ospf" || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [ospf_accept_connected] Accepting OSPF connected route ", {self.functions.route_info()},
                    " due to connected route match";
                accept;
            }}"""

    @bird_function("ospf_accept_ospf")
    def accept_ospf(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD ospf_accept_ospf function."""

        return f"""\
            # Accept OSPF route
            function ospf_accept_ospf(string filter_name) {{
                if (source !~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2] || {self.functions.is_default()}) then
                    return false;
                if DEBUG then print filter_name,
                    " [ospf_accept_ospf] Accepting OSPF route ", {self.functions.route_info()}, " due to OSPF route match";
                accept;
            }}"""

    @bird_function("ospf_accept_ospf_default")
    def accept_ospf_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD ospf_accept_ospf_default function."""

        return f"""\
            # Accept OSPF route
            function ospf_accept_ospf_default(string filter_name) {{
                if (source !~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2] || !{self.functions.is_default()}) then
                    return false;
                if DEBUG then print filter_name,
                    " [accept_ospf] Accepting OSPF default route ", {self.functions.route_info()},
                    " due to OSPF default route match";
                accept;
            }}"""

    @bird_function("ospf_is_connected")
    def is_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD ospf_is_connected function."""

        return """\
            # Check if this is an connected route
            function ospf_is_connected(string filter_name) {
                if (proto = "direct4_ospf" || proto = "direct6_ospf") then return true;
                return false;
            }"""

    @bird_function("ospf_redistribute_connected")
    def redistribute_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD ospf_redistribute_connected function."""

        return f"""\
            # Accept OSPF connected routes
            function ospf_redistribute_connected(string filter_name) {{
                if (!{self.is_connected()} || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [ospf_redistribute_connected] Redistributing OSPF connected route ", {self.functions.route_info()},
                    " due to connected route match";
                accept;
            }}"""
