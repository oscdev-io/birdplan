# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_static4 = {
    "0.0.0.0/0": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "192.168.20.0/24": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
}

r1_t_static6 = {
    "::/0": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc20::/64": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
}

r1_t_rip4 = {
    "0.0.0.0/0": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "192.168.20.0/24": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_rip4 = {
    "0.0.0.0/0": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "192.168.20.0/24": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
}

r3_t_rip4 = {
    "192.168.20.0/24": [
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
    "192.168.30.0/24": [
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
}

r1_t_rip6 = {
    "::/0": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc20::/64": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_rip6 = {
    "::/0": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
    "fc20::/64": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
}

r3_t_rip6 = {
    "fc20::/64": [
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
    "fc30::/64": [
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

r1_master4 = {
    "0.0.0.0/0": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
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
        }
    ],
    "192.168.20.0/24": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
}

r2_master4 = {
    "100.102.0.0/24": [
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
        }
    ],
    "192.168.20.0/24": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
}

r3_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "192.168.20.0/24": [
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
    "192.168.30.0/24": [
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
}

r1_master6 = {
    "::/0": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:100::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
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
    "fc20::/64": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
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
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc20::/64": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
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
    "fc20::/64": [
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
    "fc30::/64": [
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

r1_t_kernel4 = {
    "0.0.0.0/0": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "192.168.20.0/24": [
        {
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_kernel4 = {
    "192.168.20.0/24": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
}

r3_t_kernel4 = {
    "192.168.20.0/24": [
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
    "192.168.30.0/24": [
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
}

r1_t_kernel6 = {
    "::/0": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc20::/64": [
        {
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_kernel6 = {
    "fc20::/64": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
}

r3_t_kernel6 = {
    "fc20::/64": [
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
    "fc30::/64": [
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

r1_inet = [
    {"dev": "eth1", "dst": "default", "flags": [], "gateway": "100.101.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "prefsrc": "100.101.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "192.168.20.0/24", "flags": [], "gateway": "100.101.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth1", "dst": "192.168.30.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
]

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "192.168.20.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "192.168.30.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r3_inet = [
    {"dev": "eth0", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "192.168.20.0/24", "flags": [], "gateway": "100.102.0.1", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "192.168.30.0/24", "flags": [], "gateway": "100.102.0.1", "metric": 600, "protocol": "bird"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:101::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc20::/64", "flags": [], "gateway": "fc00:101::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc30::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "default", "flags": [], "gateway": "fc00:101::2", "metric": 600, "pref": "medium", "protocol": "bird"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dev": "eth0",
        "dst": "fc20::/64",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dev": "eth0",
        "dst": "fc30::/64",
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
    {"dev": "eth0", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dev": "eth0",
        "dst": "fc20::/64",
        "flags": [],
        "gateway": "fe80::2:ff:fe00:2",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dev": "eth0",
        "dst": "fc30::/64",
        "flags": [],
        "gateway": "fe80::2:ff:fe00:2",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
