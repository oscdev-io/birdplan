#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2024, AllWorldIT
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

import enum
from typing import Dict, List, Optional, Union

from .actions import BGPPeerActions

from ......exceptions import BirdPlanError

__all__ = [
    "BGPPeerLargeCommunitiesOutgoing",
    "BGPPeerLargeCommunities",
    "BGPPeerPrependItem",
    "BGPPeerPrepend",
    "BGPPeerRoutePolicyAccept",
    "BGPPeerImportFilterPolicy",
    "BGPPeerLocation",
    "BGPPeerRoutePolicyRedistribute",
    "BGPPeerConstraints",
    "BGPPeerAttributes",
]

# This type is a string as we can have it set to "peeringdb"
BGPPeerPrefixLimit = Optional[str]

BGPPeerFilterItem = Union[str, List[str]]
BGPPeerFilter = Dict[str, BGPPeerFilterItem]


# Define BGP prefix limit action enum
class BGPPeerImportPrefixLimitAction(enum.Enum):
    """BGP peer import prefix limit action."""

    RESTART = "restart"
    DISABLE = "disable"


class BGPPeerCommunitiesOutgoing:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer outgoing communities.

    Attributes
    ----------
    connected: List[str]
        Connected route outgoing communities.
    kernel: List[str]
        Kernel route outgoing communities.
    kernel_blackhole: List[str]
        Kernel blackhole route outgoing communities.
    kernel_default: List[str]
        Kernel default route outgoing communities.
    originated: List[str]
        Originated route outgoing communities.
    originated_default: List[str]
        Originated default route outgoing communities.
    static: List[str]
        Static route outgoing communities.
    static_blackhole: List[str]
        Static blackhole route outgoing communities.
    static_default: List[str]
        Static default route outgoing communities.
    bgp_own: List[str]
        BGP own route outgoing communities.
    bgp_own_blackhole: List[str]
        BGP own blackhole route outgoing communities.
    bgp_own_default: List[str]
        BGP own default route outgoing communities.
    bgp_customer: List[str]
        BGP customer route outgoing communities.
    bgp_customer_blackhole: List[str]
        BGP customer blackhole route outgoing communities.
    bgp_peering: List[str]
        BGP peering route outgoing communities.
    bgp_transit: List[str]
        BGP transit route outgoing communities.
    bgp_transit_default: List[str]
        BGP transit default route outgoing communities.

    """

    connected: List[str]
    kernel: List[str]
    kernel_blackhole: List[str]
    kernel_default: List[str]
    originated: List[str]
    originated_default: List[str]
    static: List[str]
    static_blackhole: List[str]
    static_default: List[str]
    bgp: List[str]
    bgp_own: List[str]
    bgp_own_blackhole: List[str]
    bgp_own_default: List[str]
    bgp_customer: List[str]
    bgp_customer_blackhole: List[str]
    bgp_peering: List[str]
    bgp_transit: List[str]
    bgp_transit_default: List[str]

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = []
        self.kernel = []
        self.kernel_blackhole = []
        self.kernel_default = []
        self.originated = []
        self.originated_default = []
        self.static = []
        self.static_blackhole = []
        self.static_default = []
        self.bgp_own = []
        self.bgp_own_blackhole = []
        self.bgp_own_default = []
        self.bgp_customer = []
        self.bgp_customer_blackhole = []
        self.bgp_peering = []
        self.bgp_transit = []
        self.bgp_transit_default = []


class BGPPeerCommunities:  # pylint: disable=too-few-public-methods
    """
    BGP peer communities.

    Attributes
    ----------
    incoming : List[str]
        List of communities to add to incoming prefixes.
    outgoing : BGPPeerCommunitiesOutgoing
        List of communities to add to outgoing prefixes.

    """

    incoming: List[str]

    outgoing: BGPPeerCommunitiesOutgoing

    def __init__(self) -> None:
        """Initialize object."""
        self.incoming = []
        self.outgoing = BGPPeerCommunitiesOutgoing()


class BGPPeerLargeCommunitiesOutgoing:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer outgoing large communities.

    Attributes
    ----------
    connected: List[str]
        Connected route outgoing large communities.
    kernel: List[str]
        Kernel route outgoing large communities.
    kernel_blackhole: List[str]
        Kernel blackhole route outgoing large communities.
    kernel_default: List[str]
        Kernel default route outgoing large communities.
    originated: List[str]
        Originated route outgoing large communities.
    originated_default: List[str]
        Originated default route outgoing large communities.
    static: List[str]
        Static route outgoing large communities.
    static_blackhole: List[str]
        Static blackhole route outgoing large communities.
    static_default: List[str]
        Static default route outgoing large communities.
    bgp_own: List[str]
        BGP own route outgoing large communities.
    bgp_own_blackhole: List[str]
        BGP own blackhole route outgoing large communities.
    bgp_own_default: List[str]
        BGP own default route outgoing large communities.
    bgp_customer: List[str]
        BGP customer route outgoing large communities.
    bgp_customer_blackhole: List[str]
        BGP customer blackhole route outgoing large communities.
    bgp_peering: List[str]
        BGP peering route outgoing large communities.
    bgp_transit: List[str]
        BGP transit route outgoing large communities.
    bgp_transit_default: List[str]
        BGP transit default route outgoing large communities.

    """

    connected: List[str]
    kernel: List[str]
    kernel_blackhole: List[str]
    kernel_default: List[str]
    originated: List[str]
    originated_default: List[str]
    static: List[str]
    static_blackhole: List[str]
    static_default: List[str]
    bgp: List[str]
    bgp_own: List[str]
    bgp_own_blackhole: List[str]
    bgp_own_default: List[str]
    bgp_customer: List[str]
    bgp_customer_blackhole: List[str]
    bgp_peering: List[str]
    bgp_transit: List[str]
    bgp_transit_default: List[str]

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = []
        self.kernel = []
        self.kernel_blackhole = []
        self.kernel_default = []
        self.originated = []
        self.originated_default = []
        self.static = []
        self.static_blackhole = []
        self.static_default = []
        self.bgp_own = []
        self.bgp_own_blackhole = []
        self.bgp_own_default = []
        self.bgp_customer = []
        self.bgp_customer_blackhole = []
        self.bgp_peering = []
        self.bgp_transit = []
        self.bgp_transit_default = []


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
    kernel: BGPPeerPrependItem
        Kernel route prepending options.
    kernel_blackhole: BGPPeerPrependItem
        Kernel blackhole route prepending options.
    kernel_default: BGPPeerPrependItem
        Kernel default route prepending options.
    originated: BGPPeerPrependItem
        Originated route prepending options.
    originated_default: BGPPeerPrependItem
        Originated default route prepending options.
    static: BGPPeerPrependItem
        Static route prepending options.
    static_blackhole: BGPPeerPrependItem
        Static blackhole route prepending options.
    static_default: BGPPeerPrependItem
        Static default route prepending options.
    bgp_own: BGPPeerPrependItem
        BGP own route prepending options.
    bgp_own_blackhole: BGPPeerPrependItem
        BGP own blackhole route prepending options.
    bgp_own_default: BGPPeerPrependItem
        BGP own default route prepending options.
    bgp_customer: BGPPeerPrependItem
        BGP customer route prepending options.
    bgp_customer_blackhole: BGPPeerPrependItem
        BGP customer blackhole route prepending options.
    bgp_peering: BGPPeerPrependItem
        BGP peering route prepending options.
    bgp_transit: BGPPeerPrependItem
        BGP transit route prepending options.
    bgp_transit_default: BGPPeerPrependItem
        BGP transit default route prepending options.

    """

    connected: BGPPeerPrependItem
    kernel: BGPPeerPrependItem
    kernel_blackhole: BGPPeerPrependItem
    kernel_default: BGPPeerPrependItem
    originated: BGPPeerPrependItem
    originated_default: BGPPeerPrependItem
    static: BGPPeerPrependItem
    static_blackhole: BGPPeerPrependItem
    static_default: BGPPeerPrependItem
    bgp_own: BGPPeerPrependItem
    bgp_own_blackhole: BGPPeerPrependItem
    bgp_own_default: BGPPeerPrependItem
    bgp_customer: BGPPeerPrependItem
    bgp_customer_blackhole: BGPPeerPrependItem
    bgp_peering: BGPPeerPrependItem
    bgp_transit: BGPPeerPrependItem
    bgp_transit_default: BGPPeerPrependItem

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = BGPPeerPrependItem()
        self.kernel = BGPPeerPrependItem()
        self.kernel_blackhole = BGPPeerPrependItem()
        self.kernel_default = BGPPeerPrependItem()
        self.originated = BGPPeerPrependItem()
        self.originated_default = BGPPeerPrependItem()
        self.static = BGPPeerPrependItem()
        self.static_blackhole = BGPPeerPrependItem()
        self.static_default = BGPPeerPrependItem()
        self.bgp_own = BGPPeerPrependItem()
        self.bgp_own_blackhole = BGPPeerPrependItem()
        self.bgp_own_default = BGPPeerPrependItem()
        self.bgp_customer = BGPPeerPrependItem()
        self.bgp_customer_blackhole = BGPPeerPrependItem()
        self.bgp_peering = BGPPeerPrependItem()
        self.bgp_transit = BGPPeerPrependItem()
        self.bgp_transit_default = BGPPeerPrependItem()


class BGPPeerRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for acceptance of routes from BGP peers into the main BGP table.

    Attributes
    ----------
    bgp_customer_blackhole : bool
        Allow accepting a blackhole route from a customer.
    bgp_own_blackhole : bool
        Allow accepting a blackhole route that originated from our own federation.
    bgp_own_default : bool
        Allow accepting a default route that originated from our own federation.
    bgp_transit_default : bool
        Allow accepting a default route that originated from a transit peer.

    """

    bgp_customer_blackhole: bool
    bgp_own_blackhole: bool
    bgp_own_default: bool
    bgp_transit_default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.bgp_customer_blackhole = False
        self.bgp_own_blackhole = False
        self.bgp_own_default = False
        self.bgp_transit_default = False


