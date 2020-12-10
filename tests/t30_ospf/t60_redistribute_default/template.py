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

"""OSPF test case for redistribution of only the default route."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """OSPF test case for redistribution of only the default route."""

    routers = ["r1", "r2"]
    switches = ["s1"]

    r1_interfaces = ["eth0", "eth1"]

    r2_interfaces = ["eth0"]

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_add_kernel_routes(self, sim):
        """Add kernel routes."""

        # Add gateway'd kernel routes
        sim.node("r1").run_ip(["route", "add", "192.168.20.0/24", "via", "100.101.0.2"])
        sim.node("r1").run_ip(["route", "add", "fc20::/64", "via", "fc00:101::2"])
        # Add link kernel routes
        sim.node("r1").run_ip(["route", "add", "192.168.30.0/24", "dev", "eth1"])
        sim.node("r1").run_ip(["route", "add", "fc30::/64", "dev", "eth1"])
        # Add default kernel route
        sim.node("r1").run_ip(["route", "add", "0.0.0.0/0", "via", "100.101.0.2"])
        sim.node("r1").run_ip(["route", "add", "::/0", "via", "fc00:101::2"])

    def _test_setup_specific(self, sim, tmpdir):
        """Set up our test - specific additions."""

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_tables_ospf4(self, sim):
        """Test BIRD t_ospf4 table."""
        self._test_bird_routers_table("t_ospf4", sim)

    def test_bird_tables_ospf6(self, sim):
        """Test BIRD t_ospf6 table."""
        self._test_bird_routers_table("t_ospf6", sim)

    def test_bird_tables_master4(self, sim):
        """Test BIRD master4 table."""
        self._test_bird_routers_table("master4", sim)

    def test_bird_tables_master6(self, sim):
        """Test BIRD master6 table."""
        self._test_bird_routers_table("master6", sim)

    def test_bird_tables_static4(self, sim):
        """Test BIRD t_static4 table."""
        self._test_bird_routers_table("t_static4", sim, routers=["r1"])

    def test_bird_tables_static6(self, sim):
        """Test BIRD t_static6 table."""
        self._test_bird_routers_table("t_static6", sim, routers=["r1"])

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
