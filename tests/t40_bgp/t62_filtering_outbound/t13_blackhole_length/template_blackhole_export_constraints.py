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

"""BGP default blackhole export constraints test case template."""

from ..template_base import TemplateBase


class Template(TemplateBase):
    """BGP default blackhole export constraints test case template."""

    r1_template_extra_config = """
      blackhole_community: true
"""

    r1_template_peer_config = """
      constraints:
        blackhole_import_minlen4: 23
"""

    e1_template_communities = "65535:666"
    e1_template_large_communities = "65000:666:65413 65000:666:65412"

    test_prefix_lengths4 = [23, 24, 32]
    test_prefix_lengths6 = [63, 64, 128]
