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

"""Common data for test cases."""


#
# BIRD t_bgp*_peer
#

r1_t_bgp4_AS65001_r2_peer = {
    "100.101.0.0/24": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"gateway": "192.168.1.2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static4",
            "type": ["static", "univ"],
        }
    ]
}
r1_t_bgp4_AS65000_r2_peer = r1_t_bgp4_AS65001_r2_peer

r1_t_bgp6_AS65001_r2_peer = {
    "fc00:101::/48": [
        {
            "attributes": {"BGP.large_community": [(65000, 3, 1)], "BGP.local_pref": 940},
            "nexthops": [{"gateway": "fc01::2", "interface": "eth1"}],
            "pref": 200,
            "prefix_type": "unicast",
            "protocol": "static6",
            "type": ["static", "univ"],
        }
    ]
}
r1_t_bgp6_AS65000_r2_peer = r1_t_bgp6_AS65001_r2_peer
