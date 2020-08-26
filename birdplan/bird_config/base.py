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

"""Bird configuration base package."""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from . import BirdConfig


class BirdConfigBase:
    """Base for our bird configuration."""

    _root: Optional["BirdConfig"]
    _parent: Optional["BirdConfigBase"]
    _config_lines: List[str]

    # pylint: disable=unused-argument
    def __init__(self, parent: Optional["BirdConfigBase"] = None, root: Optional["BirdConfig"] = None, **kwargs):
        """Initialize the object."""
        self._parent = parent

        # Setup our config lines
        if self.parent:
            self._config_lines = self.parent.config_lines
        else:
            self._config_lines = []

        # Set the root
        self._root = root
        if not self._root and parent:
            # If we didn't get anything, set it as the parent root
            self._root = parent.root

    def _addline(self, line: str, debug: bool = False):
        """
        Add line to config output.

        Parameters
        ----------
        line : str
            Line to add.
        debug : bool, optional
            Is this a debugging line? (default: False)

        """
        if debug and (not self.root or not self.root.debug):
            return
        self.config_lines.append(line)

    def _addlines(self, lines: List[str], debug: bool = False):
        """Add a list of lines."""
        if debug and (not self.root or not self.root.debug):
            return
        self.config_lines.extend(lines)

    def _addtitle(self, title: str):
        """Configure a title for a block of configuration."""
        self._addline("#")
        self._addline(f"# {title}")
        self._addline("#")
        self._addline("")

    def is_test_mode(self) -> bool:
        """Return if we're in test mode or not."""
        if self.root and self.root.test_mode:
            return True
        return False

    @property
    def root(self) -> Optional["BirdConfig"]:
        """Return our root configuration object."""
        return self._root

    @property
    def parent(self) -> Optional["BirdConfigBase"]:
        """Return our parent configuration object."""
        return self._parent

    @property
    def config_lines(self) -> List[str]:
        """Return the configuration lines."""
        return self._config_lines
