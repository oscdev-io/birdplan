# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65000_e1_peer = {
    "100.64.101.0/24": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_e1_peer = {
    "fc00:101::/48": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6 = {
    "fc00:101::/48": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
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
    "100.64.101.0/24": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        }
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
        }
    ],
    "fc00:101::/48": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ],
}

r1_t_kernel4 = {
    "100.64.101.0/24": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_kernel6 = {
    "fc00:101::/48": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.ext_community": [
                    ("ro", 0, 0),
                    ("ro", 1, 1),
                    ("ro", 2, 2),
                    ("ro", 3, 3),
                    ("ro", 4, 4),
                    ("ro", 5, 5),
                    ("ro", 6, 6),
                    ("ro", 7, 7),
                    ("ro", 8, 8),
                    ("ro", 9, 9),
                    ("ro", 10, 10),
                    ("ro", 11, 11),
                    ("ro", 12, 12),
                    ("ro", 13, 13),
                    ("ro", 14, 14),
                    ("ro", 15, 15),
                    ("ro", 16, 16),
                    ("ro", 17, 17),
                    ("ro", 18, 18),
                    ("ro", 19, 19),
                    ("ro", 20, 20),
                    ("ro", 21, 21),
                    ("ro", 22, 22),
                    ("ro", 23, 23),
                    ("ro", 24, 24),
                ],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.101.0/24", "flags": [], "gateway": "100.64.0.2", "metric": 600, "protocol": "bird"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dev": "eth0",
        "dst": "fc00:101::/48",
        "flags": [],
        "gateway": "fc00:100::2",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
