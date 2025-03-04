#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2025, AllWorldIT.
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

import os
import pathlib
import pprint
import time
from typing import Any

from nsnetsim.generic_node import GenericNode
from nsnetsim.topology import Topology

import birdplan.yaml
from birdplan import BirdPlan  # pylint: disable=import-error

__all__ = ["Simulation"]


class Simulation:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """Simulation class, storing the topology and nodes."""

    _configs: dict[str, BirdPlan]
    _report: dict[str, str]
    # All the variables we're testing and their values from the simulation
    _variables: dict[str, str]

    # Test directory
    _test_dir: str | None
    # Current test being run
    _test_file: str | None

    _expected_data: dict[str, Any] | None

    _conffiles: dict[str, str]
    _logfiles: dict[str, str]
    _topology: Topology
    _delay: int

    _yaml: birdplan.yaml.YAML

    def __init__(self):
        """Initialize object."""
        self.new()
        self._yaml = birdplan.yaml.YAML()

    def new(self):
        """Prepare for simulation of a new topology."""
        self._configs = {}
        self._report = {}
        self._variables = {}

        self._test_dir = None
        self._test_file = None

        self._expected_data = None

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
        # Check if we're delaying testing (for convergeance)
        if self.delay:
            time.sleep(self.delay)

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
        self._variables[name] = content

    def report(self) -> list[tuple[str, str]]:
        """Build a report for the current test."""

        items = []

        # Loop with report info to add
        for name, info in self._report.items():
            items.append((name, info))

        return items

    def report_logs(self) -> list[tuple[str, str]]:
        """Build a report, containing our log file contents."""

        items = []

        # Loop with log files to add
        for name, filename in self._logfiles.items():
            # If the file does not exist, just output a message
            if not os.path.exists(filename):
                items.append((name, "-- NOT CREATED --"))
                continue
            # If it does exist add its contents to our items
            with open(filename, encoding="UTF-8") as logfile:
                contents = logfile.read()
            items.append((name, contents))

        return items

    def report_configs(self) -> list[tuple[str, str]]:
        """Build a report, containing our config file contents."""

        items = []

        # Loop with configuration files to add
        for name, filename in self.conffiles.items():
            # If the file does not exist, just output a message
            if not os.path.exists(filename):
                items.append((name, "-- NOT CREATED --"))
                continue
            # If it does exist loop with each line, number it and add
            contents = ""
            with open(filename, encoding="UTF-8") as conffile:
                for lineno, line in enumerate(conffile.readlines()):
                    contents += f"{lineno + 1}: {line}"
            # Add report
            items.append((name, contents))

        return items

    def set_test(self, testpath: str) -> None:
        """Set test we're busy running."""

        # Grab the filename of the test
        self._test_file = os.path.basename(testpath)
        # Grab the directory the test is running in
        self._test_dir = os.path.dirname(testpath)

    def get_data(self, data_name: str) -> Any:
        """Return simulation data that we loaded."""

        if self._expected_data is None:
            return None

        data = self._expected_data.get(data_name, ValueError("No Data"))

        return data

    def load_data(self) -> None:
        """Read in simulation data."""

        # If our expected data doesn't exist, then abort loading it
        if not os.path.exists(self.expected_data_filepath):
            return

        # Load our data
        self._expected_data = self.yaml.load(pathlib.Path(self.expected_data_filepath))

    def write_data(self) -> None:
        """Write out simulation data."""

        # Write out our data
        self.yaml.dump(self._variables, pathlib.Path(self.expected_data_filepath))

        # Grab the expected configuration file
        expected_conf_filename_base = self.test_file.replace(".py", "")
        expected_conf_filepath_base = f"{self.test_dir}/{expected_conf_filename_base}"
        for conffile_name, sim_conffile_path in self.conffiles.items():
            # Work out expected config filepath
            expected_conf_filepath = f"{expected_conf_filepath_base}_{conffile_name}"
            expected_conf_filepath = expected_conf_filepath.replace("_birdplan.yaml.", ".birdplan.") + ".conf"
            # If this is a birdplan config file, write it out
            if "birdplan" in conffile_name:
                # We need to replace some options that are variable so files don't change between runs
                with open(sim_conffile_path, encoding="UTF-8") as config_file:
                    conf_lines = config_file.readlines()
                with open(expected_conf_filepath, "w", encoding="UTF-8") as config_file:
                    for line in conf_lines:
                        if "log_file:" in line:
                            line = "log_file: /var/log/birdplan.log\n"
                        config_file.write(line)

    @property
    def expected_data_filepath(self) -> str:
        """Return our expected data filepath."""

        # Work out our data file name and path
        expected_data_filename = self.test_file.replace(".py", ".yaml")
        return f"{self.test_dir}/{expected_data_filename}"

    @property
    def conffiles(self) -> dict[str, str]:
        """Return our configuration files."""
        return self._conffiles

    @property
    def logfiles(self) -> dict[str, str]:
        """Return our log files."""
        return self._logfiles

    @property
    def variables_py(self) -> str:
        """Build the variable list that we should of gotten."""

        result = ""
        for name, data in self._variables.items():
            content = pprint.pformat(data, width=132, compact=True)
            result += f"{name} = {content}\n\n"

        return result

    @property
    def test_dir(self) -> str:
        """Return our test directory."""
        return self._test_dir

    @property
    def test_file(self) -> str:
        """Return our test file."""
        return self._test_file

    @property
    def delay(self) -> int:
        """Return our simulation delay."""
        return self._delay

    @delay.setter
    def delay(self, delay: int):
        """Set our simulation delay."""
        self._delay = delay

    @property
    def yaml(self) -> birdplan.yaml.YAML:
        """Return our YAML parser."""
        return self._yaml

    @yaml.setter
    def yaml(self, yaml: birdplan.yaml.YAML) -> None:
        """Set our YAML parser."""
        self._yaml = yaml
