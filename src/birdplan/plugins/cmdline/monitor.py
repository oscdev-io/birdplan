#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""BirdPlan commandline options for "birdplan monitor"."""

import argparse
import json
import logging
import pathlib
from typing import Any

from ...cmdline import BIRDPLAN_MONITOR_FILE, BirdPlanCommandLine, BirdPlanCommandlineResult
from ...exceptions import BirdPlanError
from .cmdline_plugin import BirdPlanCmdlinePluginBase

__all__ = ["BirdPlanCmdlineMonitor"]


class BirdPlanCmdlineMonitor(BirdPlanCmdlinePluginBase):
    """BirdPlan "configure" command."""

    # Output filename
    _output_filename: pathlib.Path | None

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Plugin setup
        self.plugin_description = "birdplan monitor"
        self.plugin_order = 10

        self._output_filename = None

    def register_parsers(self, args: dict[str, Any]) -> None:
        """
        Register commandline parsers.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        root_parser = args["root_parser"]

        subparser = root_parser.add_parser("monitor", help="Monitor BIRD status")

        subparser.add_argument(
            "--action",
            action="store_const",
            const="monitor",
            default="monitor",
            help=argparse.SUPPRESS,
        )

        # Output filename
        subparser.add_argument(
            "-o",
            "--output-file",
            nargs=1,
            metavar="MONITOR_OUTPUT_FILE",
            default=[BIRDPLAN_MONITOR_FILE],
            help=f"Monitor filename to output to, using '-' will output to stdout (default: {BIRDPLAN_MONITOR_FILE})",
        )

        # Set our internal subparser property
        self._subparser = subparser
        self._subparsers = None

    def cmd_monitor(self, args: dict[str, Any]) -> BirdPlanCommandlineResult:
        """
        Commandline handler for "monitor" action.

        Parameters
        ----------
        args : Dict[str, Any]
            Method argument(s).

        """

        cmdline: BirdPlanCommandLine = args["cmdline"]

        # Grab Bird control socket
        bird_socket = cmdline.args.bird_socket[0]

        # Suppress info output
        cmdline.birdplan.birdconf.birdconfig_globals.suppress_info = True

        # Load BirdPlan configuration
        cmdline.birdplan_load_config(ignore_irr_changes=True, ignore_peeringdb_changes=True, use_cached=True)

        # Save the output filename
        self.output_filename = cmdline.args.output_file[0]

        # Grab information to return
        bgp_protocol = cmdline.birdplan.state_bgp_peer_summary(bird_socket=bird_socket)
        ospf_protocol = cmdline.birdplan.state_ospf_summary(bird_socket=bird_socket)

        # Build structure
        monitor_status = {
            "bgp": bgp_protocol,
            "ospf": ospf_protocol,
        }

        # If we're outputting to file, write it here
        if self.output_filename and self.output_filename != "-":
            self._write_monitor_file(monitor_status)
            return BirdPlanCommandlineResult(monitor_status, has_console_output=False)

        return BirdPlanCommandlineResult(monitor_status)

    def _write_monitor_file(self, data: dict[str, Any]) -> None:
        """
        Write out monitor file with data.

        Parameters
        ----------
        data : str
            Monitor data.

        """

        if not self.output_filename:
            raise RuntimeError("Attribute 'output_filename' must be set")

        # Write out config file
        try:
            with self.output_filename.open("w", encoding="UTF-8") as config_file:
                # Write out data json
                logging.debug("Writing monitor file '%s'", self.output_filename)
                config_file.write(json.dumps(data, indent=4, sort_keys=True))
        except OSError as err:  # pragma: no cover
            raise BirdPlanError(f"Failed to open '{self.output_filename}' for writing: {err}") from None

    @property
    def output_filename(self) -> pathlib.Path | None:
        """Config file name to write out."""
        return self._output_filename

    @output_filename.setter
    def output_filename(self, output_filename: pathlib.Path) -> None:
        """Config file name to write out."""
        self._output_filename = output_filename
