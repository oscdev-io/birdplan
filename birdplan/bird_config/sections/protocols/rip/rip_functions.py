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


class RIPFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """RIP functions configuration."""

    _section: str = "RIP Functions"

    @bird_function("rip_accept_connected_route")
    def accept_connected_route(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD rip_accept_connected_route function."""

        return """\
            # Accept RIP connected routes
            function rip_accept_connected_route(string filter_name) {
                if (proto != "direct4_rip" && proto != "direct6_rip") then return false;
                if DEBUG then print filter_name,
                    " [rip_accept_connected_route] Accepting RIP connected route ", net;
                accept;
            }"""
