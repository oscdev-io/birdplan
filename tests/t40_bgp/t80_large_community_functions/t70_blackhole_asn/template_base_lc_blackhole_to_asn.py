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
# pylint: disable=import-error,too-few-public-methods

"""BGP large community functions test case template."""

from .template_base_blackhole import TemplateSetBase


class TemplateBase(TemplateSetBase):
    """BGP large community functions test case template."""

    def _test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""

        # ASN component to generate routes for, these are eBGP peers
        for asn_c in [0, 1, 3, 4, 5, 9]:
            # Work out the IP component to use
            ip_component = (asn_c * 10) + 2

            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor 100.64.0.1 announce route 100.64.101.{ip_component}/31 next-hop 100.64.0.100 "
                    f"large-community [ {self.e1_template_communities} {self.e1_template_extra} 65000:666:6500{asn_c} ] "
                    "community [65535:666]"
                    f"{self.e1_template_extra}"
                ],
            )
            self._exabgpcli(
                sim,
                "e1",
                [
                    f"neighbor fc00:100::1 announce route fc00:101::{ip_component}/127 next-hop fc00:100::100 "
                    f"large-community [ {self.e1_template_communities} {self.e1_template_extra} 65000:666:6500{asn_c} ] "
                    "community [65535:666]"
                    f"{self.e1_template_extra}"
                ],
            )
