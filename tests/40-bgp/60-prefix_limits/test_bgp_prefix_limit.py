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

"""BGP prefix limits."""

from typing import Tuple
import os
from template_exabgp import BirdplanBaseTestCaseExabgp


class BGPPrefixLimitBase(BirdplanBaseTestCaseExabgp):
    """BGP prefix limits."""

    test_dir = os.path.dirname(__file__)
    routers = ["r1"]

    def _announce_too_many_prefixes(self, sim) -> Tuple:
        """Announce too many prefixes from ExaBGP to BIRD."""

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

        route_limit_exceeded = self._bird_log_matches(sim, "r1", r"bgp4_AS6500[01]_e1: Route limit exceeded, shutting down")
        assert route_limit_exceeded, "Failed to shut down IPv4 connection when route limit exceeded"

        route_limit_exceeded = self._bird_log_matches(sim, "r1", r"bgp6_AS6500[01]_e1: Route limit exceeded, shutting down")
        assert route_limit_exceeded, "Failed to shut down IPv6 connection when route limit exceeded"

        # Grab IPv4 table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name)
        assert len(peer_bgp4_table) == 0, "Failed to announce IPv4 with community"

        # Grab IPv6 table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name)
        assert len(peer_bgp6_table) == 0, "Failed to announce IPv6 with community"

        # Return our two routing tables
        return (peer_bgp4_table, peer_bgp6_table)


class TestCustomer(BGPPrefixLimitBase):
    """Test too many prefixes for the 'customer' peer type."""

    # BIRD configuration
    peer_type = "customer"
    extra_config = """
      filter:
        asns: [65001]
"""

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'customer' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"


class TestPeer(BGPPrefixLimitBase):
    """Test too many prefixes for the 'peer' peer type."""

    # BIRD configuration
    peer_type = "peer"

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'peer' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"


class TestTransit(BGPPrefixLimitBase):
    """Test too many prefixes for the 'transit' peer type."""

    # BIRD configuration
    peer_type = "transit"

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'transit' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"


class TestRrclient(BGPPrefixLimitBase):
    """Test too many prefixes for the 'rrclient' peer type."""

    # BIRD configuration
    peer_asn = "65000"
    peer_type = "rrclient"
    extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'rrclient' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"


class TestRrserver(BGPPrefixLimitBase):
    """Test too many prefixes for the 'rrserver' peer type."""

    # BIRD configuration
    peer_asn = "65000"
    peer_type = "rrserver"
    extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'rrserver' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"


class TestRrserverRrserver(BGPPrefixLimitBase):
    """Test too many prefixes for the 'rrserver-rrserver' peer type."""

    # BIRD configuration
    peer_asn = "65000"
    peer_type = "rrserver-rrserver"
    extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'rrserver-rrserver' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"


class TestRoutecollector(BGPPrefixLimitBase):
    """Test too many prefixes for the 'routecollector' peer type."""

    # BIRD configuration
    peer_type = "routecollector"

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'routecollector' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"


class TestRouteserver(BGPPrefixLimitBase):
    """Test too many prefixes for the 'routeserver' peer type."""

    # BIRD configuration
    peer_type = "routeserver"

    def test_too_many_prefixes_announce(self, sim, tmpdir):
        """Test too many prefixes for the 'routeserver' peer type."""

        # Setup environment
        self._setup(sim, tmpdir)

        # Announce prefixes
        ipv4_table, ipv6_table = self._announce_too_many_prefixes(sim)

        # Check peer BGP table
        correct_result = {}
        assert ipv4_table == correct_result, "Result for R1 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {}
        assert ipv6_table == correct_result, "Result for R1 BIRD IPv6 BGP peer routing table does not match what it should be"
