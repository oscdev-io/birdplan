# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65100_e1_peer = {
    "100.64.101.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
    "100.64.101.0/29": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
    "100.64.104.0/24": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
}

r1_t_bgp4_AS65009_r10_peer = {}

r1_t_bgp4_AS65001_r2_peer = {}

r1_t_bgp4_AS65000_r3_peer = {}

r1_t_bgp4_AS65003_r4_peer = {}

r1_t_bgp4_AS65004_r5_peer = {}

r1_t_bgp4_AS65005_r6_peer = {}

r1_t_bgp4_AS65000_r7_peer = {}

r1_t_bgp4_AS65000_r8_peer = {}

r1_t_bgp4_AS65000_r9_peer = {}

r2_t_bgp4_AS65000_r1_peer = {}

r3_t_bgp4_AS65000_r1_peer = {}

r4_t_bgp4_AS65000_r1_peer = {}

r5_t_bgp4_AS65000_r1_peer = {}

r6_t_bgp4_AS65000_r1_peer = {}

r7_t_bgp4_AS65000_r1_peer = {}

r8_t_bgp4_AS65000_r1_peer = {}

r9_t_bgp4_AS65000_r1_peer = {}

r10_t_bgp4_AS65000_r1_peer = {}

r1_t_bgp6_AS65100_e1_peer = {
    "fc00:101::/64": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
    "fc00:101::/96": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
    "fc00:104::/64": [
        {
            "asn": "AS65100",
            "attributes": {
                "BGP.as_path": [65100],
                "BGP.community": [(65535, 666)],
                "BGP.large_community": [(65000, 1101, 17)],
                "BGP.local_pref": 100,
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
    ],
}

r1_t_bgp6_AS65009_r10_peer = {}

r1_t_bgp6_AS65001_r2_peer = {}

r1_t_bgp6_AS65000_r3_peer = {}

r1_t_bgp6_AS65003_r4_peer = {}

r1_t_bgp6_AS65004_r5_peer = {}

r1_t_bgp6_AS65005_r6_peer = {}

r1_t_bgp6_AS65000_r7_peer = {}

r1_t_bgp6_AS65000_r8_peer = {}

r1_t_bgp6_AS65000_r9_peer = {}

r2_t_bgp6_AS65000_r1_peer = {}

r3_t_bgp6_AS65000_r1_peer = {}

r4_t_bgp6_AS65000_r1_peer = {}

r5_t_bgp6_AS65000_r1_peer = {}

r6_t_bgp6_AS65000_r1_peer = {}

r7_t_bgp6_AS65000_r1_peer = {}

r8_t_bgp6_AS65000_r1_peer = {}

r9_t_bgp6_AS65000_r1_peer = {}

r10_t_bgp6_AS65000_r1_peer = {}

r1_t_bgp4 = {}

r2_t_bgp4 = {}

r3_t_bgp4 = {}

r4_t_bgp4 = {}

r5_t_bgp4 = {}

r6_t_bgp4 = {}

r7_t_bgp4 = {}

r8_t_bgp4 = {}

r9_t_bgp4 = {}

r10_t_bgp4 = {}

r1_t_bgp6 = {}

r2_t_bgp6 = {}

r3_t_bgp6 = {}

r4_t_bgp6 = {}

r5_t_bgp6 = {}

r6_t_bgp6 = {}

r7_t_bgp6 = {}

r8_t_bgp6 = {}

r9_t_bgp6 = {}

r10_t_bgp6 = {}
