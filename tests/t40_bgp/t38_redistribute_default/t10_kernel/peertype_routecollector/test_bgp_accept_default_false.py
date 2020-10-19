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

"""BGP test case for redistribution of kernel default routes, with accept:default set to false."""

from ...template import Template


class Test(Template):
    """BGP test case for redistribution of kernel default routes, with accept:default set to false."""

    routers_config_exception = {
        "r1": r"Having 'redistribute\[default\]' as True for peer 'r2' with type 'routecollector' makes no sense",
        "r2": r"Having 'accept\[default\]' as True for peer 'r1' with type 'routecollector' makes no sense",
    }

    r1_peer_type = "routecollector"
    r1_peer_config = """
      redistribute:
        default: True
        kernel: True
"""

    r2_peer_type = "routecollector"
    r2_global_config = """
  accept:
    default: False
"""
    r2_peer_config = """
      accept:
        default: True
"""

    def _test_setup_specific(self, sim, tmpdir):
        """Set up our test - specific additions."""
        # We cannot add a route to r1 due to invalid configuration
        # sim.node("r1").run_ip(["route", "add", "0.0.0.0/0", "via", "100.101.0.2"])
        # sim.node("r1").run_ip(["route", "add", "::/0", "via", "fc00:101::2"])
