# type: ignore

"""Expected test result data."""

r1_t_rip4 = {}

r2_t_rip4 = {}

r1_t_rip6 = {}

r2_t_rip6 = {}

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
        }
    ],
    "192.168.20.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_master4 = {
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ]
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
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
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
    ]
}

r1_t_kernel4 = {
    "192.168.20.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "192.168.30.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_kernel4 = {}

r1_t_kernel6 = {
    "fc20::/64": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc30::/64": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_kernel6 = {}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "prefsrc": "100.101.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "192.168.20.0/24", "flags": [], "gateway": "100.101.0.2"},
    {"dev": "eth1", "dst": "192.168.30.0/24", "flags": [], "scope": "link"},
]

r2_inet = [{"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"}]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:101::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc20::/64", "flags": [], "gateway": "fc00:101::2", "metric": 1024, "pref": "medium"},
    {"dev": "eth1", "dst": "fc30::/64", "flags": [], "metric": 1024, "pref": "medium"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
