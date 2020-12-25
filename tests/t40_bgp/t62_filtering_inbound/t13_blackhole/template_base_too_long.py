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

"""BGP blackhole too long test case template."""

from .template_base import TemplateSetBase


class TemplateBase(TemplateSetBase):
    """BGP blackhole too long test case template."""

    test_blackhole_length4 = 32
    test_blackhole_length6 = 128

    def _test_announce_routes(self, sim):
        """Announce a BGP blackhole that is too long."""

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type") in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        self._exabgpcli(
            sim,
            "e1",
            [
                f"neighbor 100.64.0.1 announce route 100.68.0.0/{self.test_blackhole_length4} next-hop 100.64.0.2 "
                f"large-community [ {large_communities} ] community [65535:666]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                f"neighbor fc00:100::1 announce route fc00:101::/{self.test_blackhole_length6} next-hop fc00:100::2 "
                f"large-community [ {large_communities} ] community [65535:666]"
            ],
        )
