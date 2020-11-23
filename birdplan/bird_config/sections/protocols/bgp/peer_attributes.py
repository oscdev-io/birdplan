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

# This type is a string as we can have it set to "peeringdb"
BGPPeerPrefixLimit = Optional[str]

BGPPeerFilterItem = Union[str, List[str]]
BGPPeerFilter = Dict[str, BGPPeerFilterItem]
BGPPeerPeeringDB = Dict[str, Any]


class BGPPeerLargeCommunitiesOutgoing:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer outgoing large communities.

    Attributes
    ----------
    connected: List[str]
        Connected route outgoing large communities.
    default: List[str]
        Default route outgoing large communities.
    kernel: List[str]
        Kernel route outgoing large communities.
    originated: List[str]
        Originated route outgoing large communities.
    static: List[str]
        Static route outgoing large communities.
    bgp: List[str]
        BGP route outgoing large communities.
    bgp_own: List[str]
        BGP own route outgoing large communities.
    bgp_customer: List[str]
        BGP customer route outgoing large communities.
    bgp_peering: List[str]
        BGP peering route outgoing large communities.
    bgp_transit: List[str]
        BGP transit route outgoing large communities.

    """

    connected: List[str]
    default: List[str]
    kernel: List[str]
    originated: List[str]
    static: List[str]
    bgp: List[str]
    bgp_own: List[str]
    bgp_customer: List[str]
    bgp_peering: List[str]
    bgp_transit: List[str]

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = []
        self.default = []
        self.kernel = []
        self.originated = []
        self.static = []
        self.bgp = []
        self.bgp_own = []
        self.bgp_customer = []
        self.bgp_peering = []
        self.bgp_transit = []


class BGPPeerLargeCommunities:  # pylint: disable=too-few-public-methods
    """
    BGP peer large communities.

    Attributes
    ----------
    incoming : List[str]
        List of large communities to add to incoming prefixes.
    outgoing : BGPPeerLargeCommunitiesOutgoing
        List of large communities to add to outgoing prefixes.

    """

    incoming: List[str]

    outgoing: BGPPeerLargeCommunitiesOutgoing

    def __init__(self) -> None:
        """Initialize object."""
        self.incoming = []
        self.outgoing = BGPPeerLargeCommunitiesOutgoing()


class BGPPeerPrependItem:  # pylint: disable=too-few-public-methods
    """
    BGP peer prepending item.

    Attributes
    ----------
    own_asn: int
        Number of times to prepend our own ASN.
    first_asn: int
        Number of times to prepend the first ASN.

    """

    own_asn: int
    # first_asn: int

    def __init__(self) -> None:
        """Initialize object."""
        self.own_asn = 0

    #    self.first_asn = 0


class BGPPeerPrepend:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer prepending.

    Attributes
    ----------
    connected: BGPPeerPrependItem
        Connected route prepending options.
    default: BGPPeerPrependItem
        Default route prepending options.
    kernel: BGPPeerPrependItem
        Kernel route prepending options.
    originated: BGPPeerPrependItem
        Originated route prepending options.
    static: BGPPeerPrependItem
        Static route prepending options.
    bgp: BGPPeerPrependItem
        BGP route prepending options.
    bgp_own: BGPPeerPrependItem
        BGP own route prepending options.
    bgp_customer: BGPPeerPrependItem
        BGP customer route prepending options.
    bgp_peering: BGPPeerPrependItem
        BGP peering route prepending options.
    bgp_transit: BGPPeerPrependItem
        BGP transit route prepending options.

    """

    connected: BGPPeerPrependItem
    default: BGPPeerPrependItem
    kernel: BGPPeerPrependItem
    originated: BGPPeerPrependItem
    static: BGPPeerPrependItem
    bgp: BGPPeerPrependItem
    bgp_own: BGPPeerPrependItem
    bgp_customer: BGPPeerPrependItem
    bgp_peering: BGPPeerPrependItem
    bgp_transit: BGPPeerPrependItem

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = BGPPeerPrependItem()
        self.default = BGPPeerPrependItem()
        self.kernel = BGPPeerPrependItem()
        self.originated = BGPPeerPrependItem()
        self.static = BGPPeerPrependItem()
        self.bgp = BGPPeerPrependItem()
        self.bgp_own = BGPPeerPrependItem()
        self.bgp_customer = BGPPeerPrependItem()
        self.bgp_peering = BGPPeerPrependItem()
        self.bgp_transit = BGPPeerPrependItem()


class BGPPeerRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for acceptance of routes from BGP peers into the main BGP table.

    Attributes
    ----------
    default : bool
        Accept default route. Defaults to `False`.
    blackhole : Union[List[str], bool]
        Accept blackhole routes. Defaults to `False`, unless the peertype is a `customer` and filter:prefixes is set or
        peertype is `internal`.

    """

    default: bool
    blackhole: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.default = False
        self.blackhole = False


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
    origin_asns : BGPPeerFilterItem
        List of origin ASNs to filter on.
    peer_asns : BGPPeerFilterItem
        List of peer ASNs to filter on.
    as_sets : BGPPeerFilterItem
        List of AS-SET's to filter on.

    """

    prefixes: BGPPeerFilterItem
    origin_asns: BGPPeerFilterItem
    peer_asns: BGPPeerFilterItem
    as_sets: BGPPeerFilterItem

    def __init__(self) -> None:
        """Initialize object."""
        self.prefixes = []
        self.origin_asns = []
        self.peer_asns = []
        self.as_sets = []


class BGPPeerLocation:  # pylint: disable=too-few-public-methods
    """
    BGP peer location.

    Attributes
    ----------
    iso3166 : Optional[int]
        ISO3166 numeric location of the peer.
    unm49 : Optional[int]
        UN.M49 location of the peer.

    """

    unm49: Optional[int]
    iso3166: Optional[int]

    def __init__(self) -> None:
        """Initialize object."""
        self.unm49 = None
        self.iso3166 = None


