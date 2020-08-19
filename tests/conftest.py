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

import re
import pytest


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


@pytest.fixture
def helpers():
    """Return our helpers."""
    return Helpers


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


@pytest.fixture(name="tmpdir", scope="class")
def fixture_tmpdir(tmpdir_factory):
    """Create a temporary path to store our config file."""
    return tmpdir_factory.mktemp("config")
