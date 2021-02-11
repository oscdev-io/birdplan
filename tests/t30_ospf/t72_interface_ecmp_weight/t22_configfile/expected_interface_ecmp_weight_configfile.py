# type: ignore
# pylint: disable=too-many-lines

"""Expected test result data."""

r1_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "nexthops": [{"gateway": "100.127.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r2_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r3_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r4_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r5_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r6_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r7_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r8_t_ospf4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 30,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r1_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r2_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r3_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r4_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r5_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r6_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r7_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r8_t_ospf6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r1_master4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "nexthops": [{"gateway": "100.127.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.127.0.0/24": [
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
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
}

r2_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.105.0.0/24": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
}

r3_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.105.0.0/24": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
}

r4_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.105.0.0/24": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
}

r5_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.105.0.0/24": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.110.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r6_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.105.0.0/24": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.110.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r7_master4 = {
    "100.102.0.0/24": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.103.0.0/24": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.104.0.0/24": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.105.0.0/24": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.110.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r8_master4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        },
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 30,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
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
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:127::/48": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
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
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:103::/64": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:104::/64": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:105::/64": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r3_master6 = {
    "fc00:100::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:103::/64": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:104::/64": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:105::/64": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r4_master6 = {
    "fc00:100::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:103::/64": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:104::/64": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:105::/64": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r5_master6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:103::/64": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:104::/64": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:105::/64": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:200::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
}

r6_master6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:103::/64": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:104::/64": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:105::/64": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:200::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
}

