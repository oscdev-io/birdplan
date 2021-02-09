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

"""BirdPlan commandline options for OSPF."""

from typing import Any, Dict
import argparse
import sys
from ..cmdline_plugin import BirdplanCmdlinePluginBase
from ....exceptions import BirdPlanError


class BirdplanCmdlineOSPF(BirdplanCmdlinePluginBase):
    """Birdplan "ospf" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan ospf"
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

        # CMD: ospf
        subparser = root_parser.add_parser("ospf", help="OSPF commands")

        subparser.add_argument(
            "--action",
            action="store_const",
            const="ospf",
            default="ospf",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser properties
        self._subparser = subparser
        self._subparsers = subparser.add_subparsers()

    def cmd_ospf(self, args: Any) -> bool:
        """
        Birdplan "ospf" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline = args["cmdline"]

        if cmdline.is_console:
            self._subparser.print_help(file=sys.stderr)
            sys.exit(1)

        raise BirdPlanError("No options specified to 'ospf' action")
