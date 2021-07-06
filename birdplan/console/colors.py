#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2021, AllWorldIT
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

import colorama


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

    # Check if we can grab the color control sequence
    color_ctrl = getattr(colorama.Fore, color.upper(), None)
    # If not throw an error
    if not color_ctrl:
        raise RuntimeError(f"No color exists '{color}'")

    # Return the colored text with a reset
    return f"{color_ctrl}{text}{colorama.Style.RESET_ALL}"