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

"""BirdPlan commandline interface."""

import argparse
import copy
import json
import logging
import logging.handlers
import os
import sys
from typing import Any, Callable, Dict, List, Literal, NoReturn, Optional

from . import BirdPlan
from .console.colors import colored
from .exceptions import BirdPlanError, BirdPlanUsageError
from .plugin import PluginCollection
from .version import __version__

__all__ = ["ColorFormatter", "BirdPlanArgumentParser", "BirdPlanCommandLine"]


# Defaults
if os.path.exists("/etc/bird/bird.conf"):
    BIRD_CONFIG_FILE = "/etc/bird/bird.conf"
else:
    BIRD_CONFIG_FILE = "/etc/bird.conf"
BIRD_SOCKET = "/run/bird/bird.ctl"
BIRDPLAN_FILE = "/etc/birdplan/birdplan.yaml"
BIRDPLAN_STATE_FILE = "/var/lib/birdplan/birdplan.state"
BIRDPLAN_MONITOR_FILE = "/var/lib/birdplan/monitor.json"


TRACE_LOG_LEVEL = 5


class ColorFormatter(logging.Formatter):
    """
    A custom log formatter class that.

    It currently...
    * Outputs the LOG_LEVEL with an appropriate color.
    * If a log call includes an `extras={"color_message": ...}` it will be used for formatting the output, instead of the plain
    text message.
    """

    level_name_colors: Dict[int, Callable[[str], str]] = {
        TRACE_LOG_LEVEL: lambda level_name: colored(str(level_name), "blue"),
        logging.DEBUG: lambda level_name: colored(str(level_name), "cyan"),
        logging.INFO: lambda level_name: colored(str(level_name), "green"),
        logging.WARNING: lambda level_name: colored(str(level_name), "yellow"),
        logging.ERROR: lambda level_name: colored(str(level_name), "red"),
        logging.CRITICAL: lambda level_name: colored(str(level_name), "bright_red"),
    }

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        use_colors: bool | None = None,
    ):
        """
        Color log formatter class.

        Arguments
        ---------
        fmt : str
            Format string.
        datefmt : str
            Date format string.
        style : str
            Format style.
        use_colors : bool
            Use colors or not.
        """

        if isinstance(use_colors, bool):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name: str, level_no: int) -> str:
        """Get colored level name from level_no."""

        def default(level_name: str) -> str:
            return str(level_name)  # pragma: no cover

        func = self.level_name_colors.get(level_no, default)
        return func(level_name)

    def should_use_colors(self) -> bool:
        """Return if we should use colors or not."""
        return True  # pragma: no cover

    def formatMessage(self, record: logging.LogRecord) -> str:  # noqa: N802
        """Format a message from a record."""

        # Copy record
        recordcopy = copy.copy(record)
        # Grab level name
        levelname = recordcopy.levelname
        # Add padding before color control codes
        seperator = " " * (8 - len(recordcopy.levelname))
        # Check if we're using color or not
        if self.use_colors:
            # If we are get the levelname in color
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            # If a color_message is present, use it instead
            if "color_message" in recordcopy.__dict__:
                recordcopy.msg = recordcopy.__dict__["color_message"]
                recordcopy.__dict__["message"] = recordcopy.getMessage()
        # Set the record levelcolor
        recordcopy.__dict__["levelcolor"] = levelname + seperator
        return super().formatMessage(recordcopy)


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
        raise BirdPlanUsageError(message, self)


class BirdPlanCommandlineResult:  # pylint: disable=too-few-public-methods
    """BirdPlan commandline result class."""

    _data: Any
    _has_console_output: bool

    def __init__(self, data: Any, has_console_output: bool = True) -> None:
        """Initialize object."""

        self._data = data
        self._has_console_output = has_console_output

    def as_console(self) -> str:
        """
        Return data as console output.

        Returns
        -------
        str
            Data as console output.
        """

        return self.as_text()

    def as_text(self) -> str:
        """
        Return data as text.

        Returns
        -------
        str
            Data as text.
        """

        return f"{self.data}"

    def as_json(self) -> str:
        """
        Return data as JSON.

        Parameters
        ----------
        data : Any
            Output data.

        Returns
        -------
        str
            Return data as JSON.
        """

        return json.dumps({"status": "success", "data": self.data})

    @property
    def data(self) -> Any:
        """
        Return raw data.

        Returns
        -------
        Any
            Return data in its raw form.
        """

        return self._data

    @property
    def has_console_output(self) -> bool:
        """
        Return whether or not data has console output.

        Returns
        -------
        bool
            Return whether or not data has console output.
        """

        return self._has_console_output


