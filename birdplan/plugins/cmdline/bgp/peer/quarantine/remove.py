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

"""BirdPlan commandline options for BGP peer quarantine remove."""

import argparse
from typing import Any, Dict

from ....cmdline_plugin import BirdPlanCmdlinePluginBase


class BirdplanCmdlineBGPPeerQuarantineRemove(BirdPlanCmdlinePluginBase):
    """Birdplan "bgp peer quarantine remove" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp peer quarantine remove"
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

        # CMD: bgp peer quarantine remove
        subparser = parent_subparsers.add_parser(
            "remove", help="Remove a BGP quarantine override flag for a specific peer or pattern"
        )
        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp_peer_quarantine_remove",
            default="bgp_peer_quarantine_remove",
            help=argparse.SUPPRESS,
        )
        subparser.add_argument(
            "peer",
            nargs=1,
            metavar="PEER",
            help="Peer name (* = pattern match character)",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_bgp_peer_quarantine_remove(self, args: Any) -> Any:
        """
        Birdplan "bgp peer quarantine remove" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline = args["cmdline"]

        # Grab the peer
        peer = cmdline.args.peer[0]

        # Load BirdPlan configuration
        cmdline.birdplan_load_config()

        # Try remove quarantine override flag
        cmdline.birdplan.state_bgp_peer_quarantine_remove(peer)

        # Commit BirdPlan our state
        cmdline.birdplan_commit_state()

        return f"BGP quarantine REMOVED from peer(s) matching '{peer}'"
