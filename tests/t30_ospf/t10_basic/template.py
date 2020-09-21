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

"""OSPF basic test case template."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """OSPF basic test case template."""

    routers = ["r1", "r2"]
    r1_interfaces = ["eth0", "eth1"]

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_tables_static4(self, sim, testpath):
        """Test BIRD t_static4 table."""
        self._test_bird_routers_table("t_static4", sim, testpath, routers=["r1"])

    def test_bird_tables_static6(self, sim, testpath):
        """Test BIRD t_static6 table."""
        self._test_bird_routers_table("t_static6", sim, testpath, routers=["r1"])

    def test_bird_tables_ospf4(self, sim, testpath):
        """Test BIRD t_ospf4 table."""
        self._test_bird_routers_table("t_ospf4", sim, testpath)

    def test_bird_tables_ospf6(self, sim, testpath):
        """Test BIRD t_ospf6 table."""
        self._test_bird_routers_table("t_ospf6", sim, testpath)

    def test_bird_tables_master4(self, sim, testpath):
        """Test BIRD master4 table."""
        self._test_bird_routers_table("master4", sim, testpath)

    def test_bird_tables_master6(self, sim, testpath):
        """Test BIRD master6 table."""
        self._test_bird_routers_table("master6", sim, testpath)

    def test_bird_tables_kernel4(self, sim, testpath):
        """Test BIRD kernel4 table."""
        self._test_bird_routers_table("t_kernel4", sim, testpath)

    def test_bird_tables_kernel6(self, sim, testpath):
        """Test BIRD kernel6 table."""
        self._test_bird_routers_table("t_kernel6", sim, testpath)

    def test_os_fib_inet(self, sim, testpath):
        """Test OS FIB for inet."""
        self._test_os_fib("inet", sim, testpath)

    def test_os_fib_inet6(self, sim, testpath):
        """Test OS FIB for inet6."""
        self._test_os_fib("inet6", sim, testpath)
