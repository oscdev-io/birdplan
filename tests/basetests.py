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

from typing import Any, Dict, List, Optional, Tuple
import inspect
import logging
import os
import re
import time
import pprint
import pytest
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.exabgp_router_node import ExaBGPRouterNode
from nsnetsim.switch_node import SwitchNode
from birdplan.cmdline import BirdPlanCommandLine
from birdplan.exceptions import BirdPlanError
from .simulation import Simulation


BirdConfigMacros = Optional[Dict[str, Dict[str, str]]]

#
# Test case base classes
#


@pytest.mark.incremental
class BirdPlanBaseTestCase:
    """Base test case for our tests."""

    # List of ExaBGP nodes to create, eg. ["e1"]
    exabgps = []

    # List of bird routers to configure, eg. ["r1", "r2"]
    routers = ["r1"]

    # List of switches to create
    switches = ["s1"]

    # Routers configuration exception catching
    routers_config_exception = {}

    # Extra macros to pull in
    template_macros = []

    # Supported attributes include:
    # rX_asn
    # rX_peer_asn
    # rX_peer_type
    # rX_global_config
    # rX_extra_config
    # rX_interfaces = [...]
    # rX_interface_ethY = {...}
    # rX_switch_ethY = "sZ"

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

    e2_asn = 65001
    e2_interfaces = ["eth0"]
    e2_interface_eth0 = {"mac": "02:e2:00:00:00:01", "ips": ["100.64.0.3/24", "fc00:100::3/64"]}
    e2_switch_eth0 = "s1"

    def _test_setup(self, sim, testpath, tmpdir):  # pylint: disable=too-many-locals
        """Set up a BIRD test scenario using our attributes."""

        # Set test we're currently running
        sim.set_test(testpath)

        # Configure our simulator with the BIRD routers
        configured_routers = self._configure_bird_routers(sim, tmpdir)
        for router in configured_routers:
            sim.add_node(BirdRouterNode(name=router, configfile=f"{tmpdir}/bird.conf.{router}", debug=True))

        # Loop with our ExaBGP's and create the nodes
        self._configure_exabgps(sim, tmpdir)
        for exabgp in self.exabgps:
            # Add ExaBGP node
            sim.add_node(ExaBGPRouterNode(name=exabgp, configfile=f"{tmpdir}/exabgp.conf.{exabgp}"))
            # Work out the log file name and add it to our simulation so we get a report for it too
            exabgp_logfile = sim.node(exabgp).logfile
            # sim.add_logfile(f"EXABGP_LOGFILE({exabgp}) => {exabgp_logfile}", exabgp_logfile)
            sim.add_logfile(f"EXABGP_LOGFILE({exabgp})", exabgp_logfile)

        # Loop with switches to create
        for switch in self.switches:
            sim.add_node(SwitchNode(switch))

        # Loop with routers
        for router in configured_routers:
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

        # Load data we may have
        sim.load_data()

        # Simulate our topology
        sim.run()

    def _test_bird_status(self, sim: Simulation):
        """Test all bird instances are up and responding."""

        # Loop with BIRD routers
        for router in self.routers:
            # If the node does not exist, then go to the next one, this means it was not configured
            if not sim.node(router):
                continue
            # Grab BIRD status
            status_output = sim.node(router).birdc_show_status()
            # Add status to the reprot
            sim.add_report_obj(f"BIRD_STATUS({router})", status_output)

            # Grab router ID
            router_id = router[1:]

            # Check BIRD router ID
            assert "router_id" in status_output, f"The status output should have 'router_id' for BIRD router '{router}'"
            assert status_output["router_id"] == f"0.0.0.{router_id}", f"The router ID should be '0.0.0.{router_id}'"

        # Check if we're delaying testing (for convergeance)
        if sim.delay:
            time.sleep(sim.delay)

    def _test_bird_routers_table_bgp_peers(self, sim: Simulation, ipv: int, routers: Optional[List[str]] = None):
        """Test BIRD BGP peer routing table."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        # Assertion data
        assert_data = {}

        # Loop with routers
        for router in routers:
            # Skip over routers not configured
            if not sim.node(router):
                continue
            # Loop with all the routers peers
            for peer in sim.config(router).birdconf.protocols.bgp.peers:
                # Grab the peer table name
                table_name = self._bird_bgp_peer_table(sim, router, peer, ipv)
                # Check if the router exists, if not add
                if router not in assert_data:
                    assert_data[router] = {}
                # Grab data for assertion below
                assert_data[router][table_name] = self._get_bird_table_data(sim, router, table_name)

        # Run asserts on the data received
        for router in assert_data:
            for table_name, data in assert_data[router].items():
                # Name variables nicely so they look good in our test output
                received_data, expected_data = data
                # Make sure table matches
                assert (
                    received_data == expected_data
                ), f"BIRD router '{router}' peer table '{table_name}' does not match what it should be"

    def _test_bird_routers_table(self, sim: Simulation, table_name: str, routers: Optional[List[str]] = None):
        """Test BIRD routing table for all routers, or those specified."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        # Assertion data
        assert_data = {}

        # Loop with our BIRD routers and grab the data for assertion below
        for router in routers:
            # Skip over routers not configured
            if not sim.node(router):
                continue
            # Grab assert data
            assert_data[router] = self._get_bird_table_data(sim, router, table_name)

        # Run asserts on the data received
        for router, data in assert_data.items():
            # Name variables nicely so they look good in our test output
            received_data, expected_data = data
            # Make sure table matches
            assert received_data == expected_data, f"BIRD router '{router}' table '{table_name}' does not match what it should be"

    def _get_bird_table_data(self, sim: Simulation, router: str, table_name: str) -> Tuple[Any, Any]:
        """Get the bird table received data and expected data."""

        # Work out variable names
        data_name = f"{router}_{table_name}"

        # Grab table data
        result_expected = sim.get_data(data_name)

        # Save the start time
        time_start = time.time()

        # Start with a blank result
        expect_timeout = 120
        result = []
        content_matches = False
        while True:
            # Grab the routers table from BIRD
            result = self._bird_route_table(sim, router, table_name)

            # If we don't have a content match, we match as we have a sleep() after bird status
            # The first case is when there is no expected data
            # The second case is when this item is missing from the expected data
            if result_expected is None or isinstance(result_expected, ValueError):
                content_matches = True
            # Else check that the result contains the content we're looking for
            elif result_expected == result:
                content_matches = True

            # Check if have what we expected
            if content_matches:
                break

            # If not, check to see if we've exceeded our timeout
            if time.time() - time_start > expect_timeout:
                break

            time.sleep(0.5)

        # Sort nexthops by protocol
        for nexthops in result.values():
            nexthops.sort(key=lambda item: item["protocol"])

        # Add report
        report_result = pprint.pformat(result, width=132, compact=True)
        sim.add_report_obj(f"BIRD_TABLE({router})[{table_name}]", f"{data_name} = {report_result}")
        # Add variable so we can keep track of its expected content for later
        sim.add_variable(data_name, result)
        # If we didn't match add the incorrect result to the report too
        if not content_matches:
            report_expected = pprint.pformat(result_expected, width=132, compact=True)
            sim.add_report_obj(f"EXPECTED_BIRD_TABLE({router})[{table_name}]", f"{data_name} = {report_expected}")

        # Return the two chunks of data for later assertion
        return (result, result_expected)

    def _test_os_rib(self, sim: Simulation, table_name: str, routers: Optional[List[str]] = None):
        """Test OS routing table."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        # Assertion data
        assert_data = {}

        # Loop with our BIRD routers and grab the data for assertion below
        for router in routers:
            # Skip over routers not configured
            if not sim.node(router):
                continue
            # Grab assert data
            assert_data[router] = self._get_os_rib_data(sim, router, table_name)

        # Run asserts on the data received
        for router, data in assert_data.items():
            # Name variables nicely so they look good in our test output
            received_data, expected_data = data
            # Make sure table matches
            assert received_data == expected_data, f"BIRD router '{router}' RIB '{table_name}' does not match what it should be"

    def _get_os_rib_data(self, sim: Simulation, router: str, table_name: str) -> Tuple[Any, Any]:
        """Get the OS RIB received data and expected data."""

        # Work out variable names
        data_name = f"{router}_{table_name}"

        # Grab table data
        result_expected = sim.get_data(data_name)

        # Save the start time
        time_start = time.time()

        # Start with a blank result
        expect_timeout = 120
        result = []
        result_matches = False
        while True:
            # Grab the routers table from BIRD
            result = sim.node(router).run_ip(["--family", table_name, "route", "list"])

            # If we don't have a content match, we match as we have a sleep() after bird status
            if result_expected is None:
                result_matches = True
            # Else check that the result contains the content we're looking for
            elif result_expected == result:
                result_matches = True

            # Check if have what we expected
            if result_matches:
                break

            # If not, check to see if we've exceeded our timeout
            if time.time() - time_start > expect_timeout:
                break

            time.sleep(0.5)

        # Add report
        report_result = pprint.pformat(result, width=132, compact=True)
        sim.add_report_obj(f"OS_RIB({router})[{table_name}]", f"{data_name} = {report_result}")
        # Add variable so we can keep track of its expected content for later
        sim.add_variable(data_name, result)
        # If we didn't match add the incorrect result to the report too
        if not result_matches:
            report_expected = pprint.pformat(result_expected, width=132, compact=True)
            sim.add_report_obj(f"EXPECTED_OS_RIB({router})[{table_name}]", f"{data_name} = {report_expected}")

        # Return the two chunks of data for later assertion
        return (result, result_expected)

    def _configure_bird_routers(self, sim: Simulation, tmpdir: str) -> List[str]:
        """Create our configuration files."""
        # Generate config files and keep track of what we configured in the case of exceptions
        configured_routers = []
        for router in self.routers:
            # If we get a positive result, add the router to the list of configured routers
            bird_config = self._birdplan_run(sim, tmpdir, router, ["configure"])
            # If we have None it is expected
            if bird_config is None:
                continue
            # If its however blank, raise exception
            if not bird_config:
                raise RuntimeError(f"BirdPlan failed to configure router '{router}'")
            # Add router to list of configured routers
            configured_routers.append(router)

        return configured_routers

    def _configure_exabgps(self, sim: Simulation, tmpdir: str) -> List[str]:
        """Create our configuration files."""

        # Loop with each ExaBGP
        for exabgp in self.exabgps:
            # Grab the configuration filename we're going to be using
            exabgp_conffile = f"{tmpdir}/exabgp.conf.{exabgp}"

            # Loop with supported attributes that translate into macros
            internal_macros = {}
            for attr in [
                "asn",
                "exabgp_config",
                "exabgp_config_neighbor1",
                "exabgp_config_neighbor2",
                "template_exabgp_config",
                "template_exabgp_config_neighbor1",
                "template_exabgp_config_neighbor2",
            ]:
                # Router specific lookup for an attribute to add a macro for
                router_attr = f"{exabgp}_{attr}"
                if hasattr(self, router_attr):
                    symbol = getattr(self, router_attr)
                    if callable(symbol):
                        symbol_signature = inspect.signature(symbol)
                        if len(symbol_signature.parameters) == 1:
                            value = symbol(sim)
                        else:
                            value = symbol()
                    else:
                        value = symbol
                else:
                    value = ""
                # Add our macro
                internal_macros[f"@{attr.upper()}@"] = value

            # Grab ExaBGP's ASN
            exabgp_asn = internal_macros["@ASN@"]

            # Work out config file name, going 2 levels up in the test directory
            exabgp_config_file = None
            for conffile_path in [
                # With ASN appended
                f"{sim.test_dir}/exabgp.conf.{exabgp}.as{exabgp_asn}",
                # Without ASN appended
                f"{sim.test_dir}/exabgp.conf.{exabgp}",
                # Parent directory with ASN appended
                f"{os.path.dirname(sim.test_dir)}/exabgp.conf.{exabgp}.as{exabgp_asn}",
                # Parent directory without ASN appended
                f"{os.path.dirname(sim.test_dir)}/exabgp.conf.{exabgp}",
                # Parent parent directory with ASN appended
                f"{os.path.dirname(os.path.dirname(sim.test_dir))}/exabgp.conf.{exabgp}.as{exabgp_asn}",
                # Parent parent directory without ASN appended
                f"{os.path.dirname(os.path.dirname(sim.test_dir))}/exabgp.conf.{exabgp}",
            ]:
                if os.path.exists(conffile_path):
                    exabgp_config_file = conffile_path
                    break
            # If we didn't get a configuration file that exists, then raise an exception
            if not exabgp_config_file:
                raise RuntimeError(f"No ExaBGP configuration file found for ExaBGP '{exabgp}' with ASN '{exabgp_asn}'")

            # Read in configuration file
            with open(exabgp_config_file, "r") as file:
                raw_config = file.read()
            # Check if we're replacing macros in our configuration file
            for macro, value in internal_macros.items():
                if isinstance(value, int):
                    value = f"{value}"
                raw_config = raw_config.replace(macro, value)
            # Write out new BirdPlan file with macros replaced
            with open(exabgp_conffile, "w") as file:
                file.write(raw_config)

            # Add config file to our simulation so we get a report for it
            sim.add_conffile(f"exabgp.conf.{exabgp}", exabgp_conffile)

    def _birdplan_run(  # pylint: disable=too-many-arguments,too-many-locals
        self, sim: Simulation, tmpdir: str, router: str, args: List[str]
    ) -> Any:
        """Run BirdPlan for a given router."""

        # Work out file names
        birdplan_file = f"{tmpdir}/birdplan.yaml.{router}"
        bird_conffile = f"{tmpdir}/bird.conf.{router}"
        bird_statefile = f"{tmpdir}/bird.state.{router}"
        bird_logfile = f"{tmpdir}/bird.log.{router}"

        # Work out what attributes we support for macros
        attr_list = [
            "asn",
            "peer_asn",
            "peer_type",
            "extra_config",
            "global_config",
            "peer_config",
            "peer_extra_config",
            "allpeer_config",
            "allpeer_extra_config",
            "template_extra_config",
            "template_global_config",
            "template_peer_config",
            "template_peer_extra_config",
            "template_allpeer_config",
        ]
        extra_attr_list = getattr(self, "template_macros")
        if extra_attr_list:
            attr_list.extend(extra_attr_list)

        # Loop with supported attributes that translate into macros
        internal_macros = {}
        for attr in attr_list:
            # Router specific lookup for an attribute to add a macro for
            router_attr = f"{router}_{attr}"
            if hasattr(self, router_attr):
                symbol = getattr(self, router_attr)
                if callable(symbol):
                    value = symbol()
                else:
                    value = symbol
            else:
                value = ""
            # Add our macro
            internal_macros[f"@{attr.upper()}@"] = value

        # Work out the macro's we'll be using
        macros = {"@LOGFILE@": bird_logfile}
        if internal_macros:
            macros.update(internal_macros)

        # Work out config file name, going up 2 directory levels
        router_config_file = None
        for conffile_path in [
            f"{sim.test_dir}/{router}.yaml",
            # Parent directories
            f"{os.path.dirname(sim.test_dir)}/{router}.yaml",
            f"{os.path.dirname(os.path.dirname(sim.test_dir))}/{router}.yaml",
        ]:
            if os.path.exists(conffile_path):
                router_config_file = conffile_path
                break
        # If we didn't get a configuration file that exists, then raise an exception
        if not router_config_file:
            raise RuntimeError("No router configuration file found")

        # Read in configuration file
        with open(router_config_file, "r") as file:
            raw_config = file.read()
        # Check if we're replacing macros in our configuration file
        for macro, value in macros.items():
            if isinstance(value, int):
                value = f"{value}"
            # Check for odd issues...
            if value is None:
                raise RuntimeError(f"Macro '{macro}' for router '{router}' has value None")
            raw_config = raw_config.replace(macro, value)
        # Write out new BirdPlan file with macros replaced
        with open(birdplan_file, "w") as file:
            file.write(raw_config)

        # Add YAML file early incase we need to check it when configuration fails
        sim.add_conffile(f"birdplan.yaml.{router}", birdplan_file)

        # Invoke by simulating the commandline...
        birdplan_cmdline = BirdPlanCommandLine(test_mode=True)
        # Disable logging for filelog
        logging.getLogger("filelock").setLevel(logging.ERROR)

        # Work out our commandline arguments
        cmdline_args = [
            "--birdplan-file",
            birdplan_file,
            "--birdplan-state-file",
            bird_statefile,
            *args,
        ]

        # If this is the configure command, we need to output the configuration file
        if args[0] == "configure":
            cmdline_args.extend(["--output-file", bird_conffile])

        # Check if we should get an exception or not
        if router in self.routers_config_exception:
            with pytest.raises(BirdPlanError, match=self.routers_config_exception[router]):
                # Run BirdPlan as if it was from the commandline
                birdplan_cmdline.run(cmdline_args)
            # Return after we got the exception
            return None

        # Run BirdPlan as if it was from the commandline
        result = birdplan_cmdline.run(cmdline_args)

        # Add test report sections
        sim.add_logfile(f"bird.log.{router}", bird_logfile)

        # Add the birdplan configuration object to the simulation
        if args[0] == "configure":
            sim.add_conffile(f"bird.conf.{router}", bird_conffile)
            sim.add_config(router, birdplan_cmdline.birdplan)

        return result

    def _birdc(self, sim: Simulation, router: str, query: str, add_report: bool = True) -> Any:
        """Birdc helper."""
        # Grab the output from birdc
        birdc_output = sim.node(router).birdc(query)

        # Check if we need to add the report
        if add_report:
            sim.add_report_obj(f"BIRDC({router})[{query}]", birdc_output)

        # Return the output from birdc
        return birdc_output

    def _bird_route_table(self, sim: Simulation, router: str, route_table_name: str, **kwargs) -> Any:
        """Routing table retrieval helper."""
        # Grab the route table
        route_table = sim.node(router).birdc_show_route_table(route_table_name, **kwargs)

        # Loop with routes in the table
        for route in route_table:
            # Loop with each destination
            for dest in route_table[route]:
                # Remove since field
                del dest["since"]
                # If this is OSPF type I, we need to remove the router_id to prevent a race condition depending which router
                # comes up first.
                if "ospf_type" in dest and dest["ospf_type"] == "I":
                    # Remove router_id
                    if "router_id" not in dest:
                        raise RuntimeError("OSPF should have a 'router_id', but does not")
                    del dest["router_id"]
                    # Check if we have attributes and if the router_id is there
                    if "attributes" in dest and "OSPF.router_id" in dest["attributes"]:
                        del dest["attributes"]["OSPF.router_id"]
            # Sort route table so its consistent
            route_table[route].sort(key=repr)

        # Return route table
        return route_table

    def _bird_bgp_peer_table(self, sim: Simulation, router: str, peer_name: str, ipv: int) -> str:
        """Get a bird BGP peer table name."""
        return sim.config(router).birdconf.protocols.bgp.peer(peer_name).bgp_table_name(ipv)

    def _bird_log_matches(self, sim: Simulation, router: str, matches: str) -> bool:
        """Check if the BIRD log file contains a string."""

        logname = f"bird.log.{router}"
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
