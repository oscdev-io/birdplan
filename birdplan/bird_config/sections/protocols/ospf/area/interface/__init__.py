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

"""BIRD OSPF area interface configuration."""

# pylint: disable=too-many-lines

import fnmatch
from typing import Optional

from ......globals import BirdConfigGlobals
from .....bird_attributes import SectionBirdAttributes
from .....constants import SectionConstants
from .....functions import SectionFunctions
from .....tables import SectionTables
from ....base import SectionProtocolBase
from ..area_attributes import OSPFAreaAttributes
from .interface_attributes import OSPFAreaInterfaceAttributes
from .ospf_area_interface_types import OSPFAreaInterfaceConfig

__all__ = ["ProtocolOSPFAreaInterface"]


class ProtocolOSPFAreaInterface(SectionProtocolBase):  # pylint: disable=too-many-public-methods,too-many-instance-attributes
    """BIRD OSPF area interface configuration."""

    # OSPF area attributes
    _area_attributes: OSPFAreaAttributes

    # OSPF area interface attributes
    _interface_attributes: OSPFAreaInterfaceAttributes

    def __init__(  # noqa: CFQ002 # pylint: disable=too-many-arguments,too-many-branches,too-many-positional-arguments
        self,
        birdconfig_globals: BirdConfigGlobals,
        birdattributes: SectionBirdAttributes,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
        area_attributes: OSPFAreaAttributes,
        interface_name: str,
        interface_config: OSPFAreaInterfaceConfig,
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals, birdattributes, constants, functions, tables)

        # Setup the OSPF area attributes
        self._area_attributes = area_attributes

        # Setup OSPF area interface attributes
        self._interface_attributes = OSPFAreaInterfaceAttributes()

        # Set our interface name
        self.name = interface_name

        # Check if we have a interface cost
        if "cost" in interface_config:
            self.cost = interface_config["cost"]

        # Check if we have an interface ECMP weight
        if "ecmp_weight" in interface_config:
            self.ecmp_weight = interface_config["ecmp_weight"]

        # Check if we have a interface hello
        if "hello" in interface_config:
            self.hello = interface_config["hello"]

        # Check if we have a interface wait
        if "wait" in interface_config:
            self.wait = interface_config["wait"]

        # Check if this interface is a stub
        if "stub" in interface_config:
            self.stub = interface_config["stub"]

        # Check if we have a interface setting overrides
        if (
            "ospf" in self.birdconfig_globals.state
            and "areas" in self.birdconfig_globals.state["ospf"]
            and self.area_attributes.name in self.birdconfig_globals.state["ospf"]["areas"]
            and "+interfaces" in self.birdconfig_globals.state["ospf"]["areas"][self.area_attributes.name]
        ):
            # Make things easier below
            interface_overrides = self.birdconfig_globals.state["ospf"]["areas"][self.area_attributes.name]["+interfaces"]

            # Check if this interface is in the override structure
            if self.name in interface_overrides:
                # Check if we have a cost override
                if "cost" in interface_overrides[self.name]:
                    self.cost = interface_overrides[self.name]["cost"]
                # Check if we have an ecmp_weight override
                if "ecmp_weight" in interface_overrides[self.name]:
                    self.ecmp_weight = interface_overrides[self.name]["ecmp_weight"]
            # If not we process the patterns
            else:
                for item in sorted(interface_overrides):
                    # Skip non patterns
                    if "*" not in item:
                        continue
                    # If pattern matches peer name, set the value for quarantine
                    if fnmatch.fnmatch(self.name, item):
                        if "cost" in interface_overrides[item]:
                            self.cost = interface_overrides[item]["cost"]
                        if "ecmp_weight" in interface_overrides[item]:
                            self.ecmp_weight = interface_overrides[item]["ecmp_weight"]

    def configure(self) -> None:
        """Configure the OSPF interface."""

        # Don't re-render the configuration, we're called twice for v4 and V6
        if self.conf.items:
            return

        super().configure()

        # Blank the OSPF area interface state
        area_interfaces_state = self.birdconfig_globals.state["ospf"]["areas"][self.area_attributes.name]["interfaces"]
        if self.name not in area_interfaces_state:
            area_interfaces_state[self.name] = {}

        # Setup our state
        interface_state = area_interfaces_state[self.name]
        interface_state["cost"] = self.cost
        interface_state["ecmp_weight"] = self.ecmp_weight

        # Start interface block
        self.conf.add(f'    interface "{self.name}" {{')
        # Check if we have a cost
        if self.cost:
            self.conf.add(f"      cost {self.cost};")
        # Check if we have a ecmp_weight
        if self.ecmp_weight:
            self.conf.add(f"      ecmp weight {self.ecmp_weight};")
        # Check if we have a hello
        if self.hello:
            self.conf.add(f"      hello {self.hello};")
        # Check if we have a wait
        if self.wait:
            self.conf.add(f"      wait {self.wait};")
        # Check our stub option
        if self.is_stub:
            self.conf.add("      stub;")
        # Close off interface block
        self.conf.add("    };")

    @property
    def is_stub(self) -> bool:
        """Return if interface is a stub."""
        return self.stub

    @property
    def area_attributes(self) -> OSPFAreaAttributes:
        """OSPF area attributes."""
        return self._area_attributes

    @property
    def interface_attributes(self) -> OSPFAreaInterfaceAttributes:
        """OSPF area interface attributes."""
        return self._interface_attributes

    @property
    def name(self) -> str:
        """Interface name."""
        return self.interface_attributes.name

    @name.setter
    def name(self, name: str) -> None:
        """Interface name."""
        self.interface_attributes.name = name

    @property
    def cost(self) -> int:
        """Interface cost."""
        return self.interface_attributes.cost

    @cost.setter
    def cost(self, cost: int) -> None:
        """Interface cost."""
        self.interface_attributes.cost = cost

    @property
    def ecmp_weight(self) -> Optional[int]:
        """Interface ECMP weight."""
        return self.interface_attributes.ecmp_weight

    @ecmp_weight.setter
    def ecmp_weight(self, ecmp_weight: int) -> None:
        """Interface ECMP weight."""
        self.interface_attributes.ecmp_weight = ecmp_weight

    @property
    def hello(self) -> Optional[int]:
        """Interface hello."""
        return self.interface_attributes.hello

    @hello.setter
    def hello(self, hello: int) -> None:
        """Interface hello."""
        self.interface_attributes.hello = hello

    @property
    def wait(self) -> Optional[int]:
        """Interface wait."""
        return self.interface_attributes.wait

    @wait.setter
    def wait(self, wait: int) -> None:
        """Interface wait."""
        self.interface_attributes.wait = wait

    @property
    def stub(self) -> bool:
        """Interface is a stub."""
        return self.interface_attributes.stub

    @stub.setter
    def stub(self, stub: bool) -> None:
        """Interface is a stub."""
        self.interface_attributes.stub = stub
