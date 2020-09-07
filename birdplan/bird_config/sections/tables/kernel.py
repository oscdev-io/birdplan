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

"""BIRD kernel table configuration."""

from ..base import SectionBase


class TableKernel(SectionBase):
    """BIRD kernel table configuration."""

    def configure(self) -> None:
        """Configure the kernel tables."""
        super().configure()

        # Setup kernel tables
        self.conf.add("# Kernel Table")
        self.conf.add("ipv4 table t_kernel4;")
        self.conf.add("ipv6 table t_kernel6;")
        self.conf.add("")
