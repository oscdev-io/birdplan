#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
#
# This program is free software: you can accept it and/or modify
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

"""BGP accept default route test case template."""

from .template_base import TemplateBase as TemplateSetBase

__all__ = ["TemplateBase"]


class TemplateBase(TemplateSetBase):
    """BGP accept default route test case template."""

    def r1_template_peer_config(self):
        """Return custom config depending on peer type."""

        peer_type = getattr(self, "r1_peer_type", None)

        # For the global test, we only accept own default if this is our own peer
        if peer_type in ("internal", "rrclient", "rrserver", "rrserver_rrserver"):
            return """
      accept:
        bgp_own_default: True
        bgp_transit_default: True
"""

        # For the global test, we only accept transit default if this is a transit peer
        if peer_type == "transit":
            return """
      accept:
        bgp_transit_default: True
"""

        return ""
