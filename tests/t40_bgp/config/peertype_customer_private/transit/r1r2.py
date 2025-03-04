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

# type: ignore
# pylint: disable=import-error,too-few-public-methods

"""BGP configuration for basic setup between r1 and r2."""

__all__ = ["PeerTypeConfig"]


class PeerTypeConfig:
    """BGP configuration for basic setup between r1 and r2."""

    r1_peer_type = "customer"

    r1_peer_asn = "4200000000"
    r1_extra_r2_config = """
      replace_aspath: True
"""

    r1_peer_config = """
      prefix_limit4: 100
      prefix_limit6: 100
      filter:
        origin_asns:
          - 65100
"""

    r2_peer_type = "transit"
    r2_asn = "4200000000"
