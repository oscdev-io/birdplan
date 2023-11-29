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

"""BIRD device protocol configuration."""

from .base import SectionProtocolBase


class ProtocolDevice(SectionProtocolBase):
    """BIRD device protocol configuration."""

    def configure(self) -> None:
        """Configure the device protocol."""
        super().configure()

        # Set section heading
        self._section = "Device Protocol"

        self.conf.add("protocol device {")
        self.conf.add('  description "Device protocol";')
        self.conf.add("")
        self.conf.add(f"  vrf {self.birdconfig_globals.vrf};")
        self.conf.add("")
        self.conf.add("  scan time 10;")
        self.conf.add("};")
        self.conf.add("")
