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

"""BIRD router ID configuration section."""

from ..globals import BirdConfigGlobals
from .base import SectionBase

__all__ = ["SectionRouterID"]


class SectionRouterID(SectionBase):
    """BIRD router ID configuration section."""

    _router_id: str

    def __init__(self, birdconfig_globals: BirdConfigGlobals):
        """Initialize object."""
        super().__init__(birdconfig_globals)

        # Set section header
        self._section = "Router ID"

        self._router_id = "0.0.0.0"  # nosec

    def configure(self) -> None:
        """Configure routing id."""
        super().configure()

        self.conf.add(f"router id {self.router_id};")
        self.conf.add("")

    @property
    def router_id(self) -> str:
        """Return our router_id."""
        return self._router_id

    @router_id.setter
    def router_id(self, router_id: str) -> None:
        """Set our router_id."""
        self._router_id = router_id
