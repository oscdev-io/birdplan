#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""Commandline colors."""

import sys

import click

__all__ = ["colored"]

# Check if we should use colors or not
USE_COLORS = sys.stdout.isatty()


def colored(text: str, color: str) -> str:
    """
    Display colored text.

    Parameters
    ----------
    text : str
        Text to color.

    color : str
        Colorama Fore color.

    """

    if USE_COLORS:
        return click.style(text, fg=color)
    return text
