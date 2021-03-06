# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65100_e1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65009_r10_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65001_r2_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65000_r3_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65003_r4_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65004_r5_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100, 65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65005_r6_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65000_r7_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65000_r8_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4_AS65000_r9_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r2_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65001, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r3_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r4_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65003, 3, 3)],
                "BGP.local_pref": 470,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r5_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65004, 1101, 17)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r6_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65005, 3, 5)],
                "BGP.local_pref": 450,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r7_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r8_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r9_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r10_t_bgp4_AS65000_r1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65009, 3, 4)],
                "BGP.local_pref": 150,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65100_e1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65009_r10_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65001_r2_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_r3_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65003_r4_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65004_r5_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100, 65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65005_r6_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_r7_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_r8_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_r9_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r2_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65001, 3, 2)],
                "BGP.local_pref": 750,
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

r3_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r4_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65003, 3, 3)],
                "BGP.local_pref": 470,
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

r5_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65004, 1101, 17)],
                "BGP.local_pref": 100,
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

r6_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65005, 3, 5)],
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

r7_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r8_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r9_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r10_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65009, 3, 4)],
                "BGP.local_pref": 150,
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
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r2_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65001, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r3_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r4_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65003, 3, 3)],
                "BGP.local_pref": 470,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r5_t_bgp4 = {}

r6_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65005, 3, 5)],
                "BGP.local_pref": 450,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r7_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r8_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r9_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["100.64.0.100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "100.64.0.1",
            "nexthops": [{"gateway": "100.64.0.100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r10_t_bgp4 = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65009, 3, 4)],
                "BGP.local_pref": 150,
                "BGP.next_hop": ["100.64.0.1"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 71, 996), (65000, 3, 2)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65100_e1",
            "type": ["BGP", "univ"],
        }
    ]
}

r2_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65001, 3, 2)],
                "BGP.local_pref": 750,
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

r3_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r4_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65003, 3, 3)],
                "BGP.local_pref": 470,
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

r5_t_bgp6 = {}

r6_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65005, 3, 5)],
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

r7_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r8_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r9_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996)],
                "BGP.local_pref": 750,
                "BGP.next_hop": ["fc00:100::100"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "from": "fc00:100::1",
            "nexthops": [{"gateway": "fc00:100::100", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_r1",
            "type": ["BGP", "univ"],
        }
    ]
}

r10_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65000, 65100],
                "BGP.large_community": [(65000, 3, 2), (65000, 71, 996), (65009, 3, 4)],
                "BGP.local_pref": 150,
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
