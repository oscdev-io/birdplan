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

"""BGP blackhole length test case template."""

from ..template_base import TemplateBase as TemplateSetBase


class TemplateBase(TemplateSetBase):
    """BGP blackhole length test case template."""

    test_blackhole_ranges = [101]
    test_blackhole_lengths4 = []
    test_blackhole_lengths6 = []

    def r1_template_peer_config(self):
        """Return custom config based on the peer type."""
        # Grab the peer type
        peer_type = getattr(self, "r1_peer_type")
        # If its a customer, return the prefixes
        if peer_type == "customer":
            return """
        prefixes:
          - 100.101.0.0/22+
          - fc00:101::/46+
"""
        # If not, just return a blank string
        return ""

    def _test_announce_routes(self, sim):
        """Announce various length blackholes."""

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type") in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        # Loop with IP ranges
        for iprange in self.test_blackhole_ranges:

            # Loop with IPv4 blackhole lenghts
            for test_blackhole_length4 in self.test_blackhole_lengths4:
                self._exabgpcli(
                    sim,
                    "e1",
                    [
                        f"neighbor 100.64.0.1 announce route 100.{iprange}.0.0/{test_blackhole_length4} next-hop 100.64.0.2 "
                        f"large-community [ {large_communities} ] community [65535:666]"
                    ],
                )

            # Loop with IPv6 blackhole lenghts
            for test_blackhole_length6 in self.test_blackhole_lengths6:
                self._exabgpcli(
                    sim,
                    "e1",
                    [
                        f"neighbor fc00:100::1 announce route fc00:{iprange}::/{test_blackhole_length6} next-hop fc00:100::2 "
                        f"large-community [ {large_communities} ] community [65535:666]"
                    ],
                )
