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

"""BirdPlan commandline options for "ospf interface cost remove"."""

import argparse
from typing import Any, Dict

from ......cmdline import BirdPlanCommandLine, BirdPlanCommandlineResult
from ....cmdline_plugin import BirdPlanCmdlinePluginBase

__all__ = ["BirdPlanCmdlineOSPFInterfaceCostRemove"]


class BirdPlanCmdlineOSPFInterfaceCostRemove(BirdPlanCmdlinePluginBase):
    """BirdPlan "ospf interface cost remove" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan ospf interface cost remove"
        self.plugin_order = 40

    def register_parsers(self, args: Dict[str, Any]) -> None:
        """
        Register commandline parsers.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        plugins = args["plugins"]

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.ospf.interface.cost", "get_subparsers", {})

        # CMD: ospf interface cost remove
        subparser = parent_subparsers.add_parser("remove", help="Remove OSPF interface cost override")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="ospf_interface_cost_remove",
            default="ospf_interface_cost_remove",
            help=argparse.SUPPRESS,
        )
        subparser.add_argument(
            "area",
            nargs=1,
            metavar="AREA",
            help="Area in which the interface is in",
        )
        subparser.add_argument(
            "interface",
            nargs=1,
            metavar="IFACE",
            help="Interface to remove OSPF cost override for",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_ospf_interface_cost_remove(self, args: Any) -> Any:
        """
        Commandline handler for "ospf interface cost remove" action.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Grab arguments
        area = cmdline.args.area[0]
        interface = cmdline.args.interface[0]

        # Suppress info output
        cmdline.birdplan.birdconf.birdconfig_globals.suppress_info = True

        # Load BirdPlan configuration using the cache
        cmdline.birdplan_load_config(ignore_irr_changes=True, ignore_peeringdb_changes=True, use_cached=True)

        # Remove the OSPF interface cost
        cmdline.birdplan.state_ospf_remove_interface_cost(area, interface)

        # Commit BirdPlan our state
        cmdline.birdplan_commit_state()

        return BirdPlanCommandlineResult(f"Removed OSPF area '{area}' interface '{interface}' cost override")
