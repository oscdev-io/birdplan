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

"""BirdPlan commandline options for BGP peer graceful shutdown show."""

import argparse
import io
from typing import TYPE_CHECKING, Any

from ......cmdline import BirdPlanCommandLine, BirdPlanCommandlineResult
from ......console.colors import colored
from ....cmdline_plugin import BirdPlanCmdlinePluginBase

if TYPE_CHECKING:
    from birdplan import BirdPlanBGPPeerGracefulShutdownStatus

__all__ = ["BirdPlanCmdlineBGPPeerGracefulShutdownShow"]


class BirdPlanCmdlineBGPPeerGracefulShutdownShowResult(BirdPlanCommandlineResult):
    """BirdPlan BGP peer graceful shutdown show result."""

    def as_text(self) -> str:  # noqa: C901
        """
        Return data in text format.

        Returns
        -------
        str
            Return data in text format.

        """

        ob = io.StringIO()

        ob.write("BGP peer graceful shutdown overrides:\n")
        ob.write("-------------------------------------\n")

        # Loop with sorted override list
        for peer in sorted(self.data["overrides"]):
            # Print out override
            status = colored("Enabled", "red") if self.data["overrides"][peer] else colored("Disabled", "green")
            ob.write(f"  {peer}: {status}\n")
        # If we have no overrides, just print out --none--
        if not self.data["overrides"]:
            ob.write("--none--\n")

        ob.write("\n")

        # Get a list of all peers we know about
        peers_all = list(self.data["current"].keys()) + list(self.data["pending"].keys())
        peers_all = sorted(set(peers_all))

        ob.write("BGP peer graceful shutdown status:\n")
        ob.write("----------------------------------\n")

        # Loop with sorted peer list
        for peer in peers_all:
            # Grab pending status
            pending_status = None
            if peer in self.data["pending"]:
                pending_status = self.data["pending"][peer]

            # Grab current status
            current_status = None
            if peer in self.data["current"]:
                current_status = self.data["current"][peer]

            # Work out our status string
            status_str = ""
            if pending_status is None:
                status_str = colored("REMOVED", "magenta")
            elif current_status and not pending_status:
                status_str = colored("PENDING-GRACEFUL-SHUTDOWN-ENTER", "blue")
            elif not current_status and pending_status:
                status_str = colored("PENDING-GRACEFUL-SHUTDOWN-EXIT", "yellow")
            elif current_status is None:
                status_str = colored("NEW", "green")
            elif pending_status:
                status_str = colored("GRACEFUL-SHUTDOWN", "red")
            else:
                status_str = "OK"

            ob.write("  Peer: " + colored(peer, "cyan") + "\n")
            ob.write(f"    State: {status_str}\n")
            ob.write("\n")

        return ob.getvalue()


class BirdPlanCmdlineBGPPeerGracefulShutdownShow(BirdPlanCmdlinePluginBase):
    """BirdPlan "bgp peer graceful-shutdown show" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp peer graceful-shutdown show"
        self.plugin_order = 30

    def register_parsers(self, args: dict[str, Any]) -> None:
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

    def cmd_bgp_peer_graceful_shutdown_show(self, args: dict[str, Any]) -> BirdPlanCmdlineBGPPeerGracefulShutdownShowResult:
        """
        Commandline handler for "bgp peer graceful-shutdown show" action.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Suppress info output
        cmdline.birdplan.birdconf.birdconfig_globals.suppress_info = True

        # Load BirdPlan configuration using the cache
        cmdline.birdplan_load_config(ignore_irr_changes=True, ignore_peeringdb_changes=True, use_cached=True)

        # Grab peer list
        res: BirdPlanBGPPeerGracefulShutdownStatus = cmdline.birdplan.state_bgp_peer_graceful_shutdown_status()

        return BirdPlanCmdlineBGPPeerGracefulShutdownShowResult(res)
