# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65000_e1_peer = {}

r1_t_bgp4_AS65001_r2_peer = {}

r2_t_bgp4_AS65000_r1_peer = {}

r1_t_bgp6_AS65000_e1_peer = {}

r1_t_bgp6_AS65001_r2_peer = {
    "fc01::/64": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 5000, 1)], "BGP.local_pref": 940},
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_bgp",
            "type": ["device", "univ"],
        }
    ]
}

r2_t_bgp6_AS65000_r1_peer = {
    "fc01::/64": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65000, 5000, 1), (65001, 3, 5)],
                "BGP.local_pref": 450,
                "BGP.next_hop": ["fc00:100::1", "fe80::1:ff:fe00:1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4 = {
    "192.168.1.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_bgp",
            "type": ["device", "univ"],
        }
    ]
}

r2_t_bgp4 = {}

r1_t_bgp6 = {
    "fc01::/64": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_bgp",
            "type": ["device", "univ"],
        }
    ]
}

r2_t_bgp6 = {
    "fc01::/64": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65000, 5000, 1), (65001, 3, 5)],
                "BGP.local_pref": 450,
                "BGP.next_hop": ["fc00:100::1", "fe80::1:ff:fe00:1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_master4 = {
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
    ],
    "fc01::/64": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65000, 5000, 1), (65001, 3, 5)],
                "BGP.local_pref": 450,
                "BGP.next_hop": ["fc00:100::1", "fe80::1:ff:fe00:1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ],
}

r1_t_kernel4 = {}

r2_t_kernel4 = {}

r1_t_kernel6 = {}

r2_t_kernel6 = {
    "fc01::/64": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65000, 5000, 1), (65001, 3, 5)],
                "BGP.local_pref": 450,
                "BGP.next_hop": ["fc00:100::1", "fe80::1:ff:fe00:1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "192.168.1.0/24", "flags": [], "prefsrc": "192.168.1.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [{"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"}]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc01::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc01::/64", "flags": [], "gateway": "fc00:100::1", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
