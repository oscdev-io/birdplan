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

"""BGP filtering of too many communities."""

from typing import List, Tuple
import os
from basetests import BirdPlanBaseTestCase


class BGPFilteringTooManyCommunitiesBase(BirdPlanBaseTestCase):
    """Base class for BGP filtering of too many communities."""

    test_dir = os.path.dirname(__file__)
    exabgps = ["e1"]
    too_many_communities: List[Tuple[int, int]] = [(1, x) for x in range(51)]
    r1_global_config = """
  community_maxlen: 50
"""

    def test_setup(self, sim, tmpdir):
        """Set up our test."""
        self._test_setup(sim, tmpdir)

    def test_announce_routes(self, sim):
        """Announce a prefix that has a too many communities from ExaBGP to BIRD."""

        # Convert to a 1:x format separated by spaces for exabgp
        too_many_communities_str = " ".join([f"{x[0]}:{x[1]}" for x in self.too_many_communities])

        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.2 community [" + too_many_communities_str + "]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::2 community [" + too_many_communities_str + "]"],
        )

    def test_results(self, sim, helpers):
        """Test results from this peer type."""
        self._test_results(sim, helpers)

    def _test_results(self, sim, helpers):
        """Test-specific results from this peer type."""
        raise NotImplementedError

    def _get_tables(self, sim) -> Tuple:
        # Grab IPv4 table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)
        assert len(peer_bgp4_table) == 1, "Failed to announce IPv4 with too many communities"

        # Grab IPv6 table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)
        assert len(peer_bgp6_table) == 1, "Failed to announce IPv6 with too many communities"

        # Return our two routing tables
        return (peer_bgp4_table, peer_bgp6_table)


class TestCustomer(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'customer' peer type."""

    # BIRD configuration
    r1_peer_type = "customer"
    r1_extra_config = """
      filter:
        asns: [65001]
"""

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 2), (65000, 1101, 16)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 2), (65000, 1101, 16)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        self._check_main_bgp_tables_empty(sim)


class TestPeer(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'peer' peer type."""

    # BIRD configuration
    r1_peer_type = "peer"

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 3), (65000, 1101, 16)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 3), (65000, 1101, 16)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        self._check_main_bgp_tables_empty(sim)


class TestTransit(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'transit' peer type."""

    # BIRD configuration
    r1_peer_type = "transit"

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 4), (65000, 1101, 16)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 4), (65000, 1101, 16)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        self._check_main_bgp_tables_empty(sim)


class TestRrclient(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'rrclient' peer type."""

    # BIRD configuration
    r1_peer_asn = "65000"
    e1_asn = "65000"
    r1_peer_type = "rrclient"
    r1_extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRrserver(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'rrserver' peer type."""

    # BIRD configuration
    r1_peer_asn = "65000"
    e1_asn = "65000"
    r1_peer_type = "rrserver"
    r1_extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRrserverRrserver(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'rrserver-rrserver' peer type."""

    # BIRD configuration
    r1_peer_asn = "65000"
    e1_asn = "65000"
    r1_peer_type = "rrserver-rrserver"
    r1_extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": self.too_many_communities,
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRoutecollector(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'routecollector' peer type."""

    # BIRD configuration
    r1_peer_type = "routecollector"

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 1101, 17)],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 1101, 17)],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        self._check_main_bgp_tables_empty(sim)


class TestRouteserver(BGPFilteringTooManyCommunitiesBase):
    """Test filtering of too many communities for the 'routeserver' peer type."""

    # BIRD configuration
    r1_peer_type = "routeserver"

    def _test_results(self, sim, helpers):
        """Test results from this peer type."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 5), (65000, 1101, 16)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": self.too_many_communities,
                        "BGP.large_community": [(65000, 3, 5), (65000, 1101, 16)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["fc00:100::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        # Check main BGP table
        self._check_main_bgp_tables_empty(sim)
