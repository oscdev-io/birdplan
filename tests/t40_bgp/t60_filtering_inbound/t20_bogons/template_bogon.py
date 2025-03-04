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

"""BGP bogon test case template."""

from ..template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP bogon test case template."""

    def _test_announce_routes(self, sim):
        """Announce a BGP bogon prefix."""

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        self._exabgpcli(
            sim,
            "e1",
            [f"neighbor 100.64.0.1 announce route 172.16.0.0/24 next-hop 100.64.0.2 large-community [{large_communities}]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            [f"neighbor fc00:100::1 announce route 2001:db8::/48 next-hop fc00:100::2 large-community [{large_communities}]"],
        )
