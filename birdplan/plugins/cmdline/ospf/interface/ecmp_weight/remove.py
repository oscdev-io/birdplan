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

"""BirdPlan commandline options for "ospf interface ecmp-weight remove"."""

from typing import Any, Dict
import argparse
import sys
from ....cmdline_plugin import BirdplanCmdlinePluginBase
from ......exceptions import BirdPlanError


class BirdplanCmdlineOSPFInterfaceECMPWeightRemove(BirdplanCmdlinePluginBase):
    """Birdplan "ospf interface ecmp-weight remove" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan ospf interface ecmp-weight remove"
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

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.ospf.interface.ecmp_weight", "get_subparsers", {})

        # CMD: ospf interface ecmp-weight remove
        subparser = parent_subparsers.add_parser("remove", help="Remove OSPF interface ECMP weight override")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="ospf_interface_ecmp_weight_remove",
            default="ospf_interface_ecmp_weight_remove",
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
            help="Interface to remove OSPF ECMP weight override for",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_ospf_interface_ecmp_weight_remove(self, args: Any) -> bool:
        """
        Birdplan "ospf interface ecmp_weight remove" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline = args["cmdline"]

        # Make sure we have an area specified
        if cmdline.args.area is None:
            if cmdline.is_console:
                print("ERROR: No OSPF area specified", file=sys.stderr)
                self._subparser.print_help(file=sys.stderr)
                sys.exit(1)
            raise BirdPlanError("No OSPF area specified")
        area = cmdline.args.area[0]

        # Make sure we have an interface specified
        if not cmdline.args.interface:
            if cmdline.is_console:
                print("ERROR: No OSPF interface name or pattern specified to remove ECMP weight override for", file=sys.stderr)
                self._subparser.print_help(file=sys.stderr)
                sys.exit(1)
            raise BirdPlanError("No OSPF interface name or pattern specified to remove ECMP weight override for")
        interface = cmdline.args.interface[0]

        # Load BirdPlan configuration
        cmdline.birdplan_load_config()

        # Check if we're on the console
        if cmdline.is_console:
            try:
                cmdline.birdplan.state_ospf_remove_interface_ecmp_weight(area, interface)
                print(f"Removed OSPF area '{area}' interface '{interface}' ECMP weight override")
            except BirdPlanError as err:
                print(f"ERROR: {err}")
                sys.exit(1)
        else:
            cmdline.birdplan.state_ospf_remove_interface_ecmp_weight(area, interface)

        # Commit BirdPlan our state
        cmdline.birdplan_commit_state()

        return True
