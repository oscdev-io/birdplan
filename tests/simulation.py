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

# type: ignore

"""Test case simulation class."""

from typing import Any, Dict, List, Tuple
import os
import pprint
from nsnetsim.generic_node import GenericNode
from nsnetsim.topology import Topology
from birdplan import BirdPlan  # pylint: disable=import-error


class Simulation:  # pylint: disable=too-many-instance-attributes
    """Simulation class, storing the topology and nodes."""

    _configs: Dict[str, BirdPlan]
    _report: Dict[str, str]
    # All the variables we're testing and their values from the simulation
    _variables: List[str]
    # Test directory
    _test_dir: str
    # The file containing our expected results
    _expected_path: str
    _conffiles: Dict[str, str]
    _logfiles: Dict[str, str]
    _topology: Topology
    _delay: int

    def __init__(self):
        """Initialize object."""
        self.new()

    def new(self):
        """Prepare for simulation of a new topology."""
        self._configs = {}
        self._report = {}
        self._variables = []
        self._test_dir = ""
        self._expected_path = ""
        self._conffiles = {}
        self._logfiles = {}
        self._topology = Topology()
        self._delay = 0

    def config(self, name: str) -> BirdPlan:
        """Return a node by name."""
        return self._configs[name]

    def add_config(self, name: str, config: BirdPlan):
        """Add a config."""
        self._configs[name] = config

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

        # If the object is a string, use it as is
        if isinstance(obj, str):
            self._report[name] = obj
        else:
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

    def add_variable(self, name: str, content: str):  # pylint: disable=unused-argument
        """Add a variable to our expected content list."""
        self._variables.append(content)

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

    @property
    def logfiles(self) -> Dict[str, str]:
        """Return our log files."""
        return self._logfiles

    @property
    def variables(self) -> str:
        """Build the variable list that we should of gotten."""

        result = ""
        for var in self._variables:
            result += f"{var}\n\n"

        return result

    @property
    def test_dir(self) -> str:
        """Return our test directory."""
        return self._test_dir

    @test_dir.setter
    def test_dir(self, test_dir: str):
        """Set our test directory."""
        self._test_dir = test_dir

    @property
    def expected_path(self) -> str:
        """
        Return our expected path.

        This is the file we get our expected results from.

        """
        return self._expected_path

    @expected_path.setter
    def expected_path(self, expected_path: str):
        """Set our expected path."""
        self._expected_path = expected_path

    @property
    def delay(self) -> int:
        """Return our simulation delay."""
        return self._delay

    @delay.setter
    def delay(self, delay: int):
        """Set our simulation delay."""
        self._delay = delay
