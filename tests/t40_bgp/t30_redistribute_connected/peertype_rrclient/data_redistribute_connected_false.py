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


from ..data_common import (  # noqa: F401 pylint: disable=unused-import
    r1_t_direct4_bgp,
    r1_t_direct6_bgp,
    r2_t_direct4_bgp,
    r2_t_direct6_bgp,
    r1_t_bgp4,
    r1_t_bgp6,
    r1_master4,
    r1_master6,
    r1_t_kernel4,
    r1_t_kernel6,
    r1_inet,
    r1_inet6,
)

from ..data_common_no_redistribution import (  # noqa: F401 pylint: disable=unused-import
    r1_t_bgp4_AS65000_r2_peer,
    r1_t_bgp6_AS65000_r2_peer,
    r2_t_bgp4_AS65000_r1_peer,
    r2_t_bgp6_AS65000_r1_peer,
    r2_master4,
    r2_master6,
    r2_t_kernel4,
    r2_t_kernel6,
    r2_inet,
    r2_inet6,
)

#
# BIRD t_bgp*
#

r2_t_bgp4 = {
    "100.102.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct4_bgp",
            "type": ["device", "univ"],
        }
    ]
}

r2_t_bgp6 = {
    "fc00:102::/64": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"interface": "eth1"}],
            "pref": 240,
            "prefix_type": "unicast",
            "protocol": "direct6_bgp",
            "type": ["device", "univ"],
        }
    ]
}
