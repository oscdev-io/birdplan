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

"""BGP quarantine test case template."""

import time
from ..template_base import TemplateBase


class Template(TemplateBase):
    """BGP quarantine test case template."""

    def _test_quarantine(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Add all peers to quarantine list
        self._birdplan_run(sim, tmpdir, "r1", ["bgp", "peer", "quarantine", "set", "*", "true"])

        # Check r2 status
        quarantine_status = self._birdplan_run(sim, tmpdir, "r1", ["bgp", "peer", "quarantine", "show"])
        assert quarantine_status == {
            "overrides": {"*": True},
            "current": {"r2": False},
            "pending": {"r2": True},
        }, "Graceful shutdown status is not correct"

        # Rewrite configuration file
        self._birdplan_run(sim, tmpdir, "r1", ["configure"])

        # Check r2 status again
        quarantine_status = self._birdplan_run(sim, tmpdir, "r1", ["bgp", "peer", "quarantine", "show"])
        assert quarantine_status == {
            "overrides": {"*": True},
            "current": {"r2": True},
            "pending": {"r2": True},
        }, "Graceful shutdown status is not correct"

        # Reconfigure BIRD
        self._birdc(sim, "r1", "configure")
        # Wait for BIRD to reply that it is up and running
        count = 0
        while True:
            # Grab status output
            status_output = self._birdc(sim, "r1", "show status")
            if "0013 Daemon is up and running" in status_output:
                break
            # Check for timeout
            if count > 10:
                break
            # If we're not up and running yet, sleep and increase count
            time.sleep(1)
            count += 1
