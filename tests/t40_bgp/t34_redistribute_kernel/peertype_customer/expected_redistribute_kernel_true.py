# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65001_r2_peer = {
    "100.101.0.0/24": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "0",
                "Kernel.source": "3",
            },
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "0",
                "Kernel.scope": "253",
                "Kernel.source": "3",
            },
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_bgp4_AS65000_r1_peer = {
    "100.101.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "100.103.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
}

r1_t_bgp6_AS65001_r2_peer = {
    "fc00:101::/48": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "1024",
                "Kernel.source": "3",
            },
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "1024",
                "Kernel.source": "3",
            },
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_bgp6_AS65000_r1_peer = {
    "fc00:101::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "fc00:103::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
}

r1_t_bgp4 = {
    "100.101.0.0/24": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "0",
                "Kernel.source": "3",
            },
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "0",
                "Kernel.scope": "253",
                "Kernel.source": "3",
            },
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.104.0.0/31": [
        {
            "attributes": {
                "BGP.community": [(65535, 666), (65535, 65281)],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "0",
                "Kernel.source": "3",
            },
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_bgp4 = {
    "100.101.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "100.103.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
}

r1_t_bgp6 = {
    "fc00:101::/48": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "1024",
                "Kernel.source": "3",
            },
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "attributes": {
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "1024",
                "Kernel.source": "3",
            },
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:104::/127": [
        {
            "attributes": {
                "BGP.community": [(65535, 666), (65535, 65281)],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 945,
                "Kernel.metric": "1024",
                "Kernel.source": "3",
            },
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_bgp6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "fc00:103::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
}

r1_master4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.104.0.0/31": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
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
    "100.101.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "100.103.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "100.64.0.0/24": [
        {
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
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:101::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:104::/127": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
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
    "fc00:101::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "fc00:103::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
}

r1_t_kernel4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.104.0.0/31": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_kernel4 = {
    "100.101.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "100.103.0.0/24": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
}

r1_t_kernel6 = {
    "fc00:101::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:103::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:104::/127": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_kernel6 = {
    "fc00:101::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
    "fc00:103::/48": [
        {
            "asn": "AS65000",
            "attributes": {
                "BGP.as_path": [65000],
                "BGP.large_community": [(65000, 3, 1), (65001, 3, 2)],
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
    ],
}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "gateway": "192.168.1.2"},
    {"dev": "eth1", "dst": "100.103.0.0/24", "flags": [], "scope": "link"},
    {"dst": "100.104.0.0/31", "flags": [], "type": "blackhole"},
    {"dev": "eth1", "dst": "192.168.1.0/24", "flags": [], "prefsrc": "192.168.1.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.101.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.103.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:101::/48", "flags": [], "gateway": "fc01::2", "metric": 1024, "pref": "medium"},
    {"dev": "eth1", "dst": "fc00:103::/48", "flags": [], "metric": 1024, "pref": "medium"},
    {"dev": "lo", "dst": "fc00:104::/127", "flags": [], "metric": 1024, "pref": "medium", "type": "blackhole"},
    {"dev": "eth1", "dst": "fc01::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dev": "eth0",
        "dst": "fc00:101::/48",
        "flags": [],
        "gateway": "fc00:100::1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dev": "eth0",
        "dst": "fc00:103::/48",
        "flags": [],
        "gateway": "fc00:100::1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
