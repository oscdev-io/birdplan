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

"""BirdPlan commandline options for BGP peer graceful shutdown show."""

from typing import Any, Dict
import argparse
from ....cmdline_plugin import BirdplanCmdlinePluginBase
from ...... import BirdPlanBGPPeerGracefulShutdownStatus
from ......console.colors import colored


class BirdplanCmdlineBGPPeerGracefulShutdownShow(BirdplanCmdlinePluginBase):
    """Birdplan "bgp peer graceful-shutdown show" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp peer graceful-shutdown show"
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

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.bgp.peer.graceful_shutdown", "get_subparsers", {})

        # CMD: bgp peer graceful-shutdown show
        subparser = parent_subparsers.add_parser("show", help="Show BGP peer graceful shutdown status")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp_peer_graceful_shutdown_show",
            default="bgp_peer_graceful_shutdown_show",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_bgp_peer_graceful_shutdown_show(self, args: Any) -> BirdPlanBGPPeerGracefulShutdownStatus:
        """
        Birdplan "bgp peer graceful-shutdown show" command.

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
        graceful_shutdown_status: BirdPlanBGPPeerGracefulShutdownStatus = cmdline.birdplan.state_bgp_peer_graceful_shutdown_status()

        if cmdline.is_console:
            if cmdline.is_json:
                self.output_json(graceful_shutdown_status)
            else:
                self.show_output_text(graceful_shutdown_status)

        return graceful_shutdown_status

    def show_output_text(  # pylint: disable=no-self-use, too-many-branches
        self, graceful_shutdown_status: BirdPlanBGPPeerGracefulShutdownStatus
    ) -> None:
        """
        Show command output in text.

        Parameters
        ----------
        graceful_shutdown_status : BirdPlanBGPPeerGracefulShutdownStatus
            Graceful shutdown status structure.

        """

        print("BGP peer graceful shutdown overrides:")
        print("-------------------------------------")

        # Loop with sorted override list
        for peer in sorted(graceful_shutdown_status["overrides"]):
            # Print out override
            status = colored("Enabled", "red") if graceful_shutdown_status["overrides"][peer] else colored("Disabled", "green")
            print(f"  {peer}: {status}")
        # If we have no overrides, just print out --none--
        if not graceful_shutdown_status["overrides"]:
            print("--none--")

        print("\n")

        # Get a list of all peers we know about
        peers_all = list(graceful_shutdown_status["current"].keys()) + list(graceful_shutdown_status["pending"].keys())
        peers_all = sorted(set(peers_all))

        print("BGP peer graceful shutdown status:")
        print("----------------------------------")

        # Loop with sorted peer list
        for peer in peers_all:

            # Grab pending status
            pending_status = None
            if peer in graceful_shutdown_status["pending"]:
                pending_status = graceful_shutdown_status["pending"][peer]

            # Grab current status
            current_status = None
            if peer in graceful_shutdown_status["current"]:
                current_status = graceful_shutdown_status["current"][peer]

            # Work out our status string
            status_str = ""
            if pending_status is None:
                status_str = colored("REMOVED", "magenta")
            else:
                if current_status and not pending_status:
                    status_str = colored("PENDING-GRACEFUL-SHUTDOWN-ENTER", "blue")
                elif not current_status and pending_status:
                    status_str = colored("PENDING-GRACEFUL-SHUTDOWN-EXIT", "yellow")
                elif current_status is None:
                    status_str = colored("NEW", "green")
                elif pending_status:
                    status_str = colored("GRACEFUL-SHUTDOWN", "red")
                else:
                    status_str = "OK"

            print("  Peer: " + colored(peer, "cyan"))
            print(f"    State: {status_str}")
            print("\n")
