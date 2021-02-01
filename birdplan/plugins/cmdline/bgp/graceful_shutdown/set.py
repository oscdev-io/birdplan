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

"""BirdPlan commandline options for "bgp graceful-shutdown set"."""

from typing import Any, Dict
import argparse
import sys
from ...cmdline_plugin import BirdplanCmdlinePluginBase
from .....exceptions import BirdPlanError


class BirdplanCmdlineBGPGracefulShutdownSet(BirdplanCmdlinePluginBase):
    """Birdplan "bgp graceful-shutdown set" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp graceful-shutdown set"
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

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.bgp.graceful_shutdown", "get_subparsers", {})

        # CMD: bgp graceful-shutdown set
        subparser = parent_subparsers.add_parser(
            "set", help="Override the BGP graceful shutdown flag for a specific peer or pattern"
        )
        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp_graceful_shutdown_set",
            default="bgp_graceful_shutdown_set",
            help=argparse.SUPPRESS,
        )
        subparser.add_argument(
            "peer",
            nargs=1,
            metavar="PEER",
            help="Peer name (* = pattern match character)",
        )
        subparser.add_argument(
            "value",
            nargs=1,
            metavar="VALUE",
            help="Flag value ('true' or 'false')",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_bgp_graceful_shutdown_set(self, args: Any) -> bool:
        """
        Birdplan "bgp graceful-shutdown set" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline = args["cmdline"]

        # Make sure we have a peer specified
        if not cmdline.args.peer:
            if cmdline.is_console:
                print("ERROR: No peer or pattern specified to set the BGP graceful shutdown override flag for", file=sys.stderr)
                self._subparser.print_help(file=sys.stderr)
                sys.exit(1)
            raise BirdPlanError("No peer or pattern specified to set the BGP graceful shutdown override flag for")
        peer = cmdline.args.peer[0]

        # Check value is valid
        if cmdline.args.value[0] not in ("true", "false"):
            if cmdline.is_console:
                print("ERROR: BGP graceful shutdown override flag value must be 'true' or 'false'", file=sys.stderr)
                self._subparser.print_help(file=sys.stderr)
                sys.exit(1)
            raise BirdPlanError("BGP graceful shutdown override flag value must be 'true' or 'false'")
        value = bool(cmdline.args.value[0] == "true")

        # Load BirdPlan configuration
        cmdline.birdplan_load_config()

        # Try set graceful shutdown flag
        if cmdline.is_console:
            try:
                cmdline.birdplan.state_bgp_graceful_shutdown_set_peer(peer, value)
                # Print some sort of nicer output instead of "True", "False"
                if value:
                    print(f"BGP graceful shutdown ENABLED for peer(s) matching '{peer}'")
                else:
                    print(f"BGP graceful shutdown DISABLED for peer(s) matching '{peer}'")
            except BirdPlanError as err:
                print(f"ERROR: {err}")
                sys.exit(1)
        else:
            cmdline.birdplan.state_bgp_graceful_shutdown_set_peer(peer, value)

        # Commit BirdPlan our state
        cmdline.birdplan_commit_state()

        return True
