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

"""BirdPlan commandline options for OSPF interface ecmp-weight."""

import argparse
from typing import Any, Dict

from ......exceptions import BirdPlanErrorUsage
from ....cmdline_plugin import BirdPlanCmdlinePluginBase


class BirdplanCmdlineOSPFInterfaceECMPWeight(BirdPlanCmdlinePluginBase):
    """Birdplan "ospf interface ecmp-weight" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan ospf interface ecmp-weight"
        self.plugin_order = 30

    def register_parsers(self, args: Dict[str, Any]) -> None:
        """
        Register commandline parsers.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        plugins = args["plugins"]

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.ospf.interface", "get_subparsers", {})

        # CMD: ospf interface ecmp-weight
        subparser = parent_subparsers.add_parser("ecmp-weight", help="OSPF interface ecmp-weight commands")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="ospf_interface_ecmp_weight",
            default="ospf_interface_ecmp_weight",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = subparser.add_subparsers()

    def cmd_ospf_interface_ecmp_weight(self, args: Any) -> Any:  # pylint: disable=unused-argument
        """
        Birdplan "ospf interface ecmp-weight" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        raise BirdPlanErrorUsage("No options specified to 'ospf interface ecmp-weight' action", self._subparser)
