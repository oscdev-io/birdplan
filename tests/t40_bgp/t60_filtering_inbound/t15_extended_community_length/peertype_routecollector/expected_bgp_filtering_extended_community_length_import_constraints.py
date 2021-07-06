# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65001_e1_peer = {
    "100.102.100.0/24": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
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
                    ("ro", 25, 25),
                    ("ro", 26, 26),
                    ("ro", 27, 27),
                    ("ro", 28, 28),
                    ("ro", 29, 29),
                    ("ro", 30, 30),
                    ("ro", 31, 31),
                    ("ro", 32, 32),
                    ("ro", 33, 33),
                    ("ro", 34, 34),
                    ("ro", 35, 35),
                    ("ro", 36, 36),
                    ("ro", 37, 37),
                    ("ro", 38, 38),
                    ("ro", 39, 39),
                    ("ro", 40, 40),
                    ("ro", 41, 41),
                    ("ro", 42, 42),
                    ("ro", 43, 43),
                    ("ro", 44, 44),
                    ("ro", 45, 45),
                    ("ro", 46, 46),
                    ("ro", 47, 47),
                    ("ro", 48, 48),
                    ("ro", 49, 49),
                    ("ro", 50, 50),
                    ("ro", 51, 51),
                    ("ro", 52, 52),
                    ("ro", 53, 53),
                    ("ro", 54, 54),
                    ("ro", 55, 55),
                    ("ro", 56, 56),
                    ("ro", 57, 57),
                    ("ro", 58, 58),
                    ("ro", 59, 59),
                    ("ro", 60, 60),
                    ("ro", 61, 61),
                    ("ro", 62, 62),
                    ("ro", 63, 63),
                    ("ro", 64, 64),
                    ("ro", 65, 65),
                    ("ro", 66, 66),
                    ("ro", 67, 67),
                    ("ro", 68, 68),
                    ("ro", 69, 69),
                    ("ro", 70, 70),
                    ("ro", 71, 71),
                    ("ro", 72, 72),
                    ("ro", 73, 73),
                    ("ro", 74, 74),
                    ("ro", 75, 75),
                    ("ro", 76, 76),
                    ("ro", 77, 77),
                    ("ro", 78, 78),
                    ("ro", 79, 79),
                    ("ro", 80, 80),
                    ("ro", 81, 81),
                    ("ro", 82, 82),
                    ("ro", 83, 83),
                    ("ro", 84, 84),
                    ("ro", 85, 85),
                    ("ro", 86, 86),
                    ("ro", 87, 87),
                    ("ro", 88, 88),
                    ("ro", 89, 89),
                    ("ro", 90, 90),
                    ("ro", 91, 91),
                    ("ro", 92, 92),
                    ("ro", 93, 93),
                    ("ro", 94, 94),
                    ("ro", 95, 95),
                    ("ro", 96, 96),
                    ("ro", 97, 97),
                    ("ro", 98, 98),
                    ("ro", 99, 99),
                ],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
    "100.102.101.0/24": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
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
                    ("ro", 25, 25),
                    ("ro", 26, 26),
                    ("ro", 27, 27),
                    ("ro", 28, 28),
                    ("ro", 29, 29),
                    ("ro", 30, 30),
                    ("ro", 31, 31),
                    ("ro", 32, 32),
                    ("ro", 33, 33),
                    ("ro", 34, 34),
                    ("ro", 35, 35),
                    ("ro", 36, 36),
                    ("ro", 37, 37),
                    ("ro", 38, 38),
                    ("ro", 39, 39),
                    ("ro", 40, 40),
                    ("ro", 41, 41),
                    ("ro", 42, 42),
                    ("ro", 43, 43),
                    ("ro", 44, 44),
                    ("ro", 45, 45),
                    ("ro", 46, 46),
                    ("ro", 47, 47),
                    ("ro", 48, 48),
                    ("ro", 49, 49),
                    ("ro", 50, 50),
                    ("ro", 51, 51),
                    ("ro", 52, 52),
                    ("ro", 53, 53),
                    ("ro", 54, 54),
                    ("ro", 55, 55),
                    ("ro", 56, 56),
                    ("ro", 57, 57),
                    ("ro", 58, 58),
                    ("ro", 59, 59),
                    ("ro", 60, 60),
                    ("ro", 61, 61),
                    ("ro", 62, 62),
                    ("ro", 63, 63),
                    ("ro", 64, 64),
                    ("ro", 65, 65),
                    ("ro", 66, 66),
                    ("ro", 67, 67),
                    ("ro", 68, 68),
                    ("ro", 69, 69),
                    ("ro", 70, 70),
                    ("ro", 71, 71),
                    ("ro", 72, 72),
                    ("ro", 73, 73),
                    ("ro", 74, 74),
                    ("ro", 75, 75),
                    ("ro", 76, 76),
                    ("ro", 77, 77),
                    ("ro", 78, 78),
                    ("ro", 79, 79),
                    ("ro", 80, 80),
                    ("ro", 81, 81),
                    ("ro", 82, 82),
                    ("ro", 83, 83),
                    ("ro", 84, 84),
                    ("ro", 85, 85),
                    ("ro", 86, 86),
                    ("ro", 87, 87),
                    ("ro", 88, 88),
                    ("ro", 89, 89),
                    ("ro", 90, 90),
                    ("ro", 91, 91),
                    ("ro", 92, 92),
                    ("ro", 93, 93),
                    ("ro", 94, 94),
                    ("ro", 95, 95),
                    ("ro", 96, 96),
                    ("ro", 97, 97),
                    ("ro", 98, 98),
                    ("ro", 99, 99),
                    ("ro", 100, 100),
                ],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
}

