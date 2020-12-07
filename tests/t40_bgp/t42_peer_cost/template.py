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

"""BGP peer cost test template."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """BGP peer cost test template."""

    routers = ["r1"]
    exabgps = ["e1"]

    r1_template_peer_config = """
      cost: 5
"""

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type") in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        self._exabgpcli(
            sim,
            "e1",
            [f"neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.2 large-community [{large_communities}]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            [f"neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::2 large-community [{large_communities}]"],
        )

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

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
