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

"""BIRD main configuration section."""

from birdplan.bird_config.globals import BirdConfigGlobals

from .base import SectionBase


class SectionMain(SectionBase):
    """BIRD main configuration section."""

    def __init__(self, birdconfig_globals: BirdConfigGlobals):
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        # Set section header
        self._section = "Main"

    def configure(self) -> None:
        """Configure main part of the config."""
        super().configure()

        self.conf.add("# Set time format for compatibility with 3rd-party programs")
        self.conf.add("timeformat base iso long;")
        self.conf.add("timeformat log iso long;")
        self.conf.add("timeformat protocol iso long;")
        self.conf.add("timeformat route iso long;")
        self.conf.add("")
