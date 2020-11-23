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

"""BGP blackhole test case template."""

from ..template_base import TemplateBase as TemplateSetBase


class TemplateBase(TemplateSetBase):  # pylint:disable=abstract-method
    """BGP blackhole test case template."""

    def r1_template_peer_config(self):
        """Return custom config based on the peer type."""
        # Grab the peer type
        peer_type = getattr(self, "r1_peer_type")
        # If its a customer, return the prefixes
        if peer_type == "customer":
            return """
        prefixes:
          - 100.64.101.0/24+
          - 100.64.104.0/22+
          - fc00:101::/64+
          - fc00:104::/48+
"""
        # If not, just return a blank string
        return ""
