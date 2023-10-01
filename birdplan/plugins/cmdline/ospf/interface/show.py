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

"""BirdPlan commandline options for OSPF interface show."""

import argparse
from typing import Any, Dict, List

from .....console.colors import colored
from ...cmdline_plugin import BirdPlanCmdlinePluginBase


class BirdplanCmdlineOSPFInterfaceShow(BirdPlanCmdlinePluginBase):
    """Birdplan "ospf interface show" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan ospf interface show"
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

        parent_subparsers = plugins.call_plugin("birdplan.plugins.cmdline.ospf.interface", "get_subparsers", {})

        # CMD: ospf interface show
        subparser = parent_subparsers.add_parser("show", help="Show OSPF interfaces")
        subparser.add_argument(
            "--action",
            action="store_const",
            const="ospf_interface_show",
            default="ospf_interface_show",
            help=argparse.SUPPRESS,
        )
        subparser.add_argument(
            "area",
            nargs="?",
            metavar="AREA",
            help="Optional area in which the interface is in",
        )
        subparser.add_argument(
            "interface",
            nargs="?",
            metavar="IFACE",
            help="Optional interface",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_ospf_interface_show(self, args: Any) -> Any:
        """
        Birdplan "ospf interface show" command.

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
        return cmdline.birdplan.state_ospf_interface_status()

    def show_output_text(  # noqa: CFQ001 # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        self, data: Any
    ) -> None:
        """
        Show command output in text.

        Parameters
        ----------
        data : BirdPlanOSPFInterfaceStatus
            OSPF interface status structure.

        """

        print("OSPF interface overrides:")
        print("-------------------------")
        # Loop with sorted override list
        if "areas" in data["overrides"]:
            for area_name, area in sorted(data["overrides"]["areas"].items()):
                # Skip if we have no interfaces
                if ("interfaces" not in area) or (not area["interfaces"]):
                    continue
                # Print out override
                print("  Area: " + colored(area_name, "cyan"))
                for interface_name, interface in area["interfaces"].items():
                    print("    Interface: " + colored(interface_name, "cyan"))
                    # Check if we have a cost override
                    if "cost" in interface:
                        print(f"      - Cost.......: {interface['cost']}")
                    # Check if we have a cost override
                    if "ecmp_weight" in interface:
                        print(f"      - ECMP Weight: {interface['ecmp_weight']}")
                print("\n")
        # If we have no overrides, just print out --none--
        if ("areas" not in data["overrides"]) or (not data["overrides"]["areas"]):
            print("--none--")
            print("\n")

        # Get a list of all areas we know about
        areas_all = list(data["current"]["areas"].keys()) + list(data["pending"]["areas"].keys())
        areas_all = sorted(set(areas_all))

        # Work out the lists of unique interfaces per area
        interfaces_all: Dict[str, List[str]] = {}
        for area_name in areas_all:
            # Initailize this areas interface list
            interfaces_all[area_name] = []
            # Check if we have interfaces in the current configuration
            if area_name in data["current"]["areas"] and "interfaces" in data["current"]["areas"][area_name]:
                interfaces_all[area_name] += data["current"]["areas"][area_name]["interfaces"].keys()
            # Check if we have interfaces in the pending configuration
            if area_name in data["pending"]["areas"] and "interfaces" in data["pending"]["areas"][area_name]:
                interfaces_all[area_name] += data["pending"]["areas"][area_name]["interfaces"].keys()
            # Make sure the interface list is unique and sorted
            interfaces_all[area_name] = sorted(set(interfaces_all[area_name]))

        print("OSPF interface status:")
        print("----------------------")

        # Loop with areas
        for area_name, interface_list in sorted(interfaces_all.items()):
            # Create area section
            print("  Area: " + colored(area_name, "cyan"))

            # Loop with sorted interface list
            for interface in interface_list:
                # Create interface section
                print("    Interface: " + colored(interface, "cyan"))

                # Check if we have pending values
                pending_cost = None
                pending_ecmp_weight = None
                if area_name in data["pending"]["areas"] and interface in data["pending"]["areas"][area_name]["interfaces"]:
                    # Make things easier
                    pending_interface = data["pending"]["areas"][area_name]["interfaces"][interface]

                    pending_cost = pending_interface["cost"]
                    pending_ecmp_weight = pending_interface["ecmp_weight"]

                # Short circuit if we don't have anything pending
                if pending_cost is None and pending_ecmp_weight is None:
                    print("      " + colored("-removed-", "magenta"))
                    continue

                # Grab current cost status
                current_cost = None
                current_ecmp_weight = None
                if area_name in data["current"]["areas"] and interface in data["current"]["areas"][area_name]["interfaces"]:
                    # Make things easier below
                    current_interface = data["current"]["areas"][area_name]["interfaces"][interface]
                    # Check if we have a current cost and ECMP weight
                    if "cost" in current_interface:  # noqa: SIM908
                        current_cost = current_interface["cost"]
                    if "ecmp_weight" in current_interface:  # noqa: SIM908
                        current_ecmp_weight = current_interface["ecmp_weight"]

                # Work out the cost string
                cost_str = None
                if (current_cost is not None) and (pending_cost is not None):
                    cost_str = (
                        f"{current_cost} → " + colored(pending_cost, "yellow")
                        if (current_cost != pending_cost)
                        else f"{pending_cost}"
                    )
                else:
                    cost_str = colored(f"{pending_cost}", "green")
                # Work out the ECMP weight
                ecmp_weight_str = None
                if (current_ecmp_weight is not None) and (pending_ecmp_weight is not None):
                    ecmp_weight_str = (
                        f"{current_ecmp_weight} → " + colored(pending_ecmp_weight, "yellow")
                        if (current_ecmp_weight != pending_ecmp_weight)
                        else f"{pending_ecmp_weight}"
                    )
                else:
                    ecmp_weight_str = colored(f"{pending_ecmp_weight}", "green")

                print(f"      - Cost.......: {cost_str}")
                print(f"      - ECMP Weight: {ecmp_weight_str}")
            # Separate areas
            print("\n")

        # Add newline to end of output
        print(colored("NEW", "green") + "        - New interface configuration")
        print(colored("CHANGED", "yellow") + "    - Pending interface configuration")
        print("\n")
