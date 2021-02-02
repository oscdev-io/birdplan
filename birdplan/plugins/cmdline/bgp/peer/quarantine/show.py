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

"""BirdPlan commandline options for BGP peer quarantine show."""

from typing import Any, Dict
import argparse
from ....cmdline_plugin import BirdplanCmdlinePluginBase
from ...... import BirdPlanBGPPeerQuarantineStatus
from ......console.colors import colored


class BirdplanCmdlineBGPPeerQuarantineShow(BirdplanCmdlinePluginBase):
    """Birdplan "bgp peer quarantine show" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp peer quarantine show"
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

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.bgp.peer.quarantine", "get_subparsers", {})

        # CMD: bgp peer quarantine show
        subparser = parent_subparsers.add_parser("show", help="Show BGP peer quarantine status")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp_peer_quarantine_show",
            default="bgp_peer_quarantine_show",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_bgp_peer_quarantine_show(self, args: Any) -> BirdPlanBGPPeerQuarantineStatus:
        """
        Birdplan "bgp peer quarantine show" command.

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
        quarantine_status: BirdPlanBGPPeerQuarantineStatus = cmdline.birdplan.state_bgp_peer_quarantine_status()

        if cmdline.is_console:
            if cmdline.is_json:
                self.output_json(quarantine_status)
            else:
                self.show_output_text(quarantine_status)

        return quarantine_status

    def show_output_text(self, quarantine_status: BirdPlanBGPPeerQuarantineStatus) -> None:  # pylint: disable=no-self-use
        """
        Show command output in text.

        Parameters
        ----------
        quarantine_status : BirdPlanBGPPeerQuarantineStatus
            Graceful shutdown status structure.

        """

        print("BGP peer quarantine overrides:")
        # Loop with sorted override list
        for peer in sorted(quarantine_status["overrides"]):
            # Print out override
            status = colored("Enabled", "red") if quarantine_status["overrides"][peer] else colored("Disabled", "green")
            print(f"  {peer}: {status}")
        # If we have no overrides, just print out --none--
        if not quarantine_status["overrides"]:
            print("--none--")

        print("\n")

        # Get a list of all peers we know about
        peers_all = list(quarantine_status["current"].keys()) + list(quarantine_status["pending"].keys())
        peers_all = sorted(set(peers_all))

        print("BGP peer quarantine status:")
        # Loop with sorted peer list
        for peer in peers_all:
            status_line = "  " + colored(peer, "cyan") + ": "

            statuses = []

            # Grab current status
            current_status = (
                nice_status(quarantine_status["current"][peer])
                if peer in quarantine_status["current"]
                else colored("-new-", "yellow")
            )
            statuses.append(f"current={current_status}")

            # Work out our pending status
            if peer in quarantine_status["pending"]:
                # If we had current configuration, then we can compare them to see if something changed
                if peer in quarantine_status["current"]:
                    # Check if we changing from Disabled to Enabled
                    if not quarantine_status["current"][peer] and quarantine_status["pending"][peer]:
                        pending_status = nice_status_colored(quarantine_status["pending"][peer])
                    # Check if we changing from Enabled to Disabled
                    elif quarantine_status["current"][peer] and not quarantine_status["pending"][peer]:
                        pending_status = nice_status_colored(quarantine_status["pending"][peer])
                    # No changes
                    else:
                        pending_status = nice_status(quarantine_status["pending"][peer])
                # Peer is new
                else:
                    pending_status = nice_status_colored(quarantine_status["pending"][peer])
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
