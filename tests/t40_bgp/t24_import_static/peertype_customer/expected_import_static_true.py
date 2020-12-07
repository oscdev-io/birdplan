# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_static4 = {
    "100.101.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.104.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
}

r1_t_static6 = {
    "fc00:101::/48": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:104::/48": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
}

r1_t_bgp4_AS65001_r2_peer = {}

r2_t_bgp4_AS65000_r1_peer = {}

r1_t_bgp6_AS65001_r2_peer = {}

r2_t_bgp6_AS65000_r1_peer = {}

r1_t_bgp4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_bgp4 = {}

r1_t_bgp6 = {
    "fc00:101::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_bgp6 = {}

r1_master4 = {
    "100.101.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.104.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "192.168.1.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
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
    "fc00:101::/48": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:104::/48": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
    "fc01::/64": [
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
        }
    ]
}

r1_t_kernel4 = {
    "100.101.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.104.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
}

r2_t_kernel4 = {}

r1_t_kernel6 = {
    "fc00:101::/48": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:104::/48": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
}

r2_t_kernel6 = {}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "gateway": "192.168.1.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth1", "dst": "100.103.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dst": "100.104.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "type": "blackhole"},
    {"dev": "eth1", "dst": "192.168.1.0/24", "flags": [], "prefsrc": "192.168.1.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [{"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"}]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:101::/48", "flags": [], "gateway": "fc01::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:103::/48", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "lo", "dst": "fc00:104::/48", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird", "type": "blackhole"},
    {"dev": "eth1", "dst": "fc01::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
