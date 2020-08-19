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

"""Basic static route test case."""

# pylint: disable=import-error,too-few-public-methods,no-self-use,too-many-locals

import pprint
from typing import Any, Dict, Optional
import pytest
from nsnetsim.topology import Topology
from nsnetsim.bird_router_node import BirdRouterNode, RouterNode
from nsnetsim.switch_node import SwitchNode
from birdplan import BirdPlan


class Simulation:
    """Simulation class, storing the topology and nodes."""

    config: Dict[str, str]
    topology: Topology
    router1: Optional[RouterNode]
    router2: Optional[RouterNode]

    def __init__(self):
        """Initialize object."""
        self.config = {}
        self.topology = Topology()
        self.router1 = None
        self.router2 = None


@pytest.fixture(name="sim", scope="class")
def fixture_sim():
    """Python fixture to create our simulation before running tests."""
    simulation = Simulation()

    yield simulation

    print("Destroying topology...")
    simulation.topology.destroy()

    return simulation


class TestBasicStatic:
    """Basic set of tests for static routing."""

    def test_configure(self, sim: Simulation, tmpdir: str):
        """Create our configuration files."""
        birdplan = BirdPlan()
        # Generate config files
        for router in ["r1", "r2"]:
            birdplan.load(f"tests/test_basic/test_basic_static-{router}.yaml", {"@TMPDIR@": f"{tmpdir}"})
            sim.config[router] = birdplan.generate(f"{tmpdir}/bird.conf.{router}")

    def test_basic_static(self, sim: Simulation, tmpdir: str, helpers):
        """Test basic static route configuration."""

        # Output router configuration
        for router in ["r1", "r2"]:
            print("CONFIG(%s):\n%s" % (router, sim.config[router]))

        print("Adding routers...")
        sim.router1 = BirdRouterNode(name="router1", configfile=f"{tmpdir}/bird.conf.r1")
        sim.topology.add_node(sim.router1)

        sim.router2 = BirdRouterNode(name="router2", configfile=f"{tmpdir}/bird.conf.r2")
        sim.topology.add_node(sim.router2)

        print("Adding interfaces...")
        router1_eth0 = sim.router1.add_interface("eth0", mac="02:01:00:00:00:01")
        router2_eth0 = sim.router2.add_interface("eth0", mac="02:01:00:00:00:01")

        print("Adding IPs...")
        router1_eth0.add_ip(["192.168.0.1/24", "fc00::1/64"])
        router2_eth0.add_ip(["192.168.0.1/24", "fc00::1/64"])

        print("Adding switches...")
        switch_a = SwitchNode("switchA")
        sim.topology.add_node(switch_a)
        switch_a.add_interface(router1_eth0)

        switch_b = SwitchNode("switchB")
        sim.topology.add_node(switch_b)
        switch_b.add_interface(router2_eth0)

        # Simulate our topology
        print("Simulate topology...")
        sim.topology.run()

        # Grab data for testing
        r1_status_output = sim.router1.birdc_show_status()
        r1_protocols_output = sim.router1.birdc_show_protocols()

        r2_status_output = sim.router2.birdc_show_status()
        r2_protocols_output = sim.router2.birdc_show_protocols()

        # BIRD tables
        r1_bird_tables = {}
        r2_bird_tables = {}
        for bird_table in ["t_static4", "t_static6", "master4", "master6", "t_kernel4", "t_kernel6"]:
            r1_bird_tables[bird_table] = sim.router1.birdc_show_route_table(bird_table)
            r2_bird_tables[bird_table] = sim.router2.birdc_show_route_table(bird_table)

        # OS RIB
        r1_os_rib = {}
        r2_os_rib = {}
        for os_rib in ["inet", "inet6"]:
            r1_os_rib[os_rib] = sim.router1.run_ip(["--family", os_rib, "route", "list"])
            r2_os_rib[os_rib] = sim.router2.run_ip(["--family", os_rib, "route", "list"])

        print("PROTOCOLS(r1):")
        pprint.pprint(r1_protocols_output)
        print("PROTOCOLS(r2):")
        pprint.pprint(r2_protocols_output)

        for table, contents in sorted(r1_bird_tables.items()):
            print(f"BIRD(r1)[{table}]:")
            pprint.pprint(contents)
        for table, contents in sorted(r2_bird_tables.items()):
            print(f"BIRD(r2)[{table}]:")
            pprint.pprint(contents)

        for table, contents in sorted(r1_os_rib.items()):
            print(f"OS(r1)[{table}]:")
            pprint.pprint(contents)
        for table, contents in sorted(r2_os_rib.items()):
            print(f"OS(r2)[{table}]:")
            pprint.pprint(contents)

        # Check BIRD router ID
        assert "router_id" in r1_status_output, "The status output should have 'router_id'"
        assert r1_status_output["router_id"] == "0.0.0.1", "The router ID should be '0.0.0.1'"

        assert "router_id" in r2_status_output, "The status output should have 'router_id'"
        assert r2_status_output["router_id"] == "0.0.0.1", "The router ID should be '0.0.0.1'"

        correct_result: Any

        # Check static4 BIRD table
        correct_result = {
            "10.0.0.0/24": [
                {
                    "nexthops": [{"gateway": "192.168.0.2", "interface": "eth0"}],
                    "pref": "200",
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert (
            r1_bird_tables["t_static4"] == correct_result
        ), "Result for R1 BIRD t_static4 routing table does not match what it should be"
        assert (
            r2_bird_tables["t_static4"] == correct_result
        ), "Result for R2 BIRD t_static4 routing table does not match what it should be"

        # Check static6 BIRD table
        correct_result = {
            "fc10::/64": [
                {
                    "nexthops": [{"gateway": "fc00::2", "interface": "eth0"}],
                    "pref": "200",
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert (
            r1_bird_tables["t_static6"] == correct_result
        ), "Result for R1 BIRD t_static6 routing table does not match what it should be"
        assert (
            r2_bird_tables["t_static6"] == correct_result
        ), "Result for R2 BIRD t_static6 routing table does not match what it should be"

        # Check master4 BIRD table
        correct_result = {
            "10.0.0.0/24": [
                {
                    "nexthops": [{"gateway": "192.168.0.2", "interface": "eth0"}],
                    "pref": "200",
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert (
            r1_bird_tables["master4"] == correct_result
        ), "Result for R1 BIRD master4 routing table does not match what it should be"
        assert (
            r2_bird_tables["master4"] == correct_result
        ), "Result for R2 BIRD master4 routing table does not match what it should be"

        # Check master6 BIRD table
        correct_result = {
            "fc10::/64": [
                {
                    "nexthops": [{"gateway": "fc00::2", "interface": "eth0"}],
                    "pref": "200",
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert (
            r1_bird_tables["master6"] == correct_result
        ), "Result for R1 BIRD master6 routing table does not match what it should be"
        assert (
            r2_bird_tables["master6"] == correct_result
        ), "Result for R2 BIRD master6 routing table does not match what it should be"

        # Check kernel4 BIRD table
        correct_result = {
            "10.0.0.0/24": [
                {
                    "nexthops": [{"gateway": "192.168.0.2", "interface": "eth0"}],
                    "pref": "200",
                    "prefix_type": "unicast",
                    "protocol": "static4",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert (
            r1_bird_tables["t_kernel4"] == correct_result
        ), "Result for R1 BIRD t_kernel4 routing table does not match what it should be"

        correct_result = {}
        assert (
            r2_bird_tables["t_kernel4"] == correct_result
        ), "Result for R2 BIRD t_kernel4 routing table does not match what it should be"

        # Check kernel6 BIRD table
        correct_result = {
            "fc10::/64": [
                {
                    "nexthops": [{"gateway": "fc00::2", "interface": "eth0"}],
                    "pref": "200",
                    "prefix_type": "unicast",
                    "protocol": "static6",
                    "since": helpers.bird_since_field(),
                    "type": ["static", "univ"],
                }
            ]
        }
        assert (
            r1_bird_tables["t_kernel6"] == correct_result
        ), "Result for R1 BIRD t_kernel6 routing table does not match what it should be"

        correct_result = {}
        assert (
            r2_bird_tables["t_kernel6"] == correct_result
        ), "Result for R2 BIRD t_kernel6 routing table does not match what it should be"

        # Check kernel has the correct IPv4 RIB
        correct_result = [
            {"dev": "eth0", "dst": "10.0.0.0/24", "flags": [], "gateway": "192.168.0.2", "metric": 600, "protocol": "bird"},
            {"dev": "eth0", "dst": "192.168.0.0/24", "flags": [], "prefsrc": "192.168.0.1", "protocol": "kernel", "scope": "link"},
        ]
        assert r1_os_rib["inet"] == correct_result, "R1 kernel IPv4 RIB does not match what it should be"

        correct_result = [
            {"dev": "eth0", "dst": "192.168.0.0/24", "flags": [], "prefsrc": "192.168.0.1", "protocol": "kernel", "scope": "link"},
        ]
        assert r2_os_rib["inet"] == correct_result, "R2 kernel IPv4 RIB does not match what it should be"

        # Check kernel has the correct IPv6 RIB
        correct_result = [
            {"dev": "eth0", "dst": "fc00::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {
                "dev": "eth0",
                "dst": "fc10::/64",
                "flags": [],
                "gateway": "fc00::2",
                "metric": 600,
                "pref": "medium",
                "protocol": "bird",
            },
            {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
        ]
        assert r1_os_rib["inet6"] == correct_result, "R1 Kernel IPv6 RIB does not match what it should be"

        correct_result = [
            {"dev": "eth0", "dst": "fc00::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
        ]
        assert r2_os_rib["inet6"] == correct_result, "R2 Kernel IPv6 RIB does not match what it should be"
