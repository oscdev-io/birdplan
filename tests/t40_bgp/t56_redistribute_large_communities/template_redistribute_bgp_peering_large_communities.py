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

"""BGP redistribute large community test case template."""

from .template_redistribute_bgp_base import TemplateBase


class Template(TemplateBase):
    """BGP redistribute large community test case template."""

    def r1_template_peer_config(self):
        """Return custom peer config."""

        return f"""
      redistribute:
        bgp_peering:
          large_communities:
            - {self.r1_asn}:5000:1
"""
