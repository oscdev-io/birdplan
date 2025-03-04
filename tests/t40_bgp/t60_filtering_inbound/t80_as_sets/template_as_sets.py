#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""BGP peer AS-SET filtered test case template."""

from .template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP peer AS-SET filtered test case template."""

    r1_template_peer_config = """
      filter:
        as_sets: "_BIRDPLAN:AS-SET"
"""

    def _test_announce_routes(self, sim):
        """Announce BGP prefixes."""

        # Announce routes from parent class
        super()._test_announce_routes(sim)

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        # Advertise an allowed prefix from the origin AS
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.2 as-path [ 65001 ] "
                f"large-community [{large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:0:101::/48 next-hop fc00:100::2 as-path [ 65001 ] "
                f"large-community [{large_communities}]"
            ],
        )

        # Advertise an allowed prefix from an invalid origin AS
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.102.0/24 next-hop 100.64.0.2 as-path [ 65001 65002 ] "
                f"large-community [{large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:0:102::/48 next-hop fc00:100::2 as-path [ 65001 65002 ] "
                f"large-community [{large_communities}]"
            ],
        )

        # Advertise an invalid prefix from a valid AS
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.121.0/24 next-hop 100.64.0.2 as-path [ 65001 65003 ] "
                f"large-community [{large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:0:121::/48 next-hop fc00:100::2 as-path [ 65001 65003 ] "
                f"large-community [{large_communities}]"
            ],
        )

        # Advertise an invalid prefix from the peer AS
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.131.0/24 next-hop 100.64.0.2 as-path [ 65001 ] "
                f"large-community [{large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:0:131::/48 next-hop fc00:100::2 as-path [ 65001 ] "
                f"large-community [{large_communities}]"
            ],
        )
