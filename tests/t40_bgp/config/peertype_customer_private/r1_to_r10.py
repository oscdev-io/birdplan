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

"""BGP configuration for a setup with r1, r2, r3, r4, r5, r6, r7, r8, r9 and r10."""


class PeerTypeConfig:
    """BGP configuration for a setup with r1, r2, r3, r4, r5, r6, r7, r8, r9 and r10."""

    r1_peer_type = "customer"

    r1_r2_asn = "4200000000"
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