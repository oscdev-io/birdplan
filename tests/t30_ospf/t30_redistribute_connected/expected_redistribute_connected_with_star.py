# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_direct4_ospf = {
    "100.101.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_ospf",
            "type": ["device", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_ospf",
            "type": ["device", "univ"],
        }
    ],
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
    ],
    "fc00:211::/64": [
        {
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_ospf",
            "type": ["device", "univ"],
        }
    ],
}

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
    "100.211.0.0/24": [
        {
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_ospf",
            "type": ["device", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
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
    "100.211.0.0/24": [
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
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r1_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
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
    "fc00:211::/64": [
        {
            "nexthops": [{"interface": "eth10"}],
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
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
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
    "fc00:211::/64": [
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
    "100.201.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "nexthops": [{"interface": "eth10"}],
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
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
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
    "100.211.0.0/24": [
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
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
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
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
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
    "fc00:201::/64": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:211::/64": [
        {
            "nexthops": [{"interface": "eth10"}],
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
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
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
    "fc00:211::/64": [
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

r1_t_kernel4 = {
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ]
}

r2_t_kernel4 = {
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
    "100.211.0.0/24": [
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
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r1_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ]
}

r2_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
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
    "fc00:211::/64": [
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

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "prefsrc": "100.101.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.201.0.0/24", "flags": [], "prefsrc": "100.201.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth10", "dst": "100.211.0.0/24", "flags": [], "prefsrc": "100.211.0.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.101.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.211.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:101::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fc00:201::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth10", "dst": "fc00:211::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth10", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
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
    {
        "dev": "eth0",
        "dst": "fc00:211::/64",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]