#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
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

"""OSPF test case for interface cost."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """OSPF test case for interface cost."""

    routers = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]
    switches = ["s1", "s2"]

    r1_interfaces = ["eth0", "eth2"]
    r1_interface_eth2 = {"mac": "02:01:02:00:00:01", "ips": ["100.201.0.1/24", "fc00:201::1/48"]}

    r2_interfaces = ["eth0", "eth1"]
    r2_interface_eth0 = {"mac": "02:02:00:00:00:01", "ips": ["100.64.0.2/24", "fc00:100::2/64"]}
    r2_interface_eth1 = {"mac": "02:02:00:00:00:02", "ips": ["100.102.0.2/24", "fc00:102::2/64"]}
    r2_switch_eth1 = "s2"

    r3_interfaces = ["eth0", "eth1"]
    r3_interface_eth0 = {"mac": "02:03:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}
    r3_interface_eth1 = {"mac": "02:03:00:00:00:02", "ips": ["100.102.0.3/24", "fc00:102::3/64"]}
    r3_switch_eth1 = "s2"

    r4_interfaces = ["eth0", "eth1"]
    r4_interface_eth0 = {"mac": "02:04:00:00:00:01", "ips": ["100.64.0.4/24", "fc00:100::4/64"]}
    r4_interface_eth1 = {"mac": "02:04:00:00:00:02", "ips": ["100.102.0.4/24", "fc00:102::4/64"]}
    r4_switch_eth0 = "s1"
    r4_switch_eth1 = "s2"

    r5_interfaces = ["eth0", "eth1"]
    r5_interface_eth0 = {"mac": "02:05:00:00:00:01", "ips": ["100.64.0.5/24", "fc00:100::5/64"]}
    r5_interface_eth1 = {"mac": "02:05:00:00:00:02", "ips": ["100.102.0.5/24", "fc00:102::5/64"]}
    r5_switch_eth0 = "s1"
    r5_switch_eth1 = "s2"

    r6_interfaces = ["eth0", "eth1"]
    r6_interface_eth0 = {"mac": "02:06:00:00:00:01", "ips": ["100.64.0.6/24", "fc00:100::6/64"]}
    r6_interface_eth1 = {"mac": "02:06:00:00:00:02", "ips": ["100.102.0.6/24", "fc00:102::6/64"]}
    r6_switch_eth0 = "s1"
    r6_switch_eth1 = "s2"

    r7_interfaces = ["eth0", "eth1"]
    r7_interface_eth0 = {"mac": "02:07:00:00:00:01", "ips": ["100.64.0.7/24", "fc00:100::7/64"]}
    r7_interface_eth1 = {"mac": "02:07:00:00:00:02", "ips": ["100.102.0.7/24", "fc00:102::7/64"]}
    r7_switch_eth0 = "s1"
    r7_switch_eth1 = "s2"

    r8_interfaces = ["eth0"]
    r8_interface_eth0 = {"mac": "02:08:00:00:00:02", "ips": ["100.102.0.8/24", "fc00:102::8/64"]}
    r8_switch_eth0 = "s2"

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    # Test configuration of interface cost
    def test_interface_attributes(self, sim, tmpdir):
        """OSPF interface cost test to customize template."""
        self._test_interface_attributes(sim, tmpdir)

    # Here is where the customizations take place per testcase
    def _test_interface_attributes(self, sim, tmpdir):
        """OSPF interface cost test to customize template."""
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
