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

"""BirdPlan commandline options for BGP peer show <peer>."""

import argparse
import io
from typing import Any

from birdplan import BirdPlanBGPPeerShow

from .....cmdline import BirdPlanCommandLine, BirdPlanCommandlineResult
from .....console.colors import colored
from ...cmdline_plugin import BirdPlanCmdlinePluginBase

__all__ = ["BirdPlanCmdlineBGPPeerShowPeerArg"]


class BirdPlanCmdlineBGPPeerShowPeerArgResult(BirdPlanCommandlineResult):
    """BirdPlan BGP peer show peer result."""

    def as_text(self) -> str:  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        """
        Return data in text format.

        Returns
        -------
        str
            Return data in text format.

        """

        ob = io.StringIO()

        # Work out filter strings to use
        aspath_filters = "none"
        origin_filters = "none"
        as_sets_filter = "none"
        if "import_filter" in self.data:
            # Check for aspath_asns in our filter
            aspath_strs = []
            if "aspath_asns" in self.data["import_filter"]:
                if "static" in self.data["import_filter"]["aspath_asns"]:
                    count = len(self.data["import_filter"]["aspath_asns"]["static"])
                    aspath_strs.append(f"{count} manual")
                if "calculated" in self.data["import_filter"]["aspath_asns"]:
                    count = len(self.data["import_filter"]["aspath_asns"]["calculated"])
                    aspath_strs.append(f"{count} calculated")
                aspath_filters = ", ".join(aspath_strs)
            # Check for origin filters
            origin_strs = []
            if "origin_asns" in self.data["import_filter"]:
                if "static" in self.data["import_filter"]["origin_asns"]:
                    count = len(self.data["import_filter"]["origin_asns"]["static"])
                    origin_strs.append(f"{count} manual")
                if "irr" in self.data["import_filter"]["origin_asns"]:
                    count = len(self.data["import_filter"]["origin_asns"]["irr"])
                    origin_strs.append(f"{count} from IRR")
                origin_filters = ", ".join(origin_strs)
            # Check for AS-SET filters
            if "as_sets" in self.data["import_filter"]:
                if isinstance(self.data["import_filter"]["as_sets"], list):
                    as_sets_filter = ", ".join(self.data["import_filter"]["as_sets"])
                elif isinstance(self.data["import_filter"]["as_sets"], str):
                    as_sets_filter = self.data["import_filter"]["as_sets"]

        ob.write(f"ASN.............: {self.data['asn']}\n")
        ob.write(f"Type............: {self.data['type']}\n")
        ob.write(f"Name............: {self.data['name']}\n")
        ob.write(f"Description.....: {self.data['description']}\n")
        ob.write(f"AS-SET..........: {as_sets_filter}\n")
        ob.write(f"Origin filters..: {origin_filters}\n")
        ob.write(f"AS-Path filters.: {aspath_filters}\n")
        if self.data.get("use_rpki"):
            ob.write("RPKI ROV........: enabled\n")

        # Loop with protocols and output self.data
        for protocol, protocol_data in self.data["protocols"].items():
            # Work out better protocol string
            protocol_str = ""
            if protocol == "ipv4":
                protocol_str = "IPv4"
            elif protocol == "ipv6":
                protocol_str = "IPv6"

            # Check for import prefix filters
            prefix_filters = "none"
            if "import_filter" in self.data:  # noqa: SIM102
                if "prefixes" in self.data["import_filter"]:
                    prefix_filter_strs = []
                    if "irr" in self.data["import_filter"]["prefixes"]:  # noqa: SIM102
                        if protocol in self.data["import_filter"]["prefixes"]["irr"]:
                            count = len(self.data["import_filter"]["prefixes"]["irr"][protocol])
                            prefix_filter_strs.append(f"{count} from IRR")
                    if "static" in self.data["import_filter"]["prefixes"]:  # noqa: SIM102
                        if protocol in self.data["import_filter"]["prefixes"]["static"]:
                            count = len(self.data["import_filter"]["prefixes"]["static"][protocol])
                            prefix_filter_strs.append(f"{count} manual")
                    prefix_filters = ", ".join(prefix_filter_strs)

            ob.write(f"\n  Protocol: {protocol_str}\n")

            # Setup o the protocol_status so we can copy-paste the below colors
            protocol_status = protocol_data["status"]
            # Set the state and info with no color
            state = protocol_status["state"]
            info = protocol_status["info"]

            # NK - Update in peer_arg show too
            # Check how we're going to color entries based on their state and info
            if protocol_status["state"] == "down":
                state = colored(protocol_status["state"], "red")
                if "last_error" in protocol_status:
                    info += " - " + colored(protocol_status["last_error"], "red")
            elif protocol_status["state"] == "up":
                if protocol_status["info"] == "established":
                    state = colored(protocol_status["state"], "green")
                    info = colored(protocol_status["info"], "green")

            # Check for quarantine flag
            quarantined = "no"
            if self.data.get("quarantine"):
                quarantined = colored("yes", "red")

            # Check for graceful shutdown flag
            graceful_shutdown = "no"
            if self.data.get("graceful_shutdown"):
                graceful_shutdown = colored("yes", "red")

            prefix_limit_str = ""
            if "prefix_limit" in self.data:
                if "peeringdb" in self.data["prefix_limit"]:
                    if protocol in self.data["prefix_limit"]["peeringdb"]:
                        prefix_limit_str = " from PeeringDB"
                elif "static" in self.data["prefix_limit"]:  # noqa: SIM102
                    if protocol in self.data["prefix_limit"]["static"]:
                        prefix_limit_str = " manual"

            ob.write(f"    Mode..............: {protocol_data['mode']}\n")
            ob.write(f"    State.............: {state} ({info}) since {protocol_status['since']}\n")
            ob.write(f"    Local AS..........: {protocol_status['local_as']}\n")

            # Work out our source address, depending if peer is up or not
            source_address = protocol_status.get("source_address", protocol_data["source_address"])
            ob.write(f"    Source IP.........: {source_address}\n")

            ob.write(f"    Neighbor AS.......: {protocol_status['neighbor_as']}\n")
            ob.write(f"    Neighbor IP.......: {protocol_status['neighbor_address']}\n")

            if "neighbor_id" in protocol_status:
                ob.write(f"    Neighbor ID.......: {protocol_status['neighbor_id']}\n")

            # Check if we have an import limit
            if "import_limit" in protocol_status:
                import_limit = protocol_status["import_limit"]
                import_limit_action = protocol_status["import_limit_action"]
                ob.write(f"    Import limit......: {import_limit}{prefix_limit_str} (action: {import_limit_action})\n")
            else:
                ob.write("    Import limit......: none\n")

            ob.write(f"    Prefix filters....: {prefix_filters}\n")

            # Check if we have route information
            if "routes_imported" in protocol_status and "routes_exported" in protocol_status:
                routes_imported = protocol_status["routes_imported"]
                routes_exported = protocol_status["routes_exported"]
                ob.write(f"    Prefixes..........: {routes_imported} imported, {routes_exported} exported\n")

            if self.data.get("security"):
                ob.write(f"    BGP security......: {', '.join(sorted(self.data['security']))}\n")

            ob.write(f"    Quarantined.......: {quarantined}\n")
            ob.write(f"    Graceful shutdown.: {graceful_shutdown}\n")

            ob.write("\n")

        ob.write("\n")

        return ob.getvalue()


