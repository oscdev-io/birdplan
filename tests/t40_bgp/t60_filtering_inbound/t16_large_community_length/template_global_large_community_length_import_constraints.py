#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
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

"""BGP large communities test case template."""

from ..template_base_community_tests import TemplateBase

# This test is changed from 20,21 to 19,20 due to the fact we add large communities


class Template(TemplateBase):
    """BGP large communities test case template."""

    test_large_community_counts = [19, 20]

    def r1_template_global_config(self):
        """Output customized global config depending on the peer type constraint specified."""

        peer_type = self.r1_peer_type

        if "replace_aspath" in getattr(self, "r1_peer_config", ""):
            peer_type = "customer.private"

        return f"""
  peertype_constraints:
    {peer_type}:
      large_community_import_maxlen: 20
"""