class BirdPlanCommandLine:
    """BirdPlan commandline handling class."""

    _is_console: bool
    _args: argparse.Namespace
    _argparser: BirdPlanArgumentParser
    _birdplan: BirdPlan

    def __init__(self, test_mode: bool = False, is_console: bool = False) -> None:
        """Instantiate object."""

        prog: Optional[str] = None
        if sys.argv[0].endswith("__main__.py"):
            prog = "python -m birdplan"

        self._is_console = is_console
        self._args = argparse.Namespace()
        self._argparser = BirdPlanArgumentParser(add_help=False, prog=prog)
        self._birdplan = BirdPlan(test_mode=test_mode)

    def run(  # noqa: CFQ001 # pylint: disable=too-many-branches,too-many-locals,too-many-statements
        self, raw_args: Optional[List[str]] = None
    ) -> BirdPlanCommandlineResult:
        """Run BirdPlan from command line."""

        # Check if we have one commandline argument, if we do and if it is --version, return our version
        if raw_args and len(raw_args) == 1 and raw_args[0] == "--version":
            result: BirdPlanCommandlineResult = BirdPlanCommandlineResult(__version__)
            # Check if we're on a console
            if self.is_console:
                # Check if we should output json
                if self.is_json:
                    print(result.as_json())
                # Else if we have console output, then output that
                elif result.has_console_output:
                    print(result.as_console())

            return result

        # If this is the console, display our version
        if self.is_console:
            print(f"BirdPlan v{__version__} - Copyright © 2019-2024, AllWorldIT.\n", file=sys.stderr)

        # Add main commandline arguments
        optional_group = self.argparser.add_argument_group("Optional arguments")
        optional_group.add_argument("-h", "--help", action="help", help="Show this help message and exit")
        optional_group.add_argument("-v", "--verbose", action="store_true", help="Display verbose logging")
        optional_group.add_argument("--version", action="store_true", help="Display version and exit")

        # Input and output file settings
        optional_group.add_argument(
            "-b",
            "--bird-socket",
            nargs=1,
            metavar="BIRD_SOCKET",
            default=[BIRD_SOCKET],
            help=f"BirdPlan needs access to the Bird control socket for some commandline functionality (default: {BIRD_SOCKET})",
        )
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
        if self.is_console:
            self._setup_logging()

        # Make sure we have an action
        if "action" not in self.args:
            raise BirdPlanUsageError("No action specified", self.argparser)

        # Generate the command line option method name
        method_name = f"cmd_{self.args.action}"

        # Grab the first plugin which has this method
        plugin_name = plugins.get_first(method_name)
        if not plugin_name:
            raise BirdPlanError("Failed to find plugin to handle command line options")

        # Grab the result from the command
        result = plugins.call_plugin(plugin_name, method_name, {"cmdline": self})

        # Check if we're on a console
        if self.is_console:
            # Check if we should output json
            if self.is_json:
                print(result.as_json())
            # Else if we have console output, then output that
            elif result.has_console_output:
                print(result.as_console())

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

        # Set the state file
        state_file: Optional[str] = None
        if self.args.birdplan_state_file[0]:
            state_file = self.args.birdplan_state_file[0]
        else:
            state_file = BIRDPLAN_STATE_FILE

        # Try load configuration
        self.birdplan.load(
            plan_file=self.args.birdplan_file[0],
            state_file=state_file,
            **kwargs,
        )

    def birdplan_commit_state(self) -> None:
        """Commit BirdPlan state."""

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

        # Remove all existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Setup console handler
        console_handler = logging.StreamHandler(sys.stderr)
        # Build log format
        log_format = ""
        # Only add a timestamp if we're not running under systemd
        if "INVOCATION_ID" not in os.environ:
            log_format += "%(asctime)s "
        log_format += "%(levelcolor)s %(message)s"
        # Use a better format for messages
        console_handler.setFormatter(ColorFormatter(log_format, "[%Y-%m-%d %H:%M:%S]"))
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
        return self._is_console

    @is_console.setter
    def is_console(self, is_console: bool) -> None:
        """
        Set property indicating we're running from a console.

        Parameters
        ----------
        is_console : bool
            Set to True indicating if we were called from the commandline.

        """
        self._is_console = is_console

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


# Main entry point from the commandline
def main() -> None:
    """Entry point function for the commandline."""
    birdplan_cmdline = BirdPlanCommandLine(is_console=True)

    try:
        birdplan_cmdline.run(sys.argv[1:])
    except BirdPlanError as exception:
        if birdplan_cmdline.is_json:
            print(json.dumps({"status": "error", "message": str(exception)}))
        else:
            print(f"ERROR: {exception}", file=sys.stderr)
            sys.exit(1)
