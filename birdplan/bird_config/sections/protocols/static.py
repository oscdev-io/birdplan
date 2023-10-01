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

"""BIRD static protocol configuration."""

from typing import Dict

from ....exceptions import BirdPlanError
from ...globals import BirdConfigGlobals
from ..constants import SectionConstants
from ..functions import SectionFunctions
from ..tables import SectionTables
from .base import SectionProtocolBase
from .pipe import ProtocolPipe

StaticRoutes = Dict[str, str]


class ProtocolStatic(SectionProtocolBase):
    """BIRD static protocol configuration."""

    _routes: StaticRoutes

    def __init__(
        self, birdconfig_globals: BirdConfigGlobals, constants: SectionConstants, functions: SectionFunctions, tables: SectionTables
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals, constants, functions, tables)

        # Set section header
        self._section = "Static Protocol"

        # Initialize our route list
        self._routes = {}

    def add_route(self, route: str) -> None:
        """Add static route."""
        (prefix, route_info) = route.split(" ", 1)
        self.routes[prefix] = route_info

    def configure(self) -> None:
        """Configure the static protocol."""
        super().configure()

        # Work out static v4 and v6 routes
        routes_ipv4 = []
        routes_ipv6 = []
        for prefix in sorted(self.routes.keys()):
            info = self.routes[prefix]
            if "." in prefix:
                routes_ipv4.append(f"{prefix} {info}")
            elif ":" in prefix:
                routes_ipv6.append(f"{prefix} {info}")
            else:
                raise BirdPlanError(f"The static route '{prefix}' is odd")

        self.tables.conf.append("# Static Protocol")
        self.tables.conf.append("ipv4 table t_static4;")
        self.tables.conf.append("ipv6 table t_static6;")
        self.tables.conf.append("")

        self.conf.add("protocol static static4 {")
        self.conf.add('  description "Static protocol for IPv4";')
        self.conf.add("")
        # FIXME - remove at some stage # pylint:disable=fixme
        self.conf.add("debug all;")
        self.conf.add("")
        self.conf.add("  ipv4 {")
        self.conf.add("    table t_static4;")
        self.conf.add("    export none;")
        self.conf.add("    import all;")
        self.conf.add("  };")
        # If we have IPv4 routes
        if routes_ipv4:
            self.conf.add("")
            # Output the routes
            for route in routes_ipv4:
                self.conf.add(f"  route {route};")
        self.conf.add("};")
        self.conf.add("")
        self.conf.add("protocol static static6 {")
        self.conf.add('  description "Static protocol for IPv6";')
        self.conf.add("")
        self.conf.add("  ipv6 {")
        self.conf.add("    table t_static6;")
        self.conf.add("    export none;")
        self.conf.add("    import all;")
        self.conf.add("  };")
        # If we have IPv6 routes
        if routes_ipv6:
            self.conf.add("")
            # Output the routes
            for route in routes_ipv6:
                self.conf.add(f"  route {route};")
        self.conf.add("};")
        self.conf.add("")

        # Configure static route pipe to the kernel
        static_kernel_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from="static",
            table_to="master",
            table_export="all",
            table_import="none",
        )
        self.conf.add(static_kernel_pipe)

    @property
    def routes(self) -> StaticRoutes:
        """Return our static routes."""
        return self._routes
