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

"""BIRD device protocol configuration."""

from ..base import BirdConfigBase


class BirdConfigProtocolDevice(BirdConfigBase):
    """BIRD device protocol configuration."""

    def configure(self):
        """Configure the device protocol."""
        self._addtitle("Device Protocol")
        self._addline("protocol device {")
        self._addline('  description "Device protocol";')
        self._addline("")
        self._addline("  scan time 10;")
        self._addline("};")
        self._addline("")