r7_master6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:103::/64": [
        {
            "nexthops": [{"interface": "eth2"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:104::/64": [
        {
            "nexthops": [{"interface": "eth3"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:105::/64": [
        {
            "nexthops": [{"interface": "eth4"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
    "fc00:200::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
}

r8_master6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "nexthops": [{"interface": "eth0"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6",
            "type": ["device", "univ"],
        },
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        },
    ],
}

r1_t_static4 = {
    "100.120.0.0/24": [
        {
            "nexthops": [{"gateway": "100.127.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}

r1_t_static6 = {}

r1_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "100.64.0.2", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.3", "interface": "eth0", "weight": 1},
                {"gateway": "100.64.0.4", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "nexthops": [{"gateway": "100.127.0.2", "interface": "eth2"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r2_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r3_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r4_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.5", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.6", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.7", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.5", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.6", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.7", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.5", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.6", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.7", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.5", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.6", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.7", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 10,
            "metric2": 10000,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r5_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r6_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r7_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 20,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.103.0.2", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.3", "interface": "eth2", "weight": 2},
                {"gateway": "100.103.0.4", "interface": "eth2", "weight": 2},
                {"gateway": "100.102.0.2", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.3", "interface": "eth1", "weight": 1},
                {"gateway": "100.102.0.4", "interface": "eth1", "weight": 1},
                {"gateway": "100.104.0.2", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.3", "interface": "eth3", "weight": 1},
                {"gateway": "100.104.0.4", "interface": "eth3", "weight": 1},
                {"gateway": "100.105.0.2", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.3", "interface": "eth4", "weight": 1},
                {"gateway": "100.105.0.4", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r8_t_kernel4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.103.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.104.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.105.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.110.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
    "100.120.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30, "OSPF.metric2": 10000, "OSPF.router_id": "0.0.0.1", "OSPF.tag": "0x00000000"},
            "metric1": 30,
            "metric2": 10000,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "E2",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "router_id": "0.0.0.1",
            "type": ["OSPF-E2", "univ"],
        }
    ],
    "100.64.0.0/24": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "100.110.0.5", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.6", "interface": "eth0", "weight": 1},
                {"gateway": "100.110.0.7", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf4",
            "type": ["OSPF", "univ"],
        }
    ],
}

r1_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r2_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r3_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r4_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::6:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::7:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::5:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::5:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r5_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r6_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r7_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::2:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::3:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::4:ff:fe00:3", "interface": "eth2", "weight": 2},
                {"gateway": "fe80::2:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::2:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::3:ff:fe00:5", "interface": "eth4", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:2", "interface": "eth1", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:4", "interface": "eth3", "weight": 1},
                {"gateway": "fe80::4:ff:fe00:5", "interface": "eth4", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth1"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth2"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth3"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth4"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r8_t_kernel6 = {
    "fc00:100::/64": [
        {
            "attributes": {"OSPF.metric1": 30},
            "metric1": 30,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:102::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:103::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:104::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:105::/64": [
        {
            "attributes": {"OSPF.metric1": 20},
            "metric1": 20,
            "nexthops": [
                {"gateway": "fe80::5:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::6:ff:fe00:1", "interface": "eth0", "weight": 1},
                {"gateway": "fe80::7:ff:fe00:1", "interface": "eth0", "weight": 1},
            ],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
    "fc00:200::/64": [
        {
            "attributes": {"OSPF.metric1": 10},
            "metric1": 10,
            "nexthops": [{"interface": "eth0"}],
            "ospf_type": "I",
            "pref": 150,
            "prefix_type": "unicast",
            "protocol": "ospf6",
            "type": ["OSPF", "univ"],
        }
    ],
}

r1_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.1", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.102.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.103.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.104.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.105.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.110.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.2", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.3", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.64.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth2", "dst": "100.120.0.0/24", "flags": [], "gateway": "100.127.0.2", "metric": 600, "protocol": "bird"},
    {"dev": "eth2", "dst": "100.127.0.0/24", "flags": [], "prefsrc": "100.127.0.1", "protocol": "kernel", "scope": "link"},
]

r2_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "prefsrc": "100.103.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "prefsrc": "100.104.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "prefsrc": "100.105.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.110.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.5", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.6", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.7", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.6", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.7", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.5", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.6", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.7", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.5", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.6", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "100.120.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r3_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.3", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.3", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "prefsrc": "100.103.0.3", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "prefsrc": "100.104.0.3", "protocol": "kernel", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "prefsrc": "100.105.0.3", "protocol": "kernel", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.110.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.5", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.6", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.7", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.6", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.7", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.5", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.6", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.7", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.5", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.6", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "100.120.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r4_inet = [
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.4", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.4", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "prefsrc": "100.103.0.4", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "prefsrc": "100.104.0.4", "protocol": "kernel", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "prefsrc": "100.105.0.4", "protocol": "kernel", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.110.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.5", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.6", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.7", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.6", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.7", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.5", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.6", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.7", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.5", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.6", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "100.120.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
]

r5_inet = [
    {
        "dst": "100.64.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.2", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.3", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.4", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.4", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.3", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.2", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.3", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.5", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "prefsrc": "100.103.0.5", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "prefsrc": "100.104.0.5", "protocol": "kernel", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "prefsrc": "100.105.0.5", "protocol": "kernel", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "prefsrc": "100.110.0.5", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.120.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.2", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.3", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.4", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.4", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.3", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.2", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.3", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
]

r6_inet = [
    {
        "dst": "100.64.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.2", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.3", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.4", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.4", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.3", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.2", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.3", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.6", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "prefsrc": "100.103.0.6", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "prefsrc": "100.104.0.6", "protocol": "kernel", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "prefsrc": "100.105.0.6", "protocol": "kernel", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "prefsrc": "100.110.0.6", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.120.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.2", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.3", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.4", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.4", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.3", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.2", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.3", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
]

r7_inet = [
    {
        "dst": "100.64.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.2", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.3", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.4", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.4", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.3", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.2", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.3", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "prefsrc": "100.102.0.7", "protocol": "kernel", "scope": "link"},
    {"dev": "eth1", "dst": "100.102.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "prefsrc": "100.103.0.7", "protocol": "kernel", "scope": "link"},
    {"dev": "eth2", "dst": "100.103.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "prefsrc": "100.104.0.7", "protocol": "kernel", "scope": "link"},
    {"dev": "eth3", "dst": "100.104.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "prefsrc": "100.105.0.7", "protocol": "kernel", "scope": "link"},
    {"dev": "eth4", "dst": "100.105.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "prefsrc": "100.110.0.7", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.120.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.2", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.3", "weight": 2},
            {"dev": "eth2", "flags": [], "gateway": "100.103.0.4", "weight": 2},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.2", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "100.102.0.4", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.3", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "100.104.0.4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.2", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.3", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "100.105.0.4", "weight": 1},
        ],
        "protocol": "bird",
    },
]

r8_inet = [
    {
        "dst": "100.64.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.5", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.6", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.102.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.5", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.6", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.103.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.5", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.6", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.104.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.5", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.6", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {
        "dst": "100.105.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.5", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.6", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "prefsrc": "100.110.0.8", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.110.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
    {
        "dst": "100.120.0.0/24",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.5", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.6", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "100.110.0.7", "weight": 1},
        ],
        "protocol": "bird",
    },
]

r1_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dst": "fc00:102::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dst": "fc00:103::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dst": "fc00:104::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dst": "fc00:105::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth2", "dst": "fc00:127::/48", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {
        "dst": "fc00:200::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::2:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::3:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::4:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dst": "fc00:200::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "fe80::5:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::6:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::7:ff:fe00:3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::5:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::5:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::5:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::6:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::6:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::6:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::7:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::7:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::7:ff:fe00:5", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r3_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dst": "fc00:200::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "fe80::5:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::6:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::7:ff:fe00:3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::5:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::5:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::5:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::6:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::6:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::6:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::7:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::7:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::7:ff:fe00:5", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r4_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dst": "fc00:200::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "fe80::5:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::6:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::7:ff:fe00:3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::5:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::5:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::5:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::6:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::6:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::6:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::7:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::7:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::7:ff:fe00:5", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r5_inet6 = [
    {
        "dst": "fc00:100::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "fe80::2:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::3:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::4:ff:fe00:3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::2:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::2:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::2:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::3:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::3:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::3:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::4:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::4:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::4:ff:fe00:5", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r6_inet6 = [
    {
        "dst": "fc00:100::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "fe80::2:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::3:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::4:ff:fe00:3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::2:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::2:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::2:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::3:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::3:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::3:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::4:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::4:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::4:ff:fe00:5", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r7_inet6 = [
    {
        "dst": "fc00:100::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth2", "flags": [], "gateway": "fe80::2:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::3:ff:fe00:3", "weight": 1},
            {"dev": "eth2", "flags": [], "gateway": "fe80::4:ff:fe00:3", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::2:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::2:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::2:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::3:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::3:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::3:ff:fe00:5", "weight": 1},
            {"dev": "eth1", "flags": [], "gateway": "fe80::4:ff:fe00:2", "weight": 1},
            {"dev": "eth3", "flags": [], "gateway": "fe80::4:ff:fe00:4", "weight": 1},
            {"dev": "eth4", "flags": [], "gateway": "fe80::4:ff:fe00:5", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fc00:102::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fc00:103::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fc00:104::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fc00:105::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth1", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth2", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth3", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth4", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]

r8_inet6 = [
    {
        "dst": "fc00:100::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::5:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::6:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::7:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dst": "fc00:102::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::5:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::6:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::7:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dst": "fc00:103::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::5:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::6:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::7:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dst": "fc00:104::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::5:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::6:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::7:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {
        "dst": "fc00:105::/64",
        "flags": [],
        "metric": 600,
        "nexthops": [
            {"dev": "eth0", "flags": [], "gateway": "fe80::5:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::6:ff:fe00:1", "weight": 1},
            {"dev": "eth0", "flags": [], "gateway": "fe80::7:ff:fe00:1", "weight": 1},
        ],
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:200::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
