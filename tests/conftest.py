#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2020, AllWorldIT.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Testing stuff."""

import os
import re
from typing import Any, Dict, List, Tuple
import pprint
import pytest
from nsnetsim.generic_node import GenericNode
from nsnetsim.topology import Topology


#
# Helpers
#


class Helpers:
    """Helpers for our tests."""

    @staticmethod
    def pytest_regex(pattern: str, flags: int = 0):
        """Regex test for pytest."""
        return CustomPytestRegex(pattern, flags)

    @staticmethod
    def bird_since_field():
        """Return our 'since' field match."""
        return CustomPytestRegex(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")


class CustomPytestRegex:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        """Inititalize object."""
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        """Check if the 'actual' string matches the regex."""
        return bool(self._regex.match(actual))

    def __repr__(self):
        """Return our representation."""
        return self._regex.pattern


@pytest.fixture
def helpers():
    """Return our helpers."""
    return Helpers


@pytest.fixture(name="tmpdir", scope="class")
def fixture_tmpdir(tmpdir_factory):
    """Create a temporary path to store our config file."""
    return tmpdir_factory.mktemp("config")


#
# Incremental marker, fail subsequent tests if one fails
#


def pytest_configure(config):
    """Dynamic pytest configuration."""
    config.addinivalue_line("markers", "incremental: test class is incremental")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Check if we failed, if we did set the parent _previousfailed."""

    # Yield so we can get the outcome from other hoooks
    outcome = yield
    report = outcome.get_result()

    # Make sure this is a call
    if report.when == "call":
        # Check if something failed
        if report.failed:
            # Check if we a "sim" fixture
            if hasattr(item, "fixturenames") and "sim" in item.fixturenames:
                # If we do, check we have a "sim" fixture
                sim = item.funcargs["sim"]
                report.sections.extend(sim.report())
                # Check if we're adding log files
                if item.config.getoption("verbose") > 1:
                    report.sections.extend(sim.report_logs())
                # Check if we're adding config files
                if item.config.getoption("verbose") > 2:
                    report.sections.extend(sim.report_configs())

            # If this is an incremental test we need to add an attribute to indicate failure
            if "incremental" in item.keywords:
                if call.excinfo is not None:
                    setattr(item.parent, "_previousfailed", item)

        # If the test passed, clear the report data
        else:
            # Grab sim and clear the report
            if hasattr(item, "fixturenames") and "sim" in item.fixturenames:
                sim = item.funcargs["sim"]
                sim.clear_report()


def pytest_runtest_setup(item):
    """Check if the previous test failed, if so xfail the rest."""

    # Clear reports before running test
    if hasattr(item.parent, "fixturenames"):
        if "sim" in item.parent.fixturenames:
            sim = item.parent.funcargs["sim"]
            sim.clear_report()

    previousfailed = getattr(item.parent, "_previousfailed", None)
    if previousfailed is not None:
        pytest.xfail(f"Previous test failed ({previousfailed.name})")


#
# Simulation fixture stuff
#


class Simulation:
    """Simulation class, storing the topology and nodes."""

    _report: Dict[str, str]
    _conffiles: Dict[str, str]
    _logfiles: Dict[str, str]
    _topology: Topology

    def __init__(self):
        """Initialize object."""
        self._report = {}
        self._conffiles = {}
        self._logfiles = {}
        self._topology = Topology()

    def node(self, name: str) -> GenericNode:
        """Return a node by name."""
        return self._topology.node(name)

    def add_node(self, node: GenericNode):
        """Add a node to our simulation."""
        self._topology.add_node(node)

    def run(self):
        """Run simulation."""
        self._topology.run()

    def destroy(self):
        """Destroy simulation."""
        self._topology.destroy()

    def add_report(self, name: str, info: str):
        """
        Add info to the test report.

        This info is output on test failure.
        """
        self._report[name] = info

    def add_report_obj(self, name: str, obj: Any):
        """
        Add obj to the test report using pprint.

        This info is output on test failure.
        """
        self._report[name] = pprint.pformat(obj)

    def clear_report(self):
        """Clear all reports we currently have."""
        self._report = {}

    def add_conffile(self, name: str, filename: str):
        """
        Add a configuration file to our reports.

        The configuration files are read and displayed on test failure.
        """
        self._conffiles[name] = filename

    def add_logfile(self, name: str, filename: str):
        """
        Add a log file to our reports.

        The log files are read and displayed on test failure.
        """
        self._logfiles[name] = filename

    def report(self) -> List[Tuple[str, str]]:
        """Build a report for the current test."""

        items = []

        # Loop with report info to add
        for name, info in self._report.items():
            items.append((name, info))

        return items

    def report_logs(self) -> List[Tuple[str, str]]:
        """Build a report, containing our log file contents."""

        items = []

        # Loop with log files to add
        for name, filename in self._logfiles.items():
            # If the file does not exist, just output a message
            if not os.path.exists(filename):
                items.append((name, "-- NOT CREATED --"))
                continue
            # If it does exist add its contents to our items
            with open(filename, "r") as logfile:
                contents = logfile.read()
            items.append((name, contents))

        return items

    def report_configs(self) -> List[Tuple[str, str]]:
        """Build a report, containing our config file contents."""

        items = []

        # Loop with configuration files to add
        for name, filename in self._conffiles.items():
            # If the file does not exist, just output a message
            if not os.path.exists(filename):
                items.append((name, "-- NOT CREATED --"))
                continue
            # If it does exist loop with each line, number it and add
            contents = ""
            with open(filename, "r") as conffile:
                lineno = 1
                for line in conffile.readlines():
                    contents += f"{lineno}: {line}"
                    lineno += 1
            # Add report
            items.append((name, contents))

        return items


@pytest.fixture(name="sim", scope="class")
def fixture_sim():
    """Python fixture to create our simulation before running tests."""
    simulation = Simulation()

    yield simulation

    print("Destroying simulation...")
    simulation.destroy()
