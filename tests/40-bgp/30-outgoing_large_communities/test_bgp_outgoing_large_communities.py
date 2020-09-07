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

"""BGP test for outgoing large communities."""

import os
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.switch_node import SwitchNode
from basetests import BirdPlanBaseTestCase


class TestBGPOutgoingLargeCommunities(BirdPlanBaseTestCase):
    """BGP test for outgoing large communities."""

    test_dir = os.path.dirname(__file__)
    routers = ["r1", "r2"]

    def test_configure(self, sim, tmpdir):
        """Create our configuration files."""
        self._test_configure(sim, tmpdir)

    def test_create_topology(self, sim, tmpdir):
        """Test topology creation."""

        print("Adding routers...")
        sim.add_node(BirdRouterNode(name="r1", configfile=f"{tmpdir}/bird.conf.r1"))
        sim.add_node(BirdRouterNode(name="r2", configfile=f"{tmpdir}/bird.conf.r2"))

        print("Adding interfaces...")
        sim.node("r1").add_interface("eth0", mac="02:01:00:00:00:01", ips=["100.64.0.1/24", "fc00:100::1/64"])
        sim.node("r1").add_interface("eth1", mac="02:01:00:00:00:02", ips=["192.168.1.1/24", "fc01::1/64"])
        sim.node("r2").add_interface("eth0", mac="02:02:00:00:00:01", ips=["100.64.0.2/24", "fc00:100::2/64"])

        print("Adding switches...")
        sim.add_node(SwitchNode("s1"))
        sim.node("s1").add_interface(sim.node("r1").interface("eth0"))
        sim.node("s1").add_interface(sim.node("r2").interface("eth0"))

        # Simulate our topology
        print("Simulate topology...")
        sim.run()

    def test_bird_status(self, sim):
        """Grab data from the simulation."""

        r1_status_output = sim.node("r1").birdc_show_status()
        r2_status_output = sim.node("r2").birdc_show_status()

        sim.add_report_obj("STATUS(r1)", r1_status_output)
        sim.add_report_obj("STATUS(r2)", r2_status_output)

        # Check BIRD router ID
        assert "router_id" in r1_status_output, "The status output should have 'router_id'"
        assert r1_status_output["router_id"] == "0.0.0.1", "The router ID should be '0.0.0.1'"

        assert "router_id" in r2_status_output, "The status output should have 'router_id'"
        assert r2_status_output["router_id"] == "0.0.0.2", "The router ID should be '0.0.0.2'"

    def test_bird_tables_bgp_peer4(self, sim, helpers):
        """Test BIRD bgp peer4 table."""

        r1r2_bgp_table = self._bird_bgp_peer_table(sim, "r1", "r2", 4)
        r2r1_bgp_table = self._bird_bgp_peer_table(sim, "r2", "r1", 4)

        r1_table = self._bird_route_table(sim, "r1", r1r2_bgp_table, expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", r2r1_bgp_table, expect_count=1)

        # Check bgp peer4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1, 0), (65000, 4, 65414)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert r1_table == correct_result, f"Result for R1 BIRD {r1r2_bgp_table} routing table does not match what it should be"

        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 1, 0), (65000, 3, 1), (65000, 4, 65414), (65001, 3, 3)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["100.64.0.1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, f"Result for R2 BIRD {r2r1_bgp_table} routing table does not match what it should be"

    def test_bird_tables_bgp_peer6(self, sim, helpers):
        """Test BIRD bgp peer6 table."""

        r1r2_bgp_table = self._bird_bgp_peer_table(sim, "r1", "r2", 6)
        r2r1_bgp_table = self._bird_bgp_peer_table(sim, "r2", "r1", 6)

        r1_table = self._bird_route_table(sim, "r1", r1r2_bgp_table, expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", r2r1_bgp_table, expect_count=1)

        # Check originate6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1, 0), (65000, 4, 65414)], "BGP.local_pref": 940},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 200,
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert r1_table == correct_result, f"Result for R1 BIRD {r1r2_bgp_table} routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 1, 0), (65000, 3, 1), (65000, 4, 65414), (65001, 3, 3)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["fc00:100::1", "fe80::1:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::1", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, f"Result for R2 BIRD {r2r1_bgp_table} routing table does not match what it should be"

    def test_bird_tables_bgp4(self, sim, helpers):
        """Test BIRD t_bgp4 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_bgp4", expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", "t_bgp4", expect_count=1)

        # Check bgp4 BIRD table
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
        assert r1_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 1, 0), (65000, 3, 1), (65000, 4, 65414), (65001, 3, 3)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["100.64.0.1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_bgp4 routing table does not match what it should be"

    def test_bird_tables_bgp6(self, sim, helpers):
        """Test BIRD t_bgp6 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_bgp6", expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", "t_bgp6", expect_count=1)

        # Check t_bgp6 BIRD table
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
        assert r1_table == correct_result, "Result for R1 BIRD t_bgp6 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 1, 0), (65000, 3, 1), (65000, 4, 65414), (65001, 3, 3)],
                        "BGP.local_pref": 470,
                        "BGP.next_hop": ["fc00:100::1", "fe80::1:ff:fe00:1"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::1", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_bgp6 routing table does not match what it should be"
