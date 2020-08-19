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

"""Birdplan package."""

from typing import Any, Dict, Optional
import yaml
from .bird_config import BirdConfig
from .exceptions import BirdPlanError


__VERSION__ = "0.0.1"


class BirdPlan:
    """
    Main BirdPlan class.

    Attributes
    ----------
    plan_file : str
        Plan file we'll be working on.

    """

    _plan_file: Optional[str]
    _config: Dict[Any, Any]

    def __init__(self):
        """Initialize object."""

        self._plan_file = None
        self._config = {}

    def load(self, plan_file: str, macros: Optional[Dict[str, str]] = None):
        """
        Initialize object.

        Parameters
        ----------
        plan_file : str
            Source plan file to generate configuration from.
        macros : Dict[str, str]
            Optional list of macros and their replacment values.

        """

        try:
            with open(plan_file, "r") as file:
                raw_config = file.read()
        except OSError as err:
            raise BirdPlanError(f"Failed to read plan file '{plan_file}': {err}") from None

        # Check if we're replacing macros
        if macros:
            for macro, value in macros.items():
                raw_config = raw_config.replace(macro, value)

        try:
            self.config = yaml.safe_load(raw_config)
        except ImportError as err:
            raise BirdPlanError(f" Failed to import plan file '{plan_file}': {err}") from None

    def generate(self, output_filename: Optional[str] = None) -> str:
        """
        Generate Bird configuration.

        Parameters
        ----------
        output_filename : Optional[str]
            Optional filename to write the generated configuration to. If this is not specified we'll just return the
            configuration.

        """

        birdconf = BirdConfig()

        # Check configuration options are supported
        for config_item in self.config:
            if config_item not in ["router_id", "log_file", "debug", "static", "export_kernel"]:
                raise BirdPlanError("The config item '{config_Item}' is not supported")

        # Check that a router ID was specified
        if "router_id" not in self.config:
            raise BirdPlanError("The 'router_id' attribute must be specified")
        birdconf.router_id = self.config["router_id"]

        # Check if we have a log_file specified to use
        if "log_file" in self.config:
            birdconf.log_file = self.config["log_file"]

        # Check if we're in debugging mode or not
        if "debug" in self.config:
            birdconf.debug = self.config["debug"]

        # Static routes
        if "static" in self.config:
            for route in self.config["static"]:
                birdconf.static.add_route(route)

        # Check if we're exporting routes from the master tables to the kernel tables
        if "export_kernel" in self.config:
            # Loop with export_kernel items
            for export, export_config in self.config["export_kernel"].items():
                # Static routes
                if export == "static":
                    birdconf.master.export_kernel_static = export_config
                # Static device routes
                elif export == "static_device":
                    birdconf.master.export_kernel_static_device = export_config
                # RIP routes
                elif export == "rip":
                    birdconf.master.export_kernel_rip = export_config
                # OSPF routes
                elif export == "ospf":
                    birdconf.master.export_kernel_ospf = export_config
                # BGP routes
                elif export == "bgp":
                    birdconf.master.export_kernel_bgp = export_config
                # If we don't understand this 'accept' entry, throw an error
                else:
                    raise BirdPlanError(f"Configuration item '{export}' not understood in 'export_kernel'")

        # Get the configuration
        config_lines = birdconf.get_config()

        # If we have a filename, write out
        if output_filename:
            try:
                with open(output_filename, "w") as config_file:
                    config_file.write("\n".join(config_lines))
            except OSError as err:  # pragma: no cover
                raise BirdPlanError(f"Failed to open '{output_filename}' for writing: {err}") from None

        return "\n".join(config_lines)

    @property
    def plan_file(self) -> Optional[str]:
        """Plan file we're using."""
        return self._plan_file

    @property
    def config(self) -> Dict[Any, Any]:
        """Return our config."""
        return self._config

    @config.setter
    def config(self, config: Dict[Any, Any]):
        """Set our configuration."""
        self._config = config
