#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""BirdPlan commandline options for OSPF interface."""

import argparse
from typing import Any

from .....exceptions import BirdPlanUsageError
from ...cmdline_plugin import BirdPlanCmdlinePluginBase

__all__ = ["BirdPlanCmdlineOSPFInterface"]


class BirdPlanCmdlineOSPFInterface(BirdPlanCmdlinePluginBase):
    """BirdPlan "ospf interface" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan ospf interface"
        self.plugin_order = 20

    def register_parsers(self, args: dict[str, Any]) -> None:
        """
        Register commandline parsers.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        plugins = args["plugins"]

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.ospf", "get_subparsers", {})

        # CMD: ospf interface
        subparser = parent_subparsers.add_parser("interface", help="OSPF interface commands")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="ospf_interface",
            default="ospf_interface",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = subparser.add_subparsers()

    def cmd_ospf_interface(self, args: dict[str, Any]) -> None:  # noqa: ARG002
        """
        Commandline handler for "ospf interface" action.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError

        raise BirdPlanUsageError("No options specified to 'ospf interface' action", self._subparser)
