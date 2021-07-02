# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_rip4 = {
    "100.101.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_rip",
            "type": ["device", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_rip",
            "type": ["device", "univ"],
        }
    ],
}

r2_t_rip4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
}

r1_t_rip6 = {
    "fc00:101::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_rip",
            "type": ["device", "univ"],
        }
    ],
    "fc00:211::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_rip",
            "type": ["device", "univ"],
        }
    ],
}

r2_t_rip6 = {
    "fc00:101::/64": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
    "fc00:211::/64": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
}

r1_master4 = {
    "0.0.0.0/0": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "bestpath": False,
            "nexthops": [{"gateway": "100.201.0.3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        },
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        },
    ],
    "100.101.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "100.121.0.0/24": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "bestpath": True,
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
            "bestpath": True,
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
            "bestpath": True,
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.132.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.133.0.0/24": [
        {"bestpath": True, "pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}
    ],
    "100.201.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
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
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "bestpath": True,
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
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "bestpath": False,
            "nexthops": [{"gateway": "fc00:201::3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        },
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        },
    ],
    "fc00:100::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:101::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:121::/48": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "bestpath": True,
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
            "bestpath": True,
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
            "bestpath": True,
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:132::/48": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:133::/64": [
        {"bestpath": True, "pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}
    ],
    "fc00:201::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:211::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth10"}],
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
            "bestpath": True,
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:101::/64": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
    "fc00:211::/64": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
}

r1_t_direct4_rip = {
    "100.101.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_rip",
            "type": ["device", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_rip",
            "type": ["device", "univ"],
        }
    ],
}

r1_t_direct6_rip = {
    "fc00:101::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_rip",
            "type": ["device", "univ"],
        }
    ],
    "fc00:211::/64": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth10"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_rip",
            "type": ["device", "univ"],
        }
    ],
}

r1_t_kernel4 = {
    "0.0.0.0/0": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "bestpath": False,
            "nexthops": [{"gateway": "100.201.0.3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        },
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        },
    ],
    "100.121.0.0/24": [
        {
            "attributes": {"Kernel.metric": 0, "Kernel.source": "RTS_DEVICE"},
            "bestpath": True,
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
            "bestpath": True,
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
            "bestpath": True,
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel4",
            "type": ["inherit", "univ"],
        }
    ],
    "100.131.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "100.201.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.132.0.0/24": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.133.0.0/24": [
        {"bestpath": True, "pref": 200, "prefix_type": "blackhole", "protocol": "static4", "type": ["static", "univ"]}
    ],
}

r2_t_kernel4 = {
    "100.101.0.0/24": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
    "100.211.0.0/24": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ],
}

r1_t_kernel6 = {
    "::/0": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "bestpath": False,
            "nexthops": [{"gateway": "fc00:201::3", "interface": "eth2"}],
            "pref": 10,
            "prefix_type": "unicast",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        },
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        },
    ],
    "fc00:121::/48": [
        {
            "attributes": {"Kernel.metric": 1024, "Kernel.source": "RTS_DEVICE"},
            "bestpath": True,
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
            "bestpath": True,
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
            "bestpath": True,
            "pref": 10,
            "prefix_type": "blackhole",
            "protocol": "kernel6",
            "type": ["inherit", "univ"],
        }
    ],
    "fc00:131::/48": [
        {
            "bestpath": True,
            "nexthops": [{"gateway": "fc00:201::2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:132::/48": [
        {
            "bestpath": True,
            "nexthops": [{"interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ],
    "fc00:133::/64": [
        {"bestpath": True, "pref": 200, "prefix_type": "blackhole", "protocol": "static6", "type": ["static", "univ"]}
    ],
}

r2_t_kernel6 = {
    "fc00:101::/64": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
    "fc00:211::/64": [
        {
            "attributes": {"RIP.metric": 3, "RIP.tag": "0000"},
            "bestpath": True,
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ],
}

r1_inet = [
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "100.201.0.3"},
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "100.201.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.101.0.0/24", "flags": [], "prefsrc": "100.101.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.121.0.0/24", "flags": [], "gateway": "100.201.0.3"},
    {"dev": "eth2", "dst": "100.122.0.0/24", "flags": [], "scope": "link"},
    {"dst": "100.123.0.0/31", "flags": [], "type": "blackhole"},
    {"dev": "eth2", "dst": "100.131.0.0/24", "flags": [], "gateway": "100.201.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth2", "dst": "100.132.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dst": "100.133.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "type": "blackhole"},
    {"dev": "eth2", "dst": "100.201.0.0/24", "flags": [], "prefsrc": "100.201.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth10", "dst": "100.211.0.0/24", "flags": [], "prefsrc": "100.211.0.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.101.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.211.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:101::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
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
    {"dev": "eth2", "dst": "fc00:201::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth10", "dst": "fc00:211::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth10", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "fc00:201::2", "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "default", "flags": [], "gateway": "fc00:201::3", "metric": 1024, "pref": "medium"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dev": "eth0",
        "dst": "fc00:101::/64",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dev": "eth0",
        "dst": "fc00:211::/64",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
