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

"""BGP large community functions test case template."""

from ..template_base import TemplateBase


class TemplateSetBase(TemplateBase):
    """BGP large community functions test case template."""

    blackhole_community = ""

    def r1_template_peer_config(self):
        """Return custom config based on the peer type."""
        # Grab the peer type
        peer_type = getattr(self, "r1_peer_type")
        # If its a customer, return the prefixes
        if peer_type == "customer":
            return """
        prefixes:
          - 100.64.101.0/24+
          - fc00:101::/48+
"""
        # If not, just return a blank string
        return ""

    @property
    def e1_template_communities(self):
        """Return additional large communities we should be using."""
        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type") in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

        return large_communities

    def _test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/31 next-hop 100.64.0.100 "
                f"large-community [ {self.e1_template_communities} {self.e1_extra_communities} {self.blackhole_community} ] "
                "community [65535:666]"
                f"{self.e1_template_extra}"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:101::/127 next-hop fc00:100::100 "
                f"large-community [ {self.e1_template_communities} {self.e1_extra_communities} {self.blackhole_community} ] "
                "community [65535:666]"
                f"{self.e1_template_extra}"
            ],
        )
