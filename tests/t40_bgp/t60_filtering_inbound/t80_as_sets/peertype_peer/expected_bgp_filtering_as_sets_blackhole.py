# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65001_e1_peer = {
    "100.64.100.0/24": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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
    ],
    "100.64.101.0/32": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26)],
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
    ],
    "100.64.102.0/32": [
        {
            "asn": "AS65002",
            "attributes": {
                "BGP.as_path": [65001, 65002],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26), (65000, 1101, 10)],
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
    ],
    "100.64.121.0/32": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26)],
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
    ],
    "100.64.131.0/32": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26)],
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
    ],
}

r1_t_bgp6_AS65001_e1_peer = {
    "fc00:0:100::/48": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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
    ],
    "fc00:0:101::/128": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26)],
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
    ],
    "fc00:0:102::/128": [
        {
            "asn": "AS65002",
            "attributes": {
                "BGP.as_path": [65001, 65002],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26), (65000, 1101, 10)],
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
    ],
    "fc00:0:121::/128": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26)],
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
    ],
    "fc00:0:131::/128": [
        {
            "asn": "AS65001",
            "attributes": {
                "BGP.as_path": [65001],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 3, 3), (65000, 1101, 26)],
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
    ],
}

r1_t_bgp4 = {
    "100.64.100.0/24": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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

r1_t_bgp6 = {
    "fc00:0:100::/48": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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
    "100.64.100.0/24": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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
    ],
}

r1_master6 = {
    "fc00:0:100::/48": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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
}

r1_t_kernel4 = {
    "100.64.100.0/24": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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

r1_t_kernel6 = {
    "fc00:0:100::/48": [
        {
            "asn": "AS65003",
            "attributes": {
                "BGP.as_path": [65001, 65003],
                "BGP.large_community": [(65000, 3, 3)],
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

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.100.0/24", "flags": [], "gateway": "100.64.0.2", "metric": 600, "protocol": "bird"},
]

r1_inet6 = [
    {
        "dev": "eth0",
        "dst": "fc00:0:100::/48",
        "flags": [],
        "gateway": "fc00:100::2",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
