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

"""RIP protocol specific functions class."""

from ....globals import BirdConfigGlobals
from ...functions import BirdFunction, BirdFunctionArg, SectionFunctions
from ..base_protocol_functions import ProtocolFunctionsBase

__all__ = ["RIPFunctions"]


class RIPFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """RIP protocol specific functions class."""

    def __init__(self, birdconfig_globals: BirdConfigGlobals, functions: SectionFunctions) -> None:
        """Initialize the object."""
        super().__init__(birdconfig_globals, functions)

        self._section = "RIP Functions"

    @BirdFunction("rip_accept_connected")
    def accept_connected(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD rip_accept_connected function."""

        return f"""\
            # Accept RIP connected routes
            function rip_accept_connected(string filter_name) -> bool {{
                if ((proto != "direct4_rip" && proto != "direct6_rip") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_accept_connected] Accepting RIP connected route ", {self.functions.route_info()},
                    " due to connected route match";
                accept;
            }}"""

    @BirdFunction("rip_accept_rip_default")
    def accept_rip_default(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD rip_accept_rip_default function."""

        return f"""\
            # Accept RIP route
            function rip_accept_rip_default(string filter_name) -> bool {{
                if (source != RTS_RIP || !{self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_accept_rip_default] Accepting RIP default route ", {self.functions.route_info()},
                    " due to default route match";
                accept;
            }}"""

    @BirdFunction("rip_accept_rip")
    def accept_rip(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD rip_accept_rip function."""

        return f"""\
            # Accept RIP route
            function rip_accept_rip(string filter_name) -> bool {{
                if (source != RTS_RIP || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_accept_rip] Accepting RIP route ", {self.functions.route_info()}, " due to RIP route match";
                accept;
            }}"""

    @BirdFunction("rip_redistribute_connected")
    def redistribute_connected(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD rip_redistribute_connected function."""

        return f"""\
            # Accept RIP connected routes
            function rip_redistribute_connected(string filter_name) -> bool {{
                if ((proto != "direct4_rip" && proto != "direct6_rip") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_redistribute_connected] Redistributing RIP connected route ", {self.functions.route_info()},
                    " due to connected route match";
                accept;
            }}"""

    @BirdFunction("rip_redistribute_rip_default")
    def redistribute_rip_default(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD rip_redistribute_rip_default function."""

        return f"""\
            # Accept RIP route
            function rip_redistribute_rip_default(string filter_name) -> bool {{
                if (source != RTS_RIP || !{self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_redistribute_rip_default] Redistributing RIP default route ", {self.functions.route_info()},
                    " due to RIP default route match";
                accept;
            }}"""

    @BirdFunction("rip_redistribute_rip")
    def redistribute_rip(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD rip_redistribute_rip function."""

        return f"""\
            # Accept RIP route
            function rip_redistribute_rip(string filter_name) -> bool {{
                if (source != RTS_RIP || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [rip_redistribute_rip] Redistributing RIP route ", {self.functions.route_info()},
                    " due to RIP route match";
                accept;
            }}"""
