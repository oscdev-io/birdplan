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
# pylint: disable=import-error,no-self-use,too-many-lines,too-many-public-methods

"""BGP test for NOEXPORT to the customer peer type."""

import os
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.exabgp_router_node import ExaBGPRouterNode
from nsnetsim.switch_node import SwitchNode
from basetests import BirdPlanBaseTestCase


class TestBGPLCNoExportCustomer(BirdPlanBaseTestCase):
    """BGP test for NOEXPORT to the customer peer type."""

    test_dir = os.path.dirname(__file__)
    routers = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9"]

    def test_configure(self, sim, tmpdir):
        """Create our configuration files."""
        self._test_configure(sim, tmpdir)

    def test_create_topology(self, sim, tmpdir):
        """Test topology creation."""

        print("Adding routers...")
        for router_name in self.routers:
            sim.add_node(BirdRouterNode(name=f"{router_name}", configfile=f"{tmpdir}/bird.conf.{router_name}"))

        exabgp_conffile = f"{self.test_dir}/exabgp.conf.e1"
        sim.add_node(ExaBGPRouterNode(name="e1", configfile=exabgp_conffile))
        sim.add_conffile("CONFFILE(e1)", exabgp_conffile)
        exalogfile = sim.node("e1").logfile
        sim.add_logfile(f"LOGFILE(e1) => {exalogfile}", sim.node("e1").logfile)

        print("Adding interfaces...")
        num = 1
        for router_name in self.routers:
            sim.node(router_name).add_interface(
                "eth0", mac=f"02:0{num}:00:00:00:01", ips=[f"100.64.0.{num}/24", f"fc00:100::{num}/64"]
            )
            num += 1
        sim.node("e1").add_interface("eth0", mac="02:10:00:00:00:01", ips=["100.64.0.10/24", "fc00:100::10/64"])

        print("Adding switches...")
        sim.add_node(SwitchNode("s1"))
        for router_name in self.routers:
            sim.node("s1").add_interface(sim.node(router_name).interface("eth0"))
        sim.node("s1").add_interface(sim.node("e1").interface("eth0"))

        # Simulate our topology
        print("Simulate topology...")
        sim.run()

        # Advertise a route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.10 large-community [ 65000:4:65414 ]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::10 large-community [ 65000:4:65414 ]"],
        )

    def test_bird_status(self, sim):
        """Grab data from the simulation."""

        status_output = {}
        status_test = {}
        for router_name in self.routers:
            status_output[router_name] = sim.node(router_name).birdc_show_status()
            sim.add_report_obj("STATUS({router_name})", status_output[router_name])
            # Build our status test dictionary
            if "router_id" in status_output[router_name]:
                status_test[router_name] = status_output[router_name]["router_id"]

        # Add report object for our router status
        sim.add_report_obj("STATUS", status_test)

        # Check BIRD router ID
        correct_result = {
            "r1": "0.0.0.1",
            "r2": "0.0.0.2",
            "r3": "0.0.0.3",
            "r4": "0.0.0.4",
            "r5": "0.0.0.5",
            "r6": "0.0.0.6",
            "r7": "0.0.0.7",
            "r8": "0.0.0.8",
            "r9": "0.0.0.9",
        }
        assert status_test == correct_result, "Something went wrong with bird startup"

    def test_bird_table_bgp_peer_r1_e1(self, sim, helpers):
        """Test r1's e1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "e1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's e1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's e1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r2(self, sim):
        """Test r1's r2 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r2", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r2", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name)

        correct_result = {}
        assert peer_bgp4_table == correct_result, "Result for r1's r2 bgp4 peer table does not match what it should be"

        correct_result = {}
        assert peer_bgp6_table == correct_result, "Result for r1's r2 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r3(self, sim, helpers):
        """Test r1's r3 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r3", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r3", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's r3 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's r3 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r4(self, sim, helpers):
        """Test r1's r4 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r4", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r4", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's r4 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's r4 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r5(self, sim, helpers):
        """Test r1's r5 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r5", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r5", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's r5 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's r5 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r6(self, sim, helpers):
        """Test r1's r6 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r6", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r6", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's r6 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's r6 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r7(self, sim, helpers):
        """Test r1's r7 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r7", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r7", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's r7 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's r7 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r8(self, sim, helpers):
        """Test r1's r8 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r8", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r8", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's r8 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's r8 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r1_r9(self, sim, helpers):
        """Test r1's r9 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r9", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r1", "r9", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r1", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r1's r9 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r1's r9 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r2_r1(self, sim):
        """Test r2's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r2", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r2", peer_bgp_table_name)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r2", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r2", peer_bgp_table_name)

        correct_result = {}
        assert peer_bgp4_table == correct_result, "Result for r2's r1 bgp4 peer table does not match what it should be"

        correct_result = {}
        assert peer_bgp6_table == correct_result, "Result for r2's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r3_r1(self, sim, helpers):
        """Test r3's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r3", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r3", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r3", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r3", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65003, 3, 3)],
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
        assert peer_bgp4_table == correct_result, "Result for r3's r1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65003, 3, 3)],
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
        assert peer_bgp6_table == correct_result, "Result for r3's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r4_r1(self, sim, helpers):
        """Test r4's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r4", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r4", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r4", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r4", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65004, 3, 2)],
                        "BGP.local_pref": 750,
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
        assert peer_bgp4_table == correct_result, "Result for r4's r1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65004, 3, 2)],
                        "BGP.local_pref": 750,
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
        assert peer_bgp6_table == correct_result, "Result for r4's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r5_r1(self, sim, helpers):
        """Test r5's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r5", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r5", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r5", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r5", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.1",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r5's r1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::1",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r5's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r6_r1(self, sim, helpers):
        """Test r6's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r6", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r6", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r6", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r6", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.1",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r6's r1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::1",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r6's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r7_r1(self, sim, helpers):
        """Test r7's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r7", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r7", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r7", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r7", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.1",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp4_table == correct_result, "Result for r7's r1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::1",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert peer_bgp6_table == correct_result, "Result for r7's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r8_r1(self, sim, helpers):
        """Test r8's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r8", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r8", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r8", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r8", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65008, 3, 3)],
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
        assert peer_bgp4_table == correct_result, "Result for r8's r1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65008, 3, 3)],
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
        assert peer_bgp6_table == correct_result, "Result for r8's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_peer_r9_r1(self, sim, helpers):
        """Test r9's r1 BGP peer table."""

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r9", "r1", 4)
        peer_bgp4_table = self._bird_route_table(sim, "r9", peer_bgp_table_name, expect_count=1)

        peer_bgp_table_name = self._bird_bgp_peer_table(sim, "r9", "r1", 6)
        peer_bgp6_table = self._bird_route_table(sim, "r9", peer_bgp_table_name, expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65009, 3, 3)],
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
        assert peer_bgp4_table == correct_result, "Result for r9's r1 bgp4 peer table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65009, 3, 3)],
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
        assert peer_bgp6_table == correct_result, "Result for r9's r1 bgp6 peer table does not match what it should be"

    def test_bird_table_bgp_r1(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r1_table4 = self._bird_route_table(sim, "r1", "t_bgp4", expect_count=1)
        r1_table6 = self._bird_route_table(sim, "r1", "t_bgp6", expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r1_table4 == correct_result, "Result for r1 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 4, 65414), (65000, 3, 2)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65010_e1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r1_table6 == correct_result, "Result for r1 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r2(self, sim):
        """Test BIRD main bgp routing tables."""

        r2_table4 = self._bird_route_table(sim, "r2", "t_bgp4")
        r2_table6 = self._bird_route_table(sim, "r2", "t_bgp6")

        correct_result = {}
        assert r2_table4 == correct_result, "Result for r2 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {}
        assert r2_table6 == correct_result, "Result for r2 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r3(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r3_table4 = self._bird_route_table(sim, "r3", "t_bgp4", expect_count=1)
        r3_table6 = self._bird_route_table(sim, "r3", "t_bgp6", expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65003, 3, 3)],
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
        assert r3_table4 == correct_result, "Result for r3 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65003, 3, 3)],
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
        assert r3_table6 == correct_result, "Result for r3 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r4(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r4_table4 = self._bird_route_table(sim, "r4", "t_bgp4")
        r4_table6 = self._bird_route_table(sim, "r4", "t_bgp6")

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65004, 3, 2)],
                        "BGP.local_pref": 750,
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
        assert r4_table4 == correct_result, "Result for r4 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65004, 3, 2)],
                        "BGP.local_pref": 750,
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
        assert r4_table6 == correct_result, "Result for r4 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r5(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r5_table4 = self._bird_route_table(sim, "r5", "t_bgp4", expect_count=1)
        r5_table6 = self._bird_route_table(sim, "r5", "t_bgp6", expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.1",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r5_table4 == correct_result, "Result for r5 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::1",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r5_table6 == correct_result, "Result for r5 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r6(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r6_table4 = self._bird_route_table(sim, "r6", "t_bgp4", expect_count=1)
        r6_table6 = self._bird_route_table(sim, "r6", "t_bgp6", expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.1",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r6_table4 == correct_result, "Result for r6 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::1",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r6_table6 == correct_result, "Result for r6 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r7(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r7_table4 = self._bird_route_table(sim, "r7", "t_bgp4", expect_count=1)
        r7_table6 = self._bird_route_table(sim, "r7", "t_bgp6", expect_count=1)

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["100.64.0.10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "100.64.0.1",
                    "nexthops": [{"gateway": "100.64.0.10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp4_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r7_table4 == correct_result, "Result for r7 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414)],
                        "BGP.local_pref": 750,
                        "BGP.next_hop": ["fc00:100::10"],
                        "BGP.origin": "IGP",
                    },
                    "bestpath": True,
                    "bgp_type": "i",
                    "from": "fc00:100::1",
                    "nexthops": [{"gateway": "fc00:100::10", "interface": "eth0"}],
                    "pref": 100,
                    "prefix_type": "unicast",
                    "protocol": "bgp6_AS65000_r1",
                    "since": helpers.bird_since_field(),
                    "type": ["BGP", "univ"],
                }
            ]
        }
        assert r7_table6 == correct_result, "Result for r7 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r8(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r8_table4 = self._bird_route_table(sim, "r8", "t_bgp4")
        r8_table6 = self._bird_route_table(sim, "r8", "t_bgp6")

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65008, 3, 3)],
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
        assert r8_table4 == correct_result, "Result for r8 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65008, 3, 3)],
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
        assert r8_table6 == correct_result, "Result for r8 BIRD t_bgp6 routing table does not match what it should be"

    def test_bird_table_bgp_r9(self, sim, helpers):
        """Test BIRD main bgp routing tables."""

        r8_table4 = self._bird_route_table(sim, "r9", "t_bgp4")
        r8_table6 = self._bird_route_table(sim, "r9", "t_bgp6")

        correct_result = {
            "100.64.101.0/24": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65009, 3, 3)],
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
        assert r8_table4 == correct_result, "Result for r9 BIRD t_bgp4 routing table does not match what it should be"

        correct_result = {
            "fc00:101::/48": [
                {
                    "asn": "AS65010",
                    "attributes": {
                        "BGP.as_path": [65000, 65010],
                        "BGP.large_community": [(65000, 3, 2), (65000, 4, 65414), (65009, 3, 3)],
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
        assert r8_table6 == correct_result, "Result for r9 BIRD t_bgp6 routing table does not match what it should be"
