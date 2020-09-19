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

"""RIP test case for redistribution of connected routes with star."""

from ...basetests import BirdPlanBaseTestCase


class Template(BirdPlanBaseTestCase):
    """RIP test case for redistribution of connected routes with star."""

    routers = ["r1", "r2"]
    r1_interfaces = ["eth0", "eth1", "eth2", "eth10"]
    r1_interface_eth2 = {"mac": "02:01:02:00:00:01", "ips": ["100.201.0.1/24", "fc00:201::1/64"]}
    r1_interface_eth10 = {"mac": "02:01:10:00:00:01", "ips": ["100.211.0.1/24", "fc00:211::1/64"]}

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_tables_direct4_rip(self, sim, testpath):
        """Test BIRD t_direct4_rip table."""
        self._test_bird_table("t_direct4_rip", sim, testpath, routers=["r1"])

    def test_bird_tables_direct6_rip(self, sim, testpath):
        """Test BIRD t_direct6_rip table."""
        self._test_bird_table("t_direct6_rip", sim, testpath, routers=["r1"])

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
