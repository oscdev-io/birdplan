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

    def _generate_originated_routes(self, next_hop4: str = "blackhole", next_hop6: str = "blackhole"):
        """Generate the routes we expect to see in BIRD."""
        originated_str = """
  originate:
"""
        # Grab lists of communities
        communities = [x for x in self.e1_template_communities.replace(":", ",").split(" ") if x]
        large_communities = [x for x in self.e1_template_large_communities.replace(":", ",").split(" ") if x]

        # Set our originated routes as ORIGINATED_OWN
        large_communities.append("65000,3,1")

        # Work out list of communities to add
        communities_list = []
        if communities:
            communities_list.extend([f"bgp_community.add(({community}));" for community in communities])
        if large_communities:
            communities_list.extend([f"bgp_large_community.add(({large_community}));" for large_community in large_communities])

        # Build string of communities
        communities_str = ""
        if communities_list:
            communities_str += "{"
            communities_str += " ".join(communities_list)
            communities_str += "}"

        # Loop with prefix lengths
        for prefix_length in self.test_prefix_lengths4:
            originated_str += f"    - '10.0.0.0/{prefix_length} {next_hop4} {communities_str}'\n"
        for prefix_length in self.test_prefix_lengths6:
            originated_str += f"    - 'fd00::/{prefix_length} {next_hop6} {communities_str}'\n"

        return originated_str

    def _test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""

        # Loop with IPv4 prefix lengths and advertise each one
        for prefix_length in self.test_prefix_lengths4:
            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor 100.64.0.1 announce route 100.0.0.0/{prefix_length} next-hop 100.64.0.100 "
                    f"large-community [ 65000:3:1 {self.e1_template_large_communities} ] "
                    f"community [ {self.e1_template_communities} ]"
                ],
            )

        # Loop with IPv6 prefix lengths and advertise each one
        for prefix_length in self.test_prefix_lengths6:
            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor fc00:100::1 announce route fc00::/{prefix_length} next-hop fc00:100::100 "
                    f"large-community [ 65000:3:1 {self.e1_template_large_communities} ] "
                    f"community [ {self.e1_template_communities} ]"
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
