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

"""Entry point into Birdplan from the commandline."""

from typing import Any, List, Optional
import argparse
import logging
import logging.handlers
import sys
from birdplan import __VERSION__, BirdPlan
from birdplan.exceptions import BirdPlanError


# Defaults
BIRDPLAN_FILE = "/etc/birdplan/birdplan.yaml"
BIRD_CONFIG_FILE = "/etc/bird.conf"
BIRDPLAN_STATE_FILE = "/var/lib/birdplan/birdplan.state"


class BirdPlanCommandLine:
    """BirdPlan commandline handling class."""

    _args: argparse.Namespace
    _argparser: argparse.ArgumentParser
    _birdplan: BirdPlan

    def __init__(self, test_mode: bool = False) -> None:
        """Instantiate object."""

        self._args = argparse.Namespace()
        self._argparser = argparse.ArgumentParser(add_help=False)
        self._birdplan = BirdPlan(test_mode=test_mode)

    def run(  # pylint: disable=too-many-branches,too-many-locals,too-many-statements
        self, raw_args: Optional[List[str]] = None
    ) -> Any:
        """Run BirdPlan from command line."""

        # Add main commandline arguments
        self._add_main_arguments()

        # Add subparsers
        subparsers = self.argparser.add_subparsers()

        # CMD: configure
        parser_configure = subparsers.add_parser("configure", help="Create BIRD configuration")
        parser_configure.add_argument(
            "--action",
            action="store_const",
            const="configure",
            default="configure",
            help=argparse.SUPPRESS,
        )
        self._add_configure_arguments(parser_configure)

        # CMD: bgp
        parser_bgp = subparsers.add_parser("bgp", help="BGP commands")
        parser_bgp.add_argument(
            "--action",
            action="store_const",
            const="bgp",
            default="bgp",
            help=argparse.SUPPRESS,
        )
        bgp_subparsers = parser_bgp.add_subparsers()

        # CMD: bgp graceful_shutdown
        parser_bgp_graceful_shutdown = bgp_subparsers.add_parser("graceful_shutdown", help="BGP graceful shutdown commands")
        parser_bgp_graceful_shutdown.add_argument(
            "--action",
            action="store_const",
            const="bgp_graceful_shutdown",
            default="bgp_graceful_shutdown",
            help=argparse.SUPPRESS,
        )
        bgp_graceful_shutdown_subparsers = parser_bgp_graceful_shutdown.add_subparsers()

        # CMD: bgp graceful_shutdown add
        parser_bgp_graceful_shutdown_add = bgp_graceful_shutdown_subparsers.add_parser(
            "add", help="Add peer(s) to BGP graceful shutdown list"
        )
        parser_bgp_graceful_shutdown_add.add_argument(
            "--action",
            action="store_const",
            const="bgp_graceful_shutdown_add",
            default="bgp_graceful_shutdown_add",
            help=argparse.SUPPRESS,
        )
        self._add_bgp_graceful_shutdown_peers_argument(parser_bgp_graceful_shutdown_add)

        # CMD: bgp graceful_shutdown remove
        parser_bgp_graceful_shutdown_remove = bgp_graceful_shutdown_subparsers.add_parser(
            "remove", help="Remove peer(s) from BGP graceful shutdown list"
        )
        parser_bgp_graceful_shutdown_remove.add_argument(
            "--action",
            action="store_const",
            const="bgp_graceful_shutdown_remove",
            default="bgp_graceful_shutdown_remove",
            help=argparse.SUPPRESS,
        )
        self._add_bgp_graceful_shutdown_peers_argument(parser_bgp_graceful_shutdown_remove)

        # CMD: bgp graceful_shutdown list
        parser_bgp_graceful_shutdown_list = bgp_graceful_shutdown_subparsers.add_parser(
            "list", help="List BGP graceful shutdown peers"
        )
        parser_bgp_graceful_shutdown_list.add_argument(
            "--action",
            action="store_const",
            const="bgp_graceful_shutdown_list",
            default="bgp_graceful_shutdown_list",
            help=argparse.SUPPRESS,
        )

        # CMD: bgp quarantine
        parser_bgp_quarantine = bgp_subparsers.add_parser("quarantine", help="BGP quarantine commands")
        parser_bgp_quarantine.add_argument(
            "--action",
            action="store_const",
            const="bgp_quarantine",
            default="bgp_quarantine",
            help=argparse.SUPPRESS,
        )
        bgp_quarantine_subparsers = parser_bgp_quarantine.add_subparsers()

        # CMD: bgp quarantine add
        parser_bgp_quarantine_add = bgp_quarantine_subparsers.add_parser("add", help="Add peer(s) to BGP quarantine list")
        parser_bgp_quarantine_add.add_argument(
            "--action",
            action="store_const",
            const="bgp_quarantine_add",
            default="bgp_quarantine_add",
            help=argparse.SUPPRESS,
        )
        self._add_bgp_quarantine_peers_argument(parser_bgp_quarantine_add)

        # CMD: bgp quarantine remove
        parser_bgp_quarantine_remove = bgp_quarantine_subparsers.add_parser(
            "remove", help="Remove peer(s) from BGP quarantine list"
        )
        parser_bgp_quarantine_remove.add_argument(
            "--action",
            action="store_const",
            const="bgp_quarantine_remove",
            default="bgp_quarantine_remove",
            help=argparse.SUPPRESS,
        )
        self._add_bgp_quarantine_peers_argument(parser_bgp_quarantine_remove)

        # CMD: bgp quarantine list
        parser_bgp_quarantine_list = bgp_quarantine_subparsers.add_parser("list", help="List BGP qurantined peers")
        parser_bgp_quarantine_list.add_argument(
            "--action",
            action="store_const",
            const="bgp_quarantine_list",
            default="bgp_quarantine_list",
            help=argparse.SUPPRESS,
        )

        # Parse args
        self._args = self.argparser.parse_args(raw_args)

        # Setup logging
        if __name__ == "__main__":
            self._setup_logging()

        # Make sure we have an action
        if "action" not in self.args:
            if __name__ == "__main__":
                print("ERROR: No action specified!", file=sys.stderr)
                self.argparser.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No action specified")

        if self.args.action == "configure":
            return self.configure()

        if self.args.action == "bgp":
            if __name__ == "__main__":
                parser_bgp.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No options specified to 'bgp' action")

        # Graceful shutdown
        elif self.args.action == "bgp_graceful_shutdown":
            if __name__ == "__main__":
                parser_bgp_graceful_shutdown.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No options specified to 'bgp graceful_shutdown' action")
        elif self.args.action == "bgp_graceful_shutdown_add":
            self.bgp_graceful_shutdown_add(parser_bgp_graceful_shutdown_add)
        elif self.args.action == "bgp_graceful_shutdown_remove":
            self.bgp_graceful_shutdown_remove(parser_bgp_graceful_shutdown_remove)
        elif self.args.action == "bgp_graceful_shutdown_list":
            return self.bgp_graceful_shutdown_list()

        # Quarantine
        elif self.args.action == "bgp_quarantine":
            if __name__ == "__main__":
                parser_bgp_quarantine.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No options specified to 'bgp quarantine' action")
        elif self.args.action == "bgp_quarantine_add":
            self.bgp_quarantine_add(parser_bgp_quarantine_add)
        elif self.args.action == "bgp_quarantine_remove":
            self.bgp_quarantine_remove(parser_bgp_quarantine_remove)
        elif self.args.action == "bgp_quarantine_list":
            return self.bgp_quarantine_list()

        return None

    def configure(self) -> bool:
        """Configure BIRD."""
        # Load BirdPlan configuration
        self._birdplan_load_config()
        # Generate BIRD configuration
        self._birdplan_configure()
        # Commit BirdPlan state
        self._birdplan_commit_state()

        return True

    def bgp_graceful_shutdown_list(self) -> List[str]:
        """Gracefully shutdown peers."""

        # Load BirdPlan configuration
        self._birdplan_load_config()

        # Grab peer list
        peer_list = self.birdplan.bgp_graceful_shutdown_peer_list()

        if __name__ == "__main__":
            print("Peers in graceful shutdown:")
            for peer in peer_list:
                print(f"  {peer}")
            if not peer_list:
                print("--none--")
            print(f"Total: {len(peer_list)}")

        return peer_list

    def bgp_graceful_shutdown_add(self, arg_group: argparse.ArgumentParser) -> None:
        """Add peer(s) to the BirdPlan BGP graceful shutdown list."""

        # Make sure we have peers specified
        if not self.args.peers:
            if __name__ == "__main__":
                print("ERROR: No BGP peer(s) specified to add for graceful shutdown", file=sys.stderr)
                arg_group.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No BGP peer(s) specified to add for graceful shutdown")

        # Load BirdPlan configuration
        self._birdplan_load_config()

        peer_list = self.birdplan.bgp_graceful_shutdown_peer_list()
        for peer in self.args.peers:
            # Check if the peer is in the list
            if peer in peer_list:
                print(f"NOTICE: BGP peer '{peer}' already added to graceful shutdown list", file=sys.stderr)
                continue
            # Try add peer
            if __name__ == "__main__":
                try:
                    self.birdplan.bgp_graceful_shutdown_add_peer(peer)
                except BirdPlanError as err:
                    print(f"ERROR: {err}")
                    sys.exit(1)
            else:
                self.birdplan.bgp_graceful_shutdown_add_peer(peer)
            print(f"BGP peer '{peer}' added to graceful shutdown list")

        # Commit BirdPlan our state
        self._birdplan_commit_state()

    def bgp_graceful_shutdown_remove(self, arg_group: argparse.ArgumentParser) -> None:
        """Remove peer(s) from the BirdPlan BGP graceful shutdown list."""

        # Make sure we have peers specified
        if not self.args.peers:
            if __name__ == "__main__":
                print("ERROR: No BGP peer(s) specified to add", file=sys.stderr)
                arg_group.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No BGP peer(s) specified to add")

        # Load BirdPlan configuration
        self._birdplan_load_config()

        peer_list = self.birdplan.bgp_graceful_shutdown_peer_list()
        for peer in self.args.peers:
            # Check if the peer is not in the list
            if peer not in peer_list:
                print(f"NOTICE: BGP peer '{peer}' not in graceful shutdown list", file=sys.stderr)
                continue
            # Try add peer
            if __name__ == "__main__":
                try:
                    self.birdplan.bgp_graceful_shutdown_remove_peer(peer)
                except BirdPlanError as err:
                    print(f"ERROR: {err}", file=sys.stderr)
                    sys.exit(1)
            else:
                self.birdplan.bgp_graceful_shutdown_remove_peer(peer)
            print(f"BGP peer '{peer}' removed from graceful shutdown list")

        # Commit BirdPlan our state
        self._birdplan_commit_state()

    def bgp_quarantine_list(self) -> List[str]:
        """Gracefully shutdown peers."""

        # Load BirdPlan configuration
        self._birdplan_load_config()

        # Grab peer list
        peer_list = self.birdplan.bgp_quarantine_peer_list()

        if __name__ == "__main__":
            print("BGP peers in quarantine:")
            for peer in peer_list:
                print(f"  {peer}")
            if not peer_list:
                print("--none--")
            print(f"Total: {len(peer_list)}")

        return peer_list

    def bgp_quarantine_add(self, arg_group: argparse.ArgumentParser) -> None:
        """Add peer(s) to the BirdPlan BGP quarantine list."""

        # Make sure we have peers specified
        if not self.args.peers:
            if __name__ == "__main__":
                print("ERROR: No BGP peer(s) specified to add to quarantine", file=sys.stderr)
                arg_group.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No BGP peer(s) specified to add to quarantine")

        # Load BirdPlan configuration
        self._birdplan_load_config()

        peer_list = self.birdplan.bgp_quarantine_peer_list()
        for peer in self.args.peers:
            # Check if the peer is in the list
            if peer in peer_list:
                print(f"NOTICE: BGP peer '{peer}' already added to qurantine list", file=sys.stderr)
                continue
            # Try add peer
            if __name__ == "__main__":
                try:
                    self.birdplan.bgp_quarantine_add_peer(peer)
                except BirdPlanError as err:
                    print(f"ERROR: {err}", file=sys.stderr)
                    sys.exit(1)
            else:
                self.birdplan.bgp_quarantine_add_peer(peer)
            print(f"BGP peer '{peer}' added to quarantine list")

        # Commit BirdPlan our state
        self._birdplan_commit_state()

    def bgp_quarantine_remove(self, arg_group: argparse.ArgumentParser) -> None:
        """Remove peer(s) from the BirdPlan BGP quarantine list."""

        # Make sure we have peers specified
        if not self.args.peers:
            if __name__ == "__main__":
                print("ERROR: No BGP peer(s) specified to remove from quarantine", file=sys.stderr)
                arg_group.print_help(file=sys.stderr)
                sys.exit(1)
            else:
                raise BirdPlanError("No BGP peer(s) specified to remove from quarantine")

        # Load BirdPlan configuration
        self._birdplan_load_config()

        peer_list = self.birdplan.bgp_quarantine_peer_list()
        for peer in self.args.peers:
            # Check if the peer is not in the list
            if peer not in peer_list:
                print(f"NOTICE: BGP peer '{peer}' not in quarantine list", file=sys.stderr)
                continue
            # Try add peer
            if __name__ == "__main__":
                try:
                    self.birdplan.bgp_quarantine_remove_peer(peer)
                except BirdPlanError as err:
                    print(f"ERROR: {err}", file=sys.stderr)
                    sys.exit(1)
            else:
                self.birdplan.bgp_quarantine_remove_peer(peer)
            print(f"BGP peer '{peer}' removed from quarantine list")

        # Commit BirdPlan our state
        self._birdplan_commit_state()

    def _birdplan_load_config(self) -> None:
        """Load BirdPlan configuration."""
        # Try load configuration
        if __name__ == "__main__":
            try:
                self.birdplan.load(plan_file=self.args.birdplan_file[0], state_file=self.args.birdplan_state_file[0])
            except BirdPlanError as err:
                print(f"ERROR: Failed to load BirdPlan configuration: {err}", file=sys.stderr)
                sys.exit(1)
        else:
            self.birdplan.load(plan_file=self.args.birdplan_file[0], state_file=self.args.birdplan_state_file[0])

    def _birdplan_configure(self) -> None:
        """Configure BirdPlan."""

        # Setup globals based on options provided
        if self.args.ignore_irr_changes:
            self.birdplan.birdconf.birdconfig_globals.ignore_irr_changes = True
        if self.args.ignore_peeringdb_changes:
            self.birdplan.birdconf.birdconfig_globals.ignore_peeringdb_changes = True
        if self.args.use_cached:
            self.birdplan.birdconf.birdconfig_globals.use_cached = True

        # Try load configuration
        if __name__ == "__main__":
            try:
                self.birdplan.configure(self.args.bird_config_file[0])
            except BirdPlanError as err:
                print(f"ERROR: Failed to generate BirdPlan configuration: {err}", file=sys.stderr)
                sys.exit(1)
        else:
            self.birdplan.configure(self.args.bird_config_file[0])

    def _birdplan_commit_state(self) -> None:
        """Commit BirdPlan state."""

        # Try commit our state if we were called from the commandline
        if __name__ == "__main__":
            # If we didn't get a state file specified, then just display a notice we're not going to write it out
            if not self.args.birdplan_state_file[0]:
                print("NOTICE: State file not written!", file=sys.stderr)
                return
            # Try commit state
            try:
                self.birdplan.commit_state()
            except BirdPlanError as err:
                print(f"ERROR: Failed to commit BirdPlan state: {err}")
                sys.exit(1)
        else:
            self.birdplan.commit_state()

    def _add_configure_arguments(self, arg_group: argparse.ArgumentParser) -> None:
        """Add configure arguments."""

        # Ignore IRR changes
        arg_group.add_argument("--ignore-irr-changes", action="store_true", help="Ignore IRR changes between last run and this run")

        # Ignore PeeringDB changes
        arg_group.add_argument(
            "--ignore-peeringdb-changes", action="store_true", help="Ignore PeeringDB changes between last run and this run"
        )

        # Use last cached data
        arg_group.add_argument(
            "--use-cached", action="store_true", help="Use cached IRR and PeeringDB data instead of doing network requests"
        )

    def _add_main_arguments(self) -> None:
        """Add main commandline arguments."""

        if __name__ == "__main__":
            print(f"BirdPlan v{__VERSION__} - Copyright © 2019-2021, AllWorldIT.\n", file=sys.stderr)

        optional_group = self.argparser.add_argument_group("Optional arguments")
        optional_group.add_argument("-h", "--help", action="help", help="Show this help message and exit")
        optional_group.add_argument("-v", "--verbose", action="store_true", help="Display verbose logging")

        # Input and output file settings
        optional_group.add_argument(
            "-i",
            "--birdplan-file",
            nargs=1,
            metavar="BIRDPLAN_FILE",
            default=[BIRDPLAN_FILE],
            help=f"BirdPlan file to process (default: {BIRDPLAN_FILE})",
        )
        optional_group.add_argument(
            "-o",
            "--bird-config-file",
            nargs=1,
            metavar="BIRD_CONFIG_FILE",
            default=[BIRD_CONFIG_FILE],
            help=f"BIRD config file, using '-' will output to stdout (default: {BIRD_CONFIG_FILE})",
        )
        optional_group.add_argument(
            "-s",
            "--birdplan-state-file",
            nargs=1,
            metavar="BIRDPLAN_STATE_FILE",
            default=[None],
            help=f"BirdPlan state file to use (default: {BIRDPLAN_STATE_FILE})",
        )

    def _add_bgp_graceful_shutdown_peers_argument(self, arg_group: argparse.ArgumentParser) -> None:  # pylint: disable=no-self-use
        """Add BGP graceful shutdown arguments for a command that takes peers."""
        arg_group.add_argument(
            "peers",
            nargs="+",
            metavar="PEER",
            help="Peer name (* = all)",
        )

    def _add_bgp_quarantine_peers_argument(self, arg_group: argparse.ArgumentParser) -> None:  # pylint: disable=no-self-use
        """Add BGP qurantine arguments for a command that takes peers."""
        arg_group.add_argument(
            "peers",
            nargs="+",
            metavar="PEER",
            help="Peer name",
        )

    def _setup_logging(self) -> None:
        """Set up logging."""

        # Setup logger and level
        logger = logging.getLogger()
        if self.args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        # Setup console handler
        console_handler = logging.StreamHandler()
        # Use a better format for messages
        console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
        logger.addHandler(console_handler)

    @property
    def args(self) -> argparse.Namespace:
        """Return our commandline arguments."""
        return self._args

    @property
    def argparser(self) -> argparse.ArgumentParser:
        """Return our ArgumentParser instance."""
        return self._argparser

    @property
    def birdplan(self) -> BirdPlan:
        """Return our BirdPlan instance."""
        return self._birdplan


if __name__ == "__main__":
    birdplan_cmdline = BirdPlanCommandLine()

    try:
        birdplan_cmdline.run()
    except BirdPlanError as exception:
        print(f"ERROR: {exception}", file=sys.stderr)
