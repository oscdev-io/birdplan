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

"""BGP RPKI functionality test case template."""

from ..template_base import TemplateBase

__all__ = ["Template"]


class Template(TemplateBase):
    """BGP RPKI functionality test case template."""

    stayrtrs = ["a1"]

    a1_use_ssh = True

    def r1_template_global_config(self):
        """Global configuration for R1."""

        return """
  rpki_source: ssh://100.64.0.101?refresh=2&retry=2&private_key=@A1_PRIVATE_KEYFILE@
"""

    def r1_template_peer_config(self):
        """Peer configuration for R1."""

        return """
      use_rpki: false
"""
