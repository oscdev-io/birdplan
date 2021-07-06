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

"""BirdPlan commandline options for BGP."""

from typing import Any, Dict
import argparse
from ..cmdline_plugin import BirdPlanCmdlinePluginBase
from ....exceptions import BirdPlanErrorUsage


class BirdplanCmdlineBGP(BirdPlanCmdlinePluginBase):
    """Birdplan "bgp" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp"
        self.plugin_order = 10

    def register_parsers(self, args: Dict[str, Any]) -> None:
        """
        Register commandline parsers.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        root_parser = args["root_parser"]

        # CMD: bgp
        subparser = root_parser.add_parser("bgp", help="BGP commands")

        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp",
            default="bgp",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser properties
        self._subparser = subparser
        self._subparsers = subparser.add_subparsers()

    def cmd_bgp(self, args: Any) -> Any:  # pylint: disable=unused-argument
        """
        Birdplan "bgp" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        raise BirdPlanErrorUsage("No options specified to 'bgp' action", self._subparser)