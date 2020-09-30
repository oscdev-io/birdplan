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


from .data_common import (  # noqa: F401 pylint: disable=unused-import
    r1_t_static4,
    r1_t_static6,
    r1_t_ospf4,
    r1_t_ospf4_expect_content,
    r1_t_ospf6,
    r1_t_ospf6_expect_content,
    r2_t_ospf4,
    r2_t_ospf6,
    r1_master4,
    r1_master6,
    r2_master4,
    r2_master6,
    r1_t_kernel4,
    r1_t_kernel6,
    r1_inet,
    r1_inet6,
)


#
# BIRD t_kernel*
#

r2_t_kernel4 = r2_t_ospf4

r2_t_kernel6 = r2_t_ospf6

#
# RIB inet*
#

r2_inet = [
    {"dev": "eth0", "dst": "10.0.0.0/24", "flags": [], "gateway": "100.64.0.1", "metric": 600, "protocol": "bird"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "prefsrc": "100.64.0.2", "protocol": "kernel", "scope": "link"},
    {"dev": "eth0", "dst": "100.64.0.0/24", "flags": [], "metric": 600, "protocol": "bird", "scope": "link"},
]

r2_inet6 = [
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
    {"dev": "eth0", "dst": "fc00:100::/64", "flags": [], "metric": 600, "pref": "medium", "protocol": "bird"},
    {
        "dev": "eth0",
        "dst": "fc10::/64",
        "flags": [],
        "gateway": "fe80::1:ff:fe00:1",
        "metric": 600,
        "pref": "medium",
        "protocol": "bird",
    },
    {"dev": "eth0", "dst": "fe80::/64", "flags": [], "metric": 256, "pref": "medium", "protocol": "kernel"},
]
