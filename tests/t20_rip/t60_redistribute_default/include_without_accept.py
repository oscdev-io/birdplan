#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2020, AllWorldIT
#
# This program is free software: you can redistfibute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distfibuted in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# type: ignore
# pylint: disable=invalid-name

"""Data for test case."""


#
# BIRD t_rip*
#

r2_t_rip4 = {
    "0.0.0.0/0": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "100.64.0.1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip4",
            "type": ["RIP", "univ"],
        }
    ]
}

r2_t_rip6 = {
    "::/0": [
        {
            "attributes": {"RIP.metric": "3", "RIP.tag": "0000"},
            "metric1": 3,
            "nexthops": [{"gateway": "fe80::1:ff:fe00:1", "interface": "eth0"}],
            "pref": 120,
            "prefix_type": "unicast",
            "protocol": "rip6",
            "type": ["RIP", "univ"],
        }
    ]
}


#
# BIRD t_master*
#

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

#
# BIRD t_kernel*
#

r2_t_kernel4 = {}

r2_t_kernel6 = {}


#
# RIB inet*
#

r2_inet = [{"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"}]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
