# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_static4 = {
    "10.0.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r1_t_static6 = {
    "fc10::/64": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}

r1_master4 = {
    "10.0.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.101.0.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.101.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
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
    "fc00:101::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc10::/64": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:101::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
}

r1_t_kernel4 = {}

r1_t_kernel6 = {}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "prefsrc": "100.101.0.1", "protocol": "kernel", "scope": "link"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:101::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
