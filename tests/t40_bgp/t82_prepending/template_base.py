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

"""BGP prepending test case template."""

from ...basetests import BirdPlanBaseTestCase

__all__ = ["TemplateBase"]


class TemplateBase(BirdPlanBaseTestCase):
    """BGP prepending test case template."""

    routers = ["r1", "r2"]

    r1_interfaces = ["eth0", "eth1", "eth2"]

    r1_interface_eth2 = {"mac": "02:01:02:00:00:01", "ips": ["100.201.0.1/24", "fc00:201::1/48"]}

    r2_interfaces = ["eth0"]

    exabgps = ["e1", "e2"]
    e1_asn = 65000
    e2_asn = 65000

    e1_interface_eth0 = {"mac": "02:e1:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}
    e2_interface_eth0 = {"mac": "02:e2:00:00:00:01", "ips": ["100.64.0.4/24", "fc00:100::4/64"]}

    def r1_template_extra_config(self):
        """Dynamic configuration."""

        config = []

        # Redistribute default routes for all but these peer types...
        r1_peer_type = getattr(self, "r1_peer_type", None)
        if r1_peer_type not in ("peer", "routecollector", "routeserver", "transit"):
            config.append("        kernel_default: True")
            config.append("        originated_default: True")
            config.append("        static_default: True")
            config.append("        bgp_own_default: True")
            config.append("        bgp_transit_default: True")
        # Redistribute blackhole routes only to the below peers that
        if r1_peer_type in ("internal", "routecollector", "routeserver", "rrclient", "rrserver", "rrserver-rrserver", "transit"):
            config.append("        kernel_blackhole: True")
            config.append("        static_blackhole: True")
        # Mark blackhole capable eBGP peers
        if r1_peer_type in ("routecollector", "routeserver", "transit"):
            config.append("      blackhole_community: True")

        return "\n".join(config)

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_add_kernel_routes(self, sim):
        """Add kernel routes to BIRD instances."""

        if "r1" in self.routers_config_exception:
            return

        # Add gateway'd kernel routes
        sim.node("r1").run_ip(["route", "add", "100.121.0.0/24", "via", "100.201.0.3"])
        sim.node("r1").run_ip(["route", "add", "fc00:121::/48", "via", "fc00:201::3"])

        # Add kernel device routes
        sim.node("r1").run_ip(["route", "add", "100.122.0.0/24", "dev", "eth2"])
        sim.node("r1").run_ip(["route", "add", "fc00:122::/48", "dev", "eth2"])

        # Add kernel default routes
        sim.node("r1").run_ip(["route", "add", "default", "via", "100.201.0.3"])
        sim.node("r1").run_ip(["route", "add", "default", "via", "fc00:201::3"])

        # Add kernel blackhole routes
        sim.node("r1").run_ip(["route", "add", "blackhole", "100.123.0.0/31"])
        sim.node("r1").run_ip(["route", "add", "blackhole", "fc00:123::/127"])

    def test_announce_routes(self, sim):  # noqa: CFQ001
        """Hook to add in routes if we need to."""

        #
        # IPV4
        #

        # Own routes
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.103.0/24 next-hop 100.64.0.3 large-community [ 65000:3:1 ]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.103.0/32 next-hop 100.64.0.3 "
                "large-community [ 65000:3:1 65000:666:65412 65000:666:65413 ] "
                "community [ 65535:666 65535:65281 ]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 0.0.0.0/0 next-hop 100.64.0.3 large-community [ 65000:3:1 ]"],
        )
        # Customer routes
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.104.0/24 next-hop 100.64.0.3 large-community [ 65000:3:2 ]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor 100.64.0.1 announce route 100.64.104.0/32 next-hop 100.64.0.3 "
                "large-community [ 65000:3:2 65000:666:65412 65000:666:65413 ] "
                "community [ 65535:666 65535:65281 ]"
            ],
        )
        # Peer route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.105.0/24 next-hop 100.64.0.3 large-community [ 65000:3:3 ]"],
        )
        # Transit routes
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.106.0/24 next-hop 100.64.0.3 large-community [ 65000:3:4 ]"],
        )
        self._exabgpcli(
            sim,
            "e2",
            [
                "neighbor 100.64.0.1 announce route 0.0.0.0/0 next-hop 100.64.0.4 "
                "large-community [ 65000:3:4 ] "
                "as-path [ 65003 ]"
            ],
        )
        # Route server route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor 100.64.0.1 announce route 100.64.107.0/24 next-hop 100.64.0.3 large-community [ 65000:3:5 ]"],
        )

        #
        # IPV6
        #

        # Own routes
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:103::/48 next-hop fc00:100::3 large-community [ 65000:3:1 ]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:103::/128 next-hop fc00:100::3 "
                "large-community [ 65000:3:1 65000:666:65412 65000:666:65413 ] "
                "community [ 65535:666 65535:65281 ]"
            ],
        )
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route ::/0 next-hop fc00:100::3 large-community [ 65000:3:1 ]"],
        )
        # Customer routes
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:104::/48 next-hop fc00:100::3 large-community [ 65000:3:2 ]"],
        )
        self._exabgpcli(
            sim,
            "e1",
            [
                "neighbor fc00:100::1 announce route fc00:104::/128 next-hop fc00:100::3 "
                "large-community [ 65000:3:2 65000:666:65412 65000:666:65413 ] "
                "community [ 65535:666 65535:65281 ]"
            ],
        )
        # Peer route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:105::/48 next-hop fc00:100::3 large-community [ 65000:3:3 ]"],
        )
        # Transit routes
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:106::/48 next-hop fc00:100::3 large-community [ 65000:3:4 ]"],
        )
        self._exabgpcli(
            sim,
            "e2",
            ["neighbor fc00:100::1 announce route ::/0 next-hop fc00:100::4 large-community [ 65000:3:4 ] as-path [ 65003 ]"],
        )
        # Route server route
        self._exabgpcli(
            sim,
            "e1",
            ["neighbor fc00:100::1 announce route fc00:107::/48 next-hop fc00:100::3 large-community [ 65000:3:5 ]"],
        )

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_bird_cmdline_bgp_peer_summary(self, sim, tmpdir):
        """Test showing BGP peer summary."""
        self._test_bird_cmdline_bgp_peer_summary(sim, tmpdir)

    def test_bird_cmdline_bgp_peer_show(self, sim, tmpdir):
        """Test showing BGP peer."""
        self._test_bird_cmdline_bgp_peer_show(sim, tmpdir)

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

    def test_bird_tables_master4(self, sim):
        """Test BIRD master4 table."""
        self._test_bird_routers_table(sim, "master4")

    def test_bird_tables_master6(self, sim):
        """Test BIRD master6 table."""
        self._test_bird_routers_table(sim, "master6")

    def test_bird_tables_kernel4(self, sim):
        """Test BIRD kernel4 table."""
        self._test_bird_routers_table(sim, "t_kernel4")

    def test_bird_tables_kernel6(self, sim):
        """Test BIRD kernel6 table."""
        self._test_bird_routers_table(sim, "t_kernel6")

    def test_os_rib_inet(self, sim):
        """Test OS RIB for inet."""
        self._test_os_rib(sim, "inet")

    def test_os_rib_inet6(self, sim):
        """Test OS RIB for inet6."""
        self._test_os_rib(sim, "inet6")
