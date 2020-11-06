# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65001_e1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
                "BGP.community": [
                    (1, 0),
                    (1, 1),
                    (1, 2),
                    (1, 3),
                    (1, 4),
                    (1, 5),
                    (1, 6),
                    (1, 7),
                    (1, 8),
                    (1, 9),
                    (1, 10),
                    (1, 11),
                    (1, 12),
                    (1, 13),
                    (1, 14),
                    (1, 15),
                    (1, 16),
                    (1, 17),
                    (1, 18),
                    (1, 19),
                    (1, 20),
                    (1, 21),
                    (1, 22),
                    (1, 23),
                    (1, 24),
                ],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 16)],
                "BGP.local_pref": 470,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65001_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65001_e1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
                "BGP.community": [
                    (1, 0),
                    (1, 1),
                    (1, 2),
                    (1, 3),
                    (1, 4),
                    (1, 5),
                    (1, 6),
                    (1, 7),
                    (1, 8),
                    (1, 9),
                    (1, 10),
                    (1, 11),
                    (1, 12),
                    (1, 13),
                    (1, 14),
                    (1, 15),
                    (1, 16),
                    (1, 17),
                    (1, 18),
                    (1, 19),
                    (1, 20),
                    (1, 21),
                    (1, 22),
                    (1, 23),
                    (1, 24),
                ],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 16)],
                "BGP.local_pref": 470,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65001_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4 = {}

r1_t_bgp6 = {}

r1_master4 = {
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
    ]
}

r1_t_kernel4 = {}

r1_t_kernel6 = {}

r1_inet = [{"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"}]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
