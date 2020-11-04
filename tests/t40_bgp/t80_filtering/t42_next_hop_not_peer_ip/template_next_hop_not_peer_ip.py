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

"""BGP next hop not peer IP test case template."""

from ..template_base import TemplateBase


class Template(TemplateBase):
    """BGP next hop not peer IP test case template."""

    def _test_announce_routes(self, sim):
        """Announce a BGP prefix where the first AS is not the peer AS."""

        self._exabgpcli(sim, "e1", ["neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.3 as-path [ 65001 ]"])
        self._exabgpcli(sim, "e1", ["neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::3 as-path [ 65001 ]"])
