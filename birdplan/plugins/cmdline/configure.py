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

"""BirdPlan commandline options for "birdplan configure"."""


from typing import Any, Dict
import argparse
from .cmdline_plugin import BirdplanCmdlinePluginBase
from ...cmdline import BIRD_CONFIG_FILE
from ...exceptions import BirdPlanError


class BirdplanCmdlineConfigure(BirdplanCmdlinePluginBase):
    """Birdplan "configure" command."""

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan configure"
        self.plugin_order = 10

    def register_parsers(self, args: Dict[str, Any]) -> None:
        """
        Register commandline parsers.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        root_parser = args["root_parser"]

        # CMD: configure
        subparser = root_parser.add_parser("configure", help="Create BIRD configuration")

        subparser.add_argument(
            "--action",
            action="store_const",
            const="configure",
            default="configure",
            help=argparse.SUPPRESS,
        )

        # Output filename
        subparser.add_argument(
            "-o",
            "--output-file",
            nargs=1,
            metavar="BIRD_CONFIG_FILE",
            default=[BIRD_CONFIG_FILE],
            help=f"BIRD config file to output, using '-' will output to stdout (default: {BIRD_CONFIG_FILE})",
        )

        # Ignore IRR changes
        subparser.add_argument(
            "--ignore-irr-changes", action="store_true", default=False, help="Ignore IRR changes between last run and this run"
        )

        # Ignore PeeringDB changes
        subparser.add_argument(
            "--ignore-peeringdb-changes",
            action="store_true",
            default=False,
            help="Ignore PeeringDB changes between last run and this run",
        )

        # Use last cached data
        subparser.add_argument(
            "--use-cached",
            action="store_true",
            default=False,
            help="Use cached IRR and PeeringDB data instead of doing network requests",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_configure(self, args: Any) -> bool:
        """
        Birdplan "configure" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        cmdline = args["cmdline"]

        # Load BirdPlan configuration
        cmdline.birdplan_load_config(
            ignore_irr_changes=cmdline.args.ignore_irr_changes,
            ignore_peeringdb_changes=cmdline.args.ignore_peeringdb_changes,
            use_cached=cmdline.args.use_cached,
        )
        # Generate BIRD configuration
        bird_config = cmdline.birdplan_configure()

        # If we were supplied with a bird configuration file on the commandline, write it out
        output_filename = cmdline.args.output_file[0]
        if output_filename:
            # If we have - as a filename, print to stdout
            if output_filename == "-":
                print(bird_config)
            # Else write out file
            else:
                try:
                    with open(output_filename, "w") as config_file:
                        config_file.write(bird_config)
                except OSError as err:  # pragma: no cover
                    raise BirdPlanError(f"Failed to open '{output_filename}' for writing: {err}") from None

        # Commit BirdPlan state
        cmdline.birdplan_commit_state()

        return True