class BirdPlanCmdlineBGPPeerShowPeerArg(BirdPlanCmdlinePluginBase):
    """BirdPlan "bgp peer show <peer>" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp peer show <peer>"
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

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.bgp.peer", "get_subparsers", {})

        # CMD: bgp peer show <peer>
        subparser = parent_subparsers.add_parser("show", help="BGP peer show commands")

        subparser.add_argument(
            "--action",
            action="store_const",
            const="bgp_peer_show",
            default="bgp_peer_show",
            help=argparse.SUPPRESS,
        )

        subparser.add_argument(
            "peer",
            nargs=1,
            metavar="PEER",
            help="Peer to show (its BirdPlan name)",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None
        # self._subparsers = subparser.add_subparsers()

    def cmd_bgp_peer_show(self, args: Any) -> Any:
        """
        Commandline handler for "bgp peer show <peer>" action.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:  # pragma: no cover
            raise RuntimeError

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Grab Bird control socket
        bird_socket = cmdline.args.bird_socket[0]

        # Grab the peer
        peer = cmdline.args.peer[0]

        # Suppress info output
        cmdline.birdplan.birdconf.birdconfig_globals.suppress_info = True

        # Load BirdPlan configuration using the cache
        cmdline.birdplan_load_config(ignore_irr_changes=True, ignore_peeringdb_changes=True, use_cached=True)

        # Try grab peer info
        res: BirdPlanBGPPeerShow = cmdline.birdplan.state_bgp_peer_show(peer, bird_socket=bird_socket)

        return BirdPlanCmdlineBGPPeerShowPeerArgResult(res)
