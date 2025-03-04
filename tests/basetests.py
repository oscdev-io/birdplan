#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""Base test classes for our tests."""

# pylint: disable=too-many-lines

import copy
import inspect
import logging
import os
import pprint
import re
import time
from typing import Any, Optional

import pytest
from nsnetsim.bird_router_node import BirdRouterNode
from nsnetsim.exabgp_router_node import ExaBGPRouterNode
from nsnetsim.stayrtr_server_node import StayRTRServerNode
from nsnetsim.switch_node import SwitchNode

from birdplan.cmdline import BirdPlanCommandLine, BirdPlanCommandlineResult
from birdplan.exceptions import BirdPlanError

from .openssh import generate_openssh_keypair
from .simulation import Simulation

__all__ = ["BirdPlanBaseTestCase"]


BirdConfigMacros = Optional[dict[str, dict[str, str]]]

#
# Test case base classes
#


@pytest.mark.incremental
class BirdPlanBaseTestCase:
    """Base test case for our tests."""

    # List of ExaBGP nodes to create, eg. ["e1"]
    exabgps = []

    # List of StayRTR nodes to create, eg. ["a1"]
    stayrtrs = []

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

    def _test_setup(  # pylint: disable=too-many-locals, too-many-branches, too-many-statements
        self, sim, testpath, tmpdir
    ):
        """Set up a BIRD test scenario using our attributes."""

        # Set test we're currently running
        sim.set_test(testpath)

        # Loop with switches to create
        for switch in self.switches:
            sim.add_node(SwitchNode(switch))

        # Loop with our StayRTR instances and create the nodes
        self._configure_stayrtrs(sim, tmpdir)
        for stayrtr in self.stayrtrs:
            # Check if we're using SSH between BIRD and StayRTR
            extra_stayrtr_params = {}

            # Check if we have ${stayrtr}_use_ssh
            if hasattr(self, f"{stayrtr}_use_ssh"):
                stayrtr_use_ssh = getattr(self, f"{stayrtr}_use_ssh")
                if stayrtr_use_ssh:
                    # Grenerate SSH keys
                    server_privkey, _ = generate_openssh_keypair()
                    client_privkey, client_pubkey = generate_openssh_keypair()

                    # Write out server private key and change mode to 0600
                    server_privkey_file = f"{tmpdir}/stayrtr.privkey.server.{stayrtr}"
                    with open(server_privkey_file, "w", encoding="UTF-8") as f:
                        f.write(server_privkey)
                    os.chmod(server_privkey_file, 0o600)
                    # Set stayrtr arg for the private key file
                    extra_stayrtr_params["ssh_key_file"] = server_privkey_file

                    # Write out server authorized keys file
                    server_authorized_keys_file = f"{tmpdir}/stayrtr.authorized_keys.{stayrtr}"
                    with open(server_authorized_keys_file, "w", encoding="UTF-8") as f:
                        f.write(client_pubkey)
                    # Set stayrtr arg for the authorized keys file
                    extra_stayrtr_params["ssh_authorized_keys_file"] = server_authorized_keys_file

                    # Write out client private key and change mode to 0600
                    client_privkey_file = f"{tmpdir}/stayrtr.privkey.client.{stayrtr}"
                    with open(client_privkey_file, "w", encoding="UTF-8") as f:
                        f.write(client_privkey)
                    os.chmod(client_privkey_file, 0o600)
                    # Set the private key location for this instance
                    setattr(self, f"{stayrtr}_private_keyfile", client_privkey_file)

            # Set up log file
            stayrtr_logfile = f"{tmpdir}/stayrtr.log.{stayrtr}"
            sim.add_logfile(f"STAYRTR_LOGFILE({stayrtr})", stayrtr_logfile)

            # Add StayRTR server node
            sim.add_node(
                StayRTRServerNode(
                    name=stayrtr,
                    slurmfile=f"{tmpdir}/stayrtr.slurm.json.{stayrtr}",
                    logfile=stayrtr_logfile,
                    **extra_stayrtr_params,
                    args=["-loglevel", "debug"],
                )
            )

        # Loop with our ExaBGP's and create the nodes
        self._configure_exabgps(sim, tmpdir)
        for exabgp in self.exabgps:
            # Add ExaBGP node
            sim.add_node(ExaBGPRouterNode(name=exabgp, configfile=f"{tmpdir}/exabgp.conf.{exabgp}"))
            # Work out the log file name and add it to our simulation so we get a report for it too
            exabgp_logfile = sim.node(exabgp).logfile
            # sim.add_logfile(f"EXABGP_LOGFILE({exabgp}) => {exabgp_logfile}", exabgp_logfile)
            sim.add_logfile(f"EXABGP_LOGFILE({exabgp})", exabgp_logfile)

        # NK: This MUST come at the end as it depends on config added by StayRTR (private key file path)
        # Configure our simulator with the BIRD routers
        configured_routers = self._configure_bird_routers(sim, tmpdir)
        for router in configured_routers:
            bird_router_node = BirdRouterNode(
                name=router, configfile=f"{tmpdir}/bird.conf.{router}", controlsocket=f"{tmpdir}/bird.ctl.{router}", debug=False
            )
            sim.add_node(bird_router_node)

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

        # Loop with StayRTR's
        for stayrtrs in self.stayrtrs:
            # Get configuration for this StayRTR instance
            stayrtrs_interfaces = getattr(self, f"{stayrtrs}_interfaces")
            # Loop with its interfaces
            for interface in stayrtrs_interfaces:
                # Grab interface config
                config = getattr(self, f"{stayrtrs}_interface_{interface}")
                sim.node(stayrtrs).add_interface(interface, config["mac"], config["ips"])
                # Check if this interface should be connected to a switch
                switch_attr = f"{stayrtrs}_switch_{interface}"
                if hasattr(self, switch_attr):
                    switch = getattr(self, switch_attr)
                    sim.node(switch).add_interface(sim.node(stayrtrs).interface(interface))

        # Load data we may have
        sim.load_data()

        # Simulate our topology
        sim.run()

    def _test_bird_status(self, sim: Simulation):
        """Test all bird instances are up and responding."""

        # Sleep for sim delay again as routers may of had external changes applied
        if sim.delay:
            time.sleep(sim.delay)

        # Loop with BIRD routers
        for router in self.routers:
            # If the node does not exist, then go to the next one, this means it was not configured
            if not sim.node(router):
                continue
            # Grab BIRD status
            status_output = sim.node(router).birdc_show_status()

            # Grab router ID
            router_id = router[1:]

            if "router_id" not in status_output or status_output["router_id"] != f"0.0.0.{router_id}":
                # Add status to the reprot
                sim.add_report_obj(f"BIRD_STATUS({router})", status_output)

            # Check BIRD router ID
            assert "router_id" in status_output, f"The status output should have 'router_id' for BIRD router '{router}'"
            assert status_output["router_id"] == f"0.0.0.{router_id}", f"The router ID should be '0.0.0.{router_id}'"

    def _test_bird_routers_table_bgp_peers(self, sim: Simulation, ipv: int, routers: list[str] | None = None):
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
        for router, results in assert_data.items():
            for table_name, data in results.items():
                # Name variables nicely so they look good in our test output
                received_data, expected_data = data
                # Make sure table matches
                assert received_data == expected_data, (
                    f"BIRD router '{router}' peer table '{table_name}' does not match what it should be"
                )

    def _test_bird_routers_table(self, sim: Simulation, table_name: str, routers: list[str] | None = None):
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

    def _get_bird_table_data(self, sim: Simulation, router: str, table_name: str) -> tuple[Any, Any]:
        """Get the bird table received data and expected data."""

        # Work out variable names
        data_name = f"{router}_{table_name}"

        # Grab table data
        result_expected = sim.get_data(data_name)

        # Save the start time
        time_start = time.time()

        # Start with a blank result
        expect_timeout = 120
        result = None
        content_matches = False
        while True:
            # Grab the routers table from BIRD
            result = self._bird_route_table(sim, router, table_name)
            # Sort nexthops by protocol
            for nexthops in result.values():
                nexthops.sort(key=lambda item: item["protocol"])

            # If we don't have a content match, we match as we have a sleep() after bird status
            # The first case is when there is no expected data
            # The second case is when this item is missing from the expected data
            if result_expected is None or isinstance(result_expected, ValueError):  # noqa: SIM114
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

        # Add variable so we can keep track of its expected content for later
        sim.add_variable(data_name, result)
        # If we didn't match add the incorrect result to the report too
        if not content_matches:
            # Add report
            report_result = pprint.pformat(result, width=132, compact=True)
            sim.add_report_obj(f"BIRD_TABLE({router})[{table_name}]", f"{data_name} = {report_result}")

            report_expected = pprint.pformat(result_expected, width=132, compact=True)
            sim.add_report_obj(f"EXPECTED_BIRD_TABLE({router})[{table_name}]", f"{data_name} = {report_expected}")

        # Return the two chunks of data for later assertion
        return (result, result_expected)

    def _test_bird_cmdline_ospf_summary(  # pylint: disable=too-many-locals,too-many-branches
        self, sim: Simulation, tmpdir: str, routers: list[str] | None = None
    ):
        """Test showing OSPF summary."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        router_summaries = {}

        # Loop with routers
        for router in routers:
            # Skip over routers not configured
            if not sim.node(router):
                continue
            # Skip over routers with config exceptions
            if router in self.routers_config_exception:
                continue

            # Work out variable names
            data_name = f"{router}_ospf_summary"

            # Grab table data
            result_expected = sim.get_data(data_name)
            router_summaries[router] = {
                "expected": result_expected,
            }

            # Save the start time
            time_start = time.time()

            # Start with a blank result
            expect_timeout = 60
            result = None
            content_matches = False
            while True:
                # Get peer summary
                birdplan_result: BirdPlanCommandlineResult = self._birdplan_run(sim, tmpdir, router, ["ospf", "summary"])

                # We need to deep copy the data as we're removing "since" below
                result = copy.deepcopy(birdplan_result.data)
                router_summaries[router]["result"] = result

                # Remove since from the result
                for _, protocol_data in result.items():
                    # NK: since is dynamic
                    if "since" in protocol_data:
                        del protocol_data["since"]

                # If we don't have a content match, we match as we have a sleep() after bird status
                # The first case is when there is no expected data
                # The second case is when this item is missing from the expected data
                if result_expected is None or isinstance(result_expected, ValueError):  # noqa: SIM114
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

            # Add variable so we can keep track of its expected content for later
            sim.add_variable(data_name, result)
            # If we didn't match add the incorrect result to the report too
            if not content_matches:
                report_expected = pprint.pformat(result_expected, width=132, compact=True)
                sim.add_report_obj(f"EXPECTED_OSPF_SUMMARY({router})", f"{data_name} = {report_expected}")

                sim.add_report_obj(f"OSPF_SUMMARY({router})[json]", birdplan_result.as_json())
                sim.add_report_obj(f"OSPF_SUMMARY({router})[text]", birdplan_result.as_text())

                report_result = pprint.pformat(result, width=132, compact=True)
                sim.add_report_obj(f"OSPF_SUMMARY({router})", f"{data_name} = {report_result}")

        # Loop and assert
        for router, data in router_summaries.items():
            assert data["result"] == data["expected"], f"BIRD router '{router}' OSPF summary does not match what it should be"

    def _test_bird_cmdline_bgp_peer_summary(  # pylint: disable=too-many-locals,too-many-branches
        self, sim: Simulation, tmpdir: str, routers: list[str] | None = None
    ):
        """Test showing BGP peer summary."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        router_summaries = {}

        # Loop with routers
        for router in routers:
            # Skip over routers not configured
            if not sim.node(router):
                continue
            # Skip over routers with config exceptions
            if router in self.routers_config_exception:
                continue

            # Work out variable names
            data_name = f"{router}_peer_summary"

            # Grab table data
            result_expected = sim.get_data(data_name)
            router_summaries[router] = {
                "expected": result_expected,
            }

            # Save the start time
            time_start = time.time()

            # Start with a blank result
            expect_timeout = 60
            result = None
            content_matches = False
            while True:
                # Get peer summary
                birdplan_result: BirdPlanCommandlineResult = self._birdplan_run(sim, tmpdir, router, ["bgp", "peer", "summary"])

                # We need to deep copy the data as we're removing "since" below
                result = copy.deepcopy(birdplan_result.data)
                router_summaries[router]["result"] = result

                # Remove since from the result
                for _, router_data in result.items():
                    if "protocols" not in router_data:
                        continue
                    for _, protocol_data in router_data["protocols"].items():
                        if "status" not in protocol_data:
                            continue
                        # NK: since is dynamic
                        if "since" in protocol_data["status"]:
                            del protocol_data["status"]["since"]
                        # NK: info can change between active/connect
                        if "info" in protocol_data["status"]:
                            if protocol_data["status"]["info"] in ("active", "connect"):
                                protocol_data["status"]["info"] = "active/connect"

                # If we don't have a content match, we match as we have a sleep() after bird status
                # The first case is when there is no expected data
                # The second case is when this item is missing from the expected data
                if result_expected is None or isinstance(result_expected, ValueError):  # noqa: SIM114
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

            # Add variable so we can keep track of its expected content for later
            sim.add_variable(data_name, result)
            # If we didn't match add the incorrect result to the report too
            if not content_matches:
                report_expected = pprint.pformat(result_expected, width=132, compact=True)
                sim.add_report_obj(f"EXPECTED_PEER_SUMMARY({router})", f"{data_name} = {report_expected}")

                sim.add_report_obj(f"PEER_SUMMARY({router})[json]", birdplan_result.as_json())
                sim.add_report_obj(f"PEER_SUMMARY({router})[text]", birdplan_result.as_text())

                report_result = pprint.pformat(result, width=132, compact=True)
                sim.add_report_obj(f"PEER_SUMMARY({router})", f"{data_name} = {report_result}")

        # Loop and assert
        for router, data in router_summaries.items():
            assert data["result"] == data["expected"], f"BIRD router '{router}' peer summary does not match what it should be"

    def _test_bird_cmdline_bgp_peer_show(  # pylint: disable=too-many-locals,too-many-branches
        self, sim: Simulation, tmpdir: str, routers: list[str] | None = None
    ):
        """Test showing BGP peer show."""

        # Check if we didn't get a router list override, if we didn't, then use all routers
        if not routers:
            routers = self.routers

        router_shows = {}

        # Loop with routers
        for router in routers:  # pylint: disable=too-many-nested-blocks
            # Skip over routers not configured
            if not sim.node(router):
                continue
            # Skip over routers with config exceptions
            if router in self.routers_config_exception:
                continue

            router_shows[router] = {}

            # Loop with all the routers peers
            for peer in sim.config(router).birdconf.protocols.bgp.peers:
                # Work out variable names
                data_name = f"{router}_peer_show_{peer}"

                # Grab table data
                result_expected = sim.get_data(data_name)
                router_shows[router][peer] = {
                    "expected": result_expected,
                }

                # Save the start time
                time_start = time.time()

                # Start with a blank result
                expect_timeout = 300
                result = None
                content_matches = False
                while True:
                    # Get peer show
                    birdplan_result: BirdPlanCommandlineResult = self._birdplan_run(
                        sim, tmpdir, router, ["bgp", "peer", "show", peer]
                    )

                    # We need to deep copy the data as we're removing "since" below
                    result = copy.deepcopy(birdplan_result.data)
                    router_shows[router][peer]["result"] = result

                    # Remove since from the result
                    if "protocols" in result:
                        for _, protocol_data in result["protocols"].items():
                            if "status" not in protocol_data:
                                continue
                            # NK: since is dynamic
                            if "since" in protocol_data["status"]:
                                del protocol_data["status"]["since"]
                            # NK: info can change between active/connect
                            if "info" in protocol_data["status"]:
                                if protocol_data["status"]["info"] in ("active", "connect"):
                                    protocol_data["status"]["info"] = "active/connect"
                    # Result used for compare so we can modify it below for data changes when making updates
                    result_compare = copy.deepcopy(result)

                    # NKDEBUG - hook in here to modify data for comparison
                    # if "protocols" in result_compare:
                    #     # for _, protocol_data in result["protocols"].items():
                    #     #     if "prefix_limit_action" in protocol_data:
                    #     #         del protocol_data["prefix_limit_action"]
                    #     if "import_filter_deny" in result_compare:
                    #         del result_compare["import_filter_deny"]
                    # if result_expected and not isinstance(result_expected, ValueError) and "protocols" in result_expected:
                    #     # for _, protocol_data in result_expected["protocols"].items():
                    #     #     if "prefix_limit_action" in protocol_data:
                    #     #         del protocol_data["prefix_limit_action"]
                    #     if "import_filter_deny" in result_expected:
                    #         del result_expected["import_filter_deny"]
                    # router_shows[router][peer]["result"] = result_compare
                    # NKDEBUG end

                    # If we don't have a content match, we match as we have a sleep() after bird status
                    # The first case is when there is no expected data
                    # The second case is when this item is missing from the expected data
                    if result_expected is None or isinstance(result_expected, ValueError):  # noqa: SIM114
                        content_matches = True
                    # Else check that the result contains the content we're looking for
                    elif result_expected == result_compare:
                        content_matches = True

                    # Check if have what we expected
                    if content_matches:
                        break

                    # If not, check to see if we've exceeded our timeout
                    if time.time() - time_start > expect_timeout:
                        break

                    time.sleep(0.5)

                # Add variable so we can keep track of its expected content for later
                sim.add_variable(data_name, result)

                # If we didn't match add the incorrect result to the report too
                if not content_matches:
                    # Add reports
                    sim.add_report_obj(f"PEER_SHOW({router}:{peer})[json]", birdplan_result.as_json())
                    sim.add_report_obj(f"PEER_SHOW({router}:{peer})[text]", birdplan_result.as_text())

                    report_result = pprint.pformat(result, width=132, compact=True)
                    sim.add_report_obj(f"PEER_SHOW({router}:{peer})", f"{data_name} = {report_result}")

                    report_expected = pprint.pformat(result_expected, width=132, compact=True)
                    sim.add_report_obj(f"EXPECTED_PEER_SHOW({router}:{peer})", f"{data_name} = {report_expected}")

        # Lets do the asserts next
        for router, peer_shows in router_shows.items():
            for peer, data in peer_shows.items():
                assert data["result"] == data["expected"], (
                    f"BIRD router '{router}' peer show on '{peer}' does not match what it should be"
                )

    def _test_os_rib(self, sim: Simulation, table_name: str, routers: list[str] | None = None):
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

    def _get_os_rib_data(self, sim: Simulation, router: str, table_name: str) -> tuple[Any, Any]:
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
            if result_expected is None:  # noqa: SIM114
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

        # Add variable so we can keep track of its expected content for later
        sim.add_variable(data_name, result)
        # If we didn't match add the incorrect result to the report too
        if not result_matches:
            report_expected = pprint.pformat(result_expected, width=132, compact=True)
            sim.add_report_obj(f"EXPECTED_OS_RIB({router})[{table_name}]", f"{data_name} = {report_expected}")
            # Add report
            report_result = pprint.pformat(result, width=132, compact=True)
            sim.add_report_obj(f"OS_RIB({router})[{table_name}]", f"{data_name} = {report_result}")

        # Return the two chunks of data for later assertion
        return (result, result_expected)

    def _configure_bird_routers(self, sim: Simulation, tmpdir: str) -> list[str]:
        """Create our configuration files."""
        # Generate config files and keep track of what we configured in the case of exceptions
        configured_routers = []
        for router in self.routers:
            # If we get a positive result, add the router to the list of configured routers
            bird_config: BirdPlanCommandlineResult = self._birdplan_run(sim, tmpdir, router, ["configure"])
            # If we have None it is expected
            if bird_config is None:
                continue
            # If its however blank, raise exception
            if not bird_config.data:
                raise RuntimeError(f"BirdPlan failed to configure router '{router}'")
            # Add router to list of configured routers
            configured_routers.append(router)

        return configured_routers

    def _configure_exabgps(self, sim: Simulation, tmpdir: str) -> list[str]:  # pylint: disable=too-many-locals,too-many-branches
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
            with open(exabgp_config_file, encoding="UTF-8") as file:
                raw_config = file.read()
            # Check if we're replacing macros in our configuration file
            for macro, value in internal_macros.items():
                if isinstance(value, int):
                    value = f"{value}"
                raw_config = raw_config.replace(macro, value)
            # Write out new BirdPlan file with macros replaced
            with open(exabgp_conffile, "w", encoding="UTF-8") as file:
                file.write(raw_config)

            # Add config file to our simulation so we get a report for it
            sim.add_conffile(f"exabgp.conf.{exabgp}", exabgp_conffile)

    def _configure_stayrtrs(self, sim: Simulation, tmpdir: str) -> list[str]:  # pylint: disable=too-many-locals,too-many-branches
        """Create our SLURM files."""

        # Loop with each StayRTR
        for stayrtr in self.stayrtrs:
            # Grab the SLURM filename we're going to be using
            stayrtr_slurmfile = f"{tmpdir}/stayrtr.slurm.json.{stayrtr}"

            # Loop with supported attributes that translate into macros
            internal_macros = {}
            for attr in [
                "asn",
                "stayrtr_slurm",
                "template_stayrtr_slurm",
            ]:
                # Router specific lookup for an attribute to add a macro for
                router_attr = f"{stayrtr}_{attr}"
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

            # Grab StayRTR's ASN
            stayrtr_asn = internal_macros["@ASN@"]

            # Work out SLURM file name, going 2 levels up in the test directory
            stayrtr_slurm_file = None
            for slurmfile_path in [
                # Without ASN appended
                f"{sim.test_dir}/stayrtr.slurm.json.{stayrtr}",
                # Parent directory without ASN appended
                f"{os.path.dirname(sim.test_dir)}/stayrtr.slurm.json.{stayrtr}",
                # Parent parent directory without ASN appended
                f"{os.path.dirname(os.path.dirname(sim.test_dir))}/stayrtr.slurm.json.{stayrtr}",
            ]:
                if os.path.exists(slurmfile_path):
                    stayrtr_slurm_file = slurmfile_path
                    break
            # If we didn't get a SLURM file that exists, then raise an exception
            if not stayrtr_slurm_file:
                raise RuntimeError(f"No StayRTR SLURM file found for StayRTR '{stayrtr}' with ASN '{stayrtr_asn}'")

            # Read in SLURM file
            with open(stayrtr_slurm_file, encoding="UTF-8") as file:
                raw_slurm = file.read()
            # Check if we're replacing macros in our SLURM file
            for macro, value in internal_macros.items():
                if isinstance(value, int):
                    value = f"{value}"
                raw_slurm = raw_slurm.replace(macro, value)
            # Write out new BirdPlan file with macros replaced
            with open(stayrtr_slurmfile, "w", encoding="UTF-8") as file:
                file.write(raw_slurm)

            # Add SLURM file to our simulation so we get a report for it
            sim.add_conffile(f"stayrtr.slurm.json.{stayrtr}", stayrtr_slurmfile)

    def _birdplan_run(  # pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
        self, sim: Simulation, tmpdir: str, router: str, args: list[str]
    ) -> BirdPlanCommandlineResult | None:
        """Run BirdPlan for a given router."""

        # Work out file names
        birdplan_file = f"{tmpdir}/birdplan.yaml.{router}"
        bird_conffile = f"{tmpdir}/bird.conf.{router}"
        bird_statefile = f"{tmpdir}/bird.state.{router}"
        bird_logfile = f"{tmpdir}/bird.log.{router}"
        bird_socket = f"{tmpdir}/bird.ctl.{router}"

        # If we're running in configure mode, then create the config file
        if args[0] == "configure":
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
            extra_attr_list = getattr(self, "template_macros", None)
            if extra_attr_list:
                attr_list.extend(extra_attr_list)
            # Loop with supported attributes that translate into macros
            internal_macros = {}
            for attr in attr_list:
                # Router specific lookup for an attribute to add a macro for
                router_attr = f"{router}_{attr}"
                value = ""
                if hasattr(self, router_attr):
                    symbol = getattr(self, router_attr)
                    if callable(symbol):
                        value = symbol()
                    else:
                        value = symbol
                # Add our macro
                internal_macros[f"@{attr.upper()}@"] = value

            # NK: We probably need to add the StayRTR private keys here
            for stayrtr in self.stayrtrs:
                # Router specific lookup for an attribute to add a macro for
                stayrtr_private_keyfile_attr = f"{stayrtr}_private_keyfile"
                if hasattr(self, stayrtr_private_keyfile_attr):
                    # Add our macro
                    internal_macros[f"@{stayrtr_private_keyfile_attr.upper()}@"] = getattr(self, stayrtr_private_keyfile_attr)

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
            with open(router_config_file, encoding="UTF-8") as file:
                raw_config = file.read()
            # Check if we're replacing macros in our configuration file
            while True:
                changed = False
                for macro, value in macros.items():
                    if isinstance(value, int):
                        value = f"{value}"
                    # Check for odd issues...
                    if value is None:
                        raise RuntimeError(f"Macro '{macro}' for router '{router}' has value None")
                    new_config = raw_config.replace(macro, value)
                    # Do recursive replace
                    if new_config != raw_config:
                        changed = True
                        raw_config = new_config
                # If nothing changed, break, else continue with recursive replacement
                if not changed:
                    break

            # Write out new BirdPlan file with macros replaced
            with open(birdplan_file, "w", encoding="UTF-8") as file:
                file.write(raw_config)

            # Add YAML file early incase we need to check it when configuration fails
            sim.add_conffile(f"birdplan.yaml.{router}", birdplan_file)

        # Invoke by simulating the commandline...
        birdplan_cmdline = BirdPlanCommandLine(test_mode=True)
        # Disable logging for filelog
        logging.getLogger("filelock").setLevel(logging.ERROR)

        # Work out our commandline arguments
        cmdline_args = [
            "--bird-socket",
            bird_socket,
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

        # Add the birdplan configuration object to the simulation
        if args[0] == "configure":
            # Add test report sections
            sim.add_logfile(f"bird.log.{router}", bird_logfile)
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
        for routes in route_table.values():
            # Loop with each destination
            for dest in routes:
                # Remove since field
                del dest["since"]
                # If this is OSPF type I, we need to remove the router_id to prevent a race condition depending which router
                # comes up first.
                if "ospf_type" in dest and dest["ospf_type"] == "I":
                    # Remove router_id
                    if "router_id" not in dest:
                        raise RuntimeError("OSPF should have a 'router_id', but does not")
                    del dest["router_id"]
                    # Check if we have attributes and if the OSPF router_id is there, if it is remove it
                    # NK: The OSPF router_id is dynamic and can change in multipath routes
                    if "attributes" in dest:
                        for attr in ("OSPF.router_id", "ospf_router_id"):
                            if attr in dest["attributes"]:
                                del dest["attributes"][attr]
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
            with open(sim.logfiles[logname], encoding="UTF-8") as logfile:
                log_str = logfile.read()
            # Check if the log contains what we're looking for
            if re.search(matches, log_str):
                return True
            # Bump tries
            tries += 1
            time.sleep(1)

    def _exabgpcli(self, sim: Simulation, exabgp_name: str, args: list[str], report_title: str = "") -> list[str]:
        """Run the ExaBGP cli."""
        # Grab the route table
        output = sim.node(exabgp_name).exabgpcli(args)
        # Add report
        sim.add_report_obj(f"EXABGP({exabgp_name})[command{report_title}]", args)
        sim.add_report_obj(f"EXABGP({exabgp_name})[output{report_title}]", output)
        # Return route table
        return output
