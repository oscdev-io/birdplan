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

"""BGP filtering of default route allowed."""

# pylint: disable=import-error,too-few-public-methods,no-self-use

from typing import Tuple
import os
import pytest
from template import BGPFilteringBase
from birdplan.exceptions import BirdPlanError


class BGPFilteringDefaultAllowedBase(BGPFilteringBase):
    """Base class for BGP filtering of default route allowed."""

    test_dir = os.path.dirname(__file__)
    routers = ["r1"]

    def _announce_default_route(self, sim) -> Tuple:
        """Announce a default route from ExaBGP to BIRD."""

        self._exabgpcli(sim, "e1", ["neighbor 100.64.0.1 announce route 0.0.0.0/0 next-hop 100.64.0.2"])
        self._exabgpcli(sim, "e1", ["neighbor fc00:100::1 announce route ::/0 next-hop fc00:100::2"])

        # Grab IPv4 table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)
        assert len(peer_bgp4_table) == 1, "Failed to announce IPv4 default route"

        # Grab IPv6 table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)
        assert len(peer_bgp6_table) == 1, "Failed to announce IPv6 default route"

        # Return our two routing tables
        return (peer_bgp4_table, peer_bgp6_table)


class TestBGPFilteringDefaultAllowedCustomer(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'customer' peer type."""

    # BIRD configuration
    peer_type = "customer"
    extra_config = """
      filter:
        asns: [65001]
      accept:
        default: True
"""

    def test_default_route_announce(self, sim, tmpdir):
        """Test filtering of default route allowed for the 'customer' peer type."""

        with pytest.raises(BirdPlanError, match=r"'customer' makes no sense"):
            # Setup environment
            self._setup(sim, tmpdir)


class TestBGPFilteringDefaultAllowedPeer(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'peer' peer type."""

    # BIRD configuration
    peer_type = "peer"
    extra_config = """
      accept:
        default: True
"""

    def test_default_route_announce(self, sim, tmpdir):
        """Test filtering of default route allowed for the 'peer' peer type."""

        with pytest.raises(BirdPlanError, match=r"'peer' makes no sense"):
            # Setup environment
            self._setup(sim, tmpdir)


class TestBGPFilteringDefaultAllowedTransit(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'transit' peer type."""

    # BIRD configuration
    peer_type = "transit"
    extra_config = """
      accept:
        default: True
"""

    def test_default_route_announce(self, sim, tmpdir, helpers):
        """Test filtering of default route allowed for the 'transit' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_default_route(sim)

        # Check bgp_originate4 BIRD table
        correct_result = {
            "0.0.0.0/0": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65000, 3, 4)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": "100.64.0.2",
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

        # Check bgp_originate4 BIRD table
        correct_result = {
            "::/0": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65000, 3, 4)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": "fc00:100::2",
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

        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {
            "0.0.0.0/0": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65000, 3, 4)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": "100.64.0.2",
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
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {
            "::/0": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65000, 3, 4)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": "fc00:100::2",
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
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestBGPFilteringDefaultAllowedRrclient(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'rrclient' peer type."""

    # BIRD configuration
    peer_asn = "65000"
    peer_type = "rrclient"
    extra_config = """
      accept:
        default: True
  rr_cluster_id: 0.0.0.1
"""

    def test_default_route_announce(self, sim, tmpdir, helpers):
        """Test filtering of default route allowed for the 'rrclient' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_default_route(sim)

        # Check bgp_originate4 BIRD table
        correct_result = {
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "100.64.0.2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check bgp_originate4 BIRD table
        correct_result = {
            "::/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "fc00:100::2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_e1",
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
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "100.64.0.2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {
            "::/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "fc00:100::2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestBGPFilteringDefaultAllowedRrserver(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'rrserver' peer type."""

    # BIRD configuration
    peer_asn = "65000"
    peer_type = "rrserver"
    extra_config = """
      accept:
        default: True
  rr_cluster_id: 0.0.0.1
"""

    def test_default_route_announce(self, sim, tmpdir, helpers):
        """Test filtering of default route allowed for the 'rrserver' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_default_route(sim)

        # Check bgp_originate4 BIRD table
        correct_result = {
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "100.64.0.2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check bgp_originate4 BIRD table
        correct_result = {
            "::/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "fc00:100::2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_e1",
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
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "100.64.0.2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {
            "::/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "fc00:100::2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestBGPFilteringDefaultAllowedRrserverRrserver(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'rrserver-rrserver' peer type."""

    # BIRD configuration
    peer_asn = "65000"
    peer_type = "rrserver-rrserver"
    extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def test_default_route_announce(self, sim, tmpdir, helpers):
        """Test filtering of default route allowed for the 'rrserver-rrserver' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_default_route(sim)

        # Check bgp_originate4 BIRD table
        correct_result = {
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "100.64.0.2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check bgp_originate4 BIRD table
        correct_result = {
            "::/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "fc00:100::2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_e1",
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
            "0.0.0.0/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "100.64.0.2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {
            "::/0": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.local_pref": 100,
                        "BGP.next_hop": "fc00:100::2",
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestBGPFilteringDefaultAllowedRoutecollector(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'routecollector' peer type."""

    # BIRD configuration
    peer_type = "routecollector"
    extra_config = """
      accept:
        default: True
"""

    def test_default_route_announce(self, sim, tmpdir):
        """Test filtering of default route allowed for the 'routecollector' peer type."""

        with pytest.raises(BirdPlanError, match=r"'routecollector' makes no sense"):
            # Setup environment
            self._setup(sim, tmpdir)


class TestBGPFilteringDefaultAllowedRouteserver(BGPFilteringDefaultAllowedBase):
    """Test filtering of default route allowed for the 'routeserver' peer type."""

    # BIRD configuration
    peer_type = "routeserver"
    extra_config = """
      accept:
        default: True
"""

    def test_default_route_announce(self, sim, tmpdir):
        """Test filtering of default route allowed for the 'routeserver' peer type."""

        with pytest.raises(BirdPlanError, match=r"'routeserver' makes no sense"):
            # Setup environment
            self._setup(sim, tmpdir)
