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

"""BirdPlan commandline options for "birdplan configure"."""


import argparse
import grp
import os
import pwd
from typing import Any, Dict, Optional

from ...cmdline import BIRD_CONFIG_FILE, BirdPlanCommandLine
from ...exceptions import BirdPlanError
from .cmdline_plugin import BirdPlanCmdlinePluginBase

__all__ = ["BirdPlanCmdlineConfigure"]


class BirdPlanCmdlineConfigure(BirdPlanCmdlinePluginBase):
    """BirdPlan "configure" command."""

    # Output config file
    _config_filename: Optional[str]

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan configure"
        self.plugin_order = 10

        self._config_filename = None

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

    def cmd_configure(self, args: Any) -> Any:
        """
        BirdPlan "configure" command.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Load BirdPlan configuration
        cmdline.birdplan_load_config(
            ignore_irr_changes=cmdline.args.ignore_irr_changes,
            ignore_peeringdb_changes=cmdline.args.ignore_peeringdb_changes,
            use_cached=cmdline.args.use_cached,
        )
        # Generate BIRD configuration
        bird_config = cmdline.birdplan.configure()

        # Commit BirdPlan state
        cmdline.birdplan_commit_state()

        # Save the output filename
        self.config_filename = cmdline.args.output_file[0]

        # If we're outputting to file, write it here
        if self.config_filename and self.config_filename != "-":
            self._write_config_file(bird_config)

        return bird_config

    def to_text(self, data: Any) -> str:
        """
        Return output in text format.

        Parameters
        ----------
        data : str
            Bird configuration

        Returns
        -------
        str
            Output in text format.

        """
        # Skip output when we're writing a config file
        if self.config_filename and self.config_filename != "-":
            return ""
        # Output config
        return super().to_text(data)

    def _write_config_file(self, data: Any) -> None:
        """
        Write out configuration file with data.

        Parameters
        ----------
        data : str
            Bird configuration

        """

        if not self.config_filename:
            raise RuntimeError("Attribute 'config_filename' must be set")

        # Get birdplan user id
        try:
            birdplan_uid = pwd.getpwnam("birdplan").pw_uid
        except KeyError:
            birdplan_uid = -1

        # Get bird group id
        try:
            bird_gid = grp.getgrnam("bird").gr_gid
        except KeyError:
            bird_gid = None

        # Write out config file
        try:
            fd = os.open(self.config_filename, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o640)
            # If we have a bird group, set it
            if bird_gid:
                os.fchown(fd, birdplan_uid, bird_gid)
            # Write out config
            with os.fdopen(fd, "w") as config_file:
                config_file.write(data)
        except OSError as err:  # pragma: no cover
            raise BirdPlanError(f"Failed to open '{self.config_filename}' for writing: {err}") from None

    @property
    def config_filename(self) -> Optional[str]:
        """Config file name to write out."""
        return self._config_filename

    @config_filename.setter
    def config_filename(self, config_filename: str) -> None:
        """Config file name to write out."""
        self._config_filename = config_filename
