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

"""BIRD BGP protocol configuration."""

# pylint: disable=too-many-lines

from typing import Dict, List, Optional
from .bgp_attributes import BGPAttributes, BGPRoutePolicyAccept, BGPRoutePolicyImport
from .peer import ProtocolBGPPeer
from .typing import BGPPeerConfig
from ..pipe import ProtocolPipe
from ..direct import ProtocolDirect
from ..base import SectionProtocolBase
from ...constants import SectionConstants
from ...functions import SectionFunctions
from ...tables import SectionTables
from ....globals import BirdConfigGlobals
from .....exceptions import BirdPlanError

BGPPeersConfig = Dict[str, BGPPeerConfig]
BGPPeers = Dict[str, ProtocolBGPPeer]
BGPOriginatedRoutes = Dict[str, str]


class ProtocolBGP(SectionProtocolBase):  # pylint: disable=too-many-public-methods
    """BIRD BGP protocol configuration."""

    _section = "BGP Protocol"

    # BGP protocol attributes
    _bgp_attributes: BGPAttributes

    # List of our peers after configuration
    _peers: BGPPeers

    # Internal config before configuration happens
    _peers_config: BGPPeersConfig
    _originated_routes: BGPOriginatedRoutes

    def __init__(
        self, birdconfig_globals: BirdConfigGlobals, constants: SectionConstants, functions: SectionFunctions, tables: SectionTables
    ):
        """Initialize the object."""
        super().__init__(birdconfig_globals, constants, functions, tables)

        # BGP
        self._peers = {}
        self._peers_config = {}
        # Routes originated from BGP
        self._originated_routes = {}

        # Setup BGP attributes
        self._bgp_attributes = BGPAttributes()

    def configure(self) -> None:
        """Configure the BGP protocol."""
        super().configure()

        self._configure_constants_bogon_asns()
        self._configure_constants_bgp()
        self._configure_constants_functions()

        self.tables.conf.append("# BGP Tables")
        self.tables.conf.append("ipv4 table t_bgp4;")
        self.tables.conf.append("ipv6 table t_bgp6;")
        self.tables.conf.append("")

        # Setup BGP origination
        self._configure_originated_routes()

        # BGP to master export filters
        self._setup_bgp_to_master_export_filters()

        # BGP to master import filters
        self._setup_bgp_to_master_import_filters()

        # Configure pipe from BGP to the master routing table
        bgp_master_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from="bgp",
            table_to="master",
            table_export_filtered=True,
            table_import_filtered=True,
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
                self.constants,
                self.functions,
                self.tables,
                name="bgp",
                interfaces=interfaces,
            )
            self.conf.add(bgp_direct_protocol)
            # Add pipe
            self._setup_bgp_to_direct_import_filters()
            bgp_direct_pipe = ProtocolPipe(
                self.birdconfig_globals,
                name="bgp",
                table_from="bgp",
                table_to="direct",
                table_export="none",
                table_import_filtered=True,
            )
            self.conf.add(bgp_direct_pipe)

        # Loop with BGP peers and configure them
        for peer_name, peer_config in sorted(self.peers_config.items()):
            peer = ProtocolBGPPeer(
                self.birdconfig_globals,
                self.constants,
                self.functions,
                self.tables,
                self.bgp_attributes,
                peer_name,
                peer_config,
            )
            self.conf.add(peer)
            # Add to our list of peer objects
            self.peers[peer_name] = peer

    def add_originated_route(self, route: str) -> None:
        """Add originated route."""
        (prefix, route_info) = route.split(" ", 1)
        self.originated_routes[prefix] = route_info

    def add_peer(self, peer_name: str, peer_config: BGPPeerConfig) -> None:
        """Add peer to BGP."""
        if peer_name not in self.peers_config:
            self.peers_config[peer_name] = peer_config

    def peer(self, name: str) -> ProtocolBGPPeer:
        """Return a BGP peer configuration object."""
        return self.peers[name]

    def _configure_constants_bogon_asns(self) -> None:
        """Configure ASN bogons."""

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
        self.constants.conf.append("  4200000000..4294967294, # RFC 6996 Private ASNs")
        self.constants.conf.append("  4294967295 # RFC 7300 Last 32 bit ASN")
        self.constants.conf.append("];")
        self.constants.conf.append("")

    def _configure_constants_bgp(self) -> None:  # pylint: disable=too-many-statements
        """Configure BGP constants."""
        self.constants.conf.append_title("BGP Constants")

        self.constants.conf.append("# Our BGP ASN")
        self.constants.conf.append(f"define BGP_ASN = {self.asn};")
        self.constants.conf.append("")

        self.constants.conf.append("# Prefix sizes we will be using")
        self.constants.conf.append(f"define BGP_PREFIX_IMPORT_MAXLEN4 = {self.bgp_attributes.prefix_import_maxlen4};")
        # If we're in test mode, we need to restrict the minimum length so we can trigger tests with 100.64.0.0/X<16
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("define BGP_PREFIX_IMPORT_MINLEN4 = 16;")
        else:
            self.constants.conf.append(f"define BGP_PREFIX_IMPORT_MINLEN4 = {self.bgp_attributes.prefix_import_minlen4};")
        self.constants.conf.append(f"define BGP_PREFIX_EXPORT_MAXLEN4 = {self.bgp_attributes.prefix_export_maxlen4};")
        # If we're in test mode, we need to restrict the minimum length so we can trigger tests with 100.64.0.0/X<16
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("define BGP_PREFIX_EXPORT_MINLEN4 = 16;")
        else:
            self.constants.conf.append(f"define BGP_PREFIX_EXPORT_MINLEN4 = {self.bgp_attributes.prefix_export_minlen4};")

        # If we're in test mode, allow smaller prefixes
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("define BGP_PREFIX_IMPORT_MAXLEN6 = 64;")
            self.constants.conf.append("define BGP_PREFIX_IMPORT_MINLEN6 = 32;")
            self.constants.conf.append("define BGP_PREFIX_EXPORT_MAXLEN6 = 64;")
            self.constants.conf.append("define BGP_PREFIX_EXPORT_MINLEN6 = 32;")
        else:
            self.constants.conf.append(f"define BGP_PREFIX_IMPORT_MAXLEN6 = {self.bgp_attributes.prefix_import_maxlen6};")
            self.constants.conf.append(f"define BGP_PREFIX_IMPORT_MINLEN6 = {self.bgp_attributes.prefix_import_minlen6};")
            self.constants.conf.append(f"define BGP_PREFIX_EXPORT_MAXLEN6 = {self.bgp_attributes.prefix_export_maxlen6};")
            self.constants.conf.append(f"define BGP_PREFIX_EXPORT_MINLEN6 = {self.bgp_attributes.prefix_export_minlen6};")
        self.constants.conf.append("")

        self.constants.conf.append("# BGP AS path min and max lengths")
        self.constants.conf.append(f"define BGP_ASPATH_MAXLEN = {self.bgp_attributes.aspath_maxlen};")
        self.constants.conf.append(f"define BGP_ASPATH_MINLEN = {self.bgp_attributes.aspath_minlen};")
        self.constants.conf.append("")

        self.constants.conf.append("# Community maximum lengths")
        self.constants.conf.append(f"define BGP_COMMUNITY_MAXLEN = {self.bgp_attributes.community_maxlen};")
        self.constants.conf.append(f"define BGP_EXTENDED_COMMUNITY_MAXLEN = {self.bgp_attributes.extended_community_maxlen};")
        self.constants.conf.append(f"define BGP_LARGE_COMMUNITY_MAXLEN = {self.bgp_attributes.large_community_maxlen};")
        self.constants.conf.append("")
        # NK: IMPORTANT IF THE ABOVE CHANGES UPDATE THE BELOW
        self.constants.conf.append("# Community stripping")
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("define BGP_COMMUNITY_STRIP = [ (2..65534, *) ];  # TESTING: Start changed from 1 to 2")
        else:
            self.constants.conf.append("define BGP_COMMUNITY_STRIP = [ (1..65534, *) ];")
        self.constants.conf.append("define BGP_LC_STRIP = [ (BGP_ASN, 5, *), (BGP_ASN, 7..61, *), (BGP_ASN, 64..65535, *) ];")
        self.constants.conf.append("define BGP_COMMUNITY_STRIP_ALL = BGP_COMMUNITY_STRIP;")
        self.constants.conf.append("define BGP_LC_STRIP_ALL = [ (BGP_ASN, *, *) ];")

        self.constants.conf.append("# BGP Route Preferences")
        self.constants.conf.append("define BGP_PREF_OWN = 950;")  # -20 = Originate, -10 = static, -5 = kernel
        self.constants.conf.append("define BGP_PREF_CUSTOMER = 750;")
        self.constants.conf.append("define BGP_PREF_PEER = 470;")
        self.constants.conf.append("define BGP_PREF_ROUTESERVER = 450;")
        self.constants.conf.append("define BGP_PREF_TRANSIT = 150;")
        self.constants.conf.append("")

        self.constants.conf.append("# Well known communities")
        self.constants.conf.append("define BGP_COMMUNITY_GRACEFUL_SHUTDOWN = (65535, 0);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community functions")
        # NK: IMPORTANT IF YOU CHANGE THE BELOW, UPDATE BGP_LC_STRIP
        self.constants.conf.append("define BGP_LC_FUNCTION_LOCATION_ISO = 1;")
        self.constants.conf.append("define BGP_LC_FUNCTION_LOCATION_UN = 2;")
        self.constants.conf.append("define BGP_LC_FUNCTION_RELATION = 3;")
        self.constants.conf.append("define BGP_LC_FUNCTION_NOEXPORT = 4;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_ONE = 6;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_TWO = 62;")
        self.constants.conf.append("define BGP_LC_FUNCTION_PREPEND_THREE = 63;")
        self.constants.conf.append("define BGP_LC_FUNCTION_INFORMATION = 1000;")
        self.constants.conf.append("define BGP_LC_FUNCTION_FILTERED = 1101;")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community noexport")
        self.constants.conf.append("define BGP_LC_EXPORT_NOTRANSIT = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65412);")
        self.constants.conf.append("define BGP_LC_EXPORT_NOPEER = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65413);")
        self.constants.conf.append("define BGP_LC_EXPORT_NOCUSTOMER = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65414);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community relations")
        self.constants.conf.append("define BGP_LC_RELATION_OWN = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 1);")
        self.constants.conf.append("define BGP_LC_RELATION_CUSTOMER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 2);")
        self.constants.conf.append("define BGP_LC_RELATION_PEER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 3);")
        self.constants.conf.append("define BGP_LC_RELATION_TRANSIT = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 4);")
        self.constants.conf.append("define BGP_LC_RELATION_ROUTESERVER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 5);")
        self.constants.conf.append("")

        self.constants.conf.append("# Large community information")
        self.constants.conf.append("define BGP_LC_INFORMATION_STRIPPED_COMMUNITY = (BGP_ASN, BGP_LC_FUNCTION_INFORMATION, 1);")
        self.constants.conf.append("define BGP_LC_INFORMATION_STRIPPED_LC = (BGP_ASN, BGP_LC_FUNCTION_INFORMATION, 3);")
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

    def _configure_constants_functions(self) -> None:  # pylint: disable=too-many-statements
        """Configure BGP functions."""
        self.functions.conf.append_title("BGP Functions")

        self.functions.conf.append("# Strip all communities we could interpret internally")
        self.functions.conf.append("function bgp_communities_strip_all() ")
        self.functions.conf.append("int stripped_community;")
        self.functions.conf.append("int stripped_lc;")
        self.functions.conf.append("{")
        self.functions.conf.append("  stripped_community = 0;")
        self.functions.conf.append("  stripped_lc = 0;")
        self.functions.conf.append("  # Sanitize communities")
        self.functions.conf.append("  if (bgp_community ~ BGP_COMMUNITY_STRIP_ALL) then {")
        self.functions.conf.append('    print "[bgp_communities_strip_all] Sanitizing communities for ", net;', debug=True)
        self.functions.conf.append("    bgp_community.delete(BGP_COMMUNITY_STRIP_ALL);")
        self.functions.conf.append("    stripped_community = 1;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  # Sanitize large communities")
        self.functions.conf.append("  if (bgp_large_community ~ BGP_LC_STRIP_ALL) then {")
        self.functions.conf.append('    print "[bgp_communities_strip_all] Sanitizing large communities for ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.delete(BGP_LC_STRIP_ALL);")
        self.functions.conf.append("    stripped_lc = 1;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if (stripped_community > 0) then {")
        self.functions.conf.append(
            '    print "[bgp_communities_strip_all] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY);")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if (stripped_lc > 0) then {")
        self.functions.conf.append(
            '    print "[bgp_communities_strip_all] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Strip internal communities")
        self.functions.conf.append("function bgp_communities_strip_internal() ")
        self.functions.conf.append("int stripped_community;")
        self.functions.conf.append("int stripped_lc;")
        self.functions.conf.append("{")
        self.functions.conf.append("  stripped_community = 0;")
        self.functions.conf.append("  stripped_lc = 0;")
        self.functions.conf.append("  # Remove stripped communities")
        self.functions.conf.append("  if (bgp_community ~ BGP_COMMUNITY_STRIP) then {")
        self.functions.conf.append(
            '    print "[bgp_communities_strip_internal] Removing stripped communities from ", net;', debug=True
        )
        self.functions.conf.append("    bgp_community.delete(BGP_COMMUNITY_STRIP);")
        self.functions.conf.append("    stripped_community = 1;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  # Remove stripped large communities")
        self.functions.conf.append("  if (bgp_large_community ~ BGP_LC_STRIP) then {")
        self.functions.conf.append(
            '    print "[bgp_communities_strip_internal] Removing stripped large communities from ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.delete(BGP_LC_STRIP);")
        self.functions.conf.append("    stripped_lc = 1;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if (stripped_community > 0) then {")
        self.functions.conf.append(
            '    print "[bgp_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY);")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if (stripped_lc > 0) then {")
        self.functions.conf.append(
            '    print "[bgp_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Import own routes")
        self.functions.conf.append("function bgp_import_own(int local_pref_cost) {")
        self.functions.conf.append(
            '  print "[bgp_import_own] Adding BGP_LC_RELATION_OWN to ", net, " with local pref ", '
            "BGP_PREF_OWN - local_pref_cost;",
            debug=True,
        )
        self.functions.conf.append("  # Tag route as a our own (originated and static) route")
        self.functions.conf.append("  bgp_large_community.add(BGP_LC_RELATION_OWN);")
        self.functions.conf.append("  # Set local preference")
        self.functions.conf.append("  bgp_local_pref = BGP_PREF_OWN - local_pref_cost;")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Import customer routes")
        self.functions.conf.append("function bgp_import_customer(int peeras; int local_pref_cost) {")
        self.functions.conf.append(
            '  print "[bgp_import_customer] Adding BGP_LC_RELATION_CUSTOMER to ", net, " with local pref ", '
            "BGP_PREF_CUSTOMER - local_pref_cost;",
            debug=True,
        )
        self.functions.conf.append("  # Tag route as a customer route")
        self.functions.conf.append("  bgp_large_community.add(BGP_LC_RELATION_CUSTOMER);")
        self.functions.conf.append("  # Set local preference")
        self.functions.conf.append("  bgp_local_pref = BGP_PREF_CUSTOMER - local_pref_cost;")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Import peer routes")
        self.functions.conf.append("function bgp_import_peer(int peeras; int local_pref_cost) {")
        self.functions.conf.append(
            '  print "[bgp_import_peer] Adding BGP_LC_RELATION_PEER to ", net, " with local pref ", '
            "BGP_PREF_PEER - local_pref_cost;",
            debug=True,
        )
        self.functions.conf.append("  # Tag route as a peer route")
        self.functions.conf.append("  bgp_large_community.add(BGP_LC_RELATION_PEER);")
        self.functions.conf.append("  # Set local preference")
        self.functions.conf.append("  bgp_local_pref = BGP_PREF_PEER - local_pref_cost;")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Import transit routes")
        self.functions.conf.append("function bgp_import_transit(int peeras; int local_pref_cost) {")
        self.functions.conf.append(
            '  print "[bgp_import_transit] Adding BGP_LC_RELATION_TRANSIT to ", net, " with local pref ", '
            "BGP_PREF_TRANSIT - local_pref_cost;",
            debug=True,
        )
        self.functions.conf.append("  # Tag route as a transit route")
        self.functions.conf.append("  bgp_large_community.add(BGP_LC_RELATION_TRANSIT);")
        self.functions.conf.append("  # Set local preference")
        self.functions.conf.append("  bgp_local_pref = BGP_PREF_TRANSIT - local_pref_cost;")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Import routeserver routes")
        self.functions.conf.append("function bgp_import_routeserver(int peeras; int local_pref_cost) {")
        self.functions.conf.append(
            '  print "[bgp_import_routeserver] Adding BGP_LC_RELATION_ROUTESERVER to ", net, " with local pref ", '
            "BGP_PREF_ROUTESERVER - local_pref_cost;",
            debug=True,
        )
        self.functions.conf.append("  # Tag route as a routeserver route")
        self.functions.conf.append("  bgp_large_community.add(BGP_LC_RELATION_ROUTESERVER);")
        self.functions.conf.append("  # Set local preference")
        self.functions.conf.append("  bgp_local_pref = BGP_PREF_ROUTESERVER - local_pref_cost;")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter routecollector routes")
        self.functions.conf.append("function bgp_filter_routecollector() {")
        self.functions.conf.append('  print "[bgp_filter_routecollector] Adding BGP_FILTERED_ROUTECOLLECTOR to ", net;', debug=True)
        self.functions.conf.append("  bgp_large_community.add(BGP_LC_FILTERED_ROUTECOLLECTOR);")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter IPv4 prefix size")
        self.functions.conf.append("function bgp_filter_size_v4() {")
        self.functions.conf.append("  if prefix_is_longer(BGP_PREFIX_IMPORT_MAXLEN4) then {")
        self.functions.conf.append('    print "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if prefix_is_shorter(BGP_PREFIX_IMPORT_MINLEN4) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter IPv6 prefix size")
        self.functions.conf.append("function bgp_filter_size_v6() {")
        self.functions.conf.append("  if prefix_is_longer(BGP_PREFIX_IMPORT_MAXLEN6) then {")
        self.functions.conf.append('    print "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if prefix_is_shorter(BGP_PREFIX_IMPORT_MINLEN6) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter IPv4 bogons")
        self.functions.conf.append("function bgp_filter_bogons_v4() {")
        self.functions.conf.append("  if is_bogon4() then {")
        self.functions.conf.append('    print "[bgp_filter_bogons_v4] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter IPv6 bogons")
        self.functions.conf.append("function bgp_filter_bogons_v6() {")
        self.functions.conf.append("  if is_bogon6() then {")
        self.functions.conf.append('    print "[bgp_filter_bogons_v6] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter prefixes (ALLOW)")
        self.functions.conf.append("function bgp_filter_allow_prefixes(prefix set prefix_list) {")
        self.functions.conf.append("  if (net !~ prefix_list) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_allow_prefixes] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("# Filter prefixes (DENY)")
        self.functions.conf.append("function bgp_filter_deny_prefixes(prefix set prefix_list) {")
        self.functions.conf.append("  if (net ~ prefix_list) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_deny_prefixes] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter IPv4 default route")
        self.functions.conf.append("function bgp_filter_default_v4() {")
        self.functions.conf.append("  if (net = DEFAULT_ROUTE_V4) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_default_v4] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);")
        self.functions.conf.append("    accept;")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter IPv6 default route")
        self.functions.conf.append("function bgp_filter_default_v6() {")
        self.functions.conf.append("  if (net = DEFAULT_ROUTE_V6) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_default_v6] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);")
        self.functions.conf.append("    accept;")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter ASNs (ALLOW list)")
        self.functions.conf.append("function bgp_filter_allow_asns(int set asns) {")
        self.functions.conf.append("  if (bgp_path.last_nonaggregated !~ asns) then {")
        self.functions.conf.append('    print "[bgp_filter_allow_asns] Adding BGP_LC_FILTERED_ORIGIN_AS to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("# Filter ASNs (DENY list)")
        self.functions.conf.append("function bgp_filter_deny_asns(int set asns) {")
        self.functions.conf.append("  if (bgp_path.last_nonaggregated ~ asns) then {")
        self.functions.conf.append('    print "[bgp_filter_deny_asns] Adding BGP_LC_FILTERED_ORIGIN_AS to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter bogon ASNs")
        self.functions.conf.append("function bgp_filter_asn_bogons() {")
        self.functions.conf.append("  # Filter bogon ASNs")
        self.functions.conf.append("  if (bgp_path ~ BOGON_ASNS) then {")
        self.functions.conf.append('    print "[bgp_filter_asn_bogons] Adding BGP_LC_FILTERED_BOGON_ASN to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_BOGON_ASN);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter transit ASNs")
        self.functions.conf.append("function bgp_filter_asn_transit() {")
        self.functions.conf.append("  # Filter transit ASNs")
        self.functions.conf.append("  if (bgp_path ~ BGP_ASNS_TRANSIT) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_asn_transit] Adding BGP_LC_FILTERED_TRANSIT_FREE_ASN to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_TRANSIT_FREE_ASN);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter long AS paths")
        self.functions.conf.append("function bgp_filter_asn_long() {")
        self.functions.conf.append("  if (bgp_path.len > BGP_ASPATH_MAXLEN) then {")
        self.functions.conf.append('    print "[bgp_filter_asn_long] Adding BGP_LC_FILTERED_ASPATH_TOO_LONG to ", net;', debug=True)
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_ASPATH_TOO_LONG);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter short AS paths")
        self.functions.conf.append("function bgp_filter_asn_short() {")
        self.functions.conf.append("  if (bgp_path.len < BGP_ASPATH_MINLEN) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_asn_short] Adding BGP_LC_FILTERED_ASPATH_TOO_SHORT to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_ASPATH_TOO_SHORT);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter too many communities")
        self.functions.conf.append("function bgp_filter_community_length() {")
        self.functions.conf.append("  if (bgp_community.len > BGP_COMMUNITY_MAXLEN) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_community_length] Adding BGP_LC_FILTERED_TOO_MANY_COMMUNITIES to ", net, '
            '" counted ", bgp_community.len;',
            debug=True,
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_COMMUNITIES);")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if (bgp_ext_community.len > BGP_EXTENDED_COMMUNITY_MAXLEN) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_community_length] Adding BGP_LC_FILTERED_TOO_MANY_EXTENDED_COMMUNITIES to ", net, '
            '" counted ", bgp_ext_community.len;',
            debug=True,
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_EXTENDED_COMMUNITIES);")
        self.functions.conf.append("  }")
        self.functions.conf.append("")
        self.functions.conf.append("  if (bgp_large_community.len > BGP_LARGE_COMMUNITY_MAXLEN) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_community_length] Adding BGP_LC_FILTERED_TOO_MANY_LARGE_COMMUNITIES to ", net, '
            '" counted ", bgp_large_community.len;',
            debug=True,
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_LARGE_COMMUNITIES);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter peer ASN != route first ASN")
        self.functions.conf.append("function bgp_filter_asn_invalid(int peeras) {")
        self.functions.conf.append("  if (bgp_path.first != peeras) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_asn_invalid] Adding BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter peer != next_hop")
        self.functions.conf.append("function bgp_filter_nexthop_not_peerip() {")
        self.functions.conf.append("  if (from != bgp_next_hop) then {")
        self.functions.conf.append(
            '    print "[bgp_filter_nexthop_not_peerip] Adding BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP to ", net;', debug=True
        )
        self.functions.conf.append("    bgp_large_community.add(BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Filter for QUARANTINE mode")
        self.functions.conf.append("function bgp_filter_quarantine() {")
        self.functions.conf.append('  print "[bgp_filter_quarantine] Adding BGP_LC_FILTERED_QUARANTINED to ", net;', debug=True)
        self.functions.conf.append("  bgp_large_community.add(BGP_LC_FILTERED_QUARANTINED);")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Graceful shutdown")
        self.functions.conf.append("function bgp_graceful_shutdown() {")
        self.functions.conf.append('  if (BGP_COMMUNITY_GRACEFUL_SHUTDOWN ~ bgp_community) then {')
        self.functions.conf.append('    print "[bgp_graceful_shutdown] Setting LOCAL_PREF to 0 for ", net;', debug=True)
        self.functions.conf.append("    bgp_local_pref = 0;")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Can we export this IPv4 BGP route to the peeras?")
        self.functions.conf.append("function bgp_can_export_v4(int peeras) {")
        self.functions.conf.append("  # Check for NOEXPORT large community")
        self.functions.conf.append("  if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peeras) ~ bgp_large_community) then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v4] Not exporting due to BGP_LC_FUNCTION_NOEXPORT for AS", peeras ," for ",' "net;",
            debug=True,
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  # Validate route before export")
        self.functions.conf.append("  if prefix_is_longer(BGP_PREFIX_EXPORT_MAXLEN4) then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v4] Not exporting due to prefix length > BGP_PREFIX_EXPORT_MAXLEN4 for ", net;', debug=True
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if prefix_is_shorter(BGP_PREFIX_EXPORT_MINLEN4) then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v4] Not exporting due to prefix length < BGP_PREFIX_EXPORT_MINLEN4 for ", net;', debug=True
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if is_bogon4() then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v4] Not exporting due to (is_bogon4 == True) for ", net;', debug=True
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  # If all above tests are ok, then we can")
        self.functions.conf.append("  return true;")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# Can we export this IPv6 BGP route to the peeras?")
        self.functions.conf.append("function bgp_can_export_v6(int peeras) {")
        self.functions.conf.append("  # Check for NOEXPORT large community")
        self.functions.conf.append("  if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peeras) ~ bgp_large_community) then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v6] Not exporting due to BGP_LC_FUNCTION_NOEXPORT for AS", peeras ," for ",' "net;",
            debug=True,
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  # Validate route before export")
        self.functions.conf.append("  if prefix_is_longer(BGP_PREFIX_EXPORT_MAXLEN6) then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v6] Not exporting due to prefix length > BGP_PREFIX_EXPORT_MAXLEN6 for ", net;', debug=True
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if prefix_is_shorter(BGP_PREFIX_EXPORT_MINLEN6) then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v6] Not exporting due to prefix length < BGP_PREFIX_EXPORT_MINLEN6 for ", net;', debug=True
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  if is_bogon6() then {")
        self.functions.conf.append(
            '    print "[bgp_can_export_v6] Not exporting due to (is_bogon6 == True) for ", net;', debug=True
        )
        self.functions.conf.append("    return false;")
        self.functions.conf.append("  }")
        self.functions.conf.append("  # If all above tests are ok, then we can")
        self.functions.conf.append("  return true;")
        self.functions.conf.append("}")
        self.functions.conf.append("")

        self.functions.conf.append("# BGP export prepending")
        self.functions.conf.append("function bgp_export_prepend(int peeras) {")
        self.functions.conf.append("  # If we are prepending three times")
        self.functions.conf.append("  if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_THREE, peeras) ~ bgp_large_community) then {")
        self.functions.conf.append('    print "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_THREE for ", net;', debug=True)
        self.functions.conf.append("    bgp_path.prepend(bgp_path.first);")
        self.functions.conf.append("    bgp_path.prepend(bgp_path.first);")
        self.functions.conf.append("    bgp_path.prepend(bgp_path.first);")
        self.functions.conf.append("  # If we are prepending two times")
        self.functions.conf.append("  } else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_TWO, peeras) ~ bgp_large_community) then {")
        self.functions.conf.append('    print "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_TWO for ", net;', debug=True)
        self.functions.conf.append("    bgp_path.prepend(bgp_path.first);")
        self.functions.conf.append("    bgp_path.prepend(bgp_path.first);")
        self.functions.conf.append("  # If we are prepending one time")
        self.functions.conf.append("  } else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_ONE, peeras) ~ bgp_large_community) then {")
        self.functions.conf.append('    print "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_ONE for ", net;', debug=True)
        self.functions.conf.append("    bgp_path.prepend(bgp_path.first);")
        self.functions.conf.append("  }")
        self.functions.conf.append("}")
        self.functions.conf.append("")

    def _configure_originated_routes(self) -> None:
        # Work out static v4 and v6 routes
        routes: Dict[str, List[str]] = {"4": [], "6": []}
        for prefix in sorted(self.originated_routes.keys()):
            info = self.originated_routes[prefix]
            if "." in prefix:
                routes["4"].append("%s %s" % (prefix, info))
            elif ":" in prefix:
                routes["6"].append("%s %s" % (prefix, info))
            else:
                raise BirdPlanError(f"The BGP originate route '{prefix}' is odd")
        # Loop with IPv4 and IPv6
        self.tables.conf.append("# BGP Origination Tables")
        for ipv in ["4", "6"]:
            self.tables.conf.append(f"ipv{ipv} table t_bgp_originate{ipv};")

            self.conf.add(f"filter f_bgp_originate{ipv}_import {{")
            self.conf.add("  # Origination import")
            self.conf.add("  bgp_import_own(20);")
            self.conf.add("  accept;")
            self.conf.add("};")
            self.conf.add("")

            self.conf.add(f"protocol static bgp_originate{ipv} {{")
            self.conf.add(f'  description "BGP route origination for IPv{ipv}";')
            self.conf.add("")
            self.conf.add(f"  ipv{ipv} {{")
            self.conf.add(f"    table t_bgp_originate{ipv};")
            self.conf.add("    export none;")
            self.conf.add(f"    import filter f_bgp_originate{ipv}_import;")
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

    def _bgp_to_master_export_filter(self, ipv: str) -> None:
        """BGP to master filter."""

        # Configure export filter to master
        self.conf.add("# Export filter FROM BGP table TO master table")
        self.conf.add(f"filter f_bgp{ipv}_master{ipv}_export {{")
        # Check if we accept the default route, if not block it
        if not self.route_policy_accept.default:
            self.conf.add("  # Do not export default routes to the master")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Accept BGP routes into the master routing table
        self.conf.add("  # Export BGP routes to the master table")
        self.conf.add("  if (source = RTS_BGP) then {")
        self.conf.add("    accept;")
        self.conf.add("  }")
        # Accept BGP routes into the master routing table
        self.conf.add("  # Export originated routes to the master table")
        self.conf.add(f'  if (proto = "bgp_originate{ipv}") then {{')
        self.conf.add("    accept;")
        self.conf.add("  }")
        # Default to reject
        self.conf.add("  # Reject everything else;")
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _bgp_to_master_import_filter(self, ipv: str) -> None:
        # Configure import filter to master
        self.conf.add("# Import filter FROM master table TO BGP table")
        self.conf.add(f"filter f_bgp{ipv}_master{ipv}_import")
        self.conf.add("{")
        # Redistribute kernel routes
        if self.route_policy_import.kernel:
            self.conf.add("  # Import kernel routes into BGP")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add("    bgp_import_own(5);")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute kernel routes
        if self.route_policy_import.static:
            self.conf.add("  # Import static routes into BGP")
            self.conf.add("  if (source = RTS_STATIC) then {")
            self.conf.add("    bgp_import_own(10);")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Else accept
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _bgp_to_direct_import_filter(self, ipv: str) -> None:
        # Configure import filter to direct
        self.conf.add(f"filter f_bgp{ipv}_direct{ipv}_import {{")
        self.conf.add("  # Origination import")
        self.conf.add("  bgp_import_own(10);")
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _setup_bgp_to_master_export_filters(self) -> None:
        """BGP main table to master export filters setup."""
        self._bgp_to_master_export_filter("4")
        self._bgp_to_master_export_filter("6")

    def _setup_bgp_to_master_import_filters(self) -> None:
        """BGP main table to master import filters setup."""
        self._bgp_to_master_import_filter("4")
        self._bgp_to_master_import_filter("6")

    def _setup_bgp_to_direct_import_filters(self) -> None:
        """BGP main table to direct import filters setup."""
        self._bgp_to_direct_import_filter("4")
        self._bgp_to_direct_import_filter("6")

    # PROPERTIES

    @property
    def bgp_attributes(self) -> BGPAttributes:
        """Return our BGP protocol attributes."""
        return self._bgp_attributes

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
        self.functions.need_functions = True

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
        """Return BGP peers."""
        return self._peers

    @property
    def peers_config(self) -> BGPPeersConfig:
        """Return BGP peers configuration."""
        return self._peers_config

    @property
    def originated_routes(self) -> BGPOriginatedRoutes:
        """Return our originated routes."""
        return self._originated_routes

    # IPV4 IMPORT PREFIX LENGTHS

    @property
    def prefix_import_maxlen4(self) -> int:
        """Return the current value of prefix_import_maxlen4."""
        return self.bgp_attributes.prefix_import_maxlen4

    @prefix_import_maxlen4.setter
    def prefix_import_maxlen4(self, prefix_import_maxlen4: int) -> None:
        """Setter for prefix_import_maxlen4."""
        self.bgp_attributes.prefix_import_maxlen4 = prefix_import_maxlen4

    @property
    def prefix_import_minlen4(self) -> int:
        """Return the current value of prefix_import_minlen4."""
        return self.bgp_attributes.prefix_import_minlen4

    @prefix_import_minlen4.setter
    def prefix_import_minlen4(self, prefix_import_minlen4: int) -> None:
        """Setter for prefix_import_minlen4."""
        self.bgp_attributes.prefix_import_minlen4 = prefix_import_minlen4

    # IPV4 EXPORT PREFIX LENGHTS

    @property
    def prefix_export_maxlen4(self) -> int:
        """Return the current value of prefix_export_maxlen4."""
        return self.bgp_attributes.prefix_export_maxlen4

    @prefix_export_maxlen4.setter
    def prefix_export_maxlen4(self, prefix_export_maxlen4: int) -> None:
        """Setter for prefix_export_maxlen4."""
        self.bgp_attributes.prefix_export_maxlen4 = prefix_export_maxlen4

    @property
    def prefix_export_minlen4(self) -> int:
        """Return the current value of prefix_export_minlen4."""
        return self.bgp_attributes.prefix_export_minlen4

    @prefix_export_minlen4.setter
    def prefix_export_minlen4(self, prefix_export_minlen4: int) -> None:
        """Setter for prefix_export_minlen4."""
        self.bgp_attributes.prefix_export_minlen4 = prefix_export_minlen4

    # IPV6 IMPORT LENGTHS

    @property
    def prefix_import_maxlen6(self) -> int:
        """Return the current value of prefix_import_maxlen6."""
        return self.bgp_attributes.prefix_import_maxlen6

    @prefix_import_maxlen6.setter
    def prefix_import_maxlen6(self, prefix_import_maxlen6: int) -> None:
        """Setter for prefix_import_maxlen6."""
        self.bgp_attributes.prefix_import_maxlen6 = prefix_import_maxlen6

    @property
    def prefix_import_minlen6(self) -> int:
        """Return the current value of prefix_import_minlen6."""
        return self.bgp_attributes.prefix_import_minlen6

    @prefix_import_minlen6.setter
    def prefix_import_minlen6(self, prefix_import_minlen6: int) -> None:
        """Setter for prefix_import_minlen6."""
        self.bgp_attributes.prefix_import_minlen6 = prefix_import_minlen6

    # IPV6 EXPORT LENGTHS

    @property
    def prefix_export_minlen6(self) -> int:
        """Return the current value of prefix_export_minlen6."""
        return self.bgp_attributes.prefix_export_minlen6

    @prefix_export_minlen6.setter
    def prefix_export_minlen6(self, prefix_export_minlen6: int) -> None:
        """Setter for prefix_export_minlen6."""
        self.bgp_attributes.prefix_export_minlen6 = prefix_export_minlen6

    @property
    def prefix_export_maxlen6(self) -> int:
        """Return the current value of prefix_export_maxlen6."""
        return self.bgp_attributes.prefix_export_maxlen6

    @prefix_export_maxlen6.setter
    def prefix_export_maxlen6(self, prefix_export_maxlen6: int) -> None:
        """Setter for prefix_export_maxlen6."""
        self.bgp_attributes.prefix_export_maxlen6 = prefix_export_maxlen6

    # AS PATH LENGTHS

    @property
    def aspath_minlen(self) -> int:
        """Return the current value of aspath_minlen."""
        return self.bgp_attributes.aspath_minlen

    @aspath_minlen.setter
    def aspath_minlen(self, aspath_minlen: int) -> None:
        """Set the AS path minlen."""
        self.bgp_attributes.aspath_minlen = aspath_minlen

    @property
    def aspath_maxlen(self) -> int:
        """Return the current value of aspath_maxlen."""
        return self.bgp_attributes.aspath_maxlen

    @aspath_maxlen.setter
    def aspath_maxlen(self, aspath_maxlen: int) -> None:
        """Set the AS path maxlen."""
        self.bgp_attributes.aspath_maxlen = aspath_maxlen

    # COMMUNITY LENGTHS

    @property
    def community_maxlen(self) -> int:
        """Return the current value of community_maxlen."""
        return self.bgp_attributes.community_maxlen

    @community_maxlen.setter
    def community_maxlen(self, community_maxlen: int) -> None:
        """Set the value of community_maxlen."""
        self.bgp_attributes.community_maxlen = community_maxlen

    @property
    def extended_community_maxlen(self) -> int:
        """Return the current value of extended_community_maxlen."""
        return self.bgp_attributes.extended_community_maxlen

    @extended_community_maxlen.setter
    def extended_community_maxlen(self, extended_community_maxlen: int) -> None:
        """Set the value of extended_community_maxlen."""
        self.bgp_attributes.extended_community_maxlen = extended_community_maxlen

    @property
    def large_community_maxlen(self) -> int:
        """Return the current value of large_community_maxlen."""
        return self.bgp_attributes.large_community_maxlen

    @large_community_maxlen.setter
    def large_community_maxlen(self, large_community_maxlen: int) -> None:
        """Set the value of large_community_maxlen."""
        self.bgp_attributes.large_community_maxlen = large_community_maxlen
