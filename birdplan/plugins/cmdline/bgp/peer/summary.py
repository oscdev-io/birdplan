#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
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

"""BirdPlan commandline options for BGP peer summary."""

import argparse
from typing import Any, Dict

from ..... import BirdPlanBGPPeerSummary
from .....cmdline import BirdPlanCommandLine
from .....console.colors import colored
from ...cmdline_plugin import BirdPlanCmdlinePluginBase


class BirdplanCmdlineBGPPeerShow(BirdPlanCmdlinePluginBase):
    """Birdplan "bgp peer summary" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp peer summary"
        self.plugin_order = 20

    def register_parsers(self, args: Dict[str, Any]) -> None:
        """
        Register commandline parsers.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        plugins = args["plugins"]

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.bgp.peer", "get_subparsers", {})

        # CMD: bgp peer summary
        subparser = parent_subparsers.add_parser("summary", help="BGP peer summary commands")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp_peer_summary",
            default="bgp_peer_summary",
            help=argparse.SUPPRESS,
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = subparser.add_subparsers()

    def cmd_bgp_peer_summary(self, args: Any) -> Any:  # pylint: disable=unused-argument
        """
        Birdplan "bgp peer summary" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Suppress info output
        cmdline.birdplan.birdconf.birdconfig_globals.suppress_info = True

        # Load BirdPlan configuration using the cache
        cmdline.birdplan_load_config(ignore_irr_changes=True, ignore_peeringdb_changes=True, use_cached=True)

        # Grab peer list
        return cmdline.birdplan.state_bgp_peer_summary()

    def show_output_text(self, data: BirdPlanBGPPeerSummary) -> None:
        """
        Show command output in text.

        Parameters
        ----------
        data : BirdPlanBGPPeerSummary
            Peer information.

        """

        # Loop with each protocol
        for peer_name, peer in data.items():
            # Loop with each family
            for ipv, protocol in peer["protocols"].items():
                protocol_status = protocol["status"]

                # Start with plain strings with no color
                state: str = protocol_status["state"]
                info: str = protocol_status["info"]
                since: str = protocol_status["since"]

                # NK - Update in peer_arg show too
                # Check how we're going to color entries based on their state and info
                if protocol_status["state"] == "down":
                    state = colored(protocol_status["state"], "red")
                    if "info_extra" in protocol_status:
                        info += " - " + colored(protocol_status["info_extra"], "red")
                elif protocol_status["state"] == "up":  # noqa: SIM102
                    if protocol_status["info"] == "established":
                        state = colored(protocol_status["state"], "green")
                        info = colored(protocol_status["info"], "green")

                print(f"| {peer_name} | {ipv} | {state} | {since} | {info} |")
