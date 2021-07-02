# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 22},
            "bestpath": True,
            "metric1": 22,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "bestpath": True,
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
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 12, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "bestpath": True,
            "metric1": 12,
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
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
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
            "bestpath": True,
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 22},
            "bestpath": True,
            "metric1": 22,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "attributes": {"OSPF.metric1": 12, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "bestpath": True,
            "metric1": 12,
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
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 22},
            "bestpath": True,
            "metric1": 22,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.201.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "bestpath": False,
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
    "100.102.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": False,
            "metric1": 12,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.131.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 12, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "bestpath": True,
            "metric1": 12,
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
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": False,
            "metric1": 12,
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
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "bestpath": False,
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 22},
            "bestpath": True,
            "metric1": 22,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:201::/48": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
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
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": False,
            "metric1": 12,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:102::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": False,
            "metric1": 12,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:131::/48": [
        {
            "attributes": {"OSPF.metric1": 12, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "bestpath": True,
            "metric1": 12,
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

r1_t_static4 = {
    "100.131.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r1_t_static6 = {
    "fc00:131::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}

r1_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 22},
            "bestpath": True,
            "metric1": 22,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "bestpath": True,
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

r2_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 12, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "bestpath": True,
            "metric1": 12,
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
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
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
            "bestpath": True,
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 22},
            "bestpath": True,
            "metric1": 22,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 12},
            "bestpath": True,
            "metric1": 12,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "attributes": {"OSPF.metric1": 12, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "bestpath": True,
            "metric1": 12,
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
    {
        "dst": "100.102.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth2", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.201.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth2", "dst": "100.201.0.0/24", "flags": [], "prefsrc": "100.201.0.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r3_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.3", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.3", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r4_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.4", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.4", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r5_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.5", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.5", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r6_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.6", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.6", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r7_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.7", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.7", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r8_inet = [
    {
        "dst": "100.64.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.102.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.8", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.131.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.102.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dst": "fc00:102::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dev": "eth2",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fc00:201::2",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth2", "dst": "fc00:201::/48", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r3_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r4_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r5_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r6_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r7_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r8_inet6 = [
    {
        "dst": "fc00:100::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:2", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dst": "fc00:131::/48",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:2", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
