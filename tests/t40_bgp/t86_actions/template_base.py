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

# type: ignore
# pylint: disable=import-error,too-few-public-methods

"""BGP outbound filtering functions test case template (base class for specific tests)."""

from ...basetests import BirdPlanBaseTestCase

__all__ = ["TemplateBase"]


class TemplateBase(BirdPlanBaseTestCase):
    """BGP outbound filtering functions test case template (base class for specific tests)."""

    routers = ["r1", "r2"]

    exabgps = ["e1"]
    e1_asn = 65000
    e1_interface_eth0 = {"mac": "02:e1:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}

    template_macros = [
        "extra_r2_config",
        "extra_e1_config",
    ]

    r1_extra_r2_config = ""
    r1_global_config = """
  rr_cluster_id: 0.0.0.1
"""

    # Communities to inject into the prefix we're advertising
    e1_template_large_communities = ""
    e1_template_communities = ""

    # Prefix lenghts to test
    test_prefix_lengths4 = []
    test_prefix_lengths6 = []

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""
        self._test_announce_routes(sim)

    def _test_announce_routes(self, sim):
        """Announce a BGP prefix with a differnt origin."""

        # Add large communities for peer types that require them
        large_communities = ""

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.100 "
                f"large-community [65000:3:1 {large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::100 "
                f"large-community [65000:3:1 {large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.111.0/24 next-hop 100.64.0.100 as-path [ 65100 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:111::/48 next-hop fc00:100::100 as-path [ 65100 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.121.0/24 next-hop 100.64.0.100 as-path [ 65200 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:121::/48 next-hop fc00:100::100 as-path [ 65200 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )

    def test_bird_cmdline_bgp_peer_summary(self, sim, tmpdir):
        """Test showing BGP peer summary."""
        self._test_bird_cmdline_bgp_peer_summary(sim, tmpdir)

    def test_bird_cmdline_bgp_peer_show(self, sim, tmpdir):
        """Test showing BGP peer."""
        self._test_bird_cmdline_bgp_peer_show(sim, tmpdir)

    def test_bird_tables_bgp4_peer(self, sim):
        """Test BIRD BGP4 peer table."""
        self._test_bird_routers_table_bgp_peers(sim, 4)

    def test_bird_tables_bgp6_peer(self, sim):
        """Test BIRD BGP6 peer table."""
        self._test_bird_routers_table_bgp_peers(sim, 6)

    def test_bird_tables_bgp4(self, sim):
        """Test BIRD t_bgp4 table."""
        self._test_bird_routers_table(sim, "t_bgp4")

    def test_bird_tables_bgp6(self, sim):
        """Test BIRD t_bgp6 table."""
        self._test_bird_routers_table(sim, "t_bgp6")
