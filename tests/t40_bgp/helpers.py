#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2020, AllWorldIT
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# type: ignore

from typing import Optional


def bgp_pref(peer_type: Optional[str] = None, route_type: Optional[str] = None) -> int:  # noqa: C901
    """Return the BGP preference for a specific peer type."""

    # Work out adjustment
    adjustment = 0
    if route_type:
        if route_type == "originated":
            adjustment = -20
        elif route_type == "static":
            adjustment = -10
        elif route_type == "direct":
            adjustment = -10
        elif route_type == "kernel":
            adjustment = -5

    pref = 0
    if not peer_type:
        pref = 950
    if peer_type == "customer":
        pref = 750
    elif peer_type == "peer":
        pref = 470
    elif peer_type == "routeserver":
        pref = 450
    elif peer_type == "transit":
        pref = 150

    return pref + adjustment


def bgp_lc(  # noqa: C901
    origin_asn: int, asn: Optional[int] = None, peer_type: Optional[str] = None, route_type: Optional[str] = None
) -> int:
    """Return the BGP large community list."""

    # Work out adjustment
    rt_lc = []
    if route_type:
        if route_type == "originated":
            rt_lc.append((origin_asn, 3, 1))
        elif route_type == "static":
            rt_lc.append((origin_asn, 3, 1))
        elif route_type == "direct":
            rt_lc.append((origin_asn, 3, 1))
        elif route_type == "kernel":
            rt_lc.append((origin_asn, 3, 1))

    if peer_type:
        if peer_type == "customer":
            rt_lc.append((asn, 3, 2))
        elif peer_type == "peer":
            rt_lc.append((asn, 3, 3))
        elif peer_type == "routeserver":
            rt_lc.append((asn, 3, 5))
        elif peer_type == "transit":
            rt_lc.append((asn, 3, 4))

    return rt_lc


def bgp_local_pref(peer_type: Optional[str] = None) -> int:  # noqa: C901
    """Return the BGP local preference."""

    # Work out adjustment
    rt_lc = []
    if route_type:
        if route_type == "originated":
            rt_lc.append((origin_asn, 3, 1))
        elif route_type == "static":
            rt_lc.append((origin_asn, 3, 1))
        elif route_type == "direct":
            rt_lc.append((origin_asn, 3, 1))
        elif route_type == "kernel":
            rt_lc.append((origin_asn, 3, 1))

    if peer_type:
        if peer_type == "customer":
            rt_lc.append((asn, 3, 2))
        elif peer_type == "peer":
            rt_lc.append((asn, 3, 3))
        elif peer_type == "routeserver":
            rt_lc.append((asn, 3, 5))
        elif peer_type == "transit":
            rt_lc.append((asn, 3, 4))

    return rt_lc
