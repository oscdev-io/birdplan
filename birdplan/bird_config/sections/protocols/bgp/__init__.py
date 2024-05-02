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

"""BIRD BGP protocol configuration."""

# pylint: disable=too-many-lines

from typing import Dict, List, Optional

from .....exceptions import BirdPlanError
from ....globals import BirdConfigGlobals
from ...bird_attributes import SectionBirdAttributes
from ...constants import SectionConstants
from ...functions import SectionFunctions
from ...tables import SectionTables
from ..base import SectionProtocolBase
from ..direct import ProtocolDirect
from ..pipe import ProtocolPipe, ProtocolPipeFilterType
from ..rpki import ProtocolRPKI, RPKISource
from .bgp_attributes import BGPAttributes, BGPPeertypeConstraints, BGPRoutePolicyAccept, BGPRoutePolicyImport
from .bgp_functions import BGPFunctions
from .bgp_types import BGPPeerConfig
from .peer import ProtocolBGPPeer

__all__ = ["ProtocolBGP"]


BGPPeersConfig = Dict[str, BGPPeerConfig]
BGPPeers = Dict[str, ProtocolBGPPeer]
BGPOriginatedRoutes = Dict[str, str]


class ProtocolBGP(SectionProtocolBase):  # pylint: disable=too-many-public-methods
    """BIRD BGP protocol configuration."""

    # BGP protocol attributes
    _bgp_attributes: BGPAttributes
    # BGP functions
    _bgp_functions: BGPFunctions

    # BGP peers
    _peers: BGPPeers

    # Internal config before configuration happens
    _originated_routes: BGPOriginatedRoutes

    def __init__(
        self,
        birdconfig_globals: BirdConfigGlobals,
        birdattributes: SectionBirdAttributes,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals, birdattributes, constants, functions, tables)

        # Set section name
        self._section = "BGP Protocol"

        # BGP peers
        self._peers = {}

        # Routes originated from BGP
        self._originated_routes = {}

        # Setup BGP attributes
        self._bgp_attributes = BGPAttributes()
        # Setup BGP functions
        self._bgp_functions = BGPFunctions(self.birdconfig_globals, self.functions)

    def configure(self) -> None:
        """Configure the BGP protocol."""
        super().configure()

        # Blank the BGP peer state
        if "bgp" not in self.birdconfig_globals.state:
            self.birdconfig_globals.state["bgp"] = {}
        self.birdconfig_globals.state["bgp"]["peers"] = {}

        self._configure_constants_bgp()

        self._configure_birdattributes_bgp()

        self.functions.conf.append(self.bgp_functions, deferred=True)

        self.tables.conf.append("# BGP Tables")
        self.tables.conf.append("ipv4 table t_bgp4;")
        self.tables.conf.append("ipv6 table t_bgp6;")
        self.tables.conf.append("")

        # Check if we're adding RPKI ROA tables
        if self.rpki_source:
            # Configure RPKI protocol
            rpki_protocol = ProtocolRPKI(self.birdconfig_globals, self.tables, self.rpki_source)
            self.conf.add(rpki_protocol)

        # Setup BGP origination
        self._configure_originated_routes()

        # BGP to master export filters
        self._setup_bgp_to_master_export_filter()

        # BGP to master import filters
        self._setup_bgp_to_master_import_filter()

        # Configure pipe from BGP to the master routing table
        bgp_master_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from="bgp",
            table_to="master",
            export_filter_type=ProtocolPipeFilterType.UNVERSIONED,
            import_filter_type=ProtocolPipeFilterType.UNVERSIONED,
        )
        self.conf.add(bgp_master_pipe)

        # Check if we're importing connected routes, if we are, create the protocol and pipe
        if self.route_policy_import.connected:
            # Create an interface list to feed to our routing table
            interfaces: List[str] = []
            if isinstance(self.route_policy_import.connected, list):
                interfaces = self.route_policy_import.connected
            # Add direct protocol for redistribution of connected routes
            bgp_direct_protocol = ProtocolDirect(
                self.birdconfig_globals,
                self.birdattributes,
                self.constants,
                self.functions,
                self.tables,
                name="bgp",
                interfaces=interfaces,
            )
            self.conf.add(bgp_direct_protocol)
            # Add pipe
            self._setup_bgp_to_direct_import_filter()
            bgp_direct_pipe = ProtocolPipe(
                self.birdconfig_globals,
                name="bgp",
                table_from="bgp",
                table_to="direct",
                table_export="none",
                import_filter_type=ProtocolPipeFilterType.UNVERSIONED,
            )
            self.conf.add(bgp_direct_pipe)

        # Loop with BGP peers and configure them
        self.conf.add("")
        for _, peer in self.peers.items():
            self.conf.add(peer)

    def add_originated_route(self, route: str) -> None:
        """Add originated route."""
        (prefix, route_info) = route.split(" ", 1)
        self.originated_routes[prefix] = route_info

    def add_peer(self, peer_name: str, peer_config: BGPPeerConfig) -> None:
        """Add peer to BGP."""

        if peer_name in self.peers:
            raise BirdPlanError(f"BGP peer '{peer_name}' already exists")

        # Create BGP peer object
        peer = ProtocolBGPPeer(
            self.birdconfig_globals,
            self.birdattributes,
            self.constants,
            self.functions,
            self.tables,
            self.bgp_attributes,
            self.bgp_functions,
            peer_name,
            peer_config,
        )

        # Add peer to our configured peer list
        self.peers[peer_name] = peer

    def peer(self, name: str) -> ProtocolBGPPeer:
        """Return a BGP peer configuration object."""
        if name not in self.peers:
            raise BirdPlanError(f"Peer '{name}' not found")
        return self.peers[name]

    def constraints(self, peer_type: str) -> BGPPeertypeConstraints:
        """Return the prefix limits for a specific peer type."""
        if peer_type not in self.bgp_attributes.peertype_constraints:
            raise BirdPlanError(f"Peer type '{peer_type}' has no implemented global prefix limits")
        return self.bgp_attributes.peertype_constraints[peer_type]

    def _configure_birdattributes_bgp(self) -> None:  # noqa: CFQ001 # pylint: disable=too-many-statements
        """Configure BGP attributes."""
        # NK: No attributes for now
        # self.birdattributes.conf.append_title("BGP Attributes")

    def _configure_constants_bgp(self) -> None:  # noqa: CFQ001 # pylint: disable=too-many-statements
        """Configure BGP constants."""
        self.constants.conf.append_title("BGP Constants")

        self.constants.conf.append("# Our BGP ASN")
        self.constants.conf.append(f"define BGP_ASN = {self.asn};")
        self.constants.conf.append("")

        self.constants.conf.append("# Ref http://bgpfilterguide.nlnog.net/guides/bogon_asns/")
        self.constants.conf.append("define BOGON_ASNS = [")
        self.constants.conf.append("  0, # RFC 7607")
        self.constants.conf.append("  23456, # RFC 4893 AS_TRANS")
        self.constants.conf.append("  64496..64511, # RFC 5398 and documentation/example ASNs")
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: 64512..65534, # RFC 6996 Private ASNs")
        else:
            self.constants.conf.append("  64512..65534, # RFC 6996 Private ASNs")
        self.constants.conf.append("  65535, # RFC 7300 Last 16 bit ASN")
        self.constants.conf.append("  65536..65551, # RFC 5398 and documentation/example ASNs")
        self.constants.conf.append("  65552..131071, # RFC IANA reserved ASNs")
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: 4200000000..4294967294, # RFC 6996 Private ASNs")
            self.constants.conf.append("  4200000000..4294900000, # RFC 6996 Private ASNs - ADJUSTED FOR TESTING")
        else:
            self.constants.conf.append("  4200000000..4294967294, # RFC 6996 Private ASNs")
        self.constants.conf.append("  4294967295 # RFC 7300 Last 32 bit ASN")
        self.constants.conf.append("];")
        self.constants.conf.append("")

        self.constants.conf.append("define PRIVATE_ASNS = [")
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: 64512..65534, # RFC 6996 Private ASNs")
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: 4200000000..4294967294, # RFC 6996 Private ASNs")
            self.constants.conf.append("  4200000000..4294900000 # RFC 6996 Private ASNs - ADJUSTED FOR TESTING")
        else:
            self.constants.conf.append("  64512..65534, # RFC 6996 Private ASNs")
            self.constants.conf.append("  4200000000..4294967294 # RFC 6996 Private ASNs")
        self.constants.conf.append("];")
        self.constants.conf.append("")

        self.constants.conf.append("# Ref http://bgpfilterguide.nlnog.net/guides/no_transit_leaks")
        self.constants.conf.append("define BGP_ASNS_TRANSIT = [")
        self.constants.conf.append("  174, # Cogent")
        self.constants.conf.append("  209, # Qwest (HE carries this on IXPs IPv6 (Jul 12 2018))")
        self.constants.conf.append("  701, # UUNET")
        self.constants.conf.append("  702, # UUNET")
        self.constants.conf.append("  1239, # Sprint")
        self.constants.conf.append("  1299, # Telia")
        self.constants.conf.append("  2914, # NTT Communications")
        self.constants.conf.append("  3257, # GTT Backbone")
        self.constants.conf.append("  3320, # Deutsche Telekom AG (DTAG)")
        self.constants.conf.append("  3356, # Level3")
        self.constants.conf.append("  3491, # PCCW")
        self.constants.conf.append("  3549, # Level3")
        self.constants.conf.append("  3561, # Savvis / CenturyLink")
        self.constants.conf.append("  4134, # Chinanet")
        self.constants.conf.append("  5511, # Chinanet")
        self.constants.conf.append("  5511, # Orange opentransit")
        self.constants.conf.append("  6453, # Tata Communications")
        self.constants.conf.append("  6461, # Zayo Bandwidth")
        self.constants.conf.append("  6762, # Seabone / Telecom Italia")
        self.constants.conf.append("  6830, # Liberty Global")
        self.constants.conf.append("  7018 # AT&T")
        self.constants.conf.append("];")
        self.constants.conf.append("")

        # NK: IMPORTANT IF THE ABOVE CHANGES UPDATE THE BELOW
        self.constants.conf.append("# Community stripping")
        self.constants.conf.append("define BGP_COMMUNITY_STRIP = [ ")
        self.constants.conf.append("  (23456, *),")
        self.constants.conf.append("  (64496..64511, *)")  # Documentation
        self.constants.conf.append("];")

        # This is used for stripping large communities from customers mostly
        self.constants.conf.append("define BGP_LC_STRIP = [ ")
        self.constants.conf.append("  (23456, *, *),")
        self.constants.conf.append("  (64496..64511, *, *),")  # Documentation
        self.constants.conf.append("  (65552..131071, *, *),")  # Reserved
        self.constants.conf.append("  (BGP_ASN, 1..3, *),")  # Strip route learned functions
        # Allow client traffic engineering: 4, 5, 6, 7, 8
        self.constants.conf.append("  (BGP_ASN, 9..60, *),")  # Strip unused
        self.constants.conf.append("  (BGP_ASN, 64..70, *),")  # Strip unused
        self.constants.conf.append("  (BGP_ASN, 74..665, *),")  # Strip unsed
        self.constants.conf.append("  (BGP_ASN, 667..4294967295, *),")  # Strip unsed + rest (incl. 1000 - info, 1101 - filter)
        # These functions should never be used on our own ASN
        self.constants.conf.append("  (BGP_ASN, 4, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 6, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 61, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 62, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 63, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 666, BGP_ASN)")
        self.constants.conf.append("];")

        # Strip communities mostly for peers and transit providers
        self.constants.conf.append("define BGP_COMMUNITY_STRIP_ALL = [")
        # This is first because of the , we need
        if self.asn and self.asn < 65535:
            self.constants.conf.append("  (BGP_ASN, *),")
        else:
            self.constants.conf.append("  # (BGP_ASN, *),  # Not stripping due to 4-byte ASN")
        self.constants.conf.append("  (23456, *),")
        self.constants.conf.append("  (64496..64511, *)")  # Documentation
        self.constants.conf.append("];")
        # This is used for stripping large communities from peers and transit providers
        self.constants.conf.append("define BGP_LC_STRIP_ALL = [")
        self.constants.conf.append("  (23456, *, *),")
        self.constants.conf.append("  (64496..64511, *, *),")  # Documentation
        self.constants.conf.append("  (65552..131071, *, *),")  # Reserved
        self.constants.conf.append("  (BGP_ASN, *, *)")
        self.constants.conf.append("];")

        # Stripping private communities
        self.constants.conf.append("define BGP_COMMUNITY_STRIP_PRIVATE = [")
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: (64512..65534, *)")  # Private
        else:
            self.constants.conf.append("  (64512..65534, *)")  # Private
        self.constants.conf.append("];")

        self.constants.conf.append("define BGP_LC_STRIP_PRIVATE = [")
        # Don't strip the lower private ASN range during testing
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: (64512..65534, *, *)")  # Private
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: (4200000000..4294967294, *, *)")
            self.constants.conf.append("  (4200000000..4294900000, *, *) # ADJUSTED FOR TESTING")
        else:
            self.constants.conf.append("  (64512..65534, *, *),")  # Private
            self.constants.conf.append("  (4200000000..4294967294, *, *)")
        self.constants.conf.append("];")

        self.constants.conf.append("# BGP Route Preferences")
        self.constants.conf.append("define BGP_PREF_OWN = 950;")  # -20 = Originate, -10 = static, -5 = kernel
        self.constants.conf.append("define BGP_PREF_CUSTOMER = 750;")
        self.constants.conf.append("define BGP_PREF_PEER = 470;")
        self.constants.conf.append("define BGP_PREF_ROUTESERVER = 450;")
        self.constants.conf.append("define BGP_PREF_TRANSIT = 150;")
        self.constants.conf.append("")

        self.constants.conf.append("# Well known communities")
        self.constants.conf.append("define BGP_COMMUNITY_GRACEFUL_SHUTDOWN = (65535, 0);")
        self.constants.conf.append("define BGP_COMMUNITY_BLACKHOLE = (65535, 666);")
        self.constants.conf.append("define BGP_COMMUNITY_NOEXPORT = (65535, 65281);")
        self.constants.conf.append("define BGP_COMMUNITY_NOADVERTISE = (65535, 65282);")
        self.constants.conf.append("")

        self.constants.conf.append("# Well known extended communities")
        self.constants.conf.append("define BGP_EXT_COMMUNITY_RPKI_VALID = (unknown 0x4300, 0, 0);")
        self.constants.conf.append("define BGP_EXT_COMMUNITY_RPKI_NOTFOUND = (unknown 0x4300, 0, 1);")
        self.constants.conf.append("define BGP_EXT_COMMUNITY_RPKI_INVALID = (unknown 0x4300, 0, 2);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community functions")
        # NK: IMPORTANT IF YOU CHANGE THE BELOW, UPDATE BGP_LC_STRIP
        self.constants.conf.append("define BGP_LC_FUNCTION_LOCATION_ISO3166 = 1;")
        self.constants.conf.append("define BGP_LC_FUNCTION_LOCATION_UNM49 = 2;")
        self.constants.conf.append("define BGP_LC_FUNCTION_RELATION = 3;")
        self.constants.conf.append("define BGP_LC_FUNCTION_NOEXPORT = 4;")
        self.constants.conf.append("define BGP_LC_FUNCTION_NOEXPORT_LOCATION = 5;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_ONE = 6;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_ONE_2 = 61;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_TWO = 62;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_THREE = 63;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_LOCATION_ONE = 7;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_LOCATION_ONE_2 = 71;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_LOCATION_TWO = 72;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_LOCATION_THREE = 73;")
        self.constants.conf.append("define BGP_LC_FUNCTION_LOCALPREF = 8;")
        self.constants.conf.append("define BGP_LC_FUNCTION_INFORMATION = 1000;")
        self.constants.conf.append("define BGP_LC_FUNCTION_FILTERED = 1101;")
        self.constants.conf.append("define BGP_LC_FUNCTION_ACTION = 1200;")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community noexport")
        self.constants.conf.append("define BGP_LC_EXPORT_NOTRANSIT = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65412);")
        self.constants.conf.append("define BGP_LC_EXPORT_NOPEER = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65413);")
        self.constants.conf.append("define BGP_LC_EXPORT_NOCUSTOMER = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65414);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community relations")
        self.constants.conf.append("define BGP_LC_RELATION = [(BGP_ASN, BGP_LC_FUNCTION_RELATION, 1..5)];")
        self.constants.conf.append("define BGP_LC_RELATION_OWN = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 1);")
        self.constants.conf.append("define BGP_LC_RELATION_CUSTOMER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 2);")
        self.constants.conf.append("define BGP_LC_RELATION_PEER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 3);")
        self.constants.conf.append("define BGP_LC_RELATION_TRANSIT = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 4);")
        self.constants.conf.append("define BGP_LC_RELATION_ROUTESERVER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 5);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large communities for LOCAL_PREF attribute manipulation")
        self.constants.conf.append("define BGP_LC_LOCALPREF_MINUS_ONE = (BGP_ASN, BGP_LC_FUNCTION_LOCALPREF, 1);")
        self.constants.conf.append("define BGP_LC_LOCALPREF_MINUS_TWO = (BGP_ASN, BGP_LC_FUNCTION_LOCALPREF, 2);")
        self.constants.conf.append("define BGP_LC_LOCALPREF_MINUS_THREE = (BGP_ASN, BGP_LC_FUNCTION_LOCALPREF, 3);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community information")
        self.constants.conf.append("define BGP_LC_INFORMATION_STRIPPED_COMMUNITY = (BGP_ASN, BGP_LC_FUNCTION_INFORMATION, 1);")
        self.constants.conf.append(
            "define BGP_LC_INFORMATION_STRIPPED_COMMUNITY_PRIVATE = (BGP_ASN, BGP_LC_FUNCTION_INFORMATION, 2);"
        )
        self.constants.conf.append("define BGP_LC_INFORMATION_STRIPPED_LC = (BGP_ASN, BGP_LC_FUNCTION_INFORMATION, 3);")
        self.constants.conf.append("define BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE = (BGP_ASN, BGP_LC_FUNCTION_INFORMATION, 4);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community filtered")
        self.constants.conf.append("define BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 1);")
        self.constants.conf.append("define BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 2);")
        self.constants.conf.append("define BGP_LC_FILTERED_BOGON = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 3);")
        self.constants.conf.append("define BGP_LC_FILTERED_BOGON_ASN = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 4);")
        self.constants.conf.append("define BGP_LC_FILTERED_ASPATH_TOO_LONG = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 5);")
        self.constants.conf.append("define BGP_LC_FILTERED_ASPATH_TOO_SHORT = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 6);")
        self.constants.conf.append("define BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 7);")
        self.constants.conf.append("define BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 8);")
        self.constants.conf.append("define BGP_LC_FILTERED_PREFIX_FILTERED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 9);")
        self.constants.conf.append("define BGP_LC_FILTERED_ORIGIN_AS = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 10);")
        # self.constants.conf.append('define BGP_LC_FILTERED_PREFIX_NOT_IN_ORIGIN_AS = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 11);')
        self.constants.conf.append("define BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 12);")
        self.constants.conf.append("define BGP_LC_FILTERED_RPKI_UNKNOWN = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 13);")
        self.constants.conf.append("define BGP_LC_FILTERED_RPKI_INVALID = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 14);")
        self.constants.conf.append("define BGP_LC_FILTERED_TRANSIT_FREE_ASN = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 15);")
        self.constants.conf.append("define BGP_LC_FILTERED_TOO_MANY_COMMUNITIES = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 16);")
        self.constants.conf.append("define BGP_LC_FILTERED_ROUTECOLLECTOR = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 17);")
        self.constants.conf.append("define BGP_LC_FILTERED_QUARANTINED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 18);")
        self.constants.conf.append(
            "define BGP_LC_FILTERED_TOO_MANY_EXTENDED_COMMUNITIES = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 19);"
        )
        self.constants.conf.append("define BGP_LC_FILTERED_TOO_MANY_LARGE_COMMUNITIES = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 20);")
        self.constants.conf.append("define BGP_LC_FILTERED_PEER_AS = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 21);")
        self.constants.conf.append("define BGP_LC_FILTERED_ASPATH_NOT_ALLOWED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 22);")
        self.constants.conf.append("define BGP_LC_FILTERED_NO_RELATION_LC = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 23);")
        self.constants.conf.append("define BGP_LC_FILTERED_BLACKHOLE_LEN_TOO_LONG = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 24);")
        self.constants.conf.append("define BGP_LC_FILTERED_BLACKHOLE_LEN_TOO_SHORT = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 25);")
        self.constants.conf.append("define BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 26);")
        self.constants.conf.append("define BGP_LC_FILTERED_DENY_ORIGIN_AS = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 27);")
        self.constants.conf.append("define BGP_LC_FILTERED_DENY_ASPATH = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 28);")
        self.constants.conf.append("define BGP_LC_FILTERED_DENY_PREFIX = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 29);")
        self.constants.conf.append("")
        self.constants.conf.append("# Large community actions")
        self.constants.conf.append("define BGP_LC_ACTION_REPLACE_ASPATH = (BGP_ASN, BGP_LC_FUNCTION_ACTION, 1);")
        self.constants.conf.append("define BGP_LC_ACTION_BLACKHOLE_ORIGINATE = (BGP_ASN, BGP_LC_FUNCTION_ACTION, 2);")
        self.constants.conf.append("")

    def _configure_originated_routes(self) -> None:
        # Work out static v4 and v6 routes
        routes: Dict[str, List[str]] = {"4": [], "6": []}
        for prefix in sorted(self.originated_routes.keys()):
            info = self.originated_routes[prefix]
            if "." in prefix:
                routes["4"].append(f"{prefix} {info}")
            elif ":" in prefix:
                routes["6"].append(f"{prefix} {info}")
            else:
                raise BirdPlanError(f"The BGP originate route '{prefix}' is odd")

        self.tables.conf.append("# BGP Origination Tables")

        filter_name = "f_bgp_originate_import"
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        self.conf.add("  # Origination import")
        self.conf.add(f"  {self.bgp_functions.import_own(20)};")
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

        # Loop with IPv4 and IPv6
        for ipv in ["4", "6"]:
            self.tables.conf.append(f"ipv{ipv} table t_bgp_originate{ipv};")

            self.conf.add(f"protocol static bgp_originate{ipv} {{")
            self.conf.add(f'  description "BGP route origination for IPv{ipv}";')
            self.conf.add("")
            self.conf.add(f"  vrf {self.birdconfig_globals.vrf};")
            self.conf.add("")
            self.conf.add(f"  ipv{ipv} {{")
            self.conf.add(f"    table t_bgp_originate{ipv};")
            self.conf.add("    export none;")
            self.conf.add(f"    import filter {filter_name};")
            self.conf.add("  };")
            # If we have IPv4 routes
            if routes[ipv]:
                self.conf.add("")
                # Output the routes
                for route in routes[ipv]:
                    self.conf.add(f"  route {route};")
            self.conf.add("};")
            self.conf.add("")

        self.tables.conf.append("")

        # Configure BGP origination route pipe to the bgp table
        originate_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from="bgp_originate",
            table_to="bgp",
            table_export="all",
            table_import="none",
        )
        self.conf.add(originate_pipe)

    def _setup_bgp_to_master_export_filter(self) -> None:
        """BGP main table to master export filters setup."""

        # Configure export filter to master
        filter_name = "f_bgp_master_export"
        self.conf.add("# Export filter FROM BGP table TO master table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Accept BGP routes into the master routing table
        self.conf.add(f"  {self.bgp_functions.accept_bgp()};")
        # Check if we accept customer blackhole routes, if not block it
        if self.route_policy_accept.bgp_customer_blackhole:
            self.conf.add(f"  {self.bgp_functions.accept_customer_blackhole()};")
        # Check if we accept our own blackhole routes, if not block it
        if self.route_policy_accept.bgp_own_blackhole:
            self.conf.add(f"  {self.bgp_functions.accept_own_blackhole()};")
        # Check if we accept default routes originated from within our federation, if not block it
        if self.route_policy_accept.bgp_own_default:
            self.conf.add(f"  {self.bgp_functions.accept_bgp_own_default()};")
        # Check if we accept default routes originated from transit peers, if not block it
        if self.route_policy_accept.bgp_transit_default:
            self.conf.add(f"  {self.bgp_functions.accept_bgp_transit_default()};")
        # Check if we accept originated routes, if not block it
        if self.route_policy_accept.originated:
            self.conf.add(f"  {self.bgp_functions.accept_originated()};")
        # Check if we accept originated routes, if not block it
        if self.route_policy_accept.originated_default:
            self.conf.add(f"  {self.bgp_functions.accept_originated_default()};")
        # Default to reject
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from t_bgp to master (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _setup_bgp_to_master_import_filter(self) -> None:
        """BGP main table to master import filters setup."""
        # Configure import filter to master
        filter_name = "f_bgp_master_import"
        self.conf.add("# Import filter FROM master table TO BGP table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # BGP importation of kernel routes
        if self.route_policy_import.kernel:
            self.conf.add(f"  {self.bgp_functions.import_kernel()};")
        # BGP importation of kernel blackhole routes
        if self.route_policy_import.kernel_blackhole:
            self.conf.add(f"  {self.bgp_functions.import_kernel_blackhole()};")
        # BGP importation of kernel default routes
        if self.route_policy_import.kernel_default:
            self.conf.add(f"  {self.bgp_functions.import_kernel_default()};")
        # BGP importation of static routes
        if self.route_policy_import.static:
            self.conf.add(f"  {self.bgp_functions.import_static()};")
        # BGP importation of static blackhole routes
        if self.route_policy_import.static_blackhole:
            self.conf.add(f"  {self.bgp_functions.import_static_blackhole()};")
        # BGP importation of static default routes
        if self.route_policy_import.static_default:
            self.conf.add(f"  {self.bgp_functions.import_static_default()};")
        # Else reject
        self.conf.add("  if DEBUG then")
        self.conf.add(f'    print "[{filter_name}] Rejecting ", net, " from master to t_bgp (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _setup_bgp_to_direct_import_filter(self) -> None:
        """BGP main table to direct import filters setup."""

        filter_name = "f_bgp_direct_import"
        self.conf.add("# Import filter FROM master table TO BGP table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        self.conf.add("  # Import connected routes")
        self.conf.add(f"  {self.bgp_functions.import_own(10)};")
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    # PROPERTIES

    @property
    def bgp_attributes(self) -> BGPAttributes:
        """Return our BGP protocol attributes."""
        return self._bgp_attributes

    @property
    def bgp_functions(self) -> BGPFunctions:
        """Return our BGP protocol functions."""
        return self._bgp_functions

    @property
    def asn(self) -> Optional[int]:
        """Return our ASN."""
        return self.bgp_attributes.asn

    @asn.setter
    def asn(self, asn: int) -> None:
        """Set our ASN."""
        self.bgp_attributes.asn = asn
        # Enable bogon constants
        self.constants.need_bogons = True

    @property
    def peertype_constraints(self) -> Dict[str, BGPPeertypeConstraints]:
        """Return our peertype constraints."""
        return self.bgp_attributes.peertype_constraints

    @property
    def rpki_source(self) -> Optional[RPKISource]:
        """Return the RPKI source to use for validation."""
        return self.bgp_attributes.rpki_source

    @rpki_source.setter
    def rpki_source(self, rpki_source: RPKISource) -> None:
        """Set the RPKI source to use for validation."""
        self.bgp_attributes.rpki_source = rpki_source

    @property
    def graceful_shutdown(self) -> bool:
        """Return our the value of graceful_shutdown."""
        return self.bgp_attributes.graceful_shutdown

    @graceful_shutdown.setter
    def graceful_shutdown(self, graceful_shutdown: bool) -> None:
        """Set the value of graceful_shutdown."""
        self.bgp_attributes.graceful_shutdown = graceful_shutdown

    @property
    def quarantine(self) -> bool:
        """Global BGP peer quarantine state."""
        return self.bgp_attributes.quarantine

    @quarantine.setter
    def quarantine(self, quarantine: bool) -> None:
        """Global BGP peer quarantine state."""
        self.bgp_attributes.quarantine = quarantine

    @property
    def rr_cluster_id(self) -> Optional[str]:
        """Return route reflector cluster ID."""
        return self.bgp_attributes.rr_cluster_id

    @rr_cluster_id.setter
    def rr_cluster_id(self, rr_cluster_id: str) -> None:
        """Set our route reflector cluster ID."""
        self.bgp_attributes.rr_cluster_id = rr_cluster_id

    @property
    def route_policy_accept(self) -> BGPRoutePolicyAccept:
        """Return our route policy for accepting of routes from peers into the main BGP table."""
        return self.bgp_attributes.route_policy_accept

    @property
    def route_policy_import(self) -> BGPRoutePolicyImport:
        """Return our route policy for importing of routes from internal tables."""
        return self.bgp_attributes.route_policy_import

    @property
    def peers(self) -> BGPPeers:
        """BGP peers."""
        return self._peers

    @property
    def originated_routes(self) -> BGPOriginatedRoutes:
        """Return our originated routes."""
        return self._originated_routes
