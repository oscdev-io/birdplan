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

"""BIRD logging configuration."""

from .base import SectionBase


class SectionLogging(SectionBase):
    """BIRD logging configuration."""

    _section = "Logging"

    def configure(self):
        """Configure logging."""
        super().configure()

        # Grab logfile if we have one
        log_file = self.birdconf_globals.log_file
        if log_file:
            self.conf.add(f'log "{log_file}" all;')
        else:
            self.conf.add("log stderr all;")
        # Check if we're in debug mode
        if self.birdconf_globals.debug:
            self.conf.add("debug protocols { states, routes, filters, interfaces, events };")
        self.conf.add("")
