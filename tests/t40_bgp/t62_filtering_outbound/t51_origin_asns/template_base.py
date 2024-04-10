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

"""BGP origin AS filtered test case template."""

from ..template_base import TemplateBase as TemplateSetBase

__all__ = ["TemplateBase"]


class TemplateBase(TemplateSetBase):
    """BGP origin AS filtered test case template."""

    test_prefix_lengths4 = [24]
    test_prefix_lengths6 = [48]

    def _test_announce_routes(self, sim):
        """Announce a BGP prefix with a differnt origin."""

        # Add large communities for peer types that require them
        large_communities = ""

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.100 "
                f"large-community [65000:3:1 {large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::100 "
                f"large-community [65000:3:1 {large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.111.0/24 next-hop 100.64.0.100 as-path [ 65100 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:111::/48 next-hop fc00:100::100 as-path [ 65100 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.121.0/24 next-hop 100.64.0.100 as-path [ 65200 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:121::/48 next-hop fc00:100::100 as-path [ 65200 ] "
                f"large-community [65000:3:4 {large_communities}]"
            ],
        )

    def r1_template_global_config(self):
        """Return R1 global config with the originated routes."""
        return self._generate_originated_routes(next_hop4="via 100.64.0.3", next_hop6="via fc00:100::3")
