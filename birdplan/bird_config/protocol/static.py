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

"""BIRD static protocol configuration."""

from ..base import BirdConfigBase
from .pipe import BirdConfigProtocolPipe
from ...exceptions import BirdPlanError


class BirdConfigProtocolStatic(BirdConfigBase):
    """BIRD static protocol configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Initialize our route list
        self._static_routes = {}

    def add_route(self, route):
        """Add static route."""
        (prefix, route_info) = route.split(" ", 1)
        self._static_routes[prefix] = route_info

    def configure(self):
        """Configure the static protocol."""
        # Work out static v4 and v6 routes
        routes_ipv4 = []
        routes_ipv6 = []
        for prefix in sorted(self.static_routes.keys()):
            info = self.static_routes[prefix]
            if "." in prefix:
                routes_ipv4.append(f"{prefix} {info}")
            elif ":" in prefix:
                routes_ipv6.append(f"{prefix} {info}")
            else:
                raise BirdPlanError(f"The static route '{prefix}' is odd")

        self._addtitle("Static Protocol")

        self._addline("ipv4 table t_static4;")
        self._addline("ipv6 table t_static6;")
        self._addline("")
        self._addline("protocol static static4 {")
        self._addline('  description "Static protocol for IPv4";')
        self._addline("")
        # FIXME - remove at some stage # pylint:disable=fixme
        self._addline("debug all;")
        self._addline("")
        self._addline("  ipv4 {")
        self._addline("    table t_static4;")
        self._addline("    export none;")
        self._addline("    import all;")
        self._addline("  };")
        # If we have IPv4 routes
        if routes_ipv4:
            self._addline("")
            # Output the routes
            for route in routes_ipv4:
                self._addline(f"  route {route};")
        self._addline("};")
        self._addline("")
        self._addline("protocol static static6 {")
        self._addline('  description "Static protocol for IPv6";')
        self._addline("")
        self._addline("  ipv6 {")
        self._addline("    table t_static6;")
        self._addline("    export none;")
        self._addline("    import all;")
        self._addline("  };")
        # If we have IPv6 routes
        if routes_ipv6:
            self._addline("")
            # Output the routes
            for route in routes_ipv6:
                self._addline(f"  route {route};")
        self._addline("};")
        self._addline("")

        # Configure static route pipe to the kernel
        static_kernel_pipe = BirdConfigProtocolPipe(
            self, table_from="static", table_to="master", table_export="all", table_import="none"
        )
        static_kernel_pipe.configure()

    @property
    def static_routes(self):
        """Return our static routes."""
        return self._static_routes
