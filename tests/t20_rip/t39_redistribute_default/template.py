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

"""RIP test case for redistribution of only the default route."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """RIP test case for redistribution of only the default route."""

    routers = ["r1", "r2", "r3"]
    switches = ["s1", "s2"]

    r1_interfaces = ["eth0", "eth2"]
    r1_interface_eth2 = {"mac": "02:01:02:00:00:01", "ips": ["100.201.0.1/24", "fc00:201::1/48"]}

    r2_interfaces = ["eth0", "eth1"]
    r2_switch_eth1 = "s2"

    r3_interface_eth0 = {"mac": "02:03:00:00:00:01", "ips": ["100.102.0.2/24", "fc00:102::2/64"]}
    r3_switch_eth0 = "s2"

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_add_kernel_routes(self, sim):
        """Add kernel routes to BIRD instances."""

        # Add gateway'd kernel routes
        sim.node("r1").run_ip(["route", "add", "100.121.0.0/24", "via", "100.201.0.3"])
        sim.node("r1").run_ip(["route", "add", "fc00:121::/48", "via", "fc00:201::3"])

        # Add kernel device routes
        sim.node("r1").run_ip(["route", "add", "100.122.0.0/24", "dev", "eth2"])
        sim.node("r1").run_ip(["route", "add", "fc00:122::/48", "dev", "eth2"])

        # Add kernel default routes
        sim.node("r1").run_ip(["route", "add", "default", "via", "100.201.0.3"])
        sim.node("r1").run_ip(["route", "add", "default", "via", "fc00:201::3"])

        # Add kernel blackhole routes
        sim.node("r1").run_ip(["route", "add", "blackhole", "100.123.0.0/31"])
        sim.node("r1").run_ip(["route", "add", "blackhole", "fc00:123::/127"])

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_tables_static4(self, sim):
        """Test BIRD t_static4 table stub."""
        self._test_bird_routers_table("t_static4", sim, routers=["r1"])

    def test_bird_tables_static6(self, sim):
        """Test BIRD t_static6 table stub."""
        self._test_bird_routers_table("t_static6", sim, routers=["r1"])

    def test_bird_tables_rip4(self, sim):
        """Test BIRD t_rip4 table."""
        self._test_bird_routers_table("t_rip4", sim)

    def test_bird_tables_rip6(self, sim):
        """Test BIRD t_rip6 table."""
        self._test_bird_routers_table("t_rip6", sim)

    def test_bird_tables_master4(self, sim):
        """Test BIRD master4 table."""
        self._test_bird_routers_table("master4", sim)

    def test_bird_tables_master6(self, sim):
        """Test BIRD master6 table."""
        self._test_bird_routers_table("master6", sim)

    def test_bird_tables_kernel4(self, sim):
        """Test BIRD kernel4 table."""
        self._test_bird_routers_table("t_kernel4", sim)

    def test_bird_tables_kernel6(self, sim):
        """Test BIRD kernel6 table."""
        self._test_bird_routers_table("t_kernel6", sim)

    def test_os_rib_inet(self, sim):
        """Test OS RIB for inet."""
        self._test_os_rib("inet", sim)

    def test_os_rib_inet6(self, sim):
        """Test OS RIB for inet6."""
        self._test_os_rib("inet6", sim)