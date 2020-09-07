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

"""BIRD configuration section base class."""

from typing import Dict, List, Union

from ..globals import BirdConfigGlobals

# Types
SectionConfigItem = Union[str, List[str], "SectionBase"]
SectionConfigItemList = List[SectionConfigItem]
SectionConfigItems = Dict[int, SectionConfigItemList]


class SectionBaseConfig:  # pylint: disable=too-few-public-methods
    """Configuration contents of the section."""

    _birdconfig_globals: BirdConfigGlobals
    _items: SectionConfigItems

    def __init__(self, birdconfig_globals: BirdConfigGlobals) -> None:
        """Initialize object."""
        self._birdconfig_globals = birdconfig_globals
        self._items = {}

    def add(self, item: SectionConfigItem, order: int = 10, deferred: bool = False, debug: bool = False) -> None:
        """
        Add configuration to the output we're going to generate.

        Parameters
        ----------
        item : SectionConfigItem
            Configuration to add, either a string, list of strings or another section.
        order : int
            Ordering of the item to add. Defaults to `10`.
        deferred : bool
            If the config item is a SectionBase, then rendering can be deferred until after configuration.
            This is needed for instance for the constants section, which other protocols may add to.
        debug : bool
            The configuration provided should only be output when we are in debug mode.

        """
        # Sanity checks
        if deferred and not isinstance(item, SectionBase):
            raise RuntimeError("Only SectionBase objects can be used as deferred configuration")

        # If we have a debug line,  exclude it if we're not in debugging mode
        if debug and not self.birdconfig_globals.debug:
            return

        # Make sure this ordering position is initialized
        if order not in self.items:
            self.items[order] = []
        items = self.items[order]

        # If this is an instance of a list, extend our lines by this list
        if isinstance(item, list):
            items.extend(item)
        # If it is an entire section, configure it and add the lines
        elif isinstance(item, SectionBase):
            # Check if we're rendering now or later
            if not deferred:
                item.configure()
                self.add(item.conf.lines)
            else:
                items.append(item)
        # Else just add it
        else:
            items.append(item)

    def append(self, item: SectionConfigItem, deferred: bool = False, debug: bool = False) -> None:
        """
        Add configuration to the output we're going to generate.

        This uses an order of `50`, which is higher than add() that defaults to `10`.

        Parameters
        ----------
        item : SectionConfigItem
            Configuration to add, either a string, list of strings or another section.
        deferred : bool
            If the config item is a SectionBase, then rendering can be deferred until after configuration.
            This is needed for instance for the constants section, which other protocols may add to.
        debug : bool
            The configuration provided should only be output when we are in debug mode.

        """
        self.add(item=item, order=50, deferred=deferred, debug=debug)

    def title(self, title: str, order: int = 10) -> None:
        """
        Add a title block.

        Parameters
        ----------
        title : str
            Add a title block
        order : int
            Ordering of the item to add. Defaults to `10`.

        """
        self.add("#", order=order)
        self.add(f"# {title}", order=order)
        self.add("#", order=order)
        self.add("", order=order)

    def append_title(self, title: str) -> None:
        """
        Add a title block.

        This uses an order of `50`, which is higher than title() that defaults to `10`.

        Parameters
        ----------
        title : str
            Add a title block

        """
        self.title(title=title, order=50)

    @property
    def items(self) -> SectionConfigItems:
        """Return our configuration items."""
        return self._items

    @property
    def lines(self) -> List[str]:
        """Return our configuration lines."""
        lines: List[str] = []
        # Loop with configuration items in order
        for _, items in sorted(self._items.items()):
            # Loop with each list
            for item in items:
                # If it is a SectionBase it means it was deferred, so configure and extend
                if isinstance(item, SectionBase):
                    item.configure()
                    lines.extend(item.conf.lines)
                # Or its just normal strings, add them all
                elif isinstance(item, str):
                    lines.append(item)
                # Or something really weird happened
                else:
                    raise RuntimeError("We should only have 'str' and 'SectionBase' items")
        # Finally return
        return lines

    @property
    def birdconfig_globals(self) -> BirdConfigGlobals:
        """Return our BirdConfig globals."""
        return self._birdconfig_globals


class SectionBase:
    """Base class for a BIRD configuration section."""

    # Section title
    _section: str = ""

    # Globals
    _birdconfig_globals: BirdConfigGlobals

    # Configuration lines to output
    _config: SectionBaseConfig

    # pylint: disable=unused-argument
    def __init__(self, birdconfig_globals: BirdConfigGlobals) -> None:
        """
        Initialize the object.

        Returns
        -------
        Nothing.

        """

        self._birdconfig_globals = birdconfig_globals

        self._config = SectionBaseConfig(birdconfig_globals=self.birdconfig_globals)

    def configure(self) -> None:
        """
        Configure this section.

        Returns
        -------
        Nothing.

        """
        if self.section:
            self.conf.title(self.section)

    @property
    def section(self) -> str:
        """Return the section name."""
        return self._section

    @property
    def birdconfig_globals(self) -> BirdConfigGlobals:
        """Return our BirdConfig globals."""
        return self._birdconfig_globals

    @property
    def conf(self) -> SectionBaseConfig:
        """Return the configuration object."""
        return self._config
