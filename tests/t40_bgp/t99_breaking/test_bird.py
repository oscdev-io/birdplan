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

"""BIRD BGP test."""

import logging
import os
import time
from ipaddress import IPv4Address, IPv6Address
from typing import Dict, List

import pytest
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.exabgp_router_node import ExaBGPRouterNode
from nsnetsim.switch_node import SwitchNode

from birdplan.cmdline import BirdPlanCommandLine

from ...simulation import Simulation


@pytest.mark.incremental()
class Test:
    """BIRD BGP test."""

    sim: Simulation

    num_bird_routers = 2500

    def test_setup(self, sim, testpath, tmpdir, enable_performance_test):  # noqa: CFQ001 # pylint: disable=too-many-locals
        """Set up our test."""

        # Make sure --enable-performance-test was specified
        if not enable_performance_test:
            return

        # Grab the directory the test is running in
        sim.test_dir = os.path.dirname(testpath)

        exabgps = []
        routers = []

        # Setup ExaBGP e1, which feeds routes to r1, which feeds them to the route amplifiers
        e1_config = self._configure_exabgp(
            sim,
            router_id="100.64.0.1",
            asn="64513",
            source4="100.64.0.1",
            source6="fc00:100::1",
            peer={
                "asn": "64514",
                "neighbor4": "100.64.0.2",
                "neighbor6": "fc00:100::2",
            },
        )
        # sim.add_report_obj("ExaBGP(e1)", e1_config)
        exabgps.append({"name": "e1", "config": e1_config, "ip4": "100.64.0.1", "ip6": "fc00:100::1"})

        # These are the peers that will be passed to the r2 configuration
        r1_peers = [{"name": "e1", "asn": "64513", "type": "transit", "neighbor4": "100.64.0.1", "neighbor6": "fc00:100::1"}]
        r2_peers = []

        for router_num in range(1, self.num_bird_routers + 1):
            router_asn = 4294900000 + router_num
            router_addr4 = IPv4Address("100.64.0.3") + router_num
            router_addr6 = IPv6Address("fc00:100::3") + router_num

            router_config = self._configure_bird(
                router_id=f"{router_addr4}",
                asn=f"{router_asn}",
                source4=f"{router_addr4}",
                source6=f"{router_addr6}",
                peers=[
                    {"name": "r1", "asn": "64514", "type": "transit", "neighbor4": "100.64.0.2", "neighbor6": "fc00:100::2"},
                    {
                        "name": "r2",
                        "asn": "64515",
                        "type": "customer",
                        "neighbor4": "100.64.0.3",
                        "neighbor6": "fc00:100::3",
                        "extra_config": "filter: {origin_asns: [64515]}",
                    },
                ],
            )
            # sim.add_report_obj(f"BIRD(a{router_num})", router_config)
            # Add router information to r2's peer list
            r1_peers.append(
                {
                    "name": f"a{router_num}",
                    "asn": f"{router_asn}",
                    "type": "customer",
                    "neighbor4": f"{router_addr4}",
                    "neighbor6": f"{router_addr6}",
                    "extra_config": f"filter: {{origin_asns: [{router_asn}]}}",
                }
            )
            r2_peers.append(
                {
                    "name": f"a{router_num}",
                    "asn": f"{router_asn}",
                    "type": "transit",
                    "neighbor4": f"{router_addr4}",
                    "neighbor6": f"{router_addr6}",
                }
            )
            routers.append({"name": f"a{router_num}", "config": router_config, "ip4": f"{router_addr4}", "ip6": f"{router_addr6}"})

        # Setup r1, which gets its routes from e1 and amplifies them to the second level of routers
        r1_config = self._configure_bird(
            router_id="100.64.0.2",
            asn="64514",
            source4="100.64.0.2",
            source6="fc00:100::2",
            peers=r1_peers,
        )
        # sim.add_report_obj("BIRD(r1)", r1_config)
        routers.append({"name": "r1", "config": r1_config, "ip4": "100.64.0.2", "ip6": "fc00:100::2"})

        # Finally create r2 configuration
        r2_config = self._configure_bird(
            router_id="100.64.0.3",
            asn="64515",
            source4="100.64.0.3",
            source6="fc00:100::3",
            peers=r2_peers,
        )
        # sim.add_report_obj("BIRD(r2)", r2_config)
        routers.append({"name": "r2", "config": r2_config, "ip4": "100.64.0.3", "ip6": "fc00:100::3"})

        sim.add_node(SwitchNode("s1"))

        # Loop with our ExaBGP's
        for exabgp in exabgps:
            exabgpconfig_filename = f"{tmpdir}/exabgp.conf.{exabgp['name']}"

            # Write out our birdplan config files
            with open(exabgpconfig_filename, "w", encoding="UTF-8") as exabgpconfig_file:
                exabgpconfig_file.write(exabgp["config"])

            sim.add_node(ExaBGPRouterNode(name=exabgp["name"], configfile=exabgpconfig_filename))
            # Add network interface to the node
            sim.node(exabgp["name"]).add_interface("eth0", None, [f"{exabgp['ip4']}/16", f"{exabgp['ip6']}/64"])
            # Connect interface to switch
            sim.node("s1").add_interface(sim.node(exabgp["name"]).interface("eth0"))
            # Add log file to report
            # sim.add_logfile(f"EXABGP_LOGFILE({exabgp})", sim.node(exabgp["name"]).logfile)

        # Loop with our BIRD routers
        for router in routers:
            bpconfig_filename = f"{tmpdir}/birdplan.conf.{router['name']}"
            birdconfig_filename = f"{tmpdir}/bird.conf.{router['name']}"
            bpstate_filename = f"{tmpdir}/birdplan.state.{router['name']}"

            # Write out our birdplan config files
            with open(bpconfig_filename, "w", encoding="UTF-8") as bpconfig_file:
                bpconfig_file.write(router["config"])

            # Invoke by simulating the commandline...
            birdplan_cmdline = BirdPlanCommandLine(test_mode=True)
            # Disable logging for filelog
            logging.getLogger("filelock").setLevel(logging.ERROR)

            # Work out our commandline arguments
            cmdline_args = [
                "--birdplan-file",
                bpconfig_filename,
                "--bird-config-file",
                birdconfig_filename,
                "--birdplan-state-file",
                bpstate_filename,
                "configure",
            ]
            # Run BirdPlan as if it was from the commandline
            birdplan_cmdline.run(cmdline_args)

            # Add BIRD router node, and point it to the config file created above
            sim.add_node(BirdRouterNode(name=router["name"], configfile=birdconfig_filename))
            # Add network interface to the node
            sim.node(router["name"]).add_interface("eth0", None, [f"{router['ip4']}/16", f"{router['ip6']}/64"])
            # Connect interface to switch
            sim.node("s1").add_interface(sim.node(router["name"]).interface("eth0"))

        sim.run()

        time.sleep(10000)

        # assert False, "OH NO"
        pytest.fail("OH NO")

    def _configure_bird(  # pylint: disable=too-many-arguments
        self, router_id: str, asn: str, source4: str, source6: str, peers: List[Dict[str, str]]
    ):
        """Configure a BIRD router."""

        # Generate the top global section of the birdplan configuration
        birdplan_config = f"""
router_id: {router_id}

log_file: /tmp/{asn}.log

export_kernel:
  bgp: False

bgp:
  asn: {asn}
  peers:
"""
        # Loop with each peer
        for peer in peers:
            extra_config = ""
            if peer.get("extra_config"):
                extra_config = peer["extra_config"]
            # Generate peer configuration blocks
            peer_config = f"""
    {peer["name"]}:
      asn: {peer["asn"]}
      type: {peer["type"]}
      description: BGP session to {peer["name"]}
      source_address4: {source4}
      source_address6: {source6}
      neighbor4: {peer["neighbor4"]}
      neighbor6: {peer["neighbor6"]}
      {extra_config}
"""
            # Add peer configuration
            birdplan_config += peer_config

        # Return BIRD config
        return birdplan_config

    def _configure_exabgp(  # noqa: CFQ002 # pylint: disable=too-many-arguments
        self, sim: Simulation, router_id: str, asn: str, source4: str, source6: str, peer: Dict[str, str]
    ):
        """Configure an ExaBGP."""

        exabgp_config = f"""

process routes-ipv4 {{
    run "{sim.test_dir}/process_routes" "{sim.test_dir}/AS174.routes.10" "{asn}" "ipv4";
    encoder json;
}}
process routes-ipv6 {{
    run "{sim.test_dir}/process_routes" "{sim.test_dir}/AS174.routes.10" "{asn}" "ipv6";
    encoder json;
}}

neighbor {peer["neighbor4"]} {{
    router-id {router_id};
    local-as {asn};
    peer-as {peer["asn"]};
    local-address {source4};
    api {{
        processes [ routes-ipv4 ];
    }}
}}

neighbor {peer["neighbor6"]} {{
    router-id {router_id};
    local-as {asn};
    peer-as {peer["asn"]};
    local-address {source6};
    api {{
        processes [ routes-ipv6 ];
    }}
}}
"""
        # Return ExaBGP config
        return exabgp_config
