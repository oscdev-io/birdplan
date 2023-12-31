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

"""BirdPlan commandline plugin base class."""


import argparse
from typing import Any, Optional

from ...plugin import Plugin

__all__ = ["BirdPlanCmdlinePluginBase"]


class BirdPlanCmdlinePluginBase(Plugin):  # pylint: disable=too-few-public-methods
    """BirdPlan commandline plugin base class."""

    _subparser: Optional[argparse.ArgumentParser]
    _subparsers: Optional[argparse.ArgumentParser]

    def __init__(self) -> None:
        """Initialize object."""

        super().__init__()

        # Initialize our internals
        self._subparser = None

    def get_subparser(self, args: Any) -> argparse.ArgumentParser:  # pylint: disable=unused-argument
        """
        Return the plugin subparser.

        The subparser is this commandline options parser for this command.

        Parameters
        ----------
        args : Any
            Method argument(s). Unused.

        Returns
        -------
        argparse.ArgumentParser subparser.

        """

        if not self._subparser:
            raise RuntimeError
        return self._subparser

    def get_subparsers(self, args: Any) -> argparse.ArgumentParser:  # pylint: disable=unused-argument
        """
        Return the plugin subparsers.

        Subparsers are created under the commandline option to implement command hierarchies.

        Parameters
        ----------
        args : Any
            Method argument(s). Unused.

        Returns
        -------
        argparse.ArgumentParser subparsers.

        """

        if not self._subparsers:
            raise RuntimeError
        return self._subparsers
