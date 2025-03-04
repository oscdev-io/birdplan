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

"""BGP blackhole test case template."""

from .template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP blackhole test case template."""

    test_blackhole_ranges = [101, 102]

    test_blackhole_lengths4 = [28, 30, 32]
    test_blackhole_lengths6 = [124, 126, 128]

    def r1_template_peer_config(self):
        """Return custom config based on the peer type."""

        output = ""

        # Grab the peer type
        peer_type = getattr(self, "r1_peer_type", None)
        # If this is not a customer peer type, we need to add the filter section
        if peer_type != "customer":
            output += """
      filter:
"""

        output += """
        prefixes:
          - 100.102.0.0/22+
          - fc00:102::/46+
"""

        return output
