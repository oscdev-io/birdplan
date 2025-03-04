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

"""Test --version option."""

# pylint: disable=redefined-outer-name

import birdplan.cmdline

__all__: list[str] = []


def test_load_from_string() -> None:
    """Test loading from string."""

    bplan = birdplan.cmdline.BirdPlanCommandLine()

    res = bplan.run(["--version"])

    test_data = res.data

    assert test_data == birdplan.__version__
