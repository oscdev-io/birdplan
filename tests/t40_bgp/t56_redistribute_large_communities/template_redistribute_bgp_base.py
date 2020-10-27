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

"""BGP redistribute large community test case template."""

from .template_base import TemplateBase as TemplateSetBase


class TemplateBase(TemplateSetBase):
    """BGP redistribute large community test case template."""

    exabgps = ["e1"]
    e1_asn = 65000
    e1_interface_eth0 = {"mac": "02:e1:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}

    def _test_announce_routes(self, sim):
        """Announce routes from ExaBGP e1."""

        # Own route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.103.0/24 next-hop 100.64.0.3 large-community [ 65000:3:1 ]"],
        )
        # Customer route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.104.0/24 next-hop 100.64.0.3 large-community [ 65000:3:2 ]"],
        )
        # Peer route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.105.0/24 next-hop 100.64.0.3 large-community [ 65000:3:3 ]"],
        )
        # Transit route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.106.0/24 next-hop 100.64.0.3 large-community [ 65000:3:4 ]"],
        )
        # Route server route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.107.0/24 next-hop 100.64.0.3 large-community [ 65000:3:5 ]"],
        )

        # Own route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:103::/48 next-hop fc00:100::3 large-community [ 65000:3:1 ]"],
        )
        # Customer route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:104::/48 next-hop fc00:100::3 large-community [ 65000:3:2 ]"],
        )
        # Peer route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:105::/48 next-hop fc00:100::3 large-community [ 65000:3:3 ]"],
        )
        # Transit route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:106::/48 next-hop fc00:100::3 large-community [ 65000:3:4 ]"],
        )
        # Route server route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:107::/48 next-hop fc00:100::3 large-community [ 65000:3:5 ]"],
        )
