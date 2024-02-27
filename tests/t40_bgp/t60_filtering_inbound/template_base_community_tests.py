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

"""BGP community test case template."""

from .template_base import TemplateBase as TemplateSetBase

__all__ = ["TemplateBase"]


class TemplateBase(TemplateSetBase):
    """BGP community test case template."""

    test_community_counts = []
    test_extended_community_counts = []
    test_large_community_counts = []

    def _test_announce_routes(self, sim):
        """Announce various length blackholes."""

        # Add large communities for peer types that require them
        relation_large_communities = ""
        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            relation_large_communities = "65000:3:1"

        # Generate community advertisements
        for community_count in self.test_community_counts:
            communities = " ".join([f"1:{x}" for x in range(community_count)])

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor 100.64.0.1 announce route 100.101.{community_count}.0/24 next-hop 100.64.0.2 "
                    f"large-community [ {relation_large_communities} ] community [ {communities} ]"
                ],
            )

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor fc00:100::1 announce route fc00:101:{community_count}::/64 next-hop fc00:100::2 "
                    f"large-community [ {relation_large_communities} ] community [ {communities} ]"
                ],
            )

        # Generate extended community advertisements
        for extended_community_count in self.test_extended_community_counts:
            extended_communities = " ".join([f"origin:{x}:{x}" for x in range(extended_community_count)])

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor 100.64.0.1 announce route 100.102.{extended_community_count}.0/24 next-hop 100.64.0.2 "
                    f"large-community [ {relation_large_communities} ] extended-community [ {extended_communities} ]"
                ],
            )

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor fc00:100::1 announce route fc00:102:{extended_community_count}::/64 next-hop fc00:100::2 "
                    f"large-community [ {relation_large_communities} ] extended-community [ {extended_communities} ]"
                ],
            )

        # Generate large community advertisements
        for large_community_count in self.test_large_community_counts:
            large_communities = " ".join([f"65001:{x}:{x}" for x in range(large_community_count)])

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor 100.64.0.1 announce route 100.103.{large_community_count}.0/24 next-hop 100.64.0.2 "
                    f"large-community [ {relation_large_communities} {large_communities} ]"
                ],
            )

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor fc00:100::1 announce route fc00:103:{large_community_count}::/64 next-hop fc00:100::2 "
                    f"large-community [ {relation_large_communities} {large_communities} ]"
                ],
            )
