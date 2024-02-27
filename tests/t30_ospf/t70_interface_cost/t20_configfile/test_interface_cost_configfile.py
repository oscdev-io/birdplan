#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2024, AllWorldIT
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

"""OSPF test case for interface cost using configuration file settings."""

from ..template import Template

__all__ = ["Test"]


class Test(Template):
    """OSPF test case for interface cost using configuration file settings."""

    r2_extra_config = """
          cost: 12
"""
    r3_extra_config = """
          cost: 12
"""

    r4_extra_config = """
          cost: 14
"""
    r5_extra_config = """
          cost: 14
"""

    r6_extra_config = """
          cost: 16
"""
    r7_extra_config = """
          cost: 16
"""

    def _test_interface_attributes(self, sim, tmpdir):
        """OSPF interface cost test to customize template."""
        # This is a configuration file test
