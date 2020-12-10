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

"""RIP protocol specific functions class."""

from typing import Any
from ..base_protocol_functions import ProtocolFunctionsBase
from ...functions import bird_function


class RIPFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """RIP protocol specific functions class."""

    _section: str = "RIP Functions"

    @bird_function("rip_accept_connected")
    def accept_connected(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD rip_accept_connected function."""

        return f"""\
            # Accept RIP connected routes
            function rip_accept_connected(string filter_name) {{
                if ((proto != "direct4_rip" && proto != "direct6_rip") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_accept_connected] Accepting RIP connected route ", net;
                accept;
            }}"""

    @bird_function("rip_accept_rip_default")
    def accept_rip_default(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD rip_accept_rip_default function."""

        return f"""\
            # Accept RIP route
            function rip_accept_rip_default(string filter_name) {{
                if (source != RTS_RIP || !{self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_accept_rip_default] Accepting RIP default route ", net;
                accept;
            }}"""

    @bird_function("rip_accept_rip")
    def accept_rip(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD rip_accept_rip function."""

        return f"""\
            # Accept RIP route
            function rip_accept_rip(string filter_name) {{
                if (source != RTS_RIP || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_accept_rip] Accepting RIP route ", net;
                accept;
            }}"""

    @bird_function("rip_redistribute_connected")
    def redistribute_connected(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD rip_redistribute_connected function."""

        return f"""\
            # Accept RIP connected routes
            function rip_redistribute_connected(string filter_name) {{
                if ((proto != "direct4_rip" && proto != "direct6_rip") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_redistribute_connected] Redistributing RIP connected route ", net;
                accept;
            }}"""

    @bird_function("rip_redistribute_rip_default")
    def redistribute_rip_default(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD rip_redistribute_rip_default function."""

        return f"""\
            # Accept RIP route
            function rip_redistribute_rip_default(string filter_name) {{
                if (source != RTS_RIP || !{self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_redistribute_rip_default] Redistributing RIP default route ", net;
                accept;
            }}"""

    @bird_function("rip_redistribute_rip")
    def redistribute_rip(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD rip_redistribute_rip function."""

        return f"""\
            # Accept RIP route
            function rip_redistribute_rip(string filter_name) {{
                if (source != RTS_RIP || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_redistribute_rip] Redistributing RIP route ", net;
                accept;
            }}"""