class BGPPeerRoutePolicyRedistribute:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer route policy for redistributing of routes.

    Attributes
    ----------
    connected : bool
        Redistribute connected routes to the peer BGP table. Defaults to `False`.
    default : bool
        Redistribute the default route to the peer BGP table. Defaults to `False`.
    originated : bool
        Redistribute originated routes to the peer BGP table. Defaults to `False`.
    kernel : bool
        Redistribute kernel routes to the peer BGP table. Defaults to `False`.
    static : bool
        Redistribute static routes to the peer BGP table. Defaults to `False`.
    bgp: bool
        Redistribute all BGP routes to the peer BGP table. Defaults to `False`.
    bgp_own: bool
        Redistribute our own originated BGP routes to the peer BGP table. Defaults to `False`.
    bgp_customer: bool
        Redistribute customer BGP routes to the peer BGP table. Defaults to `False`.
    bgp_peering: bool
        Redistribute peering BGP routes to the peer BGP table. Defaults to `False`.
    bgp_transit: bool
        Redistribute transit BGP routes to the peer BGP table. Defaults to `False`.

    """

    connected: bool
    default: bool
    kernel: bool
    originated: bool
    static: bool
    bgp: bool
    bgp_own: bool
    bgp_customer: bool
    bgp_peering: bool
    bgp_transit: bool

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
    location : BGPPeerLocation
        Peer location.
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
    large_communities: BGPPeerLargeCommunities
        Incoming and outgoing large communities.
    prepend:
        AS-PATH prepending.
    passive : bool
        Indicate if this is a passive peer or not.
    quarantined : bool
        Set if the peer is quarantined.
    prefix_limit4 : BGPPeerPrefixLimit
        Prefix limit for IPv4.
    prefix_limit6 : BGPPeerPrefixLimit
        Prefix limit for IPv6.
    replace_aspath : Optional[int]
        ASN to substitute in the AS-PATH.
    route_policy_accept : BGPPeerRoutePolicyAccept
        Route policy for acceptance of routes from BGP peers into our main BGP table.
    route_policy_redistribute : BGPPeerRoutePolicyRedistribute
        Route policy for redistribution of routes to the BGP peer.
    filter: BGPPeerFilter
        BGP peer filtering options.
    peeringdb: Optional[BGPPeerPeeringDB]
        BGP peer peeringdb entry.
    blackhole_maxlen4 : Optional[int]
        Blackhole maximum length for IPv4.
    blackhole_minlen4 : Optional[int]
        Blackhole minimum length for IPv4.
    blackhole_maxlen6 : Optional[int]
        Blackhole maximum length for IPv6.
    blackhole_minlen6 : Optional[int]
        Blackhole minimum length for IPv6.
    prefix_import_maxlen4 : Optional[int]
        Prefix import maximum length for IPv4.
    prefix_import_minlen4 : Optional[int]
        Prefix import minimum length for IPv4.
    prefix_export_maxlen4 : Optional[int]
        Prefix export maximum length for IPv4.
    prefix_export_minlen4 : Optional[int]
        Prefix export minimum length for IPv4.
    prefix_import_maxlen6 : Optional[int]
        Prefix import maximum length for IPv6.
    prefix_import_minlen6 : Optional[int]
        Prefix import minimum length for IPv6.
    prefix_export_maxlen6 : Optional[int]
        Prefix export maximum length for IPv6.
    prefix_export_minlen6 : Optional[int]
        Prefix export minimum length for IPv6.
    aspath_import_maxlen : Optional[int]
        AS-PATH maximum length.
    aspath_import_minlen : Optional[int]
        AS-PATH minimum length.
    community_maxlen : Optional[int]
        Community maximum length.
    extended_community_maxlen : Optional[int]
        Extended community maximum length.
    large_community_maxlen : Optional[int]
        Large community maximum length.

    """

    _name: Optional[str]
    _description: Optional[str]
    location: BGPPeerLocation

    _peer_type: Optional[str]
    _asn: Optional[int]

    neighbor4: Optional[str]
    neighbor6: Optional[str]
    source_address4: Optional[str]
    source_address6: Optional[str]

    connect_delay_time: Optional[str]
    connect_retry_time: Optional[str]
    error_wait_time: Optional[str]
    multihop: Optional[str]
    password: Optional[str]

    cost: int

    graceful_shutdown: bool

    large_communities: BGPPeerLargeCommunities

    prepend: BGPPeerPrepend

    # Default to disabling passive mode
    passive: bool

    quarantined: bool

    prefix_limit4: BGPPeerPrefixLimit
    prefix_limit6: BGPPeerPrefixLimit

    replace_aspath: bool

    route_policy_accept: BGPPeerRoutePolicyAccept
    route_policy_redistribute: BGPPeerRoutePolicyRedistribute

    filter_policy: BGPPeerFilterPolicy

    _peeringdb: Optional[BGPPeerPeeringDB]

    blackhole_maxlen4: Optional[int]
    blackhole_minlen4: Optional[int]

    blackhole_maxlen6: Optional[int]
    blackhole_minlen6: Optional[int]

    prefix_import_maxlen4: Optional[int]
    prefix_import_minlen4: Optional[int]

    prefix_export_maxlen4: Optional[int]
    prefix_export_minlen4: Optional[int]

    prefix_import_maxlen6: Optional[int]
    prefix_import_minlen6: Optional[int]

    prefix_export_maxlen6: Optional[int]
    prefix_export_minlen6: Optional[int]

    aspath_import_maxlen: Optional[int]
    aspath_import_minlen: Optional[int]

    community_import_maxlen: Optional[int]
    extended_community_import_maxlen: Optional[int]
    large_community_import_maxlen: Optional[int]

    def __init__(self) -> None:
        """Initialize object."""

        self._name = None
        self._description = None
        self.location = BGPPeerLocation()

        self._peer_type = None
        self._asn = None

        self.neighbor4 = None
        self.neighbor6 = None
        self.source_address4 = None
        self.source_address6 = None

        self.connect_delay_time = None
        self.connect_retry_time = None
        self.error_wait_time = None
        self.multihop = None
        self.password = None

        self.cost = 0

        self.graceful_shutdown = False

        self.large_communities = BGPPeerLargeCommunities()

        self.prepend = BGPPeerPrepend()

        # Default to disabling passive mode
        self.passive = False

        self.quarantined = False

        self.prefix_limit4 = None
        self.prefix_limit6 = None

        self.replace_aspath = False

        # Route policies
        self.route_policy_accept = BGPPeerRoutePolicyAccept()
        self.route_policy_redistribute = BGPPeerRoutePolicyRedistribute()

        self.filter_policy = BGPPeerFilterPolicy()

        self._peeringdb = None

        self.blackhole_maxlen4 = None
        self.blackhole_minlen4 = None

        self.blackhole_maxlen6 = None
        self.blackhole_minlen6 = None

        self.prefix_import_maxlen4 = None
        self.prefix_import_minlen4 = None

        self.prefix_export_maxlen4 = None
        self.prefix_export_minlen4 = None

        self.prefix_import_maxlen6 = None
        self.prefix_import_minlen6 = None

        self.prefix_export_maxlen6 = None
        self.prefix_export_minlen6 = None

        self.aspath_import_maxlen = None
        self.aspath_import_minlen = None

        self.community_import_maxlen = None
        self.extended_community_import_maxlen = None
        self.large_community_import_maxlen = None

    @property
    def peeringdb(self) -> BGPPeerPeeringDB:
        """Return our peeringdb entry, if there is one."""
        # We cannot do lookups on private ASN's
        if (self.asn >= 64512 and self.asn <= 65534) or (self.asn >= 4200000000 and self.asn <= 4294967294):
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
