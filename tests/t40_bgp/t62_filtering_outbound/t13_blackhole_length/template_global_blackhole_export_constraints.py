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

"""BGP global blackhole export constraints test case template."""

from ..template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP global blackhole export constraints test case template."""

    e1_template_communities = "65535:666"
    e1_template_large_communities = "65000:666:65413 65000:666:65412"

    test_prefix_lengths4 = [28, 30, 32]
    test_prefix_lengths6 = [124, 126, 128]

    def r1_template_extra_config(self):
        """Return R1 extra config with the blackhole community."""

        r1_peer_type = getattr(self, "r1_peer_type")  # noqa: B009
        if r1_peer_type and r1_peer_type in ("routeserver", "routecollector", "transit"):
            return """
      blackhole_community: true
"""
        return ""

    def r1_template_global_config(self):
        """Output customized global config depending on the peer type constraint specified."""

        peer_type = getattr(self, "r1_peer_type")  # noqa: B009
        if not peer_type:
            return ""

        if "replace_aspath" in getattr(self, "r1_extra_r2_config", ""):
            peer_type = "customer.private"

        return f"""
{self._generate_originated_routes()}

  peertype_constraints:
    {peer_type}:
      blackhole_export_minlen4: 29
      blackhole_export_maxlen4: 31
      blackhole_export_minlen6: 125
      blackhole_export_maxlen6: 127
"""
