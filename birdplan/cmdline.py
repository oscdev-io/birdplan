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

from typing import Any, List, NoReturn, Optional
import argparse
import json
import logging
import logging.handlers
import sys
from . import __VERSION__, BirdPlan
from .exceptions import BirdPlanError, BirdPlanErrorUsage
from .plugin import PluginCollection


# Defaults
BIRDPLAN_FILE = "/etc/birdplan/birdplan.yaml"
BIRD_CONFIG_FILE = "/etc/bird.conf"
BIRDPLAN_STATE_FILE = "/var/lib/birdplan/birdplan.state"


class BirdPlanArgumentParser(argparse.ArgumentParser):
    """ArgumentParser override class to output errors slightly better."""

    def error(self, message: str) -> NoReturn:
        """
        Slightly better error message handler for ArgumentParser.

        Argument
        --------
        message : str
            Error message.

        """
        raise BirdPlanErrorUsage(message, self)


class BirdPlanCommandLine:
    """BirdPlan commandline handling class."""

    _args: argparse.Namespace
    _argparser: BirdPlanArgumentParser
    _birdplan: BirdPlan

    def __init__(self, test_mode: bool = False) -> None:
        """Instantiate object."""

        self._args = argparse.Namespace()
        self._argparser = BirdPlanArgumentParser(add_help=False)
        self._birdplan = BirdPlan(test_mode=test_mode)

    def run(  # pylint: disable=too-many-branches,too-many-locals,too-many-statements
        self, raw_args: Optional[List[str]] = None
    ) -> Any:
        """Run BirdPlan from command line."""

        # Don't output copyright when we output in JSON format
        if self.is_console and not self.is_json:
            print(f"BirdPlan v{__VERSION__} - Copyright © 2019-2021, AllWorldIT.\n", file=sys.stderr)

        # Add main commandline arguments

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
            "-n",
            "--no-write-state",
            action="store_true",
            default=False,
            help="Disable writing state file",
        )
        optional_group.add_argument(
            "-j",
            "--json",
            action="store_true",
            default=False,
            help="Output in JSON",
        )

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
            raise BirdPlanErrorUsage("No action specified", self.argparser)

        # Generate the command line option method name
        method_name = f"cmd_{self.args.action}"

        # Grab the first plugin which has this method
        plugin_name = plugins.get_first(method_name)
        if not plugin_name:
            raise BirdPlanError("Failed to find plugin to handle command line options")

        # Grab the result from the command
        result = plugins.call_plugin(plugin_name, method_name, {"cmdline": self})

        # Check if we should output JSON
        if self.is_console:
            if self.is_json:
                plugins.call_plugin(plugin_name, "show_output_json", result)
            # If not, we need to output text
            else:
                plugins.call_plugin(plugin_name, "show_output_text", result)

        return result

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
        self.birdplan.load(
            plan_file=self.args.birdplan_file[0],
            state_file=self.args.birdplan_state_file[0],
            **kwargs,
        )

    def birdplan_commit_state(self) -> None:
        """Commit BirdPlan state."""

        # If we didn't get a state file specified, then just display a notice we're not going to write it out
        if not self.args.birdplan_state_file[0]:
            return
        # Check if we need to skip writing the state
        if self.args.no_write_state:
            return

        self.birdplan.commit_state()

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

        if ("--json" in sys.argv) or ("-j" in sys.argv):
            return True
        return False


if __name__ == "__main__":
    birdplan_cmdline = BirdPlanCommandLine()

    try:
        birdplan_cmdline.run()
    except BirdPlanError as exception:
        if birdplan_cmdline.is_json:
            print(json.dumps({"status": "error", "message": str(exception)}))
        else:
            print(f"ERROR: {exception}", file=sys.stderr)
            sys.exit(1)

    except BirdPlanErrorUsage as exception:
        if birdplan_cmdline.is_json:
            print(json.dumps({"status": "error", "message": exception.message}))
        else:
            print(f"ERROR: {exception}", file=sys.stderr)
            sys.exit(2)

