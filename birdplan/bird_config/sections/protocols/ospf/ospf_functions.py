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

from typing import Any
from ..base_protocol_functions import ProtocolFunctionsBase
from ...functions import bird_function


class OSPFFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """OSPF functions configuration."""

    _section: str = "OSPF Functions"

    @bird_function("ospf_accept_connected_route")
    def accept_connected_route(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD ospf_accept_connected_route function."""

        return """\
            # Accept OSPF connected routes
            function ospf_accept_connected_route(string filter_name) {
                if (proto != "direct4_ospf" && proto != "direct6_ospf") then return false;
                if DEBUG then print filter_name,
                    " [ospf_accept_connected_route] Accepting OSPF connected route ", net;
                accept;
            }"""
