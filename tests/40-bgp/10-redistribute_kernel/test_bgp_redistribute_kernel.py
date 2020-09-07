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

"""BGP test for redistribution of kernel routes."""

import os
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.switch_node import SwitchNode
from basetests import BirdPlanBaseTestCase


class TestBGPRedistributeKernel(BirdPlanBaseTestCase):
    """BGP test for redistribution of kernel routes."""

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
        sim.node("r2").add_interface("eth1", mac="02:02:00:00:00:02", ips=["192.168.2.1/24", "fc02::1/64"])

        print("Adding switches...")
        sim.add_node(SwitchNode("s1"))
        sim.node("s1").add_interface(sim.node("r1").interface("eth0"))
        sim.node("s1").add_interface(sim.node("r2").interface("eth0"))

        # Simulate our topology
        print("Simulate topology...")
        sim.run()

        # Add gateway'd kernel routes
        sim.node("r1").run_ip(["route", "add", "100.101.0.0/24", "via", "192.168.1.2"])
        sim.node("r1").run_ip(["route", "add", "fc00:101::/48", "via", "fc01::2"])
        sim.node("r2").run_ip(["route", "add", "100.102.0.0/24", "via", "192.168.2.2"])
        sim.node("r2").run_ip(["route", "add", "fc00:102::/48", "via", "fc02::2"])
        # Add link kernel routes
        sim.node("r1").run_ip(["route", "add", "100.103.0.0/24", "dev", "eth1"])
        sim.node("r1").run_ip(["route", "add", "fc00:103::/48", "dev", "eth1"])
        sim.node("r2").run_ip(["route", "add", "100.104.0.0/24", "dev", "eth1"])
        sim.node("r2").run_ip(["route", "add", "fc00:104::/48", "dev", "eth1"])

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

    def test_bird_tables_bgp_originate4(self, sim):
        """Test BIRD bgp_originate4 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_bgp_originate4")
        r2_table = self._bird_route_table(sim, "r2", "t_bgp_originate4")

        # Check bgp_originate4 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD t_bgp_originate4 routing table does not match what it should be"

        correct_result = {}
        assert r2_table == correct_result, "Result for R2 BIRD t_bgp_originate4 routing table does not match what it should be"

    def test_bird_tables_bgp_originate6(self, sim):
        """Test BIRD bgp_originate6 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_bgp_originate6")
        r2_table = self._bird_route_table(sim, "r2", "t_bgp_originate6")

        # Check bgp_originate6 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD t_bgp_originate6 routing table does not match what it should be"

        correct_result = {}
        assert r2_table == correct_result, "Result for R2 BIRD t_bgp_originate6 routing table does not match what it should be"

    def test_bird_tables_bgp_peer4(self, sim, helpers):
        """Test BIRD bgp peer4 table."""

        r1r2_bgp_table = self._bird_bgp_peer_table(sim, "r1", "r2", 4)
        r2r1_bgp_table = self._bird_bgp_peer_table(sim, "r2", "r1", 4)

        r1_table = self._bird_route_table(sim, "r1", r1r2_bgp_table, expect_count=2)
        r2_table = self._bird_route_table(sim, "r2", r2r1_bgp_table, expect_count=2)

        # Check bgp peer4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "0",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "100.103.0.0/24": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "0",
                        "Kernel.scope": "253",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, f"Result for R1 BIRD {r1r2_bgp_table} routing table does not match what it should be"

        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "100.103.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
        }
        assert r2_table == correct_result, f"Result for R2 BIRD {r2r1_bgp_table} routing table does not match what it should be"

    def test_bird_tables_bgp_peer6(self, sim, helpers):
        """Test BIRD bgp peer6 table."""

        r1r2_bgp_table = self._bird_bgp_peer_table(sim, "r1", "r2", 6)
        r2r1_bgp_table = self._bird_bgp_peer_table(sim, "r2", "r1", 6)

        r1_table = self._bird_route_table(sim, "r1", r1r2_bgp_table, expect_count=2)
        r2_table = self._bird_route_table(sim, "r2", r2r1_bgp_table, expect_count=2)

        # Check originate6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "1024",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "fc00:103::/48": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "1024",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, f"Result for R1 BIRD {r1r2_bgp_table} routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "fc00:103::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
        }
        assert r2_table == correct_result, f"Result for R2 BIRD {r2r1_bgp_table} routing table does not match what it should be"

    def test_bird_tables_bgp4(self, sim, helpers):
        """Test BIRD t_bgp4 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_bgp4", expect_count=2)
        r2_table = self._bird_route_table(sim, "r2", "t_bgp4", expect_count=4)

        # Check bgp4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "0",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "100.103.0.0/24": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "0",
                        "Kernel.scope": "253",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "100.102.0.0/24": [
                {
                    "attributes": {
                        "BGP.large_community": [(65001, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "0",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"gateway": "192.168.2.2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "100.103.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "100.104.0.0/24": [
                {
                    "attributes": {
                        "BGP.large_community": [(65001, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "0",
                        "Kernel.scope": "253",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_bgp4 routing table does not match what it should be"

    def test_bird_tables_bgp6(self, sim, helpers):
        """Test BIRD t_bgp6 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_bgp6", expect_count=2)
        r2_table = self._bird_route_table(sim, "r2", "t_bgp6", expect_count=4)

        # Check t_bgp6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "1024",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "fc00:103::/48": [
                {
                    "attributes": {
                        "BGP.large_community": [(65000, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "1024",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_bgp6 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "fc00:102::/48": [
                {
                    "attributes": {
                        "BGP.large_community": [(65001, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "1024",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"gateway": "fc02::2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "fc00:103::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "fc00:104::/48": [
                {
                    "attributes": {
                        "BGP.large_community": [(65001, 3, 1)],
                        "BGP.local_pref": 945,
                        "Kernel.metric": "1024",
                        "Kernel.source": "3",
                    },
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_tables_master4(self, sim, helpers):
        """Test BIRD master4 table."""

        r1_table = self._bird_route_table(sim, "r1", "master4", expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", "master4", expect_count=2)

        # Check master4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "100.103.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, "Result for R1 BIRD master4 routing table does not match what it should be"

        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "100.102.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "192.168.2.2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "100.103.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "100.104.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r2_table == correct_result, "Result for R2 BIRD master4 routing table does not match what it should be"

    def test_bird_tables_master6(self, sim, helpers):
        """Test BIRD master6 table."""

        r1_table = self._bird_route_table(sim, "r1", "master6", expect_count=2)
        r2_table = self._bird_route_table(sim, "r2", "master6", expect_count=4)

        # Check master6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "fc00:103::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, "Result for R1 BIRD master6 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "fc00:102::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "fc02::2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "fc00:103::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "fc00:104::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r2_table == correct_result, "Result for R2 BIRD master6 routing table does not match what it should be"

    def test_bird_tables_kernel4(self, sim, helpers):
        """Test BIRD kernel4 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_kernel4", expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", "t_kernel4", expect_count=2)

        # Check kernel4 BIRD table
        correct_result = {
            "100.101.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "100.103.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_kernel4 routing table does not match what it should be"

        correct_result = {
            "100.101.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "100.102.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "192.168.2.2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "100.103.0.0/24": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "100.104.0.0/24": [
                {
                    "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel4",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_kernel4 routing table does not match what it should be"

    def test_bird_tables_kernel6(self, sim, helpers):
        """Test BIRD kernel6 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_kernel6", expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", "t_kernel6", expect_count=2)

        # Check kernel6 BIRD table
        correct_result = {
            "fc00:101::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "fc00:103::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_kernel6 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "fc00:102::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"gateway": "fc02::2", "interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
            "fc00:103::/48": [
                {
                    "asn": "AS65000",
                    "attributes": {
                        "BGP.as_path": [65000],
                        "BGP.large_community": [(65000, 3, 1), (65001, 3, 3)],
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
            ],
            "fc00:104::/48": [
                {
                    "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
                    "nexthops": [{"interface": "eth1"}],
                    "pref": 10,
                    "prefix_type": "unicast",
                    "protocol": "kernel6",
                    "since": helpers.bird_since_field(),
                    "type": ["inherit", "univ"],
                }
            ],
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_kernel6 routing table does not match what it should be"

    def test_os_rib_inet(self, sim):
        """Test OS rib inet table."""

        r1_os_rib = sim.node("r1").run_ip(["--family", "inet", "route", "list"])
        r2_os_rib = sim.node("r2").run_ip(["--family", "inet", "route", "list"])

        sim.add_report_obj("OS(r1)[inet]", r1_os_rib)
        sim.add_report_obj("OS(r2)[inet]", r2_os_rib)

        # Check kernel has the correct IPv4 RIB
        correct_result = [
            {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
            {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "gateway": "192.168.1.2"},
            {"dev": "eth1", "dst": "100.103.0.0/24", "flags": [], "scope": "link"},
            {"dev": "eth1", "dst": "192.168.1.0/24", "flags": [], "prefsrc": "192.168.1.1", "protocol": "kernel", "scope": "link"},
        ]
        assert r1_os_rib == correct_result, "R1 kernel IPv4 RIB does not match what it should be"

        correct_result = [
            {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
            {"dev": "eth0", "dst": "100.101.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
            {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "gateway": "192.168.2.2"},
            {"dev": "eth0", "dst": "100.103.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
            {"dev": "eth1", "dst": "100.104.0.0/24", "flags": [], "scope": "link"},
            {"dev": "eth1", "dst": "192.168.2.0/24", "flags": [], "prefsrc": "192.168.2.1", "protocol": "kernel", "scope": "link"},
        ]
        assert r2_os_rib == correct_result, "R2 kernel IPv4 RIB does not match what it should be"

    def test_os_rib_inet6(self, sim):
        """Test OS rib inet6 table."""

        r1_os_rib = sim.node("r1").run_ip(["--family", "inet6", "route", "list"])
        r2_os_rib = sim.node("r2").run_ip(["--family", "inet6", "route", "list"])

        sim.add_report_obj("OS(r1)[inet6]", r1_os_rib)
        sim.add_report_obj("OS(r2)[inet6]", r2_os_rib)

        # Check kernel has the correct IPv6 RIB
        correct_result = [
            {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth1", "dst": "fc00:101::/48", "flags": [], "gateway": "fc01::2", "metric": 1024, "pref": "medium"},
            {"dev": "eth1", "dst": "fc00:103::/48", "flags": [], "metric": 1024, "pref": "medium"},
            {"dev": "eth1", "dst": "fc01::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
        ]
        assert r1_os_rib == correct_result, "R1 Kernel IPv6 RIB does not match what it should be"

        correct_result = [
            {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {
                "dev": "eth0",
                "dst": "fc00:101::/48",
                "flags": [],
                "gateway": "fc00:100::1",
                "metric": 600,
                "pref": "medium",
                "protocol": "bird",
            },
            {"dev": "eth1", "dst": "fc00:102::/48", "flags": [], "gateway": "fc02::2", "metric": 1024, "pref": "medium"},
            {
                "dev": "eth0",
                "dst": "fc00:103::/48",
                "flags": [],
                "gateway": "fc00:100::1",
                "metric": 600,
                "pref": "medium",
                "protocol": "bird",
            },
            {"dev": "eth1", "dst": "fc00:104::/48", "flags": [], "metric": 1024, "pref": "medium"},
            {"dev": "eth1", "dst": "fc02::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
        ]
        assert r2_os_rib == correct_result, "R2 Kernel IPv6 RIB does not match what it should be"
