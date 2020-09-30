#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2020, AllWorldIT
#
# This program is free software: you can redistfibute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distfibuted in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# type: ignore
# pylint: disable=invalid-name,missing-function-docstring

"""Data for test case."""

#
# BIRD t_bgp*_peer
#

r1_t_bgp4_AS65000_e1_peer = {
    "100.64.101.0/24": [
        {
            "attributes": {"BGP.as_path": [], "BGP.local_pref": 100, "BGP.next_hop": ["100.64.0.2"], "BGP.origin": "IGP"},
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_e1_peer = {
    "fc00:101::/48": [
        {
            "attributes": {"BGP.as_path": [], "BGP.local_pref": 100, "BGP.next_hop": ["fc00:100::2"], "BGP.origin": "IGP"},
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ]
}


#
# BIRD t_bgp*
#

r1_t_bgp4 = r1_t_bgp4_AS65000_e1_peer

r1_t_bgp6 = r1_t_bgp6_AS65000_e1_peer


#
# BIRD t_master*
#

r1_master4 = {
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    **r1_t_bgp4,
}

r1_master6 = {
    "fc00:100::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    **r1_t_bgp6,
}
