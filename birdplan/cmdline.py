#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2021, AllWorldIT
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
from . import __VERSION__, BirdPlan
from .exceptions import BirdPlanError
from .plugin import PluginCollection


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

        # Don't output copyright when we output in JSON format
        if (__name__ == "__main__") and not ("--json" in sys.argv or "-j" in sys.argv):
            print(f"BirdPlan v{__VERSION__} - Copyright © 2019-2021, AllWorldIT.\n", file=sys.stderr)

        # Add main commandline arguments
        self._add_main_arguments()

        # Add subparsers
        subparsers = self.argparser.add_subparsers()

        # configure
        plugins = PluginCollection(["birdplan.plugins.cmdline"])

        # Register commandline parsers
        plugins.call_if_exists("register_parsers", {"root_parser": subparsers, "plugins": plugins})

        # Parse commandline args
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

        # Call first plugin that matches the commandline option
        return plugins.call_first(f"cmd_{self.args.action}", {"cmdline": self})

    def birdplan_load_config(self, **kwargs: Any) -> None:
        """
        Load BirdPlan configuration.

        Parameters
        ----------
        ignore_irr_changes : bool
            Optional parameter to ignore IRR lookups during configuration load.

        ignore_peeringdb_changes : bool
            Optional parameter to ignore peering DB lookups during configuraiton load.

        use_cached : bool
            Optional parameter to use cached values from state during configuration load.

        """

        # Try load configuration
        if __name__ == "__main__":
            try:
                self.birdplan.load(
                    plan_file=self.args.birdplan_file[0],
                    state_file=self.args.birdplan_state_file[0],
                    **kwargs,
                )
            except BirdPlanError as err:
                print(f"ERROR: Failed to load BirdPlan configuration: {err}", file=sys.stderr)
                sys.exit(1)
        else:
            self.birdplan.load(
                plan_file=self.args.birdplan_file[0],
                state_file=self.args.birdplan_state_file[0],
                **kwargs,
            )

    def birdplan_configure(self) -> str:
        """Configure BirdPlan."""

        # Try load configuration
        if __name__ == "__main__":
            try:
                bird_config = self.birdplan.configure()
            except BirdPlanError as err:
                print(f"ERROR: Failed to generate BirdPlan configuration: {err}", file=sys.stderr)
                sys.exit(1)
        else:
            bird_config = self.birdplan.configure()

        return bird_config

    def birdplan_commit_state(self) -> None:
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

    def _add_main_arguments(self) -> None:
        """Add main commandline arguments."""

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
            "-s",
            "--birdplan-state-file",
            nargs=1,
            metavar="BIRDPLAN_STATE_FILE",
            default=[None],
            help=f"BirdPlan state file to use (default: {BIRDPLAN_STATE_FILE})",
        )
        optional_group.add_argument(
            "-j",
            "--json",
            action="store_true",
            default=False,
            help="Output in JSON",
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

    @property
    def is_console(self) -> bool:
        """
        Property indicating True or False if we're being called from the commandline.

        Returns
        -------
        bool indicating if we were called from the commandline.

        """
        return __name__ == "__main__"

    @property
    def is_json(self) -> bool:
        """
        Property indicating that we should output in JSON on the commandline.

        Returns
        -------
        bool : indicating if we should output in JSON from the commandline.

        """
        if self.args.json:
            return True
        return False


if __name__ == "__main__":
    birdplan_cmdline = BirdPlanCommandLine()

    try:
        birdplan_cmdline.run()
    except BirdPlanError as exception:
        print(f"ERROR: {exception}", file=sys.stderr)
