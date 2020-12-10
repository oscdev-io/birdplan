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
from ..base_protocol_functions import ProtocolFunctionsBase
from ...functions import bird_function


class OSPFFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """OSPF protocol specific functions class."""

    _section: str = "OSPF Functions"

    @bird_function("ospf_accept_connected")
    def accept_connected(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD ospf_accept_connected function."""

        return f"""\
            # Accept OSPF connected routes
            function ospf_accept_connected(string filter_name) {{
                if (proto != "direct4_ospf" && proto != "direct6_ospf" || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [ospf_accept_connected] Accepting OSPF connected route ", net;
                accept;
            }}"""

    @bird_function("ospf_accept_ospf")
    def accept_ospf(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD ospf_accept_ospf function."""

        return f"""\
            # Accept OSPF route
            function ospf_accept_ospf(string filter_name) {{
                if (source !~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2] || {self.functions.is_default()}) then
                    return false;
                if DEBUG then print filter_name,
                    " [ospf_accept_ospf] Accepting OSPF route ", net;
                accept;
            }}"""

    @bird_function("ospf_accept_ospf_default")
    def accept_ospf_default(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD ospf_accept_ospf_default function."""

        return f"""\
            # Accept OSPF route
            function ospf_accept_ospf_default(string filter_name) {{
                if (source !~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2] || !{self.functions.is_default()}) then
                    return false;
                if DEBUG then print filter_name,
                    " [accept_ospf] Accepting OSPF default route ", net;
                accept;
            }}"""

    @bird_function("ospf_redistribute_connected")
    def redistribute_connected(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD ospf_redistribute_connected function."""

        return f"""\
            # Accept OSPF connected routes
            function ospf_redistribute_connected(string filter_name) {{
                if (proto != "direct4_ospf" && proto != "direct6_ospf" || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [ospf_redistribute_connected] Redistributing OSPF connected route ", net;
                accept;
            }}"""
