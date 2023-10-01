#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
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

from typing import Any, Dict, Optional


class BirdConfigGlobals:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BirdConfig configuration globals.

    Attributes
    ----------
    log_file : Optional[str]
        BIRD log file
    debug : bool
        Enable additional output from BIRD while running
    state : Dict[str, Any]
        Current configuration state, used for persistent data storage.
    test_mode : bool
        Enable test mode, this modifies some internals to allow for better and more complete testing
    vrf: str
        VRF to use for BIRD.
    routing_table: int
        Kernel routing table to add the routes to.
    """

    log_file: Optional[str]
    debug: bool
    ignore_irr_changes: bool
    ignore_peeringdb_changes: bool
    use_cached: bool
    state: Dict[str, Any]
    test_mode: bool
    vrf: str
    routing_table: int | None

    def __init__(self, test_mode: bool = False) -> None:
        """Initialize object."""

        self.log_file = None
        self.ignore_irr_changes = False
        self.ignore_peeringdb_changes = False
        self.use_cached = False
        self.vrf = "default"
        self.routing_table = None

        # Debugging
        self.debug = False
        self.test_mode = test_mode

        # State
        self.state = {}
