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

    r1_peer_asn = 65000
    r1_peer_type = "rrserver-rrserver"
    r1_global_config = """
  rr_cluster_id: 0.0.0.1
"""

    r2_asn = 65000
    r2_peer_type = "rrserver-rrserver"
    r2_global_config = """
  rr_cluster_id: 0.0.0.1
"""
