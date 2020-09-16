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
# pylint: disable=import-error,too-few-public-methods,no-self-use,too-many-lines

"""BGP graceful shutdown outbound from commandline."""

from typing import Tuple
import os
import time
from basetests import BirdPlanBaseTestCase


class BGPGracefulShutdownOutboundCmdlineBase(BirdPlanBaseTestCase):
    """Base class for BGP graceful shutdown outbound from commandline."""

    test_dir = os.path.dirname(__file__)
    routers = ["r1", "r2"]
    r2_asn = "65001"
    r2_interfaces = ["eth0", "eth1"]
    r2_interface_eth1 = {"mac": "02:02:00:00:00:02", "ips": ["192.168.1.1/24", "fc01::1/64"]}
    r2_extra_config = """
      filter:
        asns: [65001]
"""

    def test_setup(self, sim, tmpdir):
        """Set up our test."""
        self._test_setup(sim, tmpdir)

    # R2 tests
    def test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""
        self._test_results_r2_no_graceful_shutdown(sim, helpers)

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test-specific results from r2."""
        raise NotImplementedError

    # R1 tests
    def test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""
        self._test_results_r1_no_graceful_shutdown(sim, helpers)

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test-specific results from r1."""
        raise NotImplementedError

    # Reconfigure peer from commandline with graceful shutdown
    def test_add_graceful_shutdown(self, sim, tmpdir):
        """Reconfigure the peer for graceful shutdown from commandline."""

        # Add r2 to graceful shutdown list
        self._birdplan_run(sim, tmpdir, "r2", ["bgp", "graceful_shutdown", "add", "r1"])

        # Check r2 was added
        graceful_shutdown_list = self._birdplan_run(sim, tmpdir, "r2", ["bgp", "graceful_shutdown", "list"])
        assert graceful_shutdown_list == ["r1"], "Router r1 is not in the graceful shutdown list"

        # Rewrite configuration file
        self._birdplan_run(sim, tmpdir, "r2", ["configure"])

        # Reconfigure BIRD
        self._birdc(sim, "r2", "configure")
        # Wait for BIRD to reply that it is up and running
        count = 0
        while True:
            # Grab status output
            status_output = self._birdc(sim, "r2", "show status")
            if "0013 Daemon is up and running" in status_output:
                break
            # Check for timeout
            if count > 10:
                break
            # If we're not up and running yet, sleep and increase count
            time.sleep(1)
            count += 1

    # R2 tests
    def test_results_r2(self, sim, helpers):
        """Test results from r2."""
        self._test_results_r2(sim, helpers)

    def _test_results_r2(self, sim, helpers):
        """Test-specific results from r2."""
        raise NotImplementedError

    # R1 tests
    def test_results_r1(self, sim, helpers):
        """Test results from r1."""
        self._test_results_r1(sim, helpers)

    def _test_results_r1(self, sim, helpers):
        """Test-specific results from r1."""
        raise NotImplementedError

    # Reconfigure peer from commandline, remove graceful shutdown
    def test_remove_graceful_shutdown(self, sim, tmpdir):
        """Reconfigure the peer without graceful shutdown from commandline."""

        # Remove r2 from graceful shutdown list
        self._birdplan_run(sim, tmpdir, "r2", ["bgp", "graceful_shutdown", "remove", "r1"])

        # Check r2 was removed
        graceful_shutdown_list = self._birdplan_run(sim, tmpdir, "r2", ["bgp", "graceful_shutdown", "list"])
        assert graceful_shutdown_list == [], "Router r2 graceful shutdown list should be empty"

        # Rewrite configuration file
        self._birdplan_run(sim, tmpdir, "r2", ["configure"])

        # Reconfigure BIRD
        self._birdc(sim, "r2", "configure")
        # Wait for BIRD to reply that it is up and running
        count = 0
        while True:
            # Grab status output
            status_output = self._birdc(sim, "r2", "show status")
            if "0013 Daemon is up and running" in status_output:
                break
            # Check for timeout
            if count > 10:
                break
            # If we're not up and running yet, sleep and increase count
            time.sleep(1)
            count += 1

    # R2 tests
    def test_results_r2_no_graceful_shutdown2(self, sim, helpers):
        """Test results from r2."""
        self._test_results_r2_no_graceful_shutdown(sim, helpers)

    # R1 tests
    def test_results_r1_no_graceful_shutdown2(self, sim, helpers):
        """Test results from r1."""
        self._test_results_r1_no_graceful_shutdown(sim, helpers)

    # Grab bgp tables from R1
    def _get_r1_bgp_tables(self, sim, expect_count=1) -> Tuple:
        # Grab our main BGP tables
        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4", expect_count=expect_count)
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6", expect_count=expect_count)
        # And return them...
        return (bgp4_table, bgp6_table)

    # Grab peer tables from R2
    def _get_r2_peer_tables(self, sim) -> Tuple:
        # Grab IPv4 peering table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r2", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r2", peer_bgp_table_name, expect_count=1)
        assert len(peer_bgp4_table) == 1, "Failed to find any routes in r2's BGP peer table"

        # Grab IPv6 peering table name and get entries
        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r2", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r2", peer_bgp_table_name, expect_count=1)
        assert len(peer_bgp6_table) == 1, "Failed to find any routes in r2's BGP peer table"

        # Return our two routing tables
        return (peer_bgp4_table, peer_bgp6_table)


