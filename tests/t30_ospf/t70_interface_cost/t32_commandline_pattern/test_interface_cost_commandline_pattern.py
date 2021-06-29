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

"""OSPF test case for interface cost using command line settings."""

import time
from ..template import Template


class Test(Template):
    """OSPF test case for interface cost using command line settings."""

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

        # Change eth1 cost on r4 to 12
        self._birdplan_run(sim, tmpdir, "r4", ["ospf", "interface", "cost", "set", "0", "eth*", "12"])

        # Check r4 status
        interface_status = self._birdplan_run(sim, tmpdir, "r4", ["ospf", "interface", "show"])
        assert interface_status == {
            "current": {
                "areas": {"0": {"interfaces": {"eth0": {"cost": 14, "ecmp_weight": 1}, "eth1": {"cost": 14, "ecmp_weight": 1}}}}
            },
            "overrides": {"areas": {"0": {"interfaces": {"eth*": {"cost": 12}}}}},
            "pending": {
                "areas": {"0": {"interfaces": {"eth0": {"cost": 12, "ecmp_weight": 1}, "eth1": {"cost": 12, "ecmp_weight": 1}}}}
            },
        }, "OSPF interface cost status is not correct"

        # Rewrite configuration file
        self._birdplan_run(sim, tmpdir, "r4", ["configure"])

        # Check r4 status again
        interface_status = self._birdplan_run(sim, tmpdir, "r4", ["ospf", "interface", "show"])
        assert interface_status == {
            "current": {
                "areas": {"0": {"interfaces": {"eth0": {"cost": 12, "ecmp_weight": 1}, "eth1": {"cost": 12, "ecmp_weight": 1}}}}
            },
            "overrides": {"areas": {"0": {"interfaces": {"eth*": {"cost": 12}}}}},
            "pending": {
                "areas": {"0": {"interfaces": {"eth0": {"cost": 12, "ecmp_weight": 1}, "eth1": {"cost": 12, "ecmp_weight": 1}}}}
            },
        }, "OSPF interface cost status is not correct"

        # Reconfigure BIRD
        self._birdc(sim, "r4", "configure")
        # Wait for BIRD to reply that it is up and running
        count = 0
        while True:
            # Grab status output
            status_output = self._birdc(sim, "r4", "show status")
            if "0013 Daemon is up and running" in status_output:
                break
            # Check for timeout
            if count > 10:
                break
            # If we're not up and running yet, sleep and increase count
            time.sleep(1)
            count += 1

        # Check if we're delaying testing (for convergeance)
        if sim.delay:
            time.sleep(sim.delay)
