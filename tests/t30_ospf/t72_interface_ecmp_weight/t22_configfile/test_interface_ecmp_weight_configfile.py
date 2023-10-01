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

"""OSPF test case for interface ECMP weight using configuration file settings."""

from ..template import Template


class Test(Template):
    """OSPF test case for interface ECMP weight using configuration file settings."""

    r2_extra_config = """
          ecmp_weight: 2
"""
    r3_extra_config = """
          ecmp_weight: 2
"""
    r4_extra_config = """
          ecmp_weight: 2
"""

    r5_extra_config = """
          ecmp_weight: 2
"""
    r6_extra_config = """
          ecmp_weight: 2
"""
    r7_extra_config = """
          ecmp_weight: 2
"""

    def _test_interface_attributes(self, sim, tmpdir):
        """OSPF interface attribute test to customize template."""
        # This is a configuration file test
