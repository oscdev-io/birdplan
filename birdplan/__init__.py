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
    _birdconf: Optional[BirdConfig]

    def __init__(self):
        """Initialize object."""

        self._plan_file = None
        self._config = {}
        self._birdconf = None

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

        self._birdconf = BirdConfig()

        # Check configuration options are supported
        for config_item in self.config:
            if config_item not in ["router_id", "log_file", "debug", "static", "export_kernel", "rip", "ospf"]:
                raise BirdPlanError(f"The config item '{config_item}' is not supported")

        # Configure sections
        self._config_global()
        self._config_static()
        self._config_export_kernel()
        self._config_rip()
        self._config_ospf()

        # Generate the configuration
        config_lines = self._birdconf.get_config()

        # If we have a filename, write out
        if output_filename:
            try:
                with open(output_filename, "w") as config_file:
                    config_file.write("\n".join(config_lines))
            except OSError as err:  # pragma: no cover
                raise BirdPlanError(f"Failed to open '{output_filename}' for writing: {err}") from None

        return "\n".join(config_lines)

    def _config_global(self):
        """Configure global options."""

        # Check that a router ID was specified
        if "router_id" not in self.config:
            raise BirdPlanError("The 'router_id' attribute must be specified")
        self._birdconf.router_id = self.config["router_id"]

        # Check if we have a log_file specified to use
        if "log_file" in self.config:
            self._birdconf.log_file = self.config["log_file"]

        # Check if we're in debugging mode or not
        if "debug" in self.config:
            self._birdconf.debug = self.config["debug"]

    def _config_static(self):
        """Configure static section."""
        # Static routes
        if "static" in self.config:
            for route in self.config["static"]:
                self._birdconf.static.add_route(route)

    def _config_export_kernel(self):
        """Configure export_kernel section."""

        # Check if we're exporting routes from the master tables to the kernel tables
        if "export_kernel" in self.config:
            # Loop with export_kernel items
            for export, export_config in self.config["export_kernel"].items():
                # Static routes
                if export == "static":
                    self._birdconf.master.export_kernel_static = export_config
                # RIP routes
                elif export == "rip":
                    self._birdconf.master.export_kernel_rip = export_config
                # OSPF routes
                elif export == "ospf":
                    self._birdconf.master.export_kernel_ospf = export_config
                # BGP routes
                elif export == "bgp":
                    self._birdconf.master.export_kernel_bgp = export_config
                # If we don't understand this 'accept' entry, throw an error
                else:
                    raise BirdPlanError(f"Configuration item '{export}' not understood in 'export_kernel'")

    def _config_rip(self):
        """Configure rip section."""

        # If we have no rip section, just return
        if "rip" not in self.config:
            return

        # Check configuration options are supported
        for config_item in self.config["rip"]:
            if config_item not in ["accept", "redistribute", "interfaces"]:
                raise BirdPlanError(f"The 'rip' config item '{config_item}' is not supported")

        self._config_rip_accept()
        self._config_rip_redistribute()
        self._config_rip_interfaces()

    def _config_rip_accept(self):
        """Configure rip:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in self.config["rip"]:
            return

        # Loop with accept items
        for accept, accept_config in self.config["rip"]["accept"].items():
            # Allow accept of the default route
            if accept == "default":
                self._birdconf.rip.accept_default = accept_config
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{accept}' not understood in RIP accept")

    def _config_rip_redistribute(self):
        """Configure rip:redistribute section."""

        # If we don't have a redistribute section just return
        if "redistribute" not in self.config["rip"]:
            return

        # Loop with redistribution items
        for redistribute, redistribute_config in self.config["rip"]["redistribute"].items():
            # Add connected route redistribution
            if redistribute == "connected":
                self._birdconf.rip.redistribute_connected = redistribute_config
            # Add static route redistribution
            elif redistribute == "static":
                self._birdconf.rip.redistribute_static = redistribute_config
            # Add kernel route redistribution
            elif redistribute == "kernel":
                self._birdconf.rip.redistribute_kernel = redistribute_config
            # Allow redistribution of the default route
            elif redistribute == "default":
                self._birdconf.rip.redistribute_default = redistribute_config
            # Allow redistribution of RIP routes
            elif redistribute == "rip":
                self._birdconf.rip.redistribute_rip = redistribute_config
            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{redistribute}' not understood in rip:redistribute")

    def _config_rip_interfaces(self):
        """Configure rip:interfaces section."""

        # If we don't have interfaces in our rip section, just return
        if "interfaces" not in self.config["rip"]:
            return

        # Loop with each interface and its config
        for interface_name, interface in self.config["rip"]["interfaces"].items():
            # See if we have interface config
            interface_config = []
            # Loop with each config item in the peer
            for config_item, config_value in interface.items():
                if config_item in ("update-time", "metric"):
                    interface_config.append({config_item: config_value})
                # If we don't understand this 'redistribute' entry, throw an error
                else:
                    raise BirdPlanError(f"Configuration item '{config_item}' not understood in RIP area")
            # Add interface
            self._birdconf.rip.add_interface(interface_name, interface_config)

    def _config_ospf(self):
        """Configure OSPF section."""

        # If we have no ospf section, just return
        if "ospf" not in self.config:
            return

        # Check configuration options are supported
        for config_item in self.config["ospf"]:
            if config_item not in ["accept", "redistribute", "areas"]:
                raise BirdPlanError(f"The 'ospf' config item '{config_item}' is not supported")

        self._config_ospf_accept()
        self._config_ospf_redistribute()
        self._config_ospf_areas()

    def _config_ospf_accept(self):
        """Configure ospf:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in self.config["ospf"]:
            return

        # Loop with accept items
        for accept, accept_config in self.config["ospf"]["accept"].items():
            # Allow accept of the default route
            if accept == "default":
                self._birdconf.ospf.accept_default = accept_config
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{accept}' not understood in ospf:accept")

    def _config_ospf_redistribute(self):
        """Configure ospf:redistribute section."""

        # If we don't have a redistribute section just return
        if "redistribute" not in self.config["ospf"]:
            return

        # Loop with redistribution items
        for redistribute, redistribute_config in self.config["ospf"]["redistribute"].items():
            # Add static route redistribution
            if redistribute == "static":
                self._birdconf.ospf.redistribute_static = redistribute_config
            # Add kernel route redistribution
            elif redistribute == "kernel":
                self._birdconf.ospf.redistribute_kernel = redistribute_config
            # Allow redistribution of the default route
            elif redistribute == "default":
                self._birdconf.ospf.redistribute_default = redistribute_config
            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanError(f"Configuration item '{redistribute}' not understood in ospf:redistribute")

    def _config_ospf_areas(self):
        """Configure ospf:interfaces section."""

        # If we don't have areas in our ospf section, just return
        if "areas" not in self.config["ospf"]:
            return

        # Loop with each area and its config
        for area_name, area in self.config["ospf"]["areas"].items():
            # Make sure we have an interface for the area
            if "interfaces" not in area:
                raise BirdPlanError(f"OSPF area '{area_name}' must contain 'interfaces'")
            # Loop with each config item
            for config_item, config_value in area.items():
                # Make sure this item is supported
                if config_item not in ("config", "interfaces"):
                    raise BirdPlanError(
                        f"Configuration item '{config_item}' with value '{config_value}' not understood in ospf:areas"
                    )
            # See if we have area config
            area_config = {}
            if "config" in area:
                # Loop with each config item in the peer
                for config_item, config_value in area["config"].iteritems():
                    # No items supported atm
                    if config_item in ("xxxxx", "yyyy"):
                        area_config[config_item] = config_value
                    # If we don't understand this 'redistribute' entry, throw an error
                    else:
                        raise BirdPlanError("Configuration item '{config_item}' not understood in OSPF area")
            # Add area
            self._birdconf.ospf.add_area(area_name, area_config)
            # Loop with interfaces in area
            for interface_name, interface_config in area["interfaces"].items():
                # Add interface to area
                self._birdconf.ospf.add_interface(area_name, interface_name, interface_config)

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
