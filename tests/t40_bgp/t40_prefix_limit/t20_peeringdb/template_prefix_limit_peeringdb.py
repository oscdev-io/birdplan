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

"""BGP prefix limit test template."""

import time
from typing import Any, List

from birdplan import peeringdb

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
                    "value": {"info_prefixes4": 5, "info_prefixes6": 5},
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

    def test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.104.0/21 next-hop 100.64.0.2 split /24 "
                f"large-community [{large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:104::/45 next-hop fc00:100::2 split /48 "
                f"large-community [{large_communities}]"
            ],
        )

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_route_limit_exceeded(self, sim):
        """Check logs to see if we reached the prefix limit."""

        # Skip over configuration exceptions for this test
        if "r1" in self.routers_config_exception and self.routers_config_exception:
            return

        # We're only interested in testing out customer and peer peer types
        if getattr(self, "r1_peer_type", None) in ("customer", "peer"):
            route_limit_exceeded = self._bird_log_matches(sim, "r1", r"bgp4_AS65001_e1: Route limit exceeded, shutting down")
            assert route_limit_exceeded, "Failed to shut down IPv4 connection when route limit exceeded"

            route_limit_exceeded = self._bird_log_matches(sim, "r1", r"bgp6_AS65001_e1: Route limit exceeded, shutting down")
            assert route_limit_exceeded, "Failed to shut down IPv6 connection when route limit exceeded"
