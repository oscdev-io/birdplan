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

"""BirdPlan commandline options for BGP peer show <peer>."""

import argparse
from typing import Any, Dict

from birdplan import BirdPlanBGPPeerShow

from .....cmdline import BirdPlanCommandLine
from .....console.colors import colored
from ...cmdline_plugin import BirdPlanCmdlinePluginBase


class BirdplanCmdlineBGPPeerShowPeerArg(BirdPlanCmdlinePluginBase):
    """Birdplan "bgp peer show <peer>" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan bgp peer show <peer>"
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
            help="Optional peer name to show",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None
        # self._subparsers = subparser.add_subparsers()

    def cmd_bgp_peer_show(self, args: Any) -> Any:
        """
        Birdplan "bgp peer show <peer>" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        if not self._subparser:
            raise RuntimeError()

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Grab the peer
        peer = cmdline.args.peer[0]

        # Suppress info output
        cmdline.birdplan.birdconf.birdconfig_globals.suppress_info = True

        # Load BirdPlan configuration using the cache
        cmdline.birdplan_load_config(ignore_irr_changes=True, ignore_peeringdb_changes=True, use_cached=True)

        # Try grab peer info
        return cmdline.birdplan.state_bgp_peer_show(peer)

    def show_output_text(  # noqa: CFQ001 # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        self, data: BirdPlanBGPPeerShow
    ) -> None:
        """
        Show command output in text.

        Parameters
        ----------
        data : BirdPlanBGPPeerShow
            Peer information.

        """

        # Work out filter strings to use
        aspath_filters = "none"
        origin_filters = "none"
        as_sets_filter = "none"
        if "filter" in data:
            # Check for aspath_asns in our filter
            aspath_strs = []
            if "aspath_asns" in data["filter"]:
                if "static" in data["filter"]["aspath_asns"]:
                    count = len(data["filter"]["aspath_asns"]["static"])
                    aspath_strs.append(f"{count} manual")
                if "calculated" in data["filter"]["aspath_asns"]:
                    count = len(data["filter"]["aspath_asns"]["calculated"])
                    aspath_strs.append(f"{count} calculated")
                aspath_filters = ", ".join(aspath_strs)
            # Check for origin filters
            origin_strs = []
            if "origin_asns" in data["filter"]:
                if "static" in data["filter"]["origin_asns"]:
                    count = len(data["filter"]["origin_asns"]["static"])
                    origin_strs.append(f"{count} manual")
                if "irr" in data["filter"]["origin_asns"]:
                    count = len(data["filter"]["origin_asns"]["irr"])
                    origin_strs.append(f"{count} from IRR")
                origin_filters = ", ".join(origin_strs)
            # Check for AS-SET filters
            if "as_sets" in data["filter"]:
                if isinstance(data["filter"]["as_sets"], list):
                    as_sets_filter = ", ".join(data["filter"]["as_sets"])
                elif isinstance(data["filter"]["as_sets"], str):
                    as_sets_filter = data["filter"]["as_sets"]

        print(f"ASN.............: {data['asn']}")
        print(f"Type............: {data['type']}")
        print(f"Name............: {data['name']}")
        print(f"Description.....: {data['description']}")
        print(f"AS-SET..........: {as_sets_filter}")
        print(f"Origin filters..: {origin_filters}")
        print(f"AS-Path filters.: {aspath_filters}")

        # Loop with protocols and output data
        for protocol, protocol_data in data["protocols"].items():
            # Work out better protocol string
            protocol_str = ""
            if protocol == "ipv4":
                protocol_str = "IPv4"
            elif protocol == "ipv6":
                protocol_str = "IPv6"

            # Check for prefix filters
            prefix_filters = "none"
            if "filter" in data:  # noqa: SIM102
                if "prefixes" in data["filter"]:
                    prefix_filter_strs = []
                    if "irr" in data["filter"]["prefixes"]:  # noqa: SIM102
                        if protocol in data["filter"]["prefixes"]["irr"]:
                            count = len(data["filter"]["prefixes"]["irr"][protocol])
                            prefix_filter_strs.append(f"{count} from IRR")
                    if "static" in data["filter"]["prefixes"]:  # noqa: SIM102
                        if protocol in data["filter"]["prefixes"]["static"]:
                            count = len(data["filter"]["prefixes"]["static"][protocol])
                            prefix_filter_strs.append(f"{count} manual")
                    prefix_filters = ", ".join(prefix_filter_strs)

            print(f"\n  Protocol: {protocol_str}")

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
            elif protocol_status["state"] == "up":  # noqa: SIM102
                if protocol_status["info"] == "established":
                    state = colored(protocol_status["state"], "green")
                    info = colored(protocol_status["info"], "green")

            # Check for quarantine flag
            quarantined = "no"
            if "quarantine" in data and data["quarantine"]:
                quarantined = colored("yes", "red")

            # Check for graceful shutdown flag
            graceful_shutdown = "no"
            if "graceful_shutdown" in data and data["graceful_shutdown"]:
                graceful_shutdown = colored("yes", "orange")

            prefix_limit_str = ""
            if "prefix_limit" in data:
                if "peeringdb" in data["prefix_limit"]:
                    if protocol in data["prefix_limit"]["peeringdb"]:
                        prefix_limit_str = " from PeeringDB"
                elif "static" in data["prefix_limit"]:  # noqa: SIM102
                    if protocol in data["prefix_limit"]["static"]:
                        prefix_limit_str = " manual"

            print(f"    Mode..............: {protocol_data['mode']}")
            print(f"    State.............: {state} ({info}) since {protocol_status['since']}")
            print(f"    Local AS..........: {protocol_status['local_as']}")

            # Work out our source address, depending if peer is up or not
            source_address = protocol_status.get("source_address", protocol_data["source_address"])
            print(f"    Source IP.........: {source_address}")

            if "neighbor_id" in protocol_status:
                print(f"    Neighbor ID.......: {protocol_status['neighbor_id']}")
            print(f"    Neighbor AS.......: {protocol_status['neighbor_as']}")

            # Check if we have an import limit
            if "import_limit" in protocol_status:
                import_limit = protocol_status["import_limit"]
                import_limit_action = protocol_status["import_limit_action"]
                print(f"    Import limit......: {import_limit}{prefix_limit_str} (action: {import_limit_action})")
            else:
                print("    Import limit......: none")

            print(f"    Prefix filters....: {prefix_filters}")

            # Check if we have route information
            if "routes_imported" in protocol_status and "routes_exported" in protocol_status:
                routes_imported = protocol_status["routes_imported"]
                routes_exported = protocol_status["routes_exported"]
                print(f"    Prefixes..........: {routes_imported} imported, {routes_exported} exported")

            print(f"    Quarantined.......: {quarantined}")
            print(f"    Graceful shutdown.: {graceful_shutdown}")

            print("")
