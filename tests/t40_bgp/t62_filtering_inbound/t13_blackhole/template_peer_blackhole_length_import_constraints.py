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

"""BGP blackhole length test case template."""

from .template_base import TemplateBase


class Template(TemplateBase):
    """BGP blackhole length test case template."""

    test_blackhole_lengths4 = [28, 30, 32]
    test_blackhole_lengths6 = [124, 126, 128]

    r1_template_peer_config = """
      constraints:
        blackhole_export_minlen4: 29
        blackhole_export_maxlen4: 31
        blackhole_export_minlen6: 125
        blackhole_export_maxlen6: 127
"""
