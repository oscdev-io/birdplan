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

"""BIRD OSPF configuration parser."""

from typing import Any

from .....exceptions import BirdPlanConfigError
from .... import BirdConfig
from ....config_parser import ConfigParser

__all__ = ["OSPFConfigParser"]


class OSPFConfigParser(ConfigParser):
    """OSPF configuration parser."""

    _birdconf: BirdConfig

    def parse(self, config: dict[str, Any]) -> None:
        """Configure OSPF protocol."""

        self._config_ospf(config)

    def _config_ospf(self, config: dict[str, Any]) -> None:
        """Configure OSPF section."""

        # If we have no ospf section, just return
        if "ospf" not in config:
            return

        # Check configuration options are supported
        for config_item in config["ospf"]:
            if config_item not in ("accept", "redistribute", "areas", "v4version"):
                raise BirdPlanConfigError(f"The 'ospf' config item '{config_item}' is not supported")

        # Check what version of OSPF we're using for IPv4
        if "v4version" in config["ospf"]:
            if isinstance(config["ospf"]["v4version"], int | str):
                v4version = f"{config['ospf']['v4version']}"
                if v4version in ("2", "3"):
                    self.birdconf.protocols.ospf.v4version = v4version
                else:
                    raise BirdPlanConfigError("The 'ospf' config item 'v4version' has unsupported value")
            else:
                raise BirdPlanConfigError("The 'ospf' config item 'v4version' has unsupported type")

        self._config_ospf_accept(config)
        self._config_ospf_redistribute(config)
        self._config_ospf_areas(config)

    def _config_ospf_accept(self, config: dict[str, Any]) -> None:
        """Configure ospf:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in config["ospf"]:
            return

        # Loop with accept items
        for accept, accept_config in config["ospf"]["accept"].items():
            # Allow accept of the default route
            if accept == "default":
                self.birdconf.protocols.ospf.route_policy_accept.default = accept_config
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanConfigError(f"Configuration item '{accept}' not understood in ospf:accept")

    def _config_ospf_redistribute(self, config: dict[str, Any]) -> None:  # noqa: C901,PLR0912
        """Configure ospf:redistribute section."""

        # If we don't have a redistribute section just return
        if "redistribute" not in config["ospf"]:
            return

        # Loop with redistribution items
        for redistribute, redistribute_config in config["ospf"]["redistribute"].items():
            # Add static route redistribution
            if redistribute == "static":
                self.birdconf.protocols.ospf.route_policy_redistribute.static = redistribute_config
            # Add connected route redistribution
            elif redistribute == "connected":
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
                            f"Configurion item '{redistribute}' has no 'interfaces' option in ospf:redistribute"
                        )
                    # If it does, check that it is a list
                    if not isinstance(redistribute_config["interfaces"], list):
                        raise BirdPlanConfigError(
                            f"Configurion item '{redistribute}:interfaces' has an invalid type in ospf:redistribute"
                        )
                    # Set redistribute_connected as the interface list
                    redistribute_connected = redistribute_config["interfaces"]
                else:
                    raise BirdPlanConfigError(f"Configurion item '{redistribute}' has an unsupported value")
                # Add configuration
                self.birdconf.protocols.ospf.route_policy_redistribute.connected = redistribute_connected
            # Add kernel route redistribution
            elif redistribute == "kernel":
                self.birdconf.protocols.ospf.route_policy_redistribute.kernel = redistribute_config
            # Add kernel default route redistribution
            elif redistribute == "kernel_default":
                self.birdconf.protocols.ospf.route_policy_redistribute.kernel_default = redistribute_config
            # Add static route redistribution
            elif redistribute == "static":
                self.birdconf.protocols.ospf.route_policy_redistribute.static = redistribute_config
            # Add static default route redistribution
            elif redistribute == "static_default":
                self.birdconf.protocols.ospf.route_policy_redistribute.static_default = redistribute_config
            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanConfigError(f"Configuration item '{redistribute}' not understood in ospf:redistribute")

    def _config_ospf_areas(self, config: dict[str, Any]) -> None:  # noqa: C901,PLR0912
        """Configure ospf:interfaces section."""

        # If we don't have areas in our ospf section, just return
        if "areas" not in config["ospf"]:
            return

        # Loop with each area and its config
        for area_name, raw_area_config in config["ospf"]["areas"].items():
            # Make sure we have an interface for the area
            if "interfaces" not in raw_area_config:
                raise BirdPlanConfigError(f"OSPF area '{area_name}' must contain 'interfaces'")
            # Loop with each config item
            area_config = {}
            for config_item, raw_config in raw_area_config.items():
                # Make sure this item is supported
                if config_item not in ("xxxxxxx", "interfaces"):
                    raise BirdPlanConfigError(
                        f"Configuration item '{config_item}' with value '{raw_config}' not understood in ospf:areas"
                    )
                # Skip over interfaces
                if config_item == "interfaces":
                    continue
                # Check for supported config options
                if config_item in ("xxxxx", "yyyy"):
                    area_config[config_item] = raw_config
                # If we don't understand this 'redistribute' entry, throw an error
                else:
                    raise BirdPlanConfigError(f"Configuration item '{config_item}' not understood in ospf:areas")

            # Add area
            area = self.birdconf.protocols.ospf.add_area(area_name, area_config)

            # Loop with interfaces in area
            for interface_name, raw_config in raw_area_config["interfaces"].items():
                # Start with no special interface configuration
                interface_config: dict[str, Any] = {}
                # Check what kind of config we've got...
                add_ospf_interface = False
                if isinstance(raw_config, bool):
                    add_ospf_interface = raw_config
                # Else if its a dict, we need to treat it a bit differently
                elif isinstance(raw_config, dict):
                    add_ospf_interface = True
                    for raw_item, raw_value in raw_config.items():
                        if raw_item in ("cost", "ecmp_weight", "hello", "stub", "wait"):
                            interface_config[raw_item] = raw_value
                        else:
                            raise BirdPlanConfigError(
                                f"Configuration item '{raw_item}' not understood in OSPF interface '{interface_name}'"
                            )
                else:
                    raise BirdPlanConfigError(
                        f"Configurion for OSPF interface name '{interface_name}' has an unsupported type: '{type(interface_name)}'"
                    )

                # Add interface to area
                if add_ospf_interface:
                    area.add_interface(interface_name, interface_config)
