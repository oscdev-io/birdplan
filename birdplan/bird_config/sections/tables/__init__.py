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

"""BIRD routing tables section."""

from ...globals import BirdConfigGlobals
from ..base import SectionBase
from .kernel import TableKernel
from .master import TableMaster


class SectionTables(SectionBase):
    """BIRD routing tables section."""

    _kernel: TableKernel
    _master: TableMaster

    def __init__(self, birdconfig_globals: BirdConfigGlobals) -> None:
        """Initialize object."""
        super().__init__(birdconfig_globals)

        # Set section header
        self._section = "Routing Tables"

        self._kernel = TableKernel(birdconfig_globals)
        self._master = TableMaster(birdconfig_globals)

    def configure(self) -> None:
        """Configure all protocols."""
        super().configure()

        self.conf.add(self.kernel)
        # Re-order the master stuff right at the end
        self.conf.append(self.master, deferred=True)

    @property
    def master(self) -> TableMaster:
        """Return the master table section."""
        return self._master

    @property
    def kernel(self) -> TableKernel:
        """Return the kernel table section."""
        return self._kernel
