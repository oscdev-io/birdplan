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

"""BGP AS-PATH AS deny test case template."""

from ..template_base import TemplateBase as TemplateSetBase

__all__ = ["TemplateBase"]


class TemplateBase(TemplateSetBase):
    """BGP AS-PATH AS deny test case template."""

    def r1_peer_extra_config(self):
        """Return extra peer configuration for R1 when peer is a customer."""
        # If this is not a customer just return no extra config
        if getattr(self, "r1_peer_type", "") != "customer":
            return ""
        # Return extra config for customer peer types
        return """
      import_filter:
        origin_asns: [65001]
"""

    def _test_announce_routes(self, sim):
        """Announce a BGP prefix with a differnt origin."""

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        # Full AS-PATH
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.2 as-path [ 65001 65002 65003 65004 65005 ] "
                f"large-community [{large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::2 as-path [ 65001 65002 65003 65004 65005 ] "
                f"large-community [{large_communities}]"
            ],
        )

        # Partial AS-PATH
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.102.0/24 next-hop 100.64.0.2 as-path [ 65001 65002 65004 65005 ] "
                f"large-community [{large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:102::/48 next-hop fc00:100::2 as-path [ 65001 65002 65004 65005 ] "
                f"large-community [{large_communities}]"
            ],
        )

        # Invalid ASN in AS-PATH
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.103.0/24 next-hop 100.64.0.2 as-path [ 65001 65002 65006 65004 65005 ] "
                f"large-community [{large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:103::/48 next-hop fc00:100::2 as-path [ 65001 65002 65006 65004 65005 ] "
                f"large-community [{large_communities}]"
            ],
        )

        # AS-PATH with just the extra 65003 to test DENY functionality
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.104.0/24 next-hop 100.64.0.2 as-path [ 65001 65003 ] "
                f"large-community [{large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:104::/48 next-hop fc00:100::2 as-path [ 65001 65003 ] "
                f"large-community [{large_communities}]"
            ],
        )

        # AS-PATH with just one ASN to test DENY functionality
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.105.0/24 next-hop 100.64.0.2 as-path [ 65001 ] "
                f"large-community [{large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:105::/48 next-hop fc00:100::2 as-path [ 65001 ] "
                f"large-community [{large_communities}]"
            ],
        )
