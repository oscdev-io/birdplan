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

"""BIRD constants configuration."""

from ..globals import BirdConfigGlobals
from .base import SectionBase

__all__ = ["SectionConstants"]


class SectionConstants(SectionBase):
    """BIRD constants configuration."""

    _need_bogons: bool

    def __init__(self, birdconfig_globals: BirdConfigGlobals) -> None:
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        # Set section header
        self._section = "Global Constants"

        # Add bogon constants to output
        self._need_bogons = False

    def configure(self) -> None:
        """Configure global constants."""
        super().configure()

        # Check if we're in debug mode or not
        if self.birdconfig_globals.debug:
            self.conf.add("# We're in DEBUG mode")
            self.conf.add("define DEBUG = true;")
        else:
            self.conf.add("# We're not in DEBUG mode")
            self.conf.add("define DEBUG = false;")

        self._configure_defaults()
        # Check if we're adding bogons constants
        if self.need_bogons:
            self._configure_bogons_ipv4()
            self._configure_bogons_ipv6()

    def _configure_defaults(self) -> None:
        """Configure default routes."""
        self.conf.add("# Default routes")
        self.conf.add("define DEFAULT_ROUTE_V4 = 0.0.0.0/0; # IPv4 default route")
        self.conf.add("define DEFAULT_ROUTE_V6 = ::/0; # IPv6 default route")
        self.conf.add("")

    def _configure_bogons_ipv4(self) -> None:
        """Configure IPv4 bogons."""
        self.conf.add("# As per http://bgpfilterguide.nlnog.net/guides/bogon_prefixes/")
        self.conf.add("define BOGONS_V4 = [")
        self.conf.add("  0.0.0.0/8+, # RFC 1122 'this' network")
        self.conf.add("  10.0.0.0/8+, # RFC 1918 private space")
        if self.birdconfig_globals.test_mode:
            self.conf.add("  # EXCLUDING DUE TO TESTING: 100.64.0.0/10+, # RFC 6598 Carrier grade nat space")
        else:
            self.conf.add("  100.64.0.0/10+, # RFC 6598 Carrier grade nat space")
        self.conf.add("  127.0.0.0/8+, # RFC 1122 localhost")
        self.conf.add("  169.254.0.0/16+, # RFC 3927 link local")
        self.conf.add("  172.16.0.0/12+, # RFC 1918 private space")
        self.conf.add("  192.0.2.0/24+, # RFC 5737 TEST-NET-1")
        self.conf.add("  192.88.99.0/24+, # RFC 7526 6to4 anycast relay")
        self.conf.add("  192.168.0.0/16+, # RFC 1918 private space")
        self.conf.add("  198.18.0.0/15+, # RFC 2544 benchmarking")
        self.conf.add("  198.51.100.0/24+, # RFC 5737 TEST-NET-2")
        self.conf.add("  203.0.113.0/24+, # RFC 5737 TEST-NET-3")
        self.conf.add("  224.0.0.0/4+, # multicast")
        self.conf.add("  240.0.0.0/4+ # reserved")
        self.conf.add("];")
        self.conf.add("")

    def _configure_bogons_ipv6(self) -> None:
        """Configure IPv6 bogons."""
        self.conf.add("# As per http://bgpfilterguide.nlnog.net/guides/bogon_prefixes/")
        self.conf.add("define BOGONS_V6 = [")
        self.conf.add("  ::/8+, # RFC 4291 IPv4-compatible, loopback, et al")
        self.conf.add("  0100::/64+, # RFC 6666 Discard-Only")
        self.conf.add("  2001:2::/48+, # RFC 5180 BMWG")
        self.conf.add("  2001:10::/28+, # RFC 4843 ORCHID")
        self.conf.add("  2001:db8::/32+, # RFC 3849 documentation")
        self.conf.add("  2002::/16+, # RFC 7526 6to4 anycast relay")
        self.conf.add("  3ffe::/16+, # RFC 3701 old 6bone")
        if self.birdconfig_globals.test_mode:
            self.conf.add("  # EXCLUDING DUE TO TESTING: fc00::/7+, # RFC 4193 unique local unicast")
        else:
            self.conf.add("  fc00::/7+, # RFC 4193 unique local unicast")
        self.conf.add("  fe80::/10+, # RFC 4291 link local unicast")
        self.conf.add("  fec0::/10+, # RFC 3879 old site local unicast")
        self.conf.add("  ff00::/8+ # RFC 4291 multicast")
        self.conf.add("];")
        self.conf.add("")

    @property
    def need_bogons(self) -> bool:
        """Return if we need bogons or not."""
        return self._need_bogons

    @need_bogons.setter
    def need_bogons(self, need_bogons: bool) -> None:
        """Add bogons to our output."""
        self._need_bogons = need_bogons
