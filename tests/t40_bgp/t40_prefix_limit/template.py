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

# type: ignore
# pylint: disable=import-error,too-few-public-methods,no-self-use

"""BGP prefix limit test template."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """BGP prefix limit test template."""

    routers = ["r1"]
    exabgps = ["e1"]

    r1_template_peer_config = """
      prefix_limit4: 5
      prefix_limit6: 5
"""

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""

        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.104.0/21 next-hop 100.64.0.2 split /24"],
        )
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:104::/45 next-hop fc00:100::2 split /48"],
        )

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_route_limit_exceeded(self, sim):
        """Check logs to see if we reached the prefix limit."""

        # Skip over configuration exceptions for this test
        if "r1" in self.routers_config_exception and self.routers_config_exception:
            return

        route_limit_exceeded = self._bird_log_matches(sim, "r1", r"bgp4_AS6500[01]_e1: Route limit exceeded, shutting down")
        assert route_limit_exceeded, "Failed to shut down IPv4 connection when route limit exceeded"

        route_limit_exceeded = self._bird_log_matches(sim, "r1", r"bgp6_AS6500[01]_e1: Route limit exceeded, shutting down")
        assert route_limit_exceeded, "Failed to shut down IPv6 connection when route limit exceeded"

    def test_bird_tables_bgp4_peer(self, sim):
        """Test BIRD BGP4 peer table."""
        self._test_bird_routers_table_bgp_peers(4, sim)

    def test_bird_tables_bgp6_peer(self, sim):
        """Test BIRD BGP6 peer table."""
        self._test_bird_routers_table_bgp_peers(6, sim)

    def test_bird_tables_bgp4(self, sim):
        """Test BIRD t_bgp4 table."""
        self._test_bird_routers_table("t_bgp4", sim)

    def test_bird_tables_bgp6(self, sim):
        """Test BIRD t_bgp6 table."""
        self._test_bird_routers_table("t_bgp6", sim)

    def test_bird_tables_master4(self, sim):
        """Test BIRD master4 table."""
        self._test_bird_routers_table("master4", sim)

    def test_bird_tables_master6(self, sim):
        """Test BIRD master6 table."""
        self._test_bird_routers_table("master6", sim)

    def test_bird_tables_kernel4(self, sim):
        """Test BIRD kernel4 table."""
        self._test_bird_routers_table("t_kernel4", sim)

    def test_bird_tables_kernel6(self, sim):
        """Test BIRD kernel6 table."""
        self._test_bird_routers_table("t_kernel6", sim)

    def test_os_rib_inet(self, sim):
        """Test OS RIB for inet."""
        self._test_os_rib("inet", sim)

    def test_os_rib_inet6(self, sim):
        """Test OS RIB for inet6."""
        self._test_os_rib("inet6", sim)
