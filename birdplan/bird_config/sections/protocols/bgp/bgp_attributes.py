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

"""BIRD BGP protocol attributes."""

from typing import List, Optional, Union


class BGPRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for acceptance of routes from the main BGP table into the master table.

    Attributes
    ----------
    bgp_default : bool
        Accept default route. Defaults to `False`.
    blackhole : bool
        Accept blackhole routes. Defaults to `True`.
    originated : bool
        Accept originated routes. Defaults to `True`.
    originated_default : bool
        Accept originated routes. Defaults to `False`.

    """

    bgp_default: bool
    blackhole: bool
    originated: bool
    originated_default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.bgp_default = False
        self.blackhole = True
        self.originated = True
        self.originated_default = False


class BGPRoutePolicyImport:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for importing of routes internally.

    Attributes
    ----------
    connected : Union[bool, List[str]]
        Import connected routes into the main BGP table. This attribute is indexed by interface name with a boolean option.
        The interface name can be an exact interface match, or a wildcard with a *.
    kernel : bool
        Import kernel routes into the main BGP table. Defaults to `False`.
    kernel_blackhole : bool
        Import kernel blackhole routes into the main BGP table. Defaults to `False`.
    kernel_default : bool
        Import kernel default routes into the main BGP table. Defaults to `False`.
    static : bool
        Import static routes into the main BGP table. Defaults to `False`.
    static_default : bool
        Import static default routes into the main BGP table. Defaults to `False`.
    static_blackhole : bool
        Import static blackhole routes into the main BGP table. Defaults to `False`.

    """

    connected: Union[bool, List[str]]
    kernel: bool
    kernel_blackhole: bool
    kernel_default: bool
    static: bool
    static_blackhole: bool
    static_default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = False
        self.kernel = False
        self.kernel_blackhole = False
        self.kernel_default = False
        self.static = False
        self.static_blackhole = False
        self.static_default = False


class BGPAttributes:  # pylint: disable=too-few-public-methods
    """
    BGP attributes.

    Attributes
    ----------
    asn : int
        BGP ASN.
    graceful_shutdown ; boolean
        Set graceful_shutdown mode for all peers.
    rr_cluster_id : Optional[str]
        Route relfector cluster ID in the case of us being a route reflector.
    route_policy_accept : BGPRoutePolicyAccept
        Route policy for acceptance of routes from the main BGP table into the master table.
    route_policy_import : BGPRoutePolicyImport
        Route policy for importing of routes from internal tables into our main BGP table.
    blackhole_import_maxlen4 : int
        Blackhole maximum length for IPv4 to import.
    blackhole_import_minlen4 : int
        Blackhole minimum length for IPv4 to import.
    blackhole_export_maxlen4 : int
        Blackhole maximum length for IPv4 to export.
    blackhole_export_minlen4 : int
        Blackhole minimum length for IPv4 to export.
    blackhole_import_maxlen6 : int
        Blackhole maximum length for IPv6 to import.
    blackhole_import_minlen6 : int
        Blackhole minimum length for IPv6 to import.
    blackhole_export_maxlen6 : int
        Blackhole maximum length for IPv6 to export.
    blackhole_export_minlen6 : int
        Blackhole minimum length for IPv6 to export.
    prefix_import_maxlen4 : int
        Prefix maximum length for IPv4 to import.
    prefix_import_minlen4 : int
        Prefix minimum length for IPv4 to import.
    prefix_export_maxlen4 : int
        Prefix maximum length for IPv4 to export.
    prefix_export_minlen4 : int
        Prefix minimum length for IPv4 to export.
    prefix_import_maxlen6 : int
        Prefix maximum length for IPv6 to import.
    prefix_import_minlen6 : int
        Prefix minimum length for IPv6 to import.
    prefix_export_maxlen6 : int
        Prefix maximum length for IPv6 to export.
    prefix_export_minlen6 : int
        Prefix minimum length for IPv6 to export.
    aspath_import_maxlen : int
        AS-PATH maximum length.
    aspath_import_minlen : int
        AS-PATH minimum length.
    community_import_maxlen : int
        Community maximum length.
    extended_community_import_maxlen : int
        Extended community maximum length.
    large_community_import_maxlen : int
        Large community maximum length.

    """

    asn: Optional[int]
    graceful_shutdown: bool
    rr_cluster_id: Optional[str]
    route_policy_accept: BGPRoutePolicyAccept
    route_policy_import: BGPRoutePolicyImport

    blackhole_import_maxlen4: int
    blackhole_import_minlen4: int

    blackhole_export_maxlen4: int
    blackhole_export_minlen4: int

    blackhole_import_maxlen6: int
    blackhole_import_minlen6: int

    blackhole_export_maxlen6: int
    blackhole_export_minlen6: int

    prefix_import_maxlen4: int
    prefix_import_minlen4: int

    prefix_export_maxlen4: int
    prefix_export_minlen4: int

    prefix_import_maxlen6: int
    prefix_import_minlen6: int

    prefix_export_maxlen6: int
    prefix_export_minlen6: int

    aspath_import_maxlen: int
    aspath_import_minlen: int

    community_import_maxlen: int
    extended_community_import_maxlen: int
    large_community_import_maxlen: int

    def __init__(self) -> None:
        """Initialize object."""

        self.asn = None

        self.graceful_shutdown = False

        self.rr_cluster_id = None

        self.route_policy_accept = BGPRoutePolicyAccept()
        self.route_policy_import = BGPRoutePolicyImport()

        self.blackhole_import_maxlen4 = 32
        self.blackhole_import_minlen4 = 24

        self.blackhole_export_maxlen4 = 32
        self.blackhole_export_minlen4 = 24

        self.blackhole_import_maxlen6 = 128
        self.blackhole_import_minlen6 = 64

        self.blackhole_export_maxlen6 = 128
        self.blackhole_export_minlen6 = 64

        self.prefix_import_maxlen4 = 24
        self.prefix_import_minlen4 = 8

        self.prefix_export_maxlen4 = 24
        self.prefix_export_minlen4 = 8

        self.prefix_import_maxlen6 = 48
        self.prefix_import_minlen6 = 16

        self.prefix_export_maxlen6 = 48
        self.prefix_export_minlen6 = 16

        self.aspath_import_maxlen = 100
        self.aspath_import_minlen = 1

        self.community_import_maxlen = 100
        self.extended_community_import_maxlen = 100
        self.large_community_import_maxlen = 100
