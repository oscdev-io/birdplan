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

# type: ignore
# pylint: disable=import-error,too-few-public-methods,no-self-use

"""BGP blackhole prefix too short test case template."""

from .template_base_too_short import TemplateBase


class Template(TemplateBase):
    """BGP blackhole prefix too short test case template."""

    r1_template_allpeer_config = """
      blackhole_export_minlen4: 25
      blackhole_export_minlen6: 65
"""
    test_blackhole_length4 = 24
    test_blackhole_length6 = 64
