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

"""BIRD RIP configuration parser."""

from typing import Any

from .....exceptions import BirdPlanConfigError
from .... import BirdConfig
from ....config_parser import ConfigParser

__all__ = ["RIPConfigParser"]


class RIPConfigParser(ConfigParser):
    """RIP configuration parser."""

    _birdconf: BirdConfig

    def parse(self, config: dict[str, Any]) -> None:
        """Configure RIP protocol."""

        self._config_rip(config)

    def _config_rip(self, config: dict[str, Any]) -> None:
        """Configure rip section."""

        # If we have no rip section, just return
        if "rip" not in config:
            return

        # Check configuration options are supported
        for config_item in config["rip"]:
            if config_item not in ("accept", "redistribute", "interfaces"):
                raise BirdPlanConfigError(f"The 'rip' config item '{config_item}' is not supported")

        self._config_rip_accept(config)
        self._config_rip_redistribute(config)
        self._config_rip_interfaces(config)

    def _config_rip_accept(self, config: dict[str, Any]) -> None:
        """Configure rip:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in config["rip"]:
            return

        # Loop with accept items
        for accept, accept_config in config["rip"]["accept"].items():
            # Allow accept of the default route
            if accept == "default":
                self.birdconf.protocols.rip.route_policy_accept.default = accept_config
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanConfigError(f"Configuration item '{accept}' not understood in RIP accept")

    def _config_rip_redistribute(self, config: dict[str, Any]) -> None:  # noqa: C901,PLR0912
        """Configure rip:redistribute section."""

        # If we don't have a redistribute section just return
        if "redistribute" not in config["rip"]:
            return

        # Loop with redistribution items
        for redistribute, redistribute_config in config["rip"]["redistribute"].items():
            # Add connected route redistribution
            if redistribute == "connected":
                # Set type
                redistribute_connected: bool | list[str]
                # Check what kind of config we go...
                if isinstance(redistribute_config, bool):
                    redistribute_connected = redistribute_config
                # Else if its a dict, we need to treat it a bit differently
                elif isinstance(redistribute_config, dict):
                    # Check it has an "interfaces" key
                    if "interfaces" not in redistribute_config:
                        raise BirdPlanConfigError(
                            f"Configurion item '{redistribute}' has no 'interfaces' option in rip:redistribute"
                        )
                    # If it does, check that it is a list
                    if not isinstance(redistribute_config["interfaces"], list):
                        raise BirdPlanConfigError(
                            f"Configurion item '{redistribute}:interfaces' has an invalid type in rip:redistribute"
                        )
                    # Set redistribute_connected as the interface list
                    redistribute_connected = redistribute_config["interfaces"]
                else:
                    raise BirdPlanConfigError(f"Configurion item '{redistribute}' has an unsupported value")
                # Add configuration
                self.birdconf.protocols.rip.route_policy_redistribute.connected = redistribute_connected
            # Add kernel route redistribution
            elif redistribute == "kernel":
                self.birdconf.protocols.rip.route_policy_redistribute.kernel = redistribute_config
            # Add kernel default route redistribution
            elif redistribute == "kernel_default":
                self.birdconf.protocols.rip.route_policy_redistribute.kernel_default = redistribute_config
            # Allow redistribution of RIP routes
            elif redistribute == "rip":
                self.birdconf.protocols.rip.route_policy_redistribute.rip = redistribute_config
            # Allow redistribution of RIP default routes
            elif redistribute == "rip_default":
                self.birdconf.protocols.rip.route_policy_redistribute.rip_default = redistribute_config
            # Add static route redistribution
            elif redistribute == "static":
                self.birdconf.protocols.rip.route_policy_redistribute.static = redistribute_config
            # Add static default route redistribution
            elif redistribute == "static_default":
                self.birdconf.protocols.rip.route_policy_redistribute.static_default = redistribute_config
            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanConfigError(f"Configuration item '{redistribute}' not understood in rip:redistribute")

    def _config_rip_interfaces(self, config: dict[str, Any]) -> None:
        """Configure rip:interfaces section."""

        # If we don't have interfaces in our rip section, just return
        if "interfaces" not in config["rip"]:
            return

        # Loop with each interface and its config
        for interface_name, interface in config["rip"]["interfaces"].items():
            # See if we have interface config
            interface_config = {}
            # Loop with each config item in the peer
            for config_item, config_value in interface.items():
                if config_item in ("update-time", "metric"):
                    interface_config[config_item] = config_value
                # If we don't understand this 'redistribute' entry, throw an error
                else:
                    raise BirdPlanConfigError(f"Configuration item '{config_item}' not understood in RIP area")
            # Add interface
            self.birdconf.protocols.rip.add_interface(interface_name, interface_config)
