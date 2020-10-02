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
# pylint: disable=invalid-name

"""Common data for test cases."""


#
# BIRD t_bgp*_peer
#

r1_t_bgp4_AS65001_r2_peer = r1_t_bgp4_AS65000_r2_peer = {}
r2_t_bgp4_AS65000_r1_peer = {}

r1_t_bgp6_AS65001_r2_peer = r1_t_bgp6_AS65000_r2_peer = {}
r2_t_bgp6_AS65000_r1_peer = {}


#
# BIRD t_bgp*
#

r2_t_bgp4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"gateway": "192.168.2.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_bgp6 = {
    "fc00:102::/48": [
        {
            "attributes": {"BGP.large_community": [(65001, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"gateway": "fc02::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}


#
# BIRD t_master*
#

r2_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.2.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "192.168.2.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
}

r2_master6 = {
    "fc00:100::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:102::/48": [
        {
            "nexthops": [{"gateway": "fc02::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc02::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
}


#
# BIRD t_kernel*
#

r2_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.2.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_kernel6 = {
    "fc00:102::/48": [
        {
            "nexthops": [{"gateway": "fc02::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}


#
# RIB inet*
#

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "gateway": "192.168.2.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth1", "dst": "192.168.2.0/24", "flags": [], "prefsrc": "192.168.2.1", "protocol": "kernel", "scope": "link"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/48", "flags": [], "gateway": "fc02::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc02::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
