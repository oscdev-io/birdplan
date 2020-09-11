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

"""Base test classes for our tests."""

from typing import Any, Dict, List, Optional
import os
import re
import time
import pytest
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.exabgp_router_node import ExaBGPRouterNode
from nsnetsim.switch_node import SwitchNode
from simulation import Simulation
from birdplan import BirdPlan  # pylint: disable=import-error


BirdConfigMacros = Optional[Dict[str, Dict[str, str]]]

#
# Test case base classes
#


@pytest.mark.incremental
class BirdPlanBaseTestCase:
    """Base test case for our tests."""

    test_dir = os.path.dirname(__file__)

    sim: Simulation

    # List of ExaBGP nodes to create, eg. ["e1"]
    exabgps = []

    # List of bird routers to configure, eg. ["r1", "r2"]
    routers = ["r1"]

    # Supported attributes include
    # rX_peer_asn
    # rX_peer_type
    # rX_global_config
    # rX_extra_config

    # Default ASN to use for r1's peer
    r1_asn = "65000"
    r1_peer_asn = "65001"
    r1_interfaces = ["eth0"]
    r1_interface_eth0 = {"mac": "02:01:00:00:00:01", "ips": ["100.64.0.1/24", "fc00:100::1/64"]}
    r1_interface_eth1 = {"mac": "02:01:00:00:00:02", "ips": ["100.101.0.1/24", "fc00:101::1/64"]}

    r2_asn = "65001"
    r2_peer_asn = "65000"
    r2_interfaces = ["eth0"]
    r2_interface_eth0 = {"mac": "02:02:00:00:00:01", "ips": ["100.64.0.2/24", "fc00:100::2/64"]}
    r2_interface_eth1 = {"mac": "02:02:00:00:00:02", "ips": ["100.102.0.1/24", "fc00:102::1/64"]}

    r3_interfaces = ["eth0"]
    r3_interface_eth0 = {"mac": "02:03:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}

    e1_asn = "65001"
    e1_interfaces = ["eth0"]
    e1_interface_eth0 = {"mac": "02:e1:00:00:00:01", "ips": ["100.64.0.2/24", "fc00:100::2/64"]}

    def _configure_bird_routers(self, sim: Simulation, tmpdir: str, extra_macros: BirdConfigMacros = None):
        """Create our configuration files."""
        # Generate config files
        for router in self.routers:
            bird_conffile = f"{tmpdir}/bird.conf.{router}"
            bird_logfile = f"{tmpdir}/bird.log.{router}"

            # Lets start configuring...
            birdplan = BirdPlan()

            # Set test mode
            birdplan.birdconf.test_mode = True

            # Work out the macro's we'll be using
            macros = {"@LOGFILE@": bird_logfile}
            if extra_macros and (router in extra_macros):
                macros.update(extra_macros[router])

            # Load yaml config
            birdplan.load(f"{self.test_dir}/{router}.yaml", macros)

            # Generate BIRD config
            birdplan.generate(bird_conffile)
            sim.add_conffile(f"CONFFILE({router})", bird_conffile)
            sim.add_logfile(f"LOGFILE({router})", bird_logfile)

            # Add the birdplan configuration object to the simulation
            sim.add_config(router, birdplan)

    def _test_setup(self, sim, tmpdir):
        """Set up a BIRD test scenario using our attributes."""

        extra_macros = {}
        # Loop with routers and build our extra_macros
        for router in self.routers:
            # Loop with supported attributes that translate into macros
            for attr in ["asn", "peer_asn", "peer_type", "global_config", "extra_config"]:
                # Router specific lookup for an attribute to add a macro for
                router_attr = f"{router}_{attr}"
                if hasattr(self, router_attr):
                    value = getattr(self, router_attr)
                else:
                    value = ""
                # Check if we have config for this router, if we don't initialize it
                if router not in extra_macros:
                    extra_macros[router] = {}
                # Add our macro
                extra_macros[router][f"@{attr.upper()}@"] = value
        # Configure our simulator with the BIRD routers
        self._configure_bird_routers(sim, tmpdir, extra_macros)
        print("Adding routers...")
        for router in self.routers:
            sim.add_node(BirdRouterNode(name=router, configfile=f"{tmpdir}/bird.conf.{router}"))

        # Loop with our ExaBGP's and create the nodes
        for exabgp in self.exabgps:
            # Grab ExaBGP's ASN
            exabgp_asn = getattr(self, f"{exabgp}_asn")
            # Work out config file name
            exabgp_conffile = f"{self.test_dir}/exabgp.conf.{exabgp}.as{exabgp_asn}"
            # Add ExaBGP node
            sim.add_node(ExaBGPRouterNode(name=exabgp, configfile=exabgp_conffile))
            # Add config file to our simulation so we get a report for it
            sim.add_conffile(f"CONFFILE({exabgp})", exabgp_conffile)
            # Work out the log file name and add it to our simulation so we get a report for it too
            exalogfile = sim.node(exabgp).logfile
            sim.add_logfile(f"LOGFILE({exabgp}) => {exalogfile}", sim.node(exabgp).logfile)

        print("Adding interfaces...")
        # Loop with routers
        for router in self.routers:
            # Get configuration for this router
            router_interfaces = getattr(self, f"{router}_interfaces")
            # Loop with its interfaces
            for interface in router_interfaces:
                # Grab interface config
                config = getattr(self, f"{router}_interface_{interface}")
                # Add each interface
                sim.node(router).add_interface(interface, config["mac"], config["ips"])
        # Loop with ExaBGP's
        for exabgp in self.exabgps:
            # Get configuration for this ExaBGP instance
            exabgp_interfaces = getattr(self, f"{exabgp}_interfaces")
            # Loop with its interfaces
            for interface in exabgp_interfaces:
                # Grab interface config
                config = getattr(self, f"{exabgp}_interface_{interface}")
                sim.node(exabgp).add_interface(interface, config["mac"], config["ips"])

        print("Adding switches...")
        sim.add_node(SwitchNode("s1"))
        # Loop with BIRD routers
        for router in self.routers:
            # Add eth0 to the switch
            sim.node("s1").add_interface(sim.node(router).interface("eth0"))
        # Loop with ExaBGP instances
        for exabgp in self.exabgps:
            # Add eth0 to the switch
            sim.node("s1").add_interface(sim.node(exabgp).interface("eth0"))

        # Simulate our topology
        print("Simulate topology...")
        sim.run()

    def _bird_route_table(self, sim: Simulation, name: str, route_table_name: str, **kwargs) -> Any:
        """Routing table retrieval helper."""
        # Grab the route table
        route_table = sim.node(name).birdc_show_route_table(route_table_name, **kwargs)
        # Add report
        sim.add_report_obj(f"BIRD({name})[{route_table_name}]", route_table)
        # Return route table
        return route_table

    def _bird_bgp_peer_table(self, sim: Simulation, name: str, peer_name: str, ipv: int) -> str:
        """Get a bird BGP peer table name."""
        return sim.config(name).birdconf.protocols.bgp.peer(peer_name).bgp_table_name(ipv)

    def _bird_log_matches(self, sim: Simulation, name: str, matches: str) -> bool:
        """Check if the BIRD log file contains a string."""

        logname = f"LOGFILE({name})"
        # Make sure the log name exists
        if logname not in sim.logfiles:
            raise RuntimeError(f"Log name not found: {logname}")

        tries = 0
        while True:
            # If we've tried too many times, return false
            if tries > 10:
                return False
            # Open log file and read in the log
            with open(sim.logfiles[logname], "r") as logfile:
                log_str = logfile.read()
            # Check if the log contains what we're looking for
            if re.search(matches, log_str):
                return True
            # Bump tries
            tries += 1
            time.sleep(1)

    def _exabgpcli(self, sim: Simulation, name: str, args: List[str], report_title: str = "") -> List[str]:
        """Run the ExaBGP cli."""
        # Grab the route table
        output = sim.node(name).exabgpcli(args)
        # Add report
        sim.add_report_obj(f"EXABGP({name})[command{report_title}]", args)
        sim.add_report_obj(f"EXABGP({name})[output{report_title}]", output)
        # Return route table
        return output

    def _check_main_bgp_tables_empty(self, sim):
        """Test BIRD t_bgp4 table."""

        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {}
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {}
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"