class BGPPeerImportFilterDenyPolicy:  # pylint: disable=too-few-public-methods
    """
    BGP filter deny policy for incoming routes from the BGP peer.

    Attributes
    ----------
    aspath_asns : BGPPeerFilterItem
        List of ASNs to filter in the AS-PATH.
    origin_asns : BGPPeerFilterItem
        List of origin ASNs to filter on.
    prefixes : BGPPeerFilterItem
        List of prefixes to filter on.


    """

    aspath_asns: BGPPeerFilterItem
    origin_asns: BGPPeerFilterItem
    prefixes: BGPPeerFilterItem

    def __init__(self) -> None:
        """Initialize object."""
        self.aspath_asns = []
        self.origin_asns = []
        self.prefixes = []


class BGPPeerImportFilterPolicy:  # pylint: disable=too-few-public-methods
    """
    BGP filter policy for incoming routes from the BGP peer.

    Attributes
    ----------
    as_sets : BGPPeerFilterItem
        List of AS-SET's to filter on.
    aspath_asns : BGPPeerFilterItem
        List of ASNs to filter in the AS-PATH.
    origin_asns : BGPPeerFilterItem
        List of origin ASNs to filter on.
    peer_asns : BGPPeerFilterItem
        List of peer ASNs to filter on.
    prefixes : BGPPeerFilterItem
        List of prefixes to filter on.
    origin_asns_irr : List[str]
        INTERNAL ONLY. These ASNs are resolved from the `as_sets` attribute.
    prefixes_irr : List[str]
        INTERNAL ONLY. These prefixes are resolved from the `as_sets` attribute.

    """

    as_sets: BGPPeerFilterItem
    aspath_asns: BGPPeerFilterItem
    origin_asns: BGPPeerFilterItem
    peer_asns: BGPPeerFilterItem
    prefixes: BGPPeerFilterItem
    origin_asns_irr: List[str]
    prefixes_irr: List[str]

    def __init__(self) -> None:
        """Initialize object."""
        self.as_sets = []
        self.aspath_asns = []
        self.origin_asns = []
        self.peer_asns = []
        self.prefixes = []
        # INTERNAL attributes, these are populated during initialization
        self.origin_asns_irr = []
        self.prefixes_irr = []


