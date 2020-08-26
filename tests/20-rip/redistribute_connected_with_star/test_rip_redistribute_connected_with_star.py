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

"""RIP test for redistributed connected routes using a star."""

# pylint: disable=import-error,too-few-public-methods,no-self-use

import os
import pytest
from nsnetsim.exceptions import NsNetSimError
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.switch_node import SwitchNode
from basetests import BirdPlanBaseTestCase


class TestRIPRedistributeConnectedWithStar(BirdPlanBaseTestCase):
    """RIP test for redistributed connected routes using a star."""

    test_dir = os.path.dirname(__file__)
    routers = ["r1", "r2"]

    def test_configure(self, sim, tmpdir):
        """Create our configuration files."""
        super()._test_configure(sim, tmpdir)

    def test_create_topology(self, sim, tmpdir):
        """Test topology creation."""

        print("Adding routers...")
        sim.add_node(BirdRouterNode(name="r1", configfile=f"{tmpdir}/bird.conf.r1"))
        sim.add_node(BirdRouterNode(name="r2", configfile=f"{tmpdir}/bird.conf.r2"))

        print("Adding interfaces...")
        sim.node("r1").add_interface("eth0", mac="02:01:00:00:00:01", ips=["192.168.0.1/24", "fc00::1/64"])
        sim.node("r1").add_interface("eth10", mac="02:01:00:00:00:02", ips=["192.168.1.1/24", "fc01::1/64"])
        sim.node("r2").add_interface("eth0", mac="02:02:00:00:00:01", ips=["192.168.0.2/24", "fc00::2/64"])

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

    def test_bird_tables_direct4(self, sim, helpers):
        """Test BIRD direct4_rip table."""

        r1_table = self._bird_route_table(sim, "r1", "t_direct4_rip", expect_count=1)
        # There is no direct4_rip table for r2
        with pytest.raises(NsNetSimError, match=r".* CF_SYM_UNDEFINED, .*"):
            sim.node("r2").birdc_show_route_table("t_direct4_rip")

        # Check direct4_rip BIRD table
        correct_result = {
            "192.168.1.0/24": [
                {
                    "nexthops": [{"interface": "eth10"}],
                    "pref": "240",
                    "prefix_type": "unicast",
                    "protocol": "direct4_rip",
                    "since": helpers.bird_since_field(),
                    "type": ["device", "univ"],
                }
            ]
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_direct4_rip routing table does not match what it should be"

    def test_bird_tables_direct6(self, sim, helpers):
        """Test BIRD direct6_rip table."""

        r1_table = self._bird_route_table(sim, "r1", "t_direct6_rip", expect_count=1)
        # There is no direct6_rip table for r2
        with pytest.raises(NsNetSimError, match=r".* CF_SYM_UNDEFINED, .*"):
            sim.node("r2").birdc_show_route_table("t_direct6_rip")

        # Check direct6_rip BIRD table
        correct_result = {
            "fc01::/64": [
                {
                    "nexthops": [{"interface": "eth10"}],
                    "pref": "240",
                    "prefix_type": "unicast",
                    "protocol": "direct6_rip",
                    "since": helpers.bird_since_field(),
                    "type": ["device", "univ"],
                }
            ]
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_direct6_rip routing table does not match what it should be"

    def test_bird_tables_static4(self, sim):
        """Test BIRD static4 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_static4")
        r2_table = self._bird_route_table(sim, "r2", "t_static4")

        # Check static4 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD t_static4 routing table does not match what it should be"
        assert r2_table == correct_result, "Result for R2 BIRD t_static4 routing table does not match what it should be"

    def test_bird_tables_static6(self, sim):
        """Test BIRD static6 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_static6")
        r2_table = self._bird_route_table(sim, "r2", "t_static6")

        # Check static6 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD t_static6 routing table does not match what it should be"
        assert r2_table == correct_result, "Result for R2 BIRD t_static6 routing table does not match what it should be"

    def test_bird_tables_master4(self, sim, helpers):
        """Test BIRD master4 table."""

        r1_table = self._bird_route_table(sim, "r1", "master4")
        r2_table = self._bird_route_table(sim, "r2", "master4", expect_count=1)

        # Check master4 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD master4 routing table does not match what it should be"

        correct_result = {
            "192.168.1.0/24": [
                {
                    "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
                    "metric1": "3",
                    "nexthops": [{"gateway": "192.168.0.1", "interface": "eth0"}],
                    "pref": "120",
                    "prefix_type": "unicast",
                    "protocol": "rip4",
                    "since": helpers.bird_since_field(),
                    "type": ["RIP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, "Result for R2 BIRD master4 routing table does not match what it should be"

    def test_bird_tables_master6(self, sim, helpers):
        """Test BIRD master6 table."""

        r1_table = self._bird_route_table(sim, "r1", "master6")
        r2_table = self._bird_route_table(sim, "r2", "master6", expect_count=1)

        # Check master6 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD master6 routing table does not match what it should be"

        correct_result = {
            "fc01::/64": [
                {
                    "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
                    "metric1": "3",
                    "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
                    "pref": "120",
                    "prefix_type": "unicast",
                    "protocol": "rip6",
                    "since": helpers.bird_since_field(),
                    "type": ["RIP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, "Result for R2 BIRD master6 routing table does not match what it should be"

    def test_bird_tables_rip4(self, sim, helpers):
        """Test BIRD rip4 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_rip4", expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", "t_rip4", expect_count=1)

        # Check rip4 BIRD tables
        correct_result = {
            "192.168.1.0/24": [
                {
                    "nexthops": [{"interface": "eth10"}],
                    "pref": "240",
                    "prefix_type": "unicast",
                    "protocol": "direct4_rip",
                    "since": helpers.bird_since_field(),
                    "type": ["device", "univ"],
                }
            ]
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_rip4 routing table does not match what it should be"

        correct_result = {
            "192.168.1.0/24": [
                {
                    "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
                    "metric1": "3",
                    "nexthops": [{"gateway": "192.168.0.1", "interface": "eth0"}],
                    "pref": "120",
                    "prefix_type": "unicast",
                    "protocol": "rip4",
                    "since": helpers.bird_since_field(),
                    "type": ["RIP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_rip4 routing table does not match what it should be"

    def test_bird_tables_rip6(self, sim, helpers):
        """Test BIRD rip6 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_rip6", expect_count=1)
        r2_table = self._bird_route_table(sim, "r2", "t_rip6", expect_count=1)

        # Check rip6 BIRD tables
        correct_result = {
            "fc01::/64": [
                {
                    "nexthops": [{"interface": "eth10"}],
                    "pref": "240",
                    "prefix_type": "unicast",
                    "protocol": "direct6_rip",
                    "since": helpers.bird_since_field(),
                    "type": ["device", "univ"],
                }
            ]
        }
        assert r1_table == correct_result, "Result for R1 BIRD t_rip6 routing table does not match what it should be"

        correct_result = {
            "fc01::/64": [
                {
                    "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
                    "metric1": "3",
                    "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
                    "pref": "120",
                    "prefix_type": "unicast",
                    "protocol": "rip6",
                    "since": helpers.bird_since_field(),
                    "type": ["RIP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_rip6 routing table does not match what it should be"

    def test_bird_tables_kernel4(self, sim, helpers):
        """Test BIRD kernel4 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_kernel4")
        r2_table = self._bird_route_table(sim, "r2", "t_kernel4", expect_count=1)

        # Check kernel4 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD t_kernel4 routing table does not match what it should be"

        correct_result = {
            "192.168.1.0/24": [
                {
                    "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
                    "metric1": "3",
                    "nexthops": [{"gateway": "192.168.0.1", "interface": "eth0"}],
                    "pref": "120",
                    "prefix_type": "unicast",
                    "protocol": "rip4",
                    "since": helpers.bird_since_field(),
                    "type": ["RIP", "univ"],
                }
            ]
        }
        assert r2_table == correct_result, "Result for R2 BIRD t_kernel4 routing table does not match what it should be"

    def test_bird_tables_kernel6(self, sim, helpers):
        """Test BIRD kernel6 table."""

        r1_table = self._bird_route_table(sim, "r1", "t_kernel6")
        r2_table = self._bird_route_table(sim, "r2", "t_kernel6", expect_count=1)

        # Check kernel6 BIRD table
        correct_result = {}
        assert r1_table == correct_result, "Result for R1 BIRD t_kernel6 routing table does not match what it should be"

        correct_result = {
            "fc01::/64": [
                {
                    "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
                    "metric1": "3",
                    "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
                    "pref": "120",
                    "prefix_type": "unicast",
                    "protocol": "rip6",
                    "since": helpers.bird_since_field(),
                    "type": ["RIP", "univ"],
                }
            ]
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
            {"dev": "eth0", "dst": "192.168.0.0/24", "flags": [], "prefsrc": "192.168.0.1", "protocol": "kernel", "scope": "link"},
            {
                "dev": "eth10",
                "dst": "192.168.1.0/24",
                "flags": [],
                "prefsrc": "192.168.1.1",
                "protocol": "kernel",
                "scope": "link",
            },
        ]
        assert r1_os_rib == correct_result, "R1 kernel IPv4 RIB does not match what it should be"

        correct_result = [
            {"dev": "eth0", "dst": "192.168.0.0/24", "flags": [], "prefsrc": "192.168.0.2", "protocol": "kernel", "scope": "link"},
            {"dev": "eth0", "dst": "192.168.1.0/24", "flags": [], "gateway": "192.168.0.1", "metric": 600, "protocol": "bird"},
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
            {"dev": "eth0", "dst": "fc00::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth10", "dst": "fc01::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {"dev": "eth10", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
        ]
        assert r1_os_rib == correct_result, "R1 Kernel IPv6 RIB does not match what it should be"

        correct_result = [
            {"dev": "eth0", "dst": "fc00::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
            {
                "dev": "eth0",
                "dst": "fc01::/64",
                "flags": [],
                "gateway": "fe80::1:ff:fe00:1",
                "metric": 600,
                "pref": "medium",
                "protocol": "bird",
            },
            {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
        ]
        assert r2_os_rib == correct_result, "R2 Kernel IPv6 RIB does not match what it should be"