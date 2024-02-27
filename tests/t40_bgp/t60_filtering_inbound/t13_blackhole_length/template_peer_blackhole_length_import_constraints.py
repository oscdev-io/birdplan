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

"""BGP blackhole length test case template."""

from .template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP blackhole length test case template."""

    test_blackhole_lengths4 = [28, 30, 32]
    test_blackhole_lengths6 = [124, 126, 128]

    def r1_template_peer_config(self):
        """Return custom config based on the peer type."""

        output = ""

        # Grab the peer type
        peer_type = getattr(self, "r1_peer_type", None)
        # If its a customer, return the prefixes
        if peer_type == "customer":
            output += """
        prefixes:
          - 100.101.0.0/22+
          - fc00:101::/46+
"""

        output += """
      constraints:
        blackhole_import_minlen4: 29
        blackhole_import_maxlen4: 31
        blackhole_import_minlen6: 125
        blackhole_import_maxlen6: 127
"""

        return output