class BGPPeerExportFilterPolicy:  # pylint: disable=too-few-public-methods
    """
    BGP filter policy for outgoing routes to the BGP peer.

    Attributes
    ----------
    origin_asns : BGPPeerFilterItem
        List of origin ASNs to filter on.
    prefixes : BGPPeerFilterItem
        List of prefixes to filter on.
    """

    origin_asns: BGPPeerFilterItem
    prefixes: BGPPeerFilterItem

    def __init__(self) -> None:
        """Initialize object."""
        self.origin_asns = []
        self.prefixes = []


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
    kernel : bool
        Redistribute kernel routes to the peer BGP table. Defaults to `False`.
    kernel_blackhole : bool
        Redistribute kernel blackhole routes to the peer BGP table. Defaults to `False`.
    kernel_default : bool
        Redistribute kernel default routes to the peer BGP table. Defaults to `False`.
    originated : bool
        Redistribute originated routes to the peer BGP table. Defaults to `False`.
    originated_default : bool
        Redistribute originated default routes to the peer BGP table. Defaults to `False`.
    static : bool
        Redistribute static routes to the peer BGP table. Defaults to `False`.
    static_blackhole : bool
        Redistribute static blackhole routes to the peer BGP table. Defaults to `False`.
    static_default : bool
        Redistribute static default routes to the peer BGP table. Defaults to `False`.
    bgp_own: bool
        Redistribute our own originated BGP routes to the peer BGP table. Defaults to `False`.
    bgp_customer : bool
        Redistribute customer BGP routes to the peer BGP table. Defaults to `False`.
    bgp_peering : bool
        Redistribute peering BGP routes to the peer BGP table. Defaults to `False`.
    bgp_transit : bool
        Redistribute transit BGP routes to the peer BGP table. Defaults to `False`.
    bgp_customer_blackhole : bool
        Redistribute customer blackhole BGP routes to the peer BGP table. Defaults to `False`.
    bgp_own_blackhole : bool
        Redistribute our own blackhole BGP routes to the peer BGP table. Defaults to `False`.
    bgp_own_default : bool
        Redistribute our own default BGP routes to the peer BGP table. Defaults to `False`.
    bgp_transit_default : bool
        Redistribute transit default BGP routes to the peer BGP table. Defaults to `False`.

    """

    connected: bool
    kernel: bool
    kernel_blackhole: bool
    kernel_default: bool
    originated: bool
    originated_default: bool
    static: bool
    static_blackhole: bool
    static_default: bool
    bgp_own: bool
    bgp_customer: bool
    bgp_peering: bool
    bgp_transit: bool
    bgp_customer_blackhole: bool
    bgp_own_blackhole: bool
    bgp_own_default: bool
    bgp_transit_default: bool

    def __init__(self) -> None:
        """Initialize object."""
        self.connected = False
        self.kernel = False
        self.kernel_blackhole = False
        self.kernel_default = False
        self.originated = False
        self.originated_default = False
        self.static = False
        self.static_blackhole = False
        self.static_default = False
        self.bgp_own = False
        self.bgp_customer = False
        self.bgp_peering = False
        self.bgp_transit = False
        self.bgp_customer_blackhole = False
        self.bgp_own_blackhole = False
        self.bgp_own_default = False
        self.bgp_transit_default = False


class BGPPeerConstraints:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    BGP peer prefix limits.

    Attributes
    ----------
    import_maxlen4 : Optional[int]
        Prefix import maximum length for IPv4.
    import_minlen4 : Optional[int]
        Prefix import minimum length for IPv4.
    export_maxlen4 : Optional[int]
        Prefix export maximum length for IPv4.
    export_minlen4 : Optional[int]
        Prefix export minimum length for IPv4.
    import_maxlen6 : Optional[int]
        Prefix import maximum length for IPv6.
    import_minlen6 : Optional[int]
        Prefix import minimum length for IPv6.
    export_maxlen6 : Optional[int]
        Prefix export maximum length for IPv6.
    export_minlen6 : Optional[int]
        Prefix export minimum length for IPv6.
    blackhole_import_maxlen4 : Optional[int]
        Blackhole maximum length for IPv4.
    blackhole_import_minlen4 : Optional[int]
        Blackhole minimum length for IPv4.
    blackhole_export_maxlen4 : Optional[int]
        Blackhole maximum length for IPv4.
    blackhole_export_minlen4 : Optional[int]
        Blackhole minimum length for IPv4.
    blackhole_import_maxlen6 : Optional[int]
        Blackhole maximum length for IPv6.
    blackhole_import_minlen6 : Optional[int]
        Blackhole minimum length for IPv6.
    blackhole_export_maxlen6 : Optional[int]
        Blackhole maximum length for IPv6.
    blackhole_export_minlen6 : Optional[int]
        Blackhole minimum length for IPv6.
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

    import_maxlen4: Optional[int]
    import_minlen4: Optional[int]

    export_maxlen4: Optional[int]
    export_minlen4: Optional[int]

    import_maxlen6: Optional[int]
    import_minlen6: Optional[int]

    export_maxlen6: Optional[int]
    export_minlen6: Optional[int]

    blackhole_import_maxlen4: Optional[int]
    blackhole_import_minlen4: Optional[int]

    blackhole_export_maxlen4: Optional[int]
    blackhole_export_minlen4: Optional[int]

    blackhole_import_maxlen6: Optional[int]
    blackhole_import_minlen6: Optional[int]

    blackhole_export_maxlen6: Optional[int]
    blackhole_export_minlen6: Optional[int]

    aspath_import_maxlen: Optional[int]
    aspath_import_minlen: Optional[int]

    community_import_maxlen: Optional[int]
    extended_community_import_maxlen: Optional[int]
    large_community_import_maxlen: Optional[int]

    def __init__(self) -> None:
        """Initialize object."""

        self.import_maxlen4 = None
        self.import_minlen4 = None

        self.export_maxlen4 = None
        self.export_minlen4 = None

        self.import_maxlen6 = None
        self.import_minlen6 = None

        self.export_maxlen6 = None
        self.export_minlen6 = None

        self.blackhole_import_maxlen4 = None
        self.blackhole_import_minlen4 = None

        self.blackhole_export_maxlen4 = None
        self.blackhole_export_minlen4 = None

        self.blackhole_import_maxlen6 = None
        self.blackhole_import_minlen6 = None

        self.blackhole_export_maxlen6 = None
        self.blackhole_export_minlen6 = None

        self.aspath_import_maxlen = None
        self.aspath_import_minlen = None

        self.community_import_maxlen = None
        self.extended_community_import_maxlen = None
        self.large_community_import_maxlen = None


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

    ttl_security: bool
        Indicate if BGP TTL security should be enabled.

    cost : int
        Cost of this peer, this is the number minused from the local_pref.

    graceful_shutdown : bool
        Set peer in GRACEFUL_SHUTDOWN mode.

    communities: BGPPeerCommunities
        Incoming and outgoing communities.

    large_communities: BGPPeerLargeCommunities
        Incoming and outgoing large communities.

    prepend:
        AS-PATH prepending.

    passive : bool
        Indicate if this is a passive peer or not.

    quarantine : bool
        Set if the peer is quarantined.

    prefix_limit_action : BGPPeerImportPrefixLimitAction
        Prefix limit action used when the import prefix count is exceeded.

    prefix_limit4 : BGPPeerPrefixLimit
        Prefix limit for IPv4.

    prefix_limit6 : BGPPeerPrefixLimit
        Prefix limit for IPv6.

    prefix_limit4_peeringdb : BGPPeerPrefixLimit
        Prefix limit for IPv4.

    prefix_limit6_peeringdb : BGPPeerPrefixLimit
        Prefix limit for IPv6.

    replace_aspath : Optional[int]
        ASN to substitute in the AS-PATH.

    route_policy_accept : BGPPeerRoutePolicyAccept
        Route policy for acceptance of routes from BGP peers into our main BGP table.

    route_policy_redistribute : BGPPeerRoutePolicyRedistribute
        Route policy for redistribution of routes to the BGP peer.

    import_filter_policy: BGPPeerImportFilterPolicy
        BGP peer import filter policy.

    import_filter_deny_policy: BGPPeerImportFilterDenyPolicy
        BGP peer import filter deny policy.

    export_filter_policy: BGPPeerExportFilterPolicy
        BGP peer export filter policy.

    blackhole_community: Optional[Union[List[str], bool]]
        Blackhole community to use for blackhole routes.

    constraints: BGPPeerConstraints
        BGP peer constraint overrides.

    use_rpki: bool
        Use RPKI validation for this peer.

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
    ttl_security: bool

    cost: int

    add_paths: Optional[str]

    graceful_shutdown: bool

    communities: BGPPeerCommunities
    large_communities: BGPPeerLargeCommunities

    prepend: BGPPeerPrepend

    # Default to disabling passive mode
    passive: bool

    quarantine: bool

    prefix_limit_action: BGPPeerImportPrefixLimitAction

    prefix_limit4: BGPPeerPrefixLimit
    prefix_limit6: BGPPeerPrefixLimit

    prefix_limit4_peeringdb: BGPPeerPrefixLimit
    prefix_limit6_peeringdb: BGPPeerPrefixLimit

    replace_aspath: bool

    route_policy_accept: BGPPeerRoutePolicyAccept
    route_policy_redistribute: BGPPeerRoutePolicyRedistribute

    import_filter_policy: BGPPeerImportFilterPolicy
    import_filter_deny_policy: BGPPeerImportFilterDenyPolicy
    export_filter_policy: BGPPeerExportFilterPolicy

    blackhole_community: Optional[Union[List[str], bool]]

    constraints: BGPPeerConstraints

    actions: Optional[BGPPeerActions]

    use_rpki: bool

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
        self.ttl_security = False

        self.cost = 0

        self.add_paths = None

        self.graceful_shutdown = False

        self.communities = BGPPeerCommunities()
        self.large_communities = BGPPeerLargeCommunities()

        self.prepend = BGPPeerPrepend()

        # Default to disabling passive mode
        self.passive = False

        self.quarantine = False

        self.prefix_limit_action = BGPPeerImportPrefixLimitAction.RESTART

        self.prefix_limit4 = None
        self.prefix_limit6 = None

        self.prefix_limit4_peeringdb = None
        self.prefix_limit6_peeringdb = None

        self.replace_aspath = False

        # Route policies
        self.route_policy_accept = BGPPeerRoutePolicyAccept()
        self.route_policy_redistribute = BGPPeerRoutePolicyRedistribute()

        self.import_filter_policy = BGPPeerImportFilterPolicy()
        self.import_filter_deny_policy = BGPPeerImportFilterDenyPolicy()
        self.export_filter_policy = BGPPeerExportFilterPolicy()

        self.blackhole_community = None

        self.constraints = BGPPeerConstraints()

        self.actions = None

        self.use_rpki = False

    @property
    def name(self) -> str:
        """Return our name."""
        if self._name is None:
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
