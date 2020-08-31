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

"""BirdConfig configuration globals."""

from typing import Optional


class BirdConfigGlobals:  # pylint: disable=too-few-public-methods
    """
    BirdConfig configuration globals.

    Attributes
    ----------
    log_File : Optional[str]
        BIRD log file
    debug : bool
        Enable additional output from BIRD while running
    test_mode : bool
        Enable test mode, this modifies some internals to allow for better and more complete testing

    """

    log_file: Optional[str]
    debug: bool
    test_mode: bool

    def __init__(self):
        """Initialize object."""

        # Log file
        self.log_file = None

        # Debugging
        self.debug = False
        self.test_mode = False
