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

"""BGP graceful shutdown test case template."""

import time

from ..template_base import TemplateBase


class Template(TemplateBase):
    """BGP graceful shutdown test case template."""

    r2_template_peer_config = """
      graceful_shutdown: True
"""

    def _test_graceful_shutdown(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Disable graceful shutdown on r2
        self._birdplan_run(sim, tmpdir, "r2", ["bgp", "peer", "graceful-shutdown", "set", "r1", "false"])

        # Check r2 status
        birdplan_result = self._birdplan_run(sim, tmpdir, "r2", ["bgp", "peer", "graceful-shutdown", "show"])

        graceful_shutdown_status = birdplan_result["raw"]
        assert graceful_shutdown_status == {
            "overrides": {"r1": False},
            "current": {"r1": True},
            "pending": {"r1": False},
        }, "Graceful shutdown status is not correct"

        # Rewrite configuration file
        self._birdplan_run(sim, tmpdir, "r2", ["configure"])

        # Check r2 status again
        birdplan_result = self._birdplan_run(sim, tmpdir, "r2", ["bgp", "peer", "graceful-shutdown", "show"])

        graceful_shutdown_status = birdplan_result["raw"]
        assert graceful_shutdown_status == {
            "overrides": {"r1": False},
            "current": {"r1": False},
            "pending": {"r1": False},
        }, "Graceful shutdown status is not correct"

        # Reconfigure BIRD
        self._birdc(sim, "r2", "configure")
        # Wait for BIRD to reply that it is up and running
        count = 0
        while True:
            # Grab status output
            status_output = self._birdc(sim, "r2", "show status")
            if "0013 Daemon is up and running" in status_output:
                break
            # Check for timeout
            if count > 10:
                break
            # If we're not up and running yet, sleep and increase count
            time.sleep(1)
            count += 1
