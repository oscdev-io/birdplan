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

"""BGP test case for redistribution of static default routes, with accept:default set to true."""

from ...template import Template


class Test(Template):
    """BGP test case for redistribution of static default routes, with accept:default set to true."""

    routers_config_exception = {
        "r1": r"Having 'redistribute:default' set for peer 'r2' with type 'transit' makes no sense",
    }

    r1_peer_type = "transit"
    r1_peer_config = """
      redistribute:
        default: True
        static: True
"""

    r2_peer_type = "transit"
    r2_global_config = """
  accept:
    default: True
"""
    r2_peer_config = """
      accept:
        default: True
"""
