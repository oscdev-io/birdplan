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

"""BGP peer prefix export constraints test case template."""

from ..template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP peer prefix export constraints test case template."""

    test_prefix_lengths4 = [19, 22, 24]
    test_prefix_lengths6 = [44, 46, 48]

    def __getattr__(self, name: str):
        """Work out what we're returning for what."""

        # Mapping of peer types to router names
        conf_map = {
            "customer": "r2",
            "internal": "r3",
            "peer": "r4",
            "routecollector": "r5",
            "routeserver": "r6",
            "rrclient": "r7",
            "rrserver": "r8",
            "rrserver-rrserver": "r9",
            "transit": "r10",
        }

        # Loop with each of the map entries
        for peer_type, router_name in conf_map.items():
            # Check if we're configuring this specific peer type
            if self.r1_peer_type == peer_type and name == f"r1_template_{router_name}_config":
                # If we are, return the constraints for it
                return """
      constraints:
        export_minlen4: 21
        export_maxlen4: 23
        export_minlen6: 45
        export_maxlen6: 47
"""

        raise AttributeError("Not valid here")
