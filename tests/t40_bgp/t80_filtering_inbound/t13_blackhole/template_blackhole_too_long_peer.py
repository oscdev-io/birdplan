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

"""BGP blackhole too long test case template."""

from .template_base_too_long import TemplateBase


class Template(TemplateBase):
    """BGP blackhole too long test case template."""

    test_blackhole_length4 = 31
    test_blackhole_length6 = 127

    def r1_template_peer_config(self):
        """Return peer configuration, taking into account we have our base class customizations."""

        return (
            super().r1_template_peer_config()
            + """
      blackhole_import_maxlen4: 30
      blackhole_import_maxlen6: 126
"""
        )