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

"""BGP base test for filtering."""

# pylint: disable=import-error,too-few-public-methods,no-self-use

import os
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.exabgp_router_node import ExaBGPRouterNode
from nsnetsim.switch_node import SwitchNode
from basetests import BirdPlanBaseTestCase


class BirdplanBaseTestCaseExabgp(BirdPlanBaseTestCase):
    """BGP base test for filtering."""

    test_dir = os.path.dirname(__file__)
    routers = ["r1"]

    # BIRD configuration
    peer_asn = "65001"
    peer_type = ""
    global_config = ""
    extra_config = ""

    def _setup(self, sim, tmpdir):
        """Set up a BIRD test scenario with a specific peer type."""

        # Configure our simulator
        self._test_configure(
            sim,
            tmpdir,
            {
                "@PEER_ASN@": self.peer_asn,
                "@PEER_TYPE@": self.peer_type,
                "@GLOBAL_CONFIG@": self.global_config,
                "@EXTRA_CONFIG@": self.extra_config,
            },
        )

        print("Adding routers...")
        sim.add_node(BirdRouterNode(name="r1", configfile=f"{tmpdir}/bird.conf.r1"))

        exabgp_conffile = f"{self.test_dir}/exabgp.conf.e1.as{self.peer_asn}"
        sim.add_node(ExaBGPRouterNode(name="e1", configfile=exabgp_conffile))
        sim.add_conffile("CONFFILE(e1)", exabgp_conffile)
        exalogfile = sim.node("e1").logfile
        sim.add_logfile(f"LOGFILE(e1) => {exalogfile}", sim.node("e1").logfile)

        print("Adding interfaces...")
        sim.node("r1").add_interface("eth0", mac="02:01:00:00:00:01", ips=["100.64.0.1/24", "fc00:100::1/64"])
        sim.node("e1").add_interface("eth0", mac="02:02:00:00:00:01", ips=["100.64.0.2/24", "fc00:100::2/64"])

        print("Adding switches...")
        sim.add_node(SwitchNode("s1"))
        sim.node("s1").add_interface(sim.node("r1").interface("eth0"))
        sim.node("s1").add_interface(sim.node("e1").interface("eth0"))

        # Simulate our topology
        print("Simulate topology...")
        sim.run()

    def _check_main_bgp_tables(self, sim):
        """Test BIRD t_bgp4 table."""

        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {}
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {}
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"
