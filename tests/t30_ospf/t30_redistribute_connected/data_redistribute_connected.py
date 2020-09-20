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


#
# BIRD t_direct*_ospf
#

r1_t_direct4_ospf = {
    "100.101.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_ospf",
            "type": ["device", "univ"],
        }
    ]
}
r1_t_direct6_ospf = {
    "fc00:101::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_ospf",
            "type": ["device", "univ"],
        }
    ]
}


#
# BIRD t_ospf*
#

r1_t_ospf4_expect_content = "'router_id': '0.0.0.2'"
r1_t_ospf4 = {
    "100.101.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_ospf",
            "type": ["device", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        }
    ],
}
r2_t_ospf4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        }
    ],
}

r1_t_ospf6_expect_content = "'router_id': '0.0.0.2'"
r1_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:101::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_ospf",
            "type": ["device", "univ"],
        }
    ],
}
r2_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:101::/64": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
}

#
# BIRD t_master*
#

r1_master4 = {
    "100.101.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        },
    ],
}
r2_master4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        },
    ],
}

r1_master6 = {
    "fc00:100::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:101::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
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
        },
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:101::/64": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
}


#
# BIRD t_kernel*
#

r1_t_kernel4 = {
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        }
    ]
}
r2_t_kernel4 = r2_t_ospf4

r1_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.router_id": "0.0.0.2"},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "router_id": "0.0.0.2",
            "type": ["OSPF", "univ"],
        }
    ]
}
r2_t_kernel6 = r2_t_ospf6


#
# FIB inet*
#

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "prefsrc": "100.101.0.1", "protocol": "kernel", "scope": "link"},
]
r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.101.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:101::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc00:101::/64",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