class TestCustomer(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'customer' peer type."""

    # BIRD configuration
    r1_peer_type = "customer"
    r1_extra_config = """
      filter:
        asns: [65001]
"""
    r2_peer_type = "transit"

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 2)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 2)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestPeer(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'peer' peer type."""

    # BIRD configuration
    r1_peer_type = "peer"
    r2_peer_type = "peer"

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 3)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 3)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 3)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 3)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestTransit(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'transit' peer type."""

    # BIRD configuration
    r1_peer_type = "transit"
    r2_peer_type = "customer"
    r2_extra_config = """
      filter:
        asns: [65000]
"""

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 4)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 4)],
                        "BGP.local_pref": 150,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 4)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 4)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRrclient(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'rrclient' peer type."""

    # BIRD configuration
    r1_peer_asn = "65000"
    r1_peer_type = "rrclient"
    r1_extra_config = """
  rr_cluster_id: 0.0.0.1
"""
    r2_asn = "65000"
    r2_peer_type = "rrserver"

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 940,
                        "BGP.next_hop": ["192.168.1.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_r2",
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
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 940,
                        "BGP.next_hop": ["fc01::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["192.168.1.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_r2",
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
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["fc01::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRrserver(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'rrserver' peer type."""

    # BIRD configuration
    r1_peer_asn = "65000"
    r1_peer_type = "rrserver"

    r2_asn = "65000"
    r2_peer_type = "rrclient"
    r2_extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 940,
                        "BGP.next_hop": ["192.168.1.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_r2",
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
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 940,
                        "BGP.next_hop": ["fc01::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["192.168.1.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_r2",
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
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["fc01::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRrserverRrserver(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'rrserver-rrserver' peer type."""

    # BIRD configuration
    r1_peer_asn = "65000"
    r1_peer_type = "rrserver-rrserver"
    r1_extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    r2_asn = "65000"
    r2_peer_type = "rrserver-rrserver"
    r2_extra_config = """
  rr_cluster_id: 0.0.0.1
"""

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 940,
                        "BGP.next_hop": ["192.168.1.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_r2",
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
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 940,
                        "BGP.next_hop": ["fc01::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.as_path": [],
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["192.168.1.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp4_AS65000_r2",
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
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["fc01::2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::2",
                    "pref": 100,
                    "prefix_type": "unreachable",
                    "protocol": "bgp6_AS65000_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRoutecollector(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'routecollector' peer type."""

    # BIRD configuration
    r1_peer_type = "routecollector"
    r2_peer_type = "peer"

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim, expect_count=0)

        # Check bgp4 BIRD table
        correct_result = {}
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {}
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim, expect_count=0)

        # Check bgp4 BIRD table
        correct_result = {}
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {}
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"


class TestRouteserver(BGPGracefulShutdownOutboundCmdlineBase):
    """Test graceful shutdown outbound for the 'routeserver' peer type."""

    # BIRD configuration
    r1_peer_type = "routeserver"
    r2_peer_type = "peer"

    def _test_results_r2_no_graceful_shutdown(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1_no_graceful_shutdown(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 5)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 5)],
                        "BGP.local_pref": 450,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

    def _test_results_r2(self, sim, helpers):
        """Test results from r2."""

        # Get routing tables
        ipv4_table, ipv6_table = self._get_r2_peer_tables(sim)

        # Check peer BGP table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv4_table == correct_result, "Result for R2 BIRD IPv4 BGP peer routing table does not match what it should be"

        # Check peer BGP table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.community": [(65535, 0)], "BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert ipv6_table == correct_result, "Result for R2 BIRD IPv6 BGP peer routing table does not match what it should be"

    def _test_results_r1(self, sim, helpers):
        """Test results from r1."""

        # Check main BGP table
        (bgp4_table, bgp6_table) = self._get_r1_bgp_tables(sim)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65001",
                    "attributes": {
                        "BGP.as_path": [65001],
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 5)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["100.64.0.2"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65001_r2",
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
                        "BGP.community": [(65535, 0)],
                        "BGP.large_community": [(65001, 3, 1), (65000, 3, 5)],
                        "BGP.local_pref": 0,
                        "BGP.next_hop": ["fc00:100::2", "fe80::2:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65001_r2",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"
