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

"""Bird configuration utility functions."""

import ipaddress
from typing import List


def sanitize_community(community: str) -> str:
    """Sanitize a string representation of a large community."""
    # Split on :
    community_components = community.split(":")
    # Re-join using , and add brackets
    community_str = f'({",".join(community_components)})'
    return community_str


def sanitize_community_list(communities: List[str]) -> List[str]:
    """Sanitize a list of communities."""

    result = []
    for community in sorted(communities):
        result.append(sanitize_community(community))

    return result


def network_count(ip_networks: List[str]) -> int:
    """Get the number of ISP networks within a list of IP networks."""

    # Loop with the networks we got
    count = 0
    for prefix_raw in ip_networks:
        # Split off possible network size constraints
        prefix = prefix_raw.split("{", 1)[0]
        # Grab network object
        ipnetwork = ipaddress.ip_network(prefix)
        # Check which IP version this is
        if ipnetwork.version == 4:
            # Split on /24 for IPv4
            prefix_count = len(list(ipnetwork.subnets(new_prefix=24)))
        else:
            # Split on /48 for IPv6
            prefix_count = len(list(ipnetwork.subnets(new_prefix=48)))
        # Add to counter
        count += prefix_count

    return count
