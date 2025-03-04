#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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
# pylint: disable=import-error,too-few-public-methods

"""OSPF test case for interface ECMP weight."""

import time

from ...basetests import BirdPlanBaseTestCase

__all__ = ["Template"]


class Template(BirdPlanBaseTestCase):
    """OSPF test case for interface ECMP weight."""

    routers = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]
    switches = ["s1", "s2", "s3", "s4", "s5", "s6"]

    r1_interfaces = ["eth0", "eth2"]
    r1_interface_eth2 = {"mac": "02:01:02:00:00:01", "ips": ["100.127.0.1/24", "fc00:127::1/48"]}

    r2_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
    r2_interface_eth0 = {"mac": "02:02:00:00:00:01", "ips": ["100.64.0.2/24", "fc00:100::2/64"]}
    r2_interface_eth1 = {"mac": "02:02:00:00:00:02", "ips": ["100.102.0.2/24", "fc00:102::2/64"]}
    r2_interface_eth2 = {"mac": "02:02:00:00:00:03", "ips": ["100.103.0.2/24", "fc00:103::2/64"]}
    r2_interface_eth3 = {"mac": "02:02:00:00:00:04", "ips": ["100.104.0.2/24", "fc00:104::2/64"]}
    r2_interface_eth4 = {"mac": "02:02:00:00:00:05", "ips": ["100.105.0.2/24", "fc00:105::2/64"]}
    r2_switch_eth1 = "s2"
    r2_switch_eth2 = "s3"
    r2_switch_eth3 = "s4"
    r2_switch_eth4 = "s5"

    r3_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
    r3_interface_eth0 = {"mac": "02:03:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}
    r3_interface_eth1 = {"mac": "02:03:00:00:00:02", "ips": ["100.102.0.3/24", "fc00:102::3/64"]}
    r3_interface_eth2 = {"mac": "02:03:00:00:00:03", "ips": ["100.103.0.3/24", "fc00:103::3/64"]}
    r3_interface_eth3 = {"mac": "02:03:00:00:00:04", "ips": ["100.104.0.3/24", "fc00:104::3/64"]}
    r3_interface_eth4 = {"mac": "02:03:00:00:00:05", "ips": ["100.105.0.3/24", "fc00:105::3/64"]}
    r3_switch_eth1 = "s2"
    r3_switch_eth2 = "s3"
    r3_switch_eth3 = "s4"
    r3_switch_eth4 = "s5"

    r4_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
    r4_interface_eth0 = {"mac": "02:04:00:00:00:01", "ips": ["100.64.0.4/24", "fc00:100::4/64"]}
    r4_interface_eth1 = {"mac": "02:04:00:00:00:02", "ips": ["100.102.0.4/24", "fc00:102::4/64"]}
    r4_interface_eth2 = {"mac": "02:04:00:00:00:03", "ips": ["100.103.0.4/24", "fc00:103::4/64"]}
    r4_interface_eth3 = {"mac": "02:04:00:00:00:04", "ips": ["100.104.0.4/24", "fc00:104::4/64"]}
    r4_interface_eth4 = {"mac": "02:04:00:00:00:05", "ips": ["100.105.0.4/24", "fc00:105::4/64"]}
    r4_switch_eth0 = "s1"
    r4_switch_eth1 = "s2"
    r4_switch_eth2 = "s3"
    r4_switch_eth3 = "s4"
    r4_switch_eth4 = "s5"

    r5_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
    r5_interface_eth0 = {"mac": "02:05:00:00:00:01", "ips": ["100.110.0.5/24", "fc00:200::5/64"]}
    r5_interface_eth1 = {"mac": "02:05:00:00:00:02", "ips": ["100.102.0.5/24", "fc00:102::5/64"]}
    r5_interface_eth2 = {"mac": "02:05:00:00:00:03", "ips": ["100.103.0.5/24", "fc00:103::5/64"]}
    r5_interface_eth3 = {"mac": "02:05:00:00:00:04", "ips": ["100.104.0.5/24", "fc00:104::5/64"]}
    r5_interface_eth4 = {"mac": "02:05:00:00:00:05", "ips": ["100.105.0.5/24", "fc00:105::5/64"]}
    r5_switch_eth0 = "s6"
    r5_switch_eth1 = "s2"
    r5_switch_eth2 = "s3"
    r5_switch_eth3 = "s4"
    r5_switch_eth4 = "s5"

    r6_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
    r6_interface_eth0 = {"mac": "02:06:00:00:00:01", "ips": ["100.110.0.6/24", "fc00:200::6/64"]}
    r6_interface_eth1 = {"mac": "02:06:00:00:00:02", "ips": ["100.102.0.6/24", "fc00:102::6/64"]}
    r6_interface_eth2 = {"mac": "02:06:00:00:00:03", "ips": ["100.103.0.6/24", "fc00:103::6/64"]}
    r6_interface_eth3 = {"mac": "02:06:00:00:00:04", "ips": ["100.104.0.6/24", "fc00:104::6/64"]}
    r6_interface_eth4 = {"mac": "02:06:00:00:00:05", "ips": ["100.105.0.6/24", "fc00:105::6/64"]}
    r6_switch_eth0 = "s6"
    r6_switch_eth1 = "s2"
    r6_switch_eth2 = "s3"
    r6_switch_eth3 = "s4"
    r6_switch_eth4 = "s5"

    r7_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
    r7_interface_eth0 = {"mac": "02:07:00:00:00:01", "ips": ["100.110.0.7/24", "fc00:200::7/64"]}
    r7_interface_eth1 = {"mac": "02:07:00:00:00:02", "ips": ["100.102.0.7/24", "fc00:102::7/64"]}
    r7_interface_eth2 = {"mac": "02:07:00:00:00:03", "ips": ["100.103.0.7/24", "fc00:103::7/64"]}
    r7_interface_eth3 = {"mac": "02:07:00:00:00:04", "ips": ["100.104.0.7/24", "fc00:104::7/64"]}
    r7_interface_eth4 = {"mac": "02:07:00:00:00:05", "ips": ["100.105.0.7/24", "fc00:105::7/64"]}
    r7_switch_eth0 = "s6"
    r7_switch_eth1 = "s2"
    r7_switch_eth2 = "s3"
    r7_switch_eth3 = "s4"
    r7_switch_eth4 = "s5"

    r8_interfaces = ["eth0"]
    r8_interface_eth0 = {"mac": "02:08:00:00:00:02", "ips": ["100.110.0.8/24", "fc00:200::8/64"]}
    r8_switch_eth0 = "s6"

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_cmdline_ospf_summary(self, sim, tmpdir: str) -> None:
        """Test BIRD cmdline for OSPF summary."""
        self._test_bird_cmdline_ospf_summary(sim, tmpdir)

    # Test configuration of interface ECMP weight
    def test_interface_attributes(self, sim, tmpdir):
        """OSPF interface ECMP weight test to customize template."""
        self._test_interface_attributes(sim, tmpdir)
        # NK: Wait again after interface attribute change to wait for settling
        if sim.delay:
            time.sleep(sim.delay)

    # Here is where the customizations take place per testcase
    def _test_interface_attributes(self, sim, tmpdir):
        """OSPF interface ECMP weight test to customize template."""
        raise NotImplementedError("This needs to be overridden")

    def test_bird_tables_ospf4(self, sim):
        """Test BIRD t_ospf4 table."""
        self._test_bird_routers_table(sim, "t_ospf4")

    def test_bird_tables_ospf6(self, sim):
        """Test BIRD t_ospf6 table."""
        self._test_bird_routers_table(sim, "t_ospf6")

    def test_bird_tables_master4(self, sim):
        """Test BIRD master4 table."""
        self._test_bird_routers_table(sim, "master4")

    def test_bird_tables_master6(self, sim):
        """Test BIRD master6 table."""
        self._test_bird_routers_table(sim, "master6")

    def test_bird_tables_static4(self, sim):
        """Test BIRD t_static4 table."""
        self._test_bird_routers_table(sim, "t_static4", routers=["r1"])

    def test_bird_tables_static6(self, sim):
        """Test BIRD t_static6 table."""
        self._test_bird_routers_table(sim, "t_static6", routers=["r1"])

    def test_bird_tables_kernel4(self, sim):
        """Test BIRD kernel4 table."""
        self._test_bird_routers_table(sim, "t_kernel4")

    def test_bird_tables_kernel6(self, sim):
        """Test BIRD kernel6 table."""
        self._test_bird_routers_table(sim, "t_kernel6")

    def test_os_rib_inet(self, sim):
        """Test OS RIB for inet."""
        self._test_os_rib(sim, "inet")

    def test_os_rib_inet6(self, sim):
        """Test OS RIB for inet6."""
        self._test_os_rib(sim, "inet6")
