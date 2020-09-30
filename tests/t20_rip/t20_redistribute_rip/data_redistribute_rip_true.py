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

"""Data for test case."""


from .data_common import (  # noqa: F401 pylint: disable=unused-import
    r1_t_static4,
    r1_t_static6,
    r1_t_rip4,
    r1_t_rip6,
    r2_t_rip4,
    r2_t_rip6,
    r1_master4,
    r1_master6,
    r2_master4,
    r2_master6,
    r1_t_kernel4,
    r1_t_kernel6,
    r2_t_kernel4,
    r2_t_kernel6,
    r1_inet,
    r1_inet6,
    r2_inet,
    r2_inet6,
)


#
# BIRD t_rip*
#

r3_t_rip4 = {
    "10.0.0.0/24": [
        {
            "attributes": {"RIP.metric": "5", "RIP.tag": "0000"},
            "metric1": 5,
            "nexthops": [{"gateway": "100.102.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ]
}

r3_t_rip6 = {
    "fc10::/64": [
        {
            "attributes": {"RIP.metric": "5", "RIP.tag": "0000"},
            "metric1": 5,
            "nexthops": [{"gateway": "fe80::2:ff:fe00:2", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ]
}


#
# BIRD t_master*
#

r3_master4 = {
    "10.0.0.0/24": [
        {
            "attributes": {"RIP.metric": "5", "RIP.tag": "0000"},
            "metric1": 5,
            "nexthops": [{"gateway": "100.102.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
}

r3_master6 = {
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc10::/64": [
        {
            "attributes": {"RIP.metric": "5", "RIP.tag": "0000"},
            "metric1": 5,
            "nexthops": [{"gateway": "fe80::2:ff:fe00:2", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
}


#
# BIRD t_kernel*
#

r3_t_kernel4 = r3_t_rip4

r3_t_kernel6 = r3_t_rip6


#
# RIB inet*
#

r3_inet = [
    {"dev": "eth0", "dst": "10.0.0.0/24", "flags": [], "gateway": "100.102.0.1", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.2", "protocol": "kernel", "scope": "link"},
]

r3_inet6 = [
    {"dev": "eth0", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dev": "eth0",
        "dst": "fc10::/64",
        "flags": [],
        "gateway": "fe80::2:ff:fe00:2",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
