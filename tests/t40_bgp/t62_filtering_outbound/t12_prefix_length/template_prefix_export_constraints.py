#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2024, AllWorldIT
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

# type: ignore
# pylint: disable=import-error,too-few-public-methods

"""BGP default prefix export constraints test case template."""

from ..template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP default prefix export constraints test case template."""

    test_prefix_lengths4 = [7, 8, 15, 16, 23, 24, 28, 30, 32]
    test_prefix_lengths6 = [15, 17, 31, 32, 47, 48, 63, 65, 128]

    def r1_template_global_config(self):
        """Return R1 global config with the originated routes."""
        return self._generate_originated_routes()