r1_t_bgp6_AS65001_e1_peer = {
    "fc00:102:100::/64": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
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
                    ("ro", 25, 25),
                    ("ro", 26, 26),
                    ("ro", 27, 27),
                    ("ro", 28, 28),
                    ("ro", 29, 29),
                    ("ro", 30, 30),
                    ("ro", 31, 31),
                    ("ro", 32, 32),
                    ("ro", 33, 33),
                    ("ro", 34, 34),
                    ("ro", 35, 35),
                    ("ro", 36, 36),
                    ("ro", 37, 37),
                    ("ro", 38, 38),
                    ("ro", 39, 39),
                    ("ro", 40, 40),
                    ("ro", 41, 41),
                    ("ro", 42, 42),
                    ("ro", 43, 43),
                    ("ro", 44, 44),
                    ("ro", 45, 45),
                    ("ro", 46, 46),
                    ("ro", 47, 47),
                    ("ro", 48, 48),
                    ("ro", 49, 49),
                    ("ro", 50, 50),
                    ("ro", 51, 51),
                    ("ro", 52, 52),
                    ("ro", 53, 53),
                    ("ro", 54, 54),
                    ("ro", 55, 55),
                    ("ro", 56, 56),
                    ("ro", 57, 57),
                    ("ro", 58, 58),
                    ("ro", 59, 59),
                    ("ro", 60, 60),
                    ("ro", 61, 61),
                    ("ro", 62, 62),
                    ("ro", 63, 63),
                    ("ro", 64, 64),
                    ("ro", 65, 65),
                    ("ro", 66, 66),
                    ("ro", 67, 67),
                    ("ro", 68, 68),
                    ("ro", 69, 69),
                    ("ro", 70, 70),
                    ("ro", 71, 71),
                    ("ro", 72, 72),
                    ("ro", 73, 73),
                    ("ro", 74, 74),
                    ("ro", 75, 75),
                    ("ro", 76, 76),
                    ("ro", 77, 77),
                    ("ro", 78, 78),
                    ("ro", 79, 79),
                    ("ro", 80, 80),
                    ("ro", 81, 81),
                    ("ro", 82, 82),
                    ("ro", 83, 83),
                    ("ro", 84, 84),
                    ("ro", 85, 85),
                    ("ro", 86, 86),
                    ("ro", 87, 87),
                    ("ro", 88, 88),
                    ("ro", 89, 89),
                    ("ro", 90, 90),
                    ("ro", 91, 91),
                    ("ro", 92, 92),
                    ("ro", 93, 93),
                    ("ro", 94, 94),
                    ("ro", 95, 95),
                    ("ro", 96, 96),
                    ("ro", 97, 97),
                    ("ro", 98, 98),
                    ("ro", 99, 99),
                ],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
    "fc00:102:101::/64": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
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
                    ("ro", 25, 25),
                    ("ro", 26, 26),
                    ("ro", 27, 27),
                    ("ro", 28, 28),
                    ("ro", 29, 29),
                    ("ro", 30, 30),
                    ("ro", 31, 31),
                    ("ro", 32, 32),
                    ("ro", 33, 33),
                    ("ro", 34, 34),
                    ("ro", 35, 35),
                    ("ro", 36, 36),
                    ("ro", 37, 37),
                    ("ro", 38, 38),
                    ("ro", 39, 39),
                    ("ro", 40, 40),
                    ("ro", 41, 41),
                    ("ro", 42, 42),
                    ("ro", 43, 43),
                    ("ro", 44, 44),
                    ("ro", 45, 45),
                    ("ro", 46, 46),
                    ("ro", 47, 47),
                    ("ro", 48, 48),
                    ("ro", 49, 49),
                    ("ro", 50, 50),
                    ("ro", 51, 51),
                    ("ro", 52, 52),
                    ("ro", 53, 53),
                    ("ro", 54, 54),
                    ("ro", 55, 55),
                    ("ro", 56, 56),
                    ("ro", 57, 57),
                    ("ro", 58, 58),
                    ("ro", 59, 59),
                    ("ro", 60, 60),
                    ("ro", 61, 61),
                    ("ro", 62, 62),
                    ("ro", 63, 63),
                    ("ro", 64, 64),
                    ("ro", 65, 65),
                    ("ro", 66, 66),
                    ("ro", 67, 67),
                    ("ro", 68, 68),
                    ("ro", 69, 69),
                    ("ro", 70, 70),
                    ("ro", 71, 71),
                    ("ro", 72, 72),
                    ("ro", 73, 73),
                    ("ro", 74, 74),
                    ("ro", 75, 75),
                    ("ro", 76, 76),
                    ("ro", 77, 77),
                    ("ro", 78, 78),
                    ("ro", 79, 79),
                    ("ro", 80, 80),
                    ("ro", 81, 81),
                    ("ro", 82, 82),
                    ("ro", 83, 83),
                    ("ro", 84, 84),
                    ("ro", 85, 85),
                    ("ro", 86, 86),
                    ("ro", 87, 87),
                    ("ro", 88, 88),
                    ("ro", 89, 89),
                    ("ro", 90, 90),
                    ("ro", 91, 91),
                    ("ro", 92, 92),
                    ("ro", 93, 93),
                    ("ro", 94, 94),
                    ("ro", 95, 95),
                    ("ro", 96, 96),
                    ("ro", 97, 97),
                    ("ro", 98, 98),
                    ("ro", 99, 99),
                    ("ro", 100, 100),
                ],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
}

r1_t_bgp4 = {}

r1_t_bgp6 = {}

r1_master4 = {
    "100.64.0.0/24": [
        {
            "bestpath": True,
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
            "bestpath": True,
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