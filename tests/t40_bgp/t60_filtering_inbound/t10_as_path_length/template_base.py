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

"""BGP AS-PATH length test case template."""

from ..template_base import TemplateBase as TemplateSetBase


class TemplateBase(TemplateSetBase):
    """BGP AS-PATH length test case template."""

    test_as_path_counts = []

    def _test_announce_routes(self, sim):
        """Announce BGP prefixes with varying length AS-PATHs."""

        # Loop with the AS-PATH counts
        for as_path_count in self.test_as_path_counts:
            as_path = [65001 for x in range(as_path_count)]

            # Add large communities for peer types that require them
            large_communities = ""
            if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
                large_communities = "65000:3:1"

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor 100.64.0.1 announce route 100.101.{as_path_count}.0/24 next-hop 100.64.0.2 as-path {as_path} "
                    f"large-community [ {large_communities} ]"
                ],
            )
            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor fc00:100::1 announce route fc00:101:{as_path_count}::/48 next-hop fc00:100::2 as-path {as_path} "
                    f"large-community [ {large_communities} ]"
                ],
            )
