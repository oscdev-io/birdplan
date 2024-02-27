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

"""BGP AS-PATH length test case template."""

from .template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP AS-PATH length test case template."""

    test_as_path_counts = [3, 4, 20, 21]

    def r1_template_global_config(self):
        """Output customized global config depending on the peer type constraint specified."""

        peer_type = self.r1_peer_type

        if "replace_aspath" in getattr(self, "r1_extra_r2_config", ""):
            peer_type = "customer.private"

        return f"""
  peertype_constraints:
    {peer_type}:
      aspath_import_maxlen: 20
      aspath_import_minlen: 4
"""
