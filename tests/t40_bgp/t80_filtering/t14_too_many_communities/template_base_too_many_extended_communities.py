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

"""BGP too many extended communities test case template."""

from ..template_base import TemplateBase as TemplateSetBase


class TemplateBase(TemplateSetBase):
    """BGP too many extended communities test case template."""

    test_community_count = 26

    def _test_announce_routes(self, sim):
        """Announce a BGP prefix with a too many extended communities."""

        # Convert to a 1:x format separated by spaces for exabgp
        too_many_communities_str = " ".join([f"origin:{x}:{x}" for x in range(self.test_community_count)])

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type") in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.2 extended-community ["
                + too_many_communities_str
                + f"] large-community [{large_communities}]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::2 extended-community ["
                + too_many_communities_str
                + f"] large-community [{large_communities}]"
            ],
        )
