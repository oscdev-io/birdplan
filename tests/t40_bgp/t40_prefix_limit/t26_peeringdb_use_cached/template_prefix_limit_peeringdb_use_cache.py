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
# pylint: disable=import-error,too-few-public-methods

"""BGP prefix limit test template."""

from typing import Any, List
import time
import pytest
from birdplan import peeringdb
from birdplan.exceptions import BirdPlanError
from ....basetests import BirdPlanBaseTestCase
from ....simulation import Simulation


class Template(BirdPlanBaseTestCase):
    """BGP prefix limit test template."""

    routers = ["r1"]
    exabgps = ["e1"]

    def _birdplan_run(  # pylint: disable=too-many-arguments,too-many-locals
        self, sim: Simulation, tmpdir: str, router: str, args: List[str]
    ) -> Any:
        """Run BirdPlan for a given router."""

        # Pre-populate cache
        peeringdb.peeringdb_cache = {
            "objects": {
                "asn:65001": {
                    "_timestamp": time.time() + 3600,
                    "value": {"info_prefixes4": 100, "info_prefixes6": 100},
                },
            }
        }

        # Save the global we have
        limit_save = peeringdb.PEERINGDB_16BIT_LOWER
        # Trigger a lookup for our private ASN
        peeringdb.PEERINGDB_16BIT_LOWER = 65002

        # Grab return result
        res = super()._birdplan_run(sim, tmpdir, router, args)

        # Restore global
        peeringdb.PEERINGDB_16BIT_LOWER = limit_save

        return res

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_peeringdb_reload(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Save the global we have
        limit_save = peeringdb.PEERINGDB_16BIT_LOWER
        # Trigger a lookup for our private ASN
        peeringdb.PEERINGDB_16BIT_LOWER = 65002

        # Rewrite configuration file
        super()._birdplan_run(sim, tmpdir, "r1", ["configure"])

        # Restore global
        peeringdb.PEERINGDB_16BIT_LOWER = limit_save

    def test_peeringdb_use_cached(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Check if we get an exception now during reconfiguration
        if getattr(self, "r1_peer_type") in ("customer", "peer"):
            super()._birdplan_run(sim, tmpdir, "r1", ["configure", "--use-cached"])

    def test_peeringdb_without_use_cached(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Check if we get an exception now during reconfiguration
        if getattr(self, "r1_peer_type") in ("customer", "peer"):
            with pytest.raises(
                BirdPlanError,
                match=r"No IPv4 PeeringDB information found for peer 'e1'",
            ):
                super()._birdplan_run(sim, tmpdir, "r1", ["configure"])
