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

from typing import Any, Dict, List, Optional, Union
import requests
from birdplan.exceptions import BirdPlanError

BGPPeerPrefixLimit = Optional[str]
BGPPeerFilterItem = Union[str, List[str]]
BGPPeerFilter = Dict[str, BGPPeerFilterItem]
BGPPeerPeeringDB = Dict[str, Any]

BGPPeerRoutePolicyRedistributeItem = Union[bool, Dict[str, Any]]


class BGPPeerLargeCommunities:  # pylint: disable=too-few-public-methods
    """
    BGP peer large communities.

    Attributes
    ----------
    incoming : List[str]
        List of large communities to add to incoming prefixes.
    outgoing : List[str]
        List of large communities to add to outgoing prefixes.

    """

    incoming: List[str]

    outgoing: List[str]

    def __init__(self) -> None:
        """Initialize object."""
        self.incoming = []
        self.outgoing = []


class BGPPeerRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for acceptance of routes from BGP peers into the main BGP table.

    Attributes
    ----------
    default : bool
        Accept default route. Defaults to `False`.

    """

    default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.default = False


class BGPRoutePolicyImport:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for importing of routes internally.

    Attributes
    ----------
    connected : Dict[str, bool]
        Import connected routes into the main BGP table. This attribute is indexed by interface name with a boolean option.
        The interface name can be an exact interface match, or a wildcard with a *.
    kernel : bool
        Import kernel routes into the main BGP table. Defaults to `False`.
    static : bool
        Import static routes into the main BGP table. Defaults to `False`.

    """

    connected: Dict[str, bool]
    kernel: bool
    static: bool

    route_policy_accept: BGPPeerRoutePolicyAccept

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = {}
        self.kernel = False
        self.static = False


class BGPPeerFilterPolicy:  # pylint: disable=too-few-public-methods
    """
    BGP filter policy for incoming routes from the BGP peer.

    Attributes
    ----------
    prefixes : BGPPeerFilterItem
        List of prefixes to filter on.
    asns : BGPPeerFilterItem
        List of ASNs to filter on.
    as_sets : BGPPeerFilterItem
        List of AS-SET's to filter on.

    """

    prefixes: BGPPeerFilterItem
    asns: BGPPeerFilterItem
    as_sets: BGPPeerFilterItem

    def __init__(self) -> None:
        """Initialize object."""
        self.prefixes = []
        self.asns = []
        self.as_sets = []


