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

"""RIP test case for redistribution of static default routes, with accept:default set to false."""

from ..template import Template


class Test(Template):
    """RIP test case for redistribution of static default routes, with accept:default set to false."""

    r1_extra_config = """
  redistribute:
    default: True
    static: True
"""
    r2_extra_config = """
  accept:
    default: False
"""

    def _test_bird_tables_static4(self, sim):
        """Test BIRD t_static4 table stub."""
        self._test_bird_routers_table("t_static4", sim, routers=["r1"])

    def _test_bird_tables_static6(self, sim):
        """Test BIRD t_static6 table stub."""
        self._test_bird_routers_table("t_static6", sim, routers=["r1"])