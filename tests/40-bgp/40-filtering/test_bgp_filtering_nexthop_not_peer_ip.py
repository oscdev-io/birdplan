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

"""BGP filtering of invalid nexthop."""

from typing import Tuple
import os
from basetests import BirdPlanBaseTestCase


class BGPFilteringWrongNexthopBase(BirdPlanBaseTestCase):
    """Base class for BGP filtering of invalid nexthop."""

    test_dir = os.path.dirname(__file__)
    exabgps = ["e1"]

    def test_setup(self, sim, tmpdir):
        """Set up our test."""
        self._test_setup(sim, tmpdir)

    def test_announce_routes(self, sim):
        """Announce a prefix that has a wrong nexthop from ExaBGP to BIRD."""

        self._exabgpcli(sim, "e1", ["neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.3 as-path [ 65001 ]"])
        self._exabgpcli(sim, "e1", ["neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::3 as-path [ 65001 ]"])

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
        assert len(peer_bgp4_table) == 1, "Failed to announce IPv4 with wrong nexthop"

        # Grab IPv6 table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)
        assert len(peer_bgp6_table) == 1, "Failed to announce IPv6 with wrong nexthop"

        # Return our two routing tables
        return (peer_bgp4_table, peer_bgp6_table)


class TestCustomer(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'customer' peer type."""

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
                        "BGP.large_community": [(65000, 3, 2), (65000, 1101, 8)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                        "BGP.large_community": [(65000, 3, 2), (65000, 1101, 8)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
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


class TestPeer(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'peer' peer type."""

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
                        "BGP.large_community": [(65000, 3, 3), (65000, 1101, 8)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                        "BGP.large_community": [(65000, 3, 3), (65000, 1101, 8)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
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


class TestTransit(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'transit' peer type."""

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
                        "BGP.large_community": [(65000, 3, 4), (65000, 1101, 8)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                        "BGP.large_community": [(65000, 3, 4), (65000, 1101, 8)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
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


class TestRrclient(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'rrclient' peer type."""

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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRrserver(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'rrserver' peer type."""

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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRrserverRrserver(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'rrserver-rrserver' peer type."""

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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRoutecollector(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'routecollector' peer type."""

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
                        "BGP.large_community": [(65000, 1101, 17)],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                        "BGP.large_community": [(65000, 1101, 17)],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
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


class TestRouteserver(BGPFilteringWrongNexthopBase):
    """Test filtering of wrong nexthops for the 'routeserver' peer type."""

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
                        "BGP.large_community": [(65000, 3, 5)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
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
                        "BGP.large_community": [(65000, 3, 5)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"

        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65000, 3, 5)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["100.64.0.3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_e1",
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
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65000, 3, 5)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["fc00:100::3"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"