class BGPPeerRoutePolicyRedistribute:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer route policy for redistributing of routes.

    Attributes
    ----------
    connected : BGPPeerRoutePolicyRedistributeItem
        Redistribute connected routes to the peer BGP table. Defaults to `False`.
    default: Dict[str, Bool]
        Redistribute the default route to the peer BGP table. Defaults to `False`.
    originated : BGPPeerRoutePolicyRedistributeItem
        Redistribute originated routes to the peer BGP table. Defaults to `False`.
    kernel : BGPPeerRoutePolicyRedistributeItem
        Redistribute kernel routes to the peer BGP table. Defaults to `False`.
    static : BGPPeerRoutePolicyRedistributeItem
        Redistribute static routes to the peer BGP table. Defaults to `False`.
    bgp: BGPPeerRoutePolicyRedistributeItem
        Redistribute all BGP routes to the peer BGP table. Defaults to `False`.
    bgp_own: BGPPeerRoutePolicyRedistributeItem
        Redistribute our own originated BGP routes to the peer BGP table. Defaults to `False`.
    bgp_customer: BGPPeerRoutePolicyRedistributeItem
        Redistribute customer BGP routes to the peer BGP table. Defaults to `False`.
    bgp_peering: BGPPeerRoutePolicyRedistributeItem
        Redistribute peering BGP routes to the peer BGP table. Defaults to `False`.
    bgp_transit: BGPPeerRoutePolicyRedistributeItem
        Redistribute transit BGP routes to the peer BGP table. Defaults to `False`.

    """

    connected: BGPPeerRoutePolicyRedistributeItem
    default: bool
    kernel: BGPPeerRoutePolicyRedistributeItem
    originated: BGPPeerRoutePolicyRedistributeItem
    static: BGPPeerRoutePolicyRedistributeItem
    bgp: BGPPeerRoutePolicyRedistributeItem
    bgp_own: BGPPeerRoutePolicyRedistributeItem
    bgp_customer: BGPPeerRoutePolicyRedistributeItem
    bgp_peering: BGPPeerRoutePolicyRedistributeItem
    bgp_transit: BGPPeerRoutePolicyRedistributeItem

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = False
        self.default = False
        self.kernel = False
        self.originated = False
        self.static = False
        self.bgp = False
        self.bgp_own = False
        self.bgp_customer = False
        self.bgp_peering = False
        self.bgp_transit = False


class BGPPeerAttributes:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer attributes.

    Attributes
    ----------
    name : str
        Peer name.
    description : str
        Description of the peer.
    peer_type : str
        Peer type.
    asn : int
        Peers ASN.
    neighbor4: Optional[str]
        Neighbor IPv4 address.
    neighbor6: Optional[str]
        Neighbor IPv6 address.
    source_address4: Optional[str]
        Source IPv4 address.
    source_address6: Optional[str]
        Source IPv6 address.
    connect_delay_time: Optional[str]
        BGP connect delay time.
    connect_retry_time: Optional[str]
        BGP connection retry time.
    error_wait_time: Optional[str]
        BGP error wait time.
    multihop: Optional[str]
        BGP multihop value.
    password: Optional[str]
        BGP password.
    cost : int
        Cost of this peer, this is the number minused from the local_pref.
    graceful_shutdown : bool
        Set peer in GRACEFUL_SHUTDOWN mode if set to True.
    passive : bool
        Indicate if this is a passive peer or not.
    quarantined : bool
        Set if the peer is quarantined.
    prefix_limit4 : BGPPeerPrefixLimit
        Prefix limit for IPv4.
    prefix_limit6 : BGPPeerPrefixLimit
        Prefix limit for IPv6.
    route_policy_accept : BGPPeerRoutePolicyAccept
        Route policy for acceptance of routes from BGP peers into our main BGP table.
    route_policy_redistribute : BGPPeerRoutePolicyRedistribute
        Route policy for redistribution of routes to the BGP peer.
    filter: BGPPeerFilter
        BGP peer filtering options.
    peeringdb: Optional[BGPPeerPeeringDB]
        BGP peer peeringdb entry.

    """

    _name: Optional[str]
    _description: Optional[str]

    _peer_type: Optional[str]
    _asn: Optional[int]

    neighbor4: Optional[str] = None
    neighbor6: Optional[str] = None
    source_address4: Optional[str] = None
    source_address6: Optional[str] = None

    connect_delay_time: Optional[str] = None
    connect_retry_time: Optional[str] = None
    error_wait_time: Optional[str] = None
    multihop: Optional[str] = None
    password: Optional[str] = None

    cost: int = 0

    graceful_shutdown: bool = False

    large_communities: BGPPeerLargeCommunities

    # Default to disabling passive mode
    passive: bool = False

    quarantined: bool = False

    prefix_limit4: BGPPeerPrefixLimit = None
    prefix_limit6: BGPPeerPrefixLimit = None

    route_policy_accept: BGPPeerRoutePolicyAccept
    route_policy_redistribute: BGPPeerRoutePolicyRedistribute

    filter_policy: BGPPeerFilterPolicy

    _peeringdb: Optional[BGPPeerPeeringDB]

    def __init__(self) -> None:
        """Initialize object."""

        self._name = None
        self._description = None

        self._peer_type = None
        self._asn = None

        self.large_communities = BGPPeerLargeCommunities()

        # Route policies
        self.route_policy_accept = BGPPeerRoutePolicyAccept()
        self.route_policy_redistribute = BGPPeerRoutePolicyRedistribute()

        self.filter_policy = BGPPeerFilterPolicy()

        self._peeringdb = None

    @property
    def peeringdb(self) -> BGPPeerPeeringDB:
        """Return our peeringdb entry, if there is one."""
        if self.asn > 64512 and self.asn < 65534:
            return {"info_prefixes4": None, "info_prefixes6": None}
        # If we don't having peerindb info, grab it
        if not self._peeringdb:
            self._peeringdb = requests.get(f"https://www.peeringdb.com/api/net?asn__in={self.asn}").json()["data"][0]
        # Check the result of peeringdb is not empty
        if not self._peeringdb:
            raise BirdPlanError("PeeringDB returned and empty result")
        # Lastly return it
        return self._peeringdb

    @property
    def name(self) -> str:
        """Return our name."""
        if not self._name:
            raise BirdPlanError("Peer name must be set")
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set our name."""
        self._name = name

    @property
    def description(self) -> str:
        """Return our description."""
        if not self._description:
            raise BirdPlanError("Peer description must be set")
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        """Set our description."""
        self._description = description

    @property
    def peer_type(self) -> str:
        """Return our peer_type."""
        if not self._peer_type:
            raise BirdPlanError("Peer peer_type must be set")
        return self._peer_type

    @peer_type.setter
    def peer_type(self, peer_type: str) -> None:
        """Set our peer_type."""
        self._peer_type = peer_type

    @property
    def asn(self) -> int:
        """Return our asn."""
        if not self._asn:
            raise BirdPlanError("Peer asn must be set")
        return self._asn

    @asn.setter
    def asn(self, asn: int) -> None:
        """Set our asn."""
        self._asn = asn
