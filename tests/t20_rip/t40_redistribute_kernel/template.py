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

"""RIP test case for redistribution of kernel routes."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """RIP test case for redistribution of kernel routes."""

    routers = ["r1", "r2"]
    r1_interfaces = ["eth0", "eth1"]

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

        # Add gateway'd kernel static routes
        sim.node("r1").run_ip(["route", "add", "192.168.20.0/24", "via", "100.101.0.2"])
        sim.node("r1").run_ip(["route", "add", "fc20::/64", "via", "fc00:101::2"])
        # Add link kernel static routes
        sim.node("r1").run_ip(["route", "add", "192.168.30.0/24", "dev", "eth1"])
        sim.node("r1").run_ip(["route", "add", "fc30::/64", "dev", "eth1"])

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_tables_rip4(self, sim, testpath):
        """Test BIRD t_rip4 table."""
        self._test_bird_table("t_rip4", sim, testpath)

    def test_bird_tables_rip6(self, sim, testpath):
        """Test BIRD t_rip6 table."""
        self._test_bird_table("t_rip6", sim, testpath)

    def test_bird_tables_master4(self, sim, testpath):
        """Test BIRD master4 table."""
        self._test_bird_table("master4", sim, testpath)

    def test_bird_tables_master6(self, sim, testpath):
        """Test BIRD master6 table."""
        self._test_bird_table("master6", sim, testpath)

    def test_bird_tables_kernel4(self, sim, testpath):
        """Test BIRD kernel4 table."""
        self._test_bird_table("t_kernel4", sim, testpath)

    def test_bird_tables_kernel6(self, sim, testpath):
        """Test BIRD kernel6 table."""
        self._test_bird_table("t_kernel6", sim, testpath)

    def test_os_fib_inet(self, sim, testpath):
        """Test OS FIB for inet."""
        self._test_os_fib("inet", sim, testpath)

    def test_os_fib_inet6(self, sim, testpath):
        """Test OS FIB for inet6."""
        self._test_os_fib("inet6", sim, testpath)
