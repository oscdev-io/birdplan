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

"""BIRD OSPF area configuration."""

# pylint: disable=too-many-lines

from typing import Any

from ......exceptions import BirdPlanError
from .....globals import BirdConfigGlobals
from ....bird_attributes import SectionBirdAttributes
from ....constants import SectionConstants
from ....functions import SectionFunctions
from ....tables import SectionTables
from ...base import SectionProtocolBase
from ..ospf_attributes import OSPFAttributes
from .area_attributes import OSPFAreaAttributes
from .interface import ProtocolOSPFAreaInterface
from .ospf_area_types import OSPFAreaConfig

__all__ = ["ProtocolOSPFArea"]


OSPFAreaInterfaceConfig = dict[str, Any]
OSPFAreaInterfaces = dict[str, ProtocolOSPFAreaInterface]


class ProtocolOSPFArea(SectionProtocolBase):  # pylint: disable=too-many-public-methods
    """BIRD OSPF area configuration."""

    # OSPF attributes
    _ospf_attributes: OSPFAttributes

    # OSPF area attributes
    _area_attributes: OSPFAreaAttributes

    # OSPF interfaces belonging to this area
    _interfaces: OSPFAreaInterfaces

    def __init__(  # noqa: PLR0913
        self,
        birdconfig_globals: BirdConfigGlobals,
        birdattributes: SectionBirdAttributes,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
        ospf_attributes: OSPFAttributes,
        area_name: str,
        area_config: OSPFAreaConfig,
    ) -> None:
        """Initialize the object."""
        super().__init__(birdconfig_globals, birdattributes, constants, functions, tables)

        # Setup OSPF attributes
        self._ospf_attributes = ospf_attributes

        # Setup OSPF area attributes
        self._area_attributes = OSPFAreaAttributes()

        # Interfaces
        self._interfaces = {}

        # Set area name
        self.name = str(area_name)

        if area_config:
            raise BirdPlanError("THIS SHOULD NOT HAPPEN UNTIL WE HAVE AREA CONFIG")

    def configure(self) -> None:
        """Configure the OSPF area."""

        # Don't re-render the configuration, we're called twice for v4 and V6
        if self.conf.items:
            return

        super().configure()

        # Blank the OSPF area state
        if "ospf" not in self.birdconfig_globals.state:
            self.birdconfig_globals.state["ospf"] = {}
        if "areas" not in self.birdconfig_globals.state["ospf"]:
            self.birdconfig_globals.state["ospf"]["areas"] = {}
        if self.name not in self.birdconfig_globals.state["ospf"]["areas"]:
            self.birdconfig_globals.state["ospf"]["areas"][self.name] = {}
        if "interfaces" not in self.birdconfig_globals.state["ospf"]["areas"][self.name]:
            self.birdconfig_globals.state["ospf"]["areas"][self.name]["interfaces"] = {}

        # Add area config block
        self.conf.add(f"  area {self.name} {{")
        # Add interfaces
        for _, interface in sorted(self.interfaces.items()):
            self.conf.add(interface)
        # Close area config block
        self.conf.add("  };")

    def add_interface(self, interface_name: str, interface_config: OSPFAreaConfig) -> ProtocolOSPFAreaInterface:
        """Add interface to OSPF."""

        # Make sure area interface doesn't exist
        if interface_name in self.interfaces:
            raise BirdPlanError(f"OSPF area '{self.name}'' interface '{interface_name}' already exists")

        # Create OSPF area interface object
        interface = ProtocolOSPFAreaInterface(
            self.birdconfig_globals,
            self.birdattributes,
            self.constants,
            self.functions,
            self.tables,
            self.area_attributes,
            interface_name,
            interface_config,
        )

        # Add interface to the area
        self.interfaces[interface_name] = interface

        return interface

    @property
    def area_attributes(self) -> OSPFAreaAttributes:
        """OSPF area attributes."""
        return self._area_attributes

    @property
    def name(self) -> str:
        """Area name."""
        return self.area_attributes.name

    @name.setter
    def name(self, name: str) -> None:
        """Area name."""
        self.area_attributes.name = name

    @property
    def interfaces(self) -> OSPFAreaInterfaces:
        """OSPF area interfaces."""
        return self._interfaces
