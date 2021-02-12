# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_bgp4_AS65000_e1_peer = {
    "0.0.0.0/0": [
        {
            "attributes": {
                "BGP.as_path": [],
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

r1_t_bgp4_AS65000_e2_peer = {
    "0.0.0.0/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 4)],
                "BGP.local_pref": 50,
                "BGP.next_hop": ["100.64.0.3"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e2",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp6_AS65000_e1_peer = {
    "::/0": [
        {
            "attributes": {
                "BGP.as_path": [],
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

r1_t_bgp6_AS65000_e2_peer = {
    "::/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 4)],
                "BGP.local_pref": 50,
                "BGP.next_hop": ["fc00:100::3"],
                "BGP.origin": "IGP",
            },
            "bestpath": True,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e2",
            "type": ["BGP", "univ"],
        }
    ]
}

r1_t_bgp4 = {
    "0.0.0.0/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 4)],
                "BGP.local_pref": 50,
                "BGP.next_hop": ["100.64.0.3"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.3", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e2",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "100.201.0.4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        },
    ],
    "100.111.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "100.201.0.4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.112.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.113.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
}

r1_t_bgp6 = {
    "::/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 4)],
                "BGP.local_pref": 50,
                "BGP.next_hop": ["fc00:100::3"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::3", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e2",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "fc00:201::4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        },
    ],
    "fc00:111::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "fc00:201::4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:112::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:113::/64": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
}

r1_master4 = {
    "0.0.0.0/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "100.201.0.3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        },
        {
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        },
    ],
    "100.111.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "100.201.0.4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.112.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.113.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.121.0.0/24": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "100.201.0.3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.122.0.0/24": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.scope": "link", "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.123.0.0/31": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.132.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.133.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
    "100.201.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
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
    "::/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "fc00:201::3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        },
        {
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
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
    "fc00:111::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "fc00:201::4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:112::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:113::/64": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:121::/48": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "fc00:201::3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:122::/48": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:123::/127": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:132::/48": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:133::/64": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
    "fc00:201::/48": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
}

r1_t_kernel4 = {
    "0.0.0.0/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["100.64.0.2"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "100.64.0.2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp4_AS65000_e1",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "100.201.0.3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        },
        {
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        },
    ],
    "100.111.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "100.201.0.4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.112.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.113.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate4",
            "type": ["static", "univ"],
        }
    ],
    "100.121.0.0/24": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "100.201.0.3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.122.0.0/24": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.scope": "link", "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.123.0.0/31": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.132.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.133.0.0/24": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}],
}

r1_t_kernel6 = {
    "::/0": [
        {
            "attributes": {
                "BGP.as_path": [],
                "BGP.large_community": [(65000, 3, 1)],
                "BGP.local_pref": 100,
                "BGP.next_hop": ["fc00:100::2"],
                "BGP.origin": "IGP",
            },
            "bestpath": False,
            "bgp_type": "i",
            "nexthops": [{"gateway": "fc00:100::2", "interface": "eth0"}],
            "pref": 100,
            "prefix_type": "unicast",
            "protocol": "bgp6_AS65000_e1",
            "type": ["BGP", "univ"],
        },
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "fc00:201::3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        },
        {
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        },
    ],
    "fc00:111::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"gateway": "fc00:201::4", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:112::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 930},
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:113::/64": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1), (65000, 1200, 2)], "BGP.local_pref": 930},
            "pref": 200,
            "prefix_type": "blackhole",
            "protocol": "bgp_originate6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:121::/48": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"gateway": "fc00:201::3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:122::/48": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "nexthops": [{"interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:123::/127": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:132::/48": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:133::/64": [{"pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}],
}

r1_inet = [
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "100.201.0.3"},
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "100.201.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.111.0.0/24", "flags": [], "gateway": "100.201.0.4", "metric": 600, "protocol": "bird"},
    {"dev": "eth2", "dst": "100.112.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dst": "100.113.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "type": "blackhole"},
    {"dev": "eth2", "dst": "100.121.0.0/24", "flags": [], "gateway": "100.201.0.3"},
    {"dev": "eth2", "dst": "100.122.0.0/24", "flags": [], "scope": "link"},
    {"dst": "100.123.0.0/31", "flags": [], "type": "blackhole"},
    {"dev": "eth2", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.201.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth2", "dst": "100.132.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dst": "100.133.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "type": "blackhole"},
    {"dev": "eth2", "dst": "100.201.0.0/24", "flags": [], "prefsrc": "100.201.0.1", "protocol": "kernel", "scope": "link"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dev": "eth2",
        "dst": "fc00:111::/48",
        "flags": [],
        "gateway": "fc00:201::4",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth2", "dst": "fc00:112::/48", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "lo", "dst": "fc00:113::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird", "type": "blackhole"},
    {"dev": "eth2", "dst": "fc00:121::/48", "flags": [], "gateway": "fc00:201::3", "metric": 1024, "pref": "medium"},
    {"dev": "eth2", "dst": "fc00:122::/48", "flags": [], "metric": 1024, "pref": "medium"},
    {"dev": "lo", "dst": "fc00:123::/127", "flags": [], "metric": 1024, "pref": "medium", "type": "blackhole"},
    {
        "dev": "eth2",
        "dst": "fc00:131::/48",
        "flags": [],
        "gateway": "fc00:201::2",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth2", "dst": "fc00:132::/48", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "lo", "dst": "fc00:133::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird", "type": "blackhole"},
    {"dev": "eth2", "dst": "fc00:201::/48", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "fc00:201::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "fc00:201::3", "metric": 1024, "pref": "medium"},
]
