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

import argparse
import logging
import logging.handlers
import sys
from birdplan import __VERSION__, BirdPlan
from birdplan.exceptions import BirdPlanError


def get_argparser() -> argparse.ArgumentParser:
    """Return an instance of argparse.ArgumentParser."""

    print(f"BirdPlan v{__VERSION__} - Copyright © 2019-2020, AllWorldIT.\n", file=sys.stderr)

    argparser = argparse.ArgumentParser(add_help=False)

    optional_group = argparser.add_argument_group("Optional arguments")
    optional_group.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    optional_group.add_argument("-v", "--verbose", action="store_true", help="Display verbose logging")

    return argparser


def add_arguments(arg_group: argparse.ArgumentParser):
    """Add arguments."""
    arg_group.add_argument(
        "--generate",
        nargs=1,
        metavar="PLAN_FILE",
        required=True,
        help="Plan file to process",
    )


def setup_logging(args: argparse.Namespace):
    """Set up logging."""

    # Setup logger and level
    logger = logging.getLogger()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    # Setup console handler
    console_handler = logging.StreamHandler()
    # Use a better format for messages
    console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(message)s"))
    logger.addHandler(console_handler)


def run_birdplan():
    """Run BirdPlan from command line."""
    # Grab our arg parser
    argparser = get_argparser()
    # Add arguments
    add_arguments(argparser)
    # Parse args
    args = argparser.parse_args()
    # Setup logging
    setup_logging(args)

    # Check if we're generating a configuration file
    if not args.generate:
        print("ERROR: No action specified!")
        argparser.print_help()
        sys.exit(1)

    # Start configuration generator
    birdplan = BirdPlan()
    # Try load and configure
    try:
        birdplan.load(args.generate[0])
        birdplan.generate("")
    except BirdPlanError as err:
        logging.error("Failed to create configuration: %s", err)
        sys.exit(1)


if __name__ == "__main__":
    run_birdplan()
