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

"""BirdPlan commandline options for BGP graceful shutdown show."""

from typing import Any, Dict
import argparse
from ...cmdline_plugin import BirdplanCmdlinePluginBase
from ..... import BirdPlanGracefulShutdownStatus
from .....console.colors import colored


class BirdplanCmdlineBGPGracefulShutdownShow(BirdplanCmdlinePluginBase):
    """Birdplan "bgp graceful-shutdown show" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp graceful-shutdown show"
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

        # CMD: bgp graceful-shutdown show
        subparser = parent_subparsers.add_parser("show", help="Show BGP graceful shutdown peers")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp_graceful_shutdown_show",
            default="bgp_graceful_shutdown_show",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_bgp_graceful_shutdown_show(self, args: Any) -> BirdPlanGracefulShutdownStatus:
        """
        Birdplan "bgp graceful-shutdown show" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline = args["cmdline"]

        # Load BirdPlan configuration
        cmdline.birdplan_load_config(use_cached=True)

        # Grab peer list
        graceful_shutdown_status: BirdPlanGracefulShutdownStatus = cmdline.birdplan.state_bgp_graceful_shutdown_status()

        if cmdline.is_console:
            if cmdline.is_json:
                self.output_json(graceful_shutdown_status)
            else:
                self.show_output_text(graceful_shutdown_status)

        return graceful_shutdown_status

    def show_output_text(self, graceful_shutdown_status: BirdPlanGracefulShutdownStatus) -> None:  # pylint: disable=no-self-use
        """
        Show command output in text.

        Parameters
        ----------
        graceful_shutdown_status : BirdplanCmdlineBGPGracefulShutdownShow
            Graceful shutdown status structure.

        """

        print("Commandline graceful shutdown overrides:")
        # Loop with sorted override list
        for peer in sorted(graceful_shutdown_status["overrides"]):
            # Print out override
            if graceful_shutdown_status["overrides"][peer]:
                status = colored("Enabled", "red")
            else:
                status = colored("Disabled", "green")
            print(f"  {peer}: {status}")
        # If we have no overrides, just print out --none--
        if not graceful_shutdown_status["overrides"]:
            print("--none--")

        print("\n")

        # Get a list of all peers we know about
        peers_all = list(graceful_shutdown_status["current"].keys()) + list(graceful_shutdown_status["pending"].keys())
        peers_all = sorted(set(peers_all))

        print("Graceful shutdown status:")
        # Loop with sorted peer list
        for peer in peers_all:
            status_line = "  " + colored(peer, "cyan") + ": "

            statuses = []

            # Grab current status
            if peer in graceful_shutdown_status["current"]:
                current_status = nice_status(graceful_shutdown_status["current"][peer])
            else:
                current_status = colored("-new-", "yellow")
            statuses.append(f"current={current_status}")

            # Work out our pending status
            if peer in graceful_shutdown_status["pending"]:
                # If we had current configuration, then we can compare them to see if something changed
                if peer in graceful_shutdown_status["current"]:
                    # Check if we changing from Disabled to Enabled
                    if not graceful_shutdown_status["current"][peer] and graceful_shutdown_status["pending"][peer]:
                        pending_status = nice_status_colored(graceful_shutdown_status["pending"][peer])
                    # Check if we changing from Enabled to Disabled
                    elif graceful_shutdown_status["current"][peer] and not graceful_shutdown_status["pending"][peer]:
                        pending_status = nice_status_colored(graceful_shutdown_status["pending"][peer])
                    # No changes
                    else:
                        pending_status = nice_status(graceful_shutdown_status["pending"][peer])
                # Peer is new
                else:
                    pending_status = nice_status_colored(graceful_shutdown_status["pending"][peer])
            else:
                pending_status = colored("-removed-", "yellow")
            statuses.append(f"pending={pending_status}")
            # Output status line with each status separated with a ,
            print(status_line + ", ".join(statuses))
        # Add newline to end of output
        print("\n")


def nice_status(state: bool) -> str:
    """Display a bool as a nicer status."""
    if state:
        return "Enabled"
    return "Disabled"


def nice_status_colored(state: bool) -> str:
    """Display a bool as a nicer status."""
    if state:
        return colored("Enabled", "red")
    return colored("Disabled", "green")
