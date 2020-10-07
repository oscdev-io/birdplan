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
import importlib
import logging
import os
import re
import time
import pathlib
import pprint
import pytest
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.exabgp_router_node import ExaBGPRouterNode
from nsnetsim.switch_node import SwitchNode
from birdplan.cmdline import BirdPlanCommandLine  # pylint: disable=import-error
from .simulation import Simulation


BirdConfigMacros = Optional[Dict[str, Dict[str, str]]]

#
# Test case base classes
#


@pytest.mark.incremental
class BirdPlanBaseTestCase:
    """Base test case for our tests."""

    sim: Simulation

    # List of ExaBGP nodes to create, eg. ["e1"]
    exabgps = []

    # List of bird routers to configure, eg. ["r1", "r2"]
    routers = ["r1"]

    # List of switches to create
    switches = ["s1"]

    # Supported attributes include
    # rX_peer_asn
    # rX_peer_type
    # rX_global_config
    # rX_extra_config

    # Default ASN to use for r1's peer
    r1_asn = 65000
    r1_peer_asn = 65001
    r1_interfaces = ["eth0"]
    r1_interface_eth0 = {"mac": "02:01:00:00:00:01", "ips": ["100.64.0.1/24", "fc00:100::1/64"]}
    r1_interface_eth1 = {"mac": "02:01:00:00:00:02", "ips": ["100.101.0.1/24", "fc00:101::1/64"]}
    r1_switch_eth0 = "s1"

    r2_asn = 65001
    r2_peer_asn = 65000
    r2_interfaces = ["eth0"]
    r2_interface_eth0 = {"mac": "02:02:00:00:00:01", "ips": ["100.64.0.2/24", "fc00:100::2/64"]}
    r2_interface_eth1 = {"mac": "02:02:00:00:00:02", "ips": ["100.102.0.1/24", "fc00:102::1/64"]}
    r2_switch_eth0 = "s1"

    r3_asn = 65002
    r3_peer_asn = 65000
    r3_interfaces = ["eth0"]
    r3_interface_eth0 = {"mac": "02:03:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}
    r3_switch_eth0 = "s1"

    e1_asn = 65001
    e1_interfaces = ["eth0"]
    e1_interface_eth0 = {"mac": "02:e1:00:00:00:01", "ips": ["100.64.0.2/24", "fc00:100::2/64"]}
    e1_switch_eth0 = "s1"

    def _test_setup(self, sim, testpath, tmpdir):
        """Set up a BIRD test scenario using our attributes."""

        # Grab the directory the test is running in
        test_dir = os.path.dirname(testpath)

        # Grab the filename of the test
        test_filename = os.path.basename(testpath)

        # Work out the expected file path
        sim.expected_path = f"{test_dir}/expected{test_filename[4:]}"

        # Configure our simulator with the BIRD routers
        self._configure_bird_routers(sim, test_dir, tmpdir)
        for router in self.routers:
            sim.add_node(BirdRouterNode(name=router, configfile=f"{tmpdir}/bird.conf.{router}"))

        # Loop with our ExaBGP's and create the nodes
        for exabgp in self.exabgps:
            # Grab ExaBGP's ASN
            exabgp_asn = getattr(self, f"{exabgp}_asn")
            # Work out config file name
            exabgp_conffile = f"{test_dir}/exabgp.conf.{exabgp}.as{exabgp_asn}"
            # Add ExaBGP node
            sim.add_node(ExaBGPRouterNode(name=exabgp, configfile=exabgp_conffile))
            # Add config file to our simulation so we get a report for it
            sim.add_conffile(f"CONFFILE({exabgp})", exabgp_conffile)
            # Work out the log file name and add it to our simulation so we get a report for it too
            exalogfile = sim.node(exabgp).logfile
            sim.add_logfile(f"LOGFILE({exabgp}) => {exalogfile}", sim.node(exabgp).logfile)

        # Loop with switches to create
        for switch in self.switches:
            sim.add_node(SwitchNode(switch))

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
                # Check if this interface should be connected to a switch
                switch_attr = f"{router}_switch_{interface}"
                if hasattr(self, switch_attr):
                    switch = getattr(self, switch_attr)
                    sim.node(switch).add_interface(sim.node(router).interface(interface))
        # Loop with ExaBGP's
        for exabgp in self.exabgps:
            # Get configuration for this ExaBGP instance
            exabgp_interfaces = getattr(self, f"{exabgp}_interfaces")
            # Loop with its interfaces
            for interface in exabgp_interfaces:
                # Grab interface config
                config = getattr(self, f"{exabgp}_interface_{interface}")
                sim.node(exabgp).add_interface(interface, config["mac"], config["ips"])
                # Check if this interface should be connected to a switch
                switch_attr = f"{exabgp}_switch_{interface}"
                if hasattr(self, switch_attr):
                    switch = getattr(self, switch_attr)
                    sim.node(switch).add_interface(sim.node(exabgp).interface(interface))

        # Simulate our topology
        sim.run()

    def _test_bird_status(self, sim):
        """Test all bird instances are up and responding."""

        # Loop with BIRD routers
        for router in self.routers:
            # Grab BIRD status
            status_output = sim.node(router).birdc_show_status()
            # Add status to the reprot
            sim.add_report_obj(f"STATUS({router})", status_output)

            # Grab router ID
            router_id = router[1:]

            # Check BIRD router ID
            assert "router_id" in status_output, f"The status output should have 'router_id' for BIRD router '{router}'"
            assert status_output["router_id"] == f"0.0.0.{router_id}", f"The router ID should be '0.0.0.{router_id}'"

        # Check if we're delaying testing (for convergeance)
        if sim.delay:
            time.sleep(sim.delay)

    def _test_bird_routers_table_bgp_peers(self, ipv: int, sim, routers: Optional[List[str]] = None):
        """Test BIRD BGP peer routing table."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        # Loop with routers...
        for router in routers:
            # Loop with all our peers...
            for peer in sim.config(router).birdconf.protocols.bgp.peers:
                # Grab the peer table name
                table_name = self._bird_bgp_peer_table(sim, router, peer, ipv)
                # Test the table
                self._test_bird_table(router, table_name, sim)

    def _test_bird_routers_table(self, table_name: str, sim, routers: Optional[List[str]] = None):
        """Test BIRD routing table for all routers, or those specified."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        # Loop with our BIRD routers
        for router in routers:
            self._test_bird_table(router, table_name, sim)

        # TODO -
        #  Loop with routers
        #    - Get data and add variables
        #  Loop with routers
        #    - Assert table contents

    def _test_bird_table(self, router: str, table_name: str, sim):
        """Test BIRD routing table for a single router."""

        # Grab the the test data module
        expected_data = self._get_expected_data(sim)

        # Work out variable names
        table_variable_name = f"{router}_{table_name}"
        expect_content_variable_name = f"{table_variable_name}_expect_content"

        # Grab table data
        table_data = self._get_expected_data_item(expected_data, table_variable_name)
        expect_content = self._get_expected_data_item(expected_data, expect_content_variable_name)

        # If we didn't find expect_content in the expected results file, check our test case...
        if not expect_content and hasattr(self, expect_content_variable_name):
            expect_content = getattr(self, expect_content_variable_name)

        # If we have entries in our routing table, we set expect_count to that number, else we don't use expect_count by
        # setting it to None
        expect_count = None
        if isinstance(table_data, dict):
            expect_count = len(table_data) or None

        # Grab the routers table from BIRD
        route_table = self._bird_route_table(sim, router, table_name, expect_count=expect_count, expect_content=expect_content)

        # Add report
        report = f"{table_variable_name} = " + pprint.pformat(route_table)
        sim.add_report_obj(f"BIRD({router})[{table_name}]", report)
        # Add variable so we can keep track of its expected content for later
        sim.add_variable(table_variable_name, report)

        # Make sure table matches
        assert route_table == table_data, f"BIRD router '{router}' table '{table_name}' does not match what it should be"

    def _test_os_rib(self, table_name: str, sim):
        """Test OS routing table."""

        # Loop with our BIRD routers
        for router in self.routers:
            # Grab the the test data module
            expected_data = self._get_expected_data(sim)

            # Work out variable names
            table_variable_name = f"{router}_{table_name}"

            # Grab table data
            table_data = self._get_expected_data_item(expected_data, table_variable_name)

            # Grab the RIB table from the OS
            route_table = sim.node(router).run_ip(["--family", table_name, "route", "list"])

            # Add report
            report = f"{table_variable_name} = " + pprint.pformat(route_table, width=132, compact=True)
            sim.add_report_obj(f"OS_RIB({router})[{table_name}]", report)
            # Add variable so we can keep track of its expected content for later
            sim.add_variable(table_variable_name, report)

            # Make sure table matches
            assert route_table == table_data, f"BIRD router '{router}' RIB '{table_name}' does not match what it should be"

    def _get_expected_data(self, sim):
        """Grab the test data module."""

        # Grab relative path of our expected results file
        relpath = pathlib.Path(sim.expected_path).relative_to(os.path.dirname(__file__))

        # Grab the expected results filename
        module_filename = os.path.basename(relpath)

        # Work out the directory name of the expected results file
        module_dirname = f"tests/{os.path.dirname(relpath)}"

        # Grab the expected results module package name, which is the directory name with / replaced with .
        module_pkgname = module_dirname.replace("/", ".")

        # Remove the .py from the data module
        module_name = f".{module_filename[:-3]}"

        # Import data module, remove .py from the data_module_filename
        try:
            expected_data = importlib.import_module(module_name, module_pkgname)
        except ModuleNotFoundError:
            expected_data = None

        return expected_data

    def _get_expected_data_item(self, expected_data, symbol_name: str) -> Any:
        """Get an item from our data module."""

        data = None
        # But if we have a variable set for this router and table, use it instead
        if hasattr(expected_data, symbol_name):
            symbol = getattr(expected_data, symbol_name)
            # If the symbol is a callable, then call it with self
            if callable(symbol):
                data = symbol(self)
            else:
                data = symbol

        return data

    def _configure_bird_routers(self, sim: Simulation, test_dir: str, tmpdir: str):
        """Create our configuration files."""
        # Generate config files
        for router in self.routers:
            self._birdplan_run(sim, test_dir, tmpdir, router, ["configure"])

    def _birdplan_run(self, sim: Simulation, test_dir: str, tmpdir: str, router: str, args: List[str]) -> Any:
        """Run BirdPlan for a given router."""

        # Work out file names
        birdplan_file = f"{tmpdir}/birdplan.yaml.{router}"
        bird_conffile = f"{tmpdir}/bird.conf.{router}"
        bird_statefile = f"{tmpdir}/bird.state.{router}"
        bird_logfile = f"{tmpdir}/bird.log.{router}"

        # Loop with supported attributes that translate into macros
        internal_macros = {}
        for attr in ["asn", "peer_asn", "peer_type", "global_config", "extra_config"]:
            # Router specific lookup for an attribute to add a macro for
            router_attr = f"{router}_{attr}"
            if hasattr(self, router_attr):
                value = getattr(self, router_attr)
            else:
                value = ""
            # Add our macro
            internal_macros[f"@{attr.upper()}@"] = value

        # Work out the macro's we'll be using
        macros = {"@LOGFILE@": bird_logfile}
        if internal_macros:
            macros.update(internal_macros)

        router_config_file = f"{test_dir}/{router}.yaml"
        # If the router config file does not exist in the test dir, look one directory upwards
        if not os.path.exists(router_config_file):
            router_config_file = f"{os.path.dirname(test_dir)}/{router}.yaml"

        # Read in configuration file
        with open(router_config_file, "r") as file:
            raw_config = file.read()
        # Check if we're replacing macros in our configuration file
        for macro, value in macros.items():
            if isinstance(value, int):
                value = f"{value}"
            raw_config = raw_config.replace(macro, value)
        # Write out new BirdPlan file with macros replaced
        with open(birdplan_file, "w") as file:
            file.write(raw_config)

        # Invoke by simulating the commandline...
        birdplan_cmdline = BirdPlanCommandLine()
        # Disable logging for filelog
        logging.getLogger("filelock").setLevel(logging.ERROR)
        # Set test mode
        birdplan_cmdline.birdplan.birdconf.test_mode = True
        # Run BirdPlan as if it was from the commandline
        result = birdplan_cmdline.run(
            [
                "--birdplan-file",
                birdplan_file,
                "--bird-config-file",
                bird_conffile,
                "--birdplan-state-file",
                bird_statefile,
                *args,
            ]
        )

        # Add test report sections
        sim.add_conffile(f"CONFFILE({router})", bird_conffile)
        sim.add_logfile(f"LOGFILE({router})", bird_logfile)

        # Add the birdplan configuration object to the simulation
        if args[0] == "configure":
            sim.add_config(router, birdplan_cmdline.birdplan)

        return result

    def _birdc(self, sim: Simulation, router: str, query: str) -> Any:
        """Birdc helper."""
        # Grab the output from birdc
        birdc_output = sim.node(router).birdc(query)
        # Add report
        sim.add_report_obj(f"BIRDC({router})[{query}]", birdc_output)
        # Return the output from birdc
        return birdc_output

    def _bird_route_table(self, sim: Simulation, router: str, route_table_name: str, **kwargs) -> Any:
        """Routing table retrieval helper."""
        # Grab the route table
        route_table = sim.node(router).birdc_show_route_table(route_table_name, **kwargs)

        # Loop with routes and remove since fields
        for route in route_table:
            for dest in route_table[route]:
                del dest["since"]

        # Return route table
        return route_table

    def _bird_bgp_peer_table(self, sim: Simulation, router: str, peer_name: str, ipv: int) -> str:
        """Get a bird BGP peer table name."""
        return sim.config(router).birdconf.protocols.bgp.peer(peer_name).bgp_table_name(ipv)

    def _bird_log_matches(self, sim: Simulation, router: str, matches: str) -> bool:
        """Check if the BIRD log file contains a string."""

        logname = f"LOGFILE({router})"
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

    def _exabgpcli(self, sim: Simulation, exabgp_name: str, args: List[str], report_title: str = "") -> List[str]:
        """Run the ExaBGP cli."""
        # Grab the route table
        output = sim.node(exabgp_name).exabgpcli(args)
        # Add report
        sim.add_report_obj(f"EXABGP({exabgp_name})[command{report_title}]", args)
        sim.add_report_obj(f"EXABGP({exabgp_name})[output{report_title}]", output)
        # Return route table
        return output

    def _check_main_bgp_tables_empty(self, sim):
        """Test BIRD t_bgp4 table."""

        raise DeprecationWarning("This shouldn't be used")

        bgp4_table = self._bird_route_table(sim, "r1", "t_bgp4")
        bgp6_table = self._bird_route_table(sim, "r1", "t_bgp6")

        # Check bgp4 BIRD table
        correct_result = {}
        assert bgp4_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"

        # Check bgp6 BIRD table
        correct_result = {}
        assert bgp6_table == correct_result, "Result for R1 BIRD t_bgp4 routing table does not match what it should be"
