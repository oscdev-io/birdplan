# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65000_r2_peer = {}

r2_t_bgp4_AS65000_r1_peer = {}

r1_t_bgp6_AS65000_r2_peer = {}

r2_t_bgp6_AS65000_r1_peer = {}

r1_t_bgp4 = {
    "0.0.0.0/0": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.101.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.116.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "192.168.1.4", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_bgp4 = {}

r1_t_bgp6 = {
    "::/0": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:101::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:116::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "fc01::4", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
}

r2_t_bgp6 = {}

r1_master4 = {
    "0.0.0.0/0": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        },
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "192.168.1.3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.111.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.112.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.113.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
    "100.114.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "192.168.1.3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.115.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
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
    "::/0": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        },
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc01::3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        },
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
    "fc00:104::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:111::/48": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:112::/48": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:113::/48": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
    "fc00:114::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc01::3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:115::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
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
    ]
}

r1_t_bgp_originate4 = {
    "0.0.0.0/0": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.101.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.116.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "192.168.1.4", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
}

r1_t_bgp_originate6 = {
    "::/0": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:101::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:116::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "fc01::4", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
}

r1_t_static4 = {
    "0.0.0.0/0": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.111.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.112.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.113.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
}

r1_t_static6 = {
    "::/0": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:111::/48": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:112::/48": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:113::/48": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
}

r1_t_kernel4 = {
    "0.0.0.0/0": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        },
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "192.168.1.3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.111.0.0/24": [
        {
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.112.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.113.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
    "100.114.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.source": "3"},
            "nexthops": [{"gateway": "192.168.1.3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.115.0.0/24": [
        {
            "attributes": {"Kernel.metric": "0", "Kernel.scope": "253", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_kernel4 = {}

r1_t_kernel6 = {
    "::/0": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        },
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc01::3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        },
    ],
    "fc00:104::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:111::/48": [
        {
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:112::/48": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:113::/48": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
    "fc00:114::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"gateway": "fc01::3", "interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:115::/48": [
        {
            "attributes": {"Kernel.metric": "1024", "Kernel.source": "3"},
            "nexthops": [{"interface": "eth1"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
}

r2_t_kernel6 = {}

r1_inet = [
    {"dev": "eth1", "dst": "default", "flags": [], "gateway": "192.168.1.3"},
    {"dev": "eth1", "dst": "default", "flags": [], "gateway": "192.168.1.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dst": "100.104.0.0/24", "flags": [], "type": "blackhole"},
    {"dev": "eth1", "dst": "100.111.0.0/24", "flags": [], "gateway": "192.168.1.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth1", "dst": "100.112.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dst": "100.113.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "type": "blackhole"},
    {"dev": "eth1", "dst": "100.114.0.0/24", "flags": [], "gateway": "192.168.1.3"},
    {"dev": "eth1", "dst": "100.115.0.0/24", "flags": [], "scope": "link"},
    {"dev": "eth1", "dst": "192.168.1.0/24", "flags": [], "prefsrc": "192.168.1.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [{"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"}]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "lo", "dst": "fc00:104::/48", "flags": [], "metric": 1024, "pref": "medium", "type": "blackhole"},
    {"dev": "eth1", "dst": "fc00:111::/48", "flags": [], "gateway": "fc01::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:112::/48", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "lo", "dst": "fc00:113::/48", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird", "type": "blackhole"},
    {"dev": "eth1", "dst": "fc00:114::/48", "flags": [], "gateway": "fc01::3", "metric": 1024, "pref": "medium"},
    {"dev": "eth1", "dst": "fc00:115::/48", "flags": [], "metric": 1024, "pref": "medium"},
    {"dev": "eth1", "dst": "fc01::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "default", "flags": [], "gateway": "fc01::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "default", "flags": [], "gateway": "fc01::3", "metric": 1024, "pref": "medium"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
