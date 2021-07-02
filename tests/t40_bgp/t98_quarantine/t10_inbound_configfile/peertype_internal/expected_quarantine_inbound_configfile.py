# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65000_r2_peer = {
    "100.101.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "bestpath": True,
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_bgp4_AS65000_r1_peer = {
    "100.101.0.0/24": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1), (65000, 1101, 18)],
                "BGP.local_pref": 940,
                "BGP.next_hop": ["192.168.1.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "pref": 100,
            "prefix_type": "unreachable",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_r2_peer = {
    "fc00:101::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "bestpath": True,
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1), (65000, 1101, 18)],
                "BGP.local_pref": 940,
                "BGP.next_hop": ["fc01::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "pref": 100,
            "prefix_type": "unreachable",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "bestpath": True,
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_bgp4 = {}

r1_t_bgp6 = {
    "fc00:101::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "bestpath": True,
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_bgp6 = {}

r1_master4 = {
    "100.101.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
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
        }
    ],
    "192.168.1.0/24": [
        {
            "bestpath": True,
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
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "192.168.2.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
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
        }
    ],
    "fc00:101::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc01::/64": [
        {
            "bestpath": True,
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
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc02::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
}

r1_t_kernel4 = {
    "100.101.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_kernel4 = {}

r1_t_kernel6 = {
    "fc00:101::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}

r2_t_kernel6 = {}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "gateway": "192.168.1.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth1", "dst": "192.168.1.0/24", "flags": [], "prefsrc": "192.168.1.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "192.168.2.0/24", "flags": [], "prefsrc": "192.168.2.1", "protocol": "kernel", "scope": "link"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:101::/48", "flags": [], "gateway": "fc01::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc01::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc02::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
