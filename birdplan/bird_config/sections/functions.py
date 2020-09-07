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

"""BIRD functions configuration."""

from birdplan.bird_config.globals import BirdConfigGlobals
from .base import SectionBase


class SectionFunctions(SectionBase):
    """BIRD functions configuration."""

    _section: str = "Global Functions"

    _need_functions: bool

    def __init__(self, birdconfig_globals: BirdConfigGlobals):
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        # Add functions to output
        self._need_functions = False

    def configure(self) -> None:
        """Configure global constants."""
        super().configure()

        # Check if we're adding functions
        if self.need_functions:
            self._configure_functions()

    def _configure_functions(self) -> None:
        """Configure functions."""
        self.conf.add('# Match a prefix longer than "size".')
        self.conf.add("function prefix_is_longer(int size) {")
        self.conf.add("  if (net.len > size) then {")
        self.conf.add('    print "[prefix_is_longer] Matched ", net, " against size ", size;', debug=True)
        self.conf.add("    return true;")
        self.conf.add("  } else {")
        self.conf.add("    return false;")
        self.conf.add("  }")
        self.conf.add("}")
        self.conf.add("")
        self.conf.add('# Match a prefix shorter than "size".')
        self.conf.add("function prefix_is_shorter(int size) {")
        self.conf.add("  if (net.len < size) then {")
        self.conf.add('    print "[prefix_is_shorter] Matched ", net, " against size ", size;', debug=True)
        self.conf.add("    return true;")
        self.conf.add("  } else {")
        self.conf.add("    return false;")
        self.conf.add("  }")
        self.conf.add("}")
        self.conf.add("")
        self.conf.add("# Match on bogons for IPv4")
        self.conf.add("function is_bogon4() {")
        self.conf.add("  if (net ~ BOGONS_V4) then {")
        self.conf.add('    print "[is_bogon4] Matched ", net;', debug=True)
        self.conf.add("    return true;")
        self.conf.add("  } else {")
        self.conf.add("    return false;")
        self.conf.add("  }")
        self.conf.add("}")
        self.conf.add("")
        self.conf.add("# Match on bogons for IPv6")
        self.conf.add("function is_bogon6() {")
        self.conf.add("  if (net ~ BOGONS_V6) then {")
        self.conf.add('    print "[is_bogon6] Matched ", net;', debug=True)
        self.conf.add("    return true;")
        self.conf.add("  } else {")
        self.conf.add("    return false;")
        self.conf.add("  }")
        self.conf.add("}")
        self.conf.add("")

    @property
    def need_functions(self) -> bool:
        """Return if functions should be added to our output constants block."""
        return self._need_functions

    @need_functions.setter
    def need_functions(self, need_functions: bool) -> None:
        """Set if functions should be added to our output constants block."""
        self._need_functions = need_functions
