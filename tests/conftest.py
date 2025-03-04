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

"""Testing stuff."""

import contextlib
import os
import re
import signal

import pytest

from .simulation import Simulation

__all__ = ["CustomPytestRegex", "Helpers"]


# Make sure basetests has its asserts rewritten
pytest.register_assert_rewrite("tests.basetests")


#
# Commandline options
#


def pytest_addoption(parser):
    """Add commandline options."""

    parser.addoption("--write-expected", action="store_true", default=False, help="Write out expected test results.")
    parser.addoption(
        "--sim-wait",
        type=int,
        default=10,
        help="Number of seconds to wait for the simulation to start. Default 10 (seconds).",
    )
    parser.addoption(
        "--enable-performance-test", action="store_true", default=False, help="WARNING: This will spawn 2,500 BIRD routers"
    )


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


@pytest.fixture(name="testpath")
def fixture_testpath(request):
    """Test file path."""
    return str(request.node.fspath)


@pytest.fixture
def enable_performance_test(pytestconfig):
    """Get the --enable-performance-test option."""
    return pytestconfig.getoption("--enable-performance-test")


def sigchld_handler(signum, frame):  # pylint: disable=unused-argument
    """Signal handler for SIGCHLD."""
    with contextlib.suppress(ChildProcessError):
        while True:
            # Wait for completion of a child process without blocking
            # os.WNOHANG makes the call non-blocking; it returns immediately if no child has exited
            # pid, status = os.waitpid(-1, os.WNOHANG)
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                # No more zombies
                break
            # Process has been reaped
            # print(f"Reaped zombie process with PID: {pid}, Exit Status: {status}")


def pytest_configure(config):
    """Dynamic pytest configuration."""
    config.addinivalue_line("markers", "incremental: test class is incremental")
    # Set the signal handler for SIGCHLD so we can reap the zombies (nsnetsim spawns many child processes)
    signal.signal(signal.SIGCHLD, sigchld_handler)


#
# Incremental marker, fail subsequent tests if one fails
#


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
            if "incremental" in item.keywords:  # noqa: SIM102
                if call.excinfo is not None:
                    setattr(item.parent, "_previousfailed", item)  # noqa: B010

        # If the test passed, clear the report data
        # Grab sim and clear the report
        elif hasattr(item, "fixturenames") and "sim" in item.fixturenames:
            sim = item.funcargs["sim"]
            sim.clear_report()


def pytest_runtest_setup(item):
    """Check if the previous test failed, if so xfail the rest."""

    # Clear reports before running test
    if hasattr(item.parent, "fixturenames"):  # noqa: SIM102
        if "sim" in item.parent.fixturenames:
            sim = item.parent.funcargs["sim"]
            sim.clear_report()

    previousfailed = getattr(item.parent, "_previousfailed", None)
    # Skip the next test if this one failed, but only if we're not writing out expected test results
    if (previousfailed is not None) and not item.config.getoption("--write-expected"):
        pytest.xfail(f"Previous test failed ({previousfailed.name})")


#
# Simulation fixture stuff
#


@pytest.fixture(name="sim", scope="class")
def fixture_sim(request):
    """Python fixture to create our simulation before running tests."""

    # Create the simulation
    simulation = Simulation()

    # Check if we're delaying the simulation
    sim_delay = 0
    if request.config.getoption("--write-expected"):
        sim_delay = request.config.getoption("--sim-wait")
    simulation.delay = sim_delay

    # Yield the simulation to the test
    yield simulation

    # Check if we're supposed to be writing out the expected results
    if request.config.getoption("--write-expected"):
        # Write out simulation data
        simulation.write_data()

    # Destroy simulation
    simulation.destroy()
