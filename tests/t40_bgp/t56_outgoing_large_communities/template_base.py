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

"""BGP outgoing large communities test case template."""

from ...basetests import BirdPlanBaseTestCase


class TemplateBase(BirdPlanBaseTestCase):
    """BGP outgoing large communities test case template."""

    routers = ["r1", "r2"]
    r1_interfaces = ["eth0", "eth1"]
    r2_interfaces = ["eth0"]

    exabgps = ["e1"]
    e1_asn = 65000
    e1_interface_eth0 = {"mac": "02:e1:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}

    def r1_template_extra_config(self):
        """Dynamic configuration."""

        # Redistribute default routes for all but these peer types...
        r1_peer_type = getattr(self, "r1_peer_type")
        if r1_peer_type not in ("peer", "routecollector", "routeserver", "transit"):
            return """
        default: True
"""
        return ""

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_announce_routes(self, sim):
        """Hook to add in routes if we need to."""

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

        # Don't continue if we have exceptions that will be raised
        if hasattr(self, "routers_config_exception"):
            return

        # Add gateway'd kernel routes
        sim.node("r1").run_ip(["route", "add", "100.121.0.0/24", "via", "100.101.0.2"])
        sim.node("r1").run_ip(["route", "add", "fc00:121::/48", "via", "fc00:101::2"])

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_tables_bgp4_peer(self, sim):
        """Test BIRD BGP4 peer table."""
        self._test_bird_routers_table_bgp_peers(4, sim)

    def test_bird_tables_bgp6_peer(self, sim):
        """Test BIRD BGP6 peer table."""
        self._test_bird_routers_table_bgp_peers(6, sim)

    def test_bird_tables_bgp4(self, sim):
        """Test BIRD t_bgp4 table."""
        self._test_bird_routers_table("t_bgp4", sim)

    def test_bird_tables_bgp6(self, sim):
        """Test BIRD t_bgp6 table."""
        self._test_bird_routers_table("t_bgp6", sim)

    def test_bird_tables_master4(self, sim):
        """Test BIRD master4 table."""
        self._test_bird_routers_table("master4", sim)

    def test_bird_tables_master6(self, sim):
        """Test BIRD master6 table."""
        self._test_bird_routers_table("master6", sim)

    def test_bird_tables_kernel4(self, sim):
        """Test BIRD kernel4 table."""
        self._test_bird_routers_table("t_kernel4", sim)

    def test_bird_tables_kernel6(self, sim):
        """Test BIRD kernel6 table."""
        self._test_bird_routers_table("t_kernel6", sim)

    def test_os_rib_inet(self, sim):
        """Test OS RIB for inet."""
        self._test_os_rib("inet", sim)

    def test_os_rib_inet6(self, sim):
        """Test OS RIB for inet6."""
        self._test_os_rib("inet6", sim)
