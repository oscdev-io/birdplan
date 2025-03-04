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

"""BGP default route test case template."""

from ..template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP default route test case template."""

    e2_asn = 65000

    @property
    def exabgps(self):
        """Add e2 if we're an iBGP peer."""
        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            return ["e1", "e2"]
        return ["e1"]

    def r1_e2_config(self):
        """Output e2 configuration."""

        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            return f"""
    e2:
      asn: {self.r1_peer_asn}
      type: {self.r1_peer_type}
      description: BGP session to e2
      source_address4: 100.64.0.1
      source_address6: fc00:100::1
      neighbor4: 100.64.0.3
      neighbor6: fc00:100::3
      connect_delay_time: 2
      connect_retry_time: 2
      error_wait_time: 2,5
{getattr(self, "r1_peer_config", "")}
{getattr(self, "r1_template_peer_config", "")}
{getattr(self, "r1_peer_extra_config", "")}
"""

        return ""

    def _test_announce_routes(self, sim):
        """Announce BGP default route prefixes."""

        # Add large communities for peer types that require them
        large_communities = ""
        if getattr(self, "r1_peer_type", None) in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            large_communities = "65000:3:1"

            self._exabgpcli(
                sim,
                "e2",
                [
                    "neighbor 100.64.0.1 announce route 0.0.0.0/0 next-hop 100.64.0.3 as-path [ 65002 ] "
                    "large-community [ 65000:3:4 ]"
                ],
            )

            self._exabgpcli(
                sim,
                "e2",
                ["neighbor fc00:100::1 announce route ::/0 next-hop fc00:100::3 as-path [ 65002 ] large-community [ 65000:3:4 ]"],
            )

        self._exabgpcli(
            sim, "e1", [f"neighbor 100.64.0.1 announce route 0.0.0.0/0 next-hop 100.64.0.2 large-community [{large_communities}]"]
        )
        self._exabgpcli(
            sim, "e1", [f"neighbor fc00:100::1 announce route ::/0 next-hop fc00:100::2 large-community [{large_communities}]"]
        )
