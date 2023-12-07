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

"""BGP large community functions test case template (base class for specific tests)."""

from ...basetests import BirdPlanBaseTestCase


class TemplateBase(BirdPlanBaseTestCase):
    """BGP large community functions test case template (base class for specific tests)."""

    routers = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"]
    exabgps = ["e1"]

    e1_template_communities = ""
    e1_template_extra = ""
    e1_extra_communities = ""

    r1_peer_asn = 65100

    r4_asn = 65003
    r4_peer_asn = 65000
    r4_interfaces = ["eth0"]
    r4_interface_eth0 = {"mac": "02:04:00:00:00:01", "ips": ["100.64.0.4/24", "fc00:100::4/64"]}
    r4_switch_eth0 = "s1"

    r5_asn = 65004
    r5_peer_asn = 65000
    r5_interfaces = ["eth0"]
    r5_interface_eth0 = {"mac": "02:05:00:00:00:01", "ips": ["100.64.0.5/24", "fc00:100::5/64"]}
    r5_switch_eth0 = "s1"

    r6_asn = 65005
    r6_peer_asn = 65000
    r6_interfaces = ["eth0"]
    r6_interface_eth0 = {"mac": "02:06:00:00:00:01", "ips": ["100.64.0.6/24", "fc00:100::6/64"]}
    r6_switch_eth0 = "s1"

    r7_asn = 65006
    r7_peer_asn = 65000
    r7_interfaces = ["eth0"]
    r7_interface_eth0 = {"mac": "02:07:00:00:00:01", "ips": ["100.64.0.7/24", "fc00:100::7/64"]}
    r7_switch_eth0 = "s1"

    r8_asn = 65007
    r8_peer_asn = 65000
    r8_interfaces = ["eth0"]
    r8_interface_eth0 = {"mac": "02:08:00:00:00:01", "ips": ["100.64.0.8/24", "fc00:100::8/64"]}
    r8_switch_eth0 = "s1"

    r9_asn = 65008
    r9_peer_asn = 65000
    r9_interfaces = ["eth0"]
    r9_interface_eth0 = {"mac": "02:09:00:00:00:01", "ips": ["100.64.0.9/24", "fc00:100::9/64"]}
    r9_switch_eth0 = "s1"

    r10_asn = 65010
    r10_peer_asn = 65000
    r10_interfaces = ["eth0"]
    r10_interface_eth0 = {"mac": "02:10:00:00:00:01", "ips": ["100.64.0.10/24", "fc00:100::10/64"]}
    r10_switch_eth0 = "s1"

    e1_asn = 65100
    e1_interfaces = ["eth0"]
    e1_interface_eth0 = {"mac": "02:e1:00:00:00:01", "ips": ["100.64.0.100/24", "fc00:100::100/64"]}
    e1_switch_eth0 = "s1"

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_announce_routes(self, sim):
        """Announce a prefix from ExaBGP to BIRD."""

        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.101.0/24 next-hop 100.64.0.100 "
                f"large-community [ {self.e1_template_communities} {self.e1_extra_communities} ] "
                f"{self.e1_template_extra}"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:101::/48 next-hop fc00:100::100 "
                f"large-community [ {self.e1_template_communities} {self.e1_extra_communities} ] "
                f"{self.e1_template_extra}"
            ],
        )

        self._test_announce_routes(sim)

    def _test_announce_routes(self, sim):
        """Announce extra prefixes from ExaBGP to BIRD."""

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_tables_bgp4_peer(self, sim):
        """Test BIRD BGP4 peer table."""
        self._test_bird_routers_table_bgp_peers(sim, 4)

    def test_bird_tables_bgp6_peer(self, sim):
        """Test BIRD BGP6 peer table."""
        self._test_bird_routers_table_bgp_peers(sim, 6)

    def test_bird_tables_bgp4(self, sim):
        """Test BIRD t_bgp4 table."""
        self._test_bird_routers_table(sim, "t_bgp4")

    def test_bird_tables_bgp6(self, sim):
        """Test BIRD t_bgp6 table."""
        self._test_bird_routers_table(sim, "t_bgp6")

    def test_bird_cmdline_bgp_peer_summary(self, sim, tmpdir):
        """Test showing BGP peer summary."""
        self._test_bird_cmdline_bgp_peer_summary(sim, tmpdir)

    def test_bird_cmdline_bgp_peer_show(self, sim, tmpdir):
        """Test showing BGP peer."""
        self._test_bird_cmdline_bgp_peer_show(sim, tmpdir)
