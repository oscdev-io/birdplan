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

"""BGP too many large communities test case template."""

from .template_base import TemplateBase


class Template(TemplateBase):
    """BGP too many large communities test case template."""

    r1_template_global_config = """
  large_community_maxlen: 5
"""

    def _test_announce_routes(self, sim):
        """Announce a BGP prefix with a too many large communities."""

        too_many_communities_str = " ".join([f"65001:{x}:{x}" for x in range(6)])

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.2 large-community ["
                + too_many_communities_str
                + "]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::2 large-community ["
                + too_many_communities_str
                + "]"
            ],
        )
