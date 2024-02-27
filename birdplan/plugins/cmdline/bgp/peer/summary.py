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

"""BirdPlan commandline options for BGP peer summary."""

import argparse
import io
from typing import Any, Dict

from ..... import BirdPlanBGPPeerSummary
from .....cmdline import BirdPlanCommandLine, BirdPlanCommandlineResult
from .....console.colors import colored
from .....exceptions import BirdPlanErrorUsage
from ...cmdline_plugin import BirdPlanCmdlinePluginBase

__all__ = ["BirdPlanCmdlineBGPPeerShow"]


class BirdPlanCmdlineBGPPeerShowResult(BirdPlanCommandlineResult):
    """BirdPlan BGP peer show result."""

    def as_text(self) -> str:
        """
        Return data in text format.

        Returns
        -------
        str
            Return data in text format.

        """

        ob = io.StringIO()

        # Write out header
        ob.write(f"+{'='*130}+\n")
        ob.write(f"| {'BGP Peer Summary'.center(128)} |\n")
        ob.write(f"+{'-'*34}+{'-'*10}+{'-'*10}+{'-'*21}+{'-'*51}+\n")
        ob.write(
            f"| {'Peer Name'.center(32)} "
            f"| {'Proto'.center(8)} "
            f"| {'Status'.center(8)} "
            f"| {'Since'.center(19)} "
            f"| {'Info'.center(49)} |\n"
        )
        ob.write(f"+{'-'*34}+{'-'*10}+{'-'*10}+{'-'*21}+{'-'*51}+\n")

        # Loop with each protocol
        for peer_name, peer in self.data.items():
            # Loop with each family
            for ipv, protocol in peer["protocols"].items():
                protocol_status = protocol["status"]

                # Start with plain strings with no color
                state: str = protocol_status["state"]
                info: str = protocol_status["info"]
                since: str = protocol_status["since"]

                # NK - Update in peer_arg show too
                # Check how we're going to color entries based on their state and info
                state_out = f"{state[:8]}".center(8)
                info_out = f"{info[:49]}".center(49)
                if protocol_status["state"] == "down":
                    state_out = colored(f"{state[:8]}".center(8), "red")
                    if "info_extra" in protocol_status:
                        info += " - " + protocol_status["info_extra"]
                        info_out = colored(f"{info[:49]}".center(49), "red")
                elif protocol_status["state"] == "up":  # noqa: SIM102
                    if protocol_status["info"] == "established":
                        state_out = colored(f"{state[:8]}".center(8), "green")
                        info_out = colored(f"{info[:49]}".center(49), "green")

                # Center some columns
                ipv_out = f"{ipv[:8]}".center(8)

                # Write out info line
                ob.write(f"| {peer_name[:32]:<32} | {ipv_out} | {state_out} | {since[:19]:<19} | {info_out} |\n")

        # Write out footer
        ob.write(f"+{'='*130}+\n")

        return ob.getvalue()


class BirdPlanCmdlineBGPPeerShow(BirdPlanCmdlinePluginBase):
    """BirdPlan "bgp peer summary" command."""

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

        subparser.add_argument(
            "--only",
            nargs=1,
            default=None,
            metavar="ONLY",
            help="Limit output to: AS<NUMBER>",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_bgp_peer_summary(self, args: Any) -> Any:  # pylint: disable=unused-argument
        """
        Commandline handler for "bgp peer summary" action.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:  # pragma: no cover
            raise RuntimeError()

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Validate extra options
        arg_only = None
        if cmdline.args.only:
            if cmdline.args.only[0][0:2] != "AS":
                raise BirdPlanErrorUsage("Invalid value for --only, must be AS<NUMBER>")
            if int(cmdline.args.only[0]) < 1:
                raise BirdPlanErrorUsage("Invalid value for --only, must be AS<NUMBER>")
            # Save the arg for later
            arg_only = cmdline.args.only[0]

        # Grab Bird control socket
        bird_socket = cmdline.args.bird_socket[0]

        # Suppress info output
        cmdline.birdplan.birdconf.birdconfig_globals.suppress_info = True

        # Load BirdPlan configuration using the cache
        cmdline.birdplan_load_config(ignore_irr_changes=True, ignore_peeringdb_changes=True, use_cached=True)

        # Grab peer list
        peer_list: BirdPlanBGPPeerSummary = cmdline.birdplan.state_bgp_peer_summary(bird_socket=bird_socket)

        # Check if we're filtering on a specific AS
        if arg_only and arg_only[0:2] == "AS":
            peer_list = {k: v for k, v in peer_list.items() if v["asn"] == int(arg_only[2:])}

        return BirdPlanCmdlineBGPPeerShowResult(peer_list)
