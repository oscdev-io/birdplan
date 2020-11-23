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
from .bgp_functions import BGPFunctions
from .peer import ProtocolBGPPeer
from .typing import BGPPeerConfig
from ..pipe import ProtocolPipe, ProtocolPipeFilterType
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
    # BGP functions
    _bgp_functions: BGPFunctions

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
        # Setup BGP functions
        self._bgp_functions = BGPFunctions(birdconfig_globals)

        # For test mode we need to slightly adjust our prefix lengths that we permit
        if self.birdconfig_globals.test_mode:
            self.aspath_import_maxlen = 25
            self.community_import_maxlen = 25
            self.extended_community_import_maxlen = 25
            self.large_community_import_maxlen = 25

            self.blackhole_maxlen4 = 31
            self.blackhole_maxlen6 = 127

            self.prefix_import_minlen4 = 16
            self.prefix_export_minlen4 = 16
            self.prefix_import_maxlen6 = 64
            self.prefix_import_minlen6 = 32
            self.prefix_export_maxlen6 = 64
            self.prefix_export_minlen6 = 32

    def configure(self) -> None:
        """Configure the BGP protocol."""
        super().configure()

        self._configure_constants_bgp()
        self.functions.conf.append(self.bgp_functions, deferred=True)

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
            export_filter_type=ProtocolPipeFilterType.VERSIONED,
            import_filter_type=ProtocolPipeFilterType.VERSIONED,
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
                import_filter_type=ProtocolPipeFilterType.VERSIONED,
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
                self.bgp_functions,
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

    def _configure_constants_bgp(self) -> None:  # pylint: disable=too-many-statements
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
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("define BGP_COMMUNITY_STRIP = [ (2..65534, *) ];  # TESTING: Start changed from 1 to 2")
        else:
            self.constants.conf.append("define BGP_COMMUNITY_STRIP = [ (1..65534, *) ];")
        # This is used for stripping large communities from customers mostly
        self.constants.conf.append("define BGP_LC_STRIP = [ ")
        self.constants.conf.append("  (BGP_ASN, 1..3, *),")  # Strip route learned functions
        # Allow client traffic engineering: 4, 5, 6, 7, 8
        self.constants.conf.append("  (BGP_ASN, 9..60, *),")  # Strip unused
        self.constants.conf.append("  (BGP_ASN, 64..70, *),")  # Strip unused
        self.constants.conf.append("  (BGP_ASN, 74..4294967295, *),")  # Strip unsed + rest (incl. 1000 - info, 1101 - filter)
        # These functions should never be used on our own ASN
        self.constants.conf.append("  (BGP_ASN, 4, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 6, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 61, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 62, BGP_ASN),")
        self.constants.conf.append("  (BGP_ASN, 63, BGP_ASN)")
        self.constants.conf.append("];")
        # Strip communities from all peer types
        self.constants.conf.append("define BGP_COMMUNITY_STRIP_ALL = BGP_COMMUNITY_STRIP;")
        # This is used for stripping large communities from peers and transit providers
        self.constants.conf.append("define BGP_LC_STRIP_ALL = [ (BGP_ASN, *, *) ];")
        self.constants.conf.append("define BGP_LC_STRIP_PRIVATE = [")
        # Don't strip the lower private ASN range during testing
        if self.birdconfig_globals.test_mode:
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: (64512..65534, *, *)")
            self.constants.conf.append("  # EXCLUDING DUE TO TESTING: (4200000000..4294967294, *, *)")
            self.constants.conf.append("  (4200000000..4294900000, *, *) # ADJUSTED FOR TESTING")
        else:
            self.constants.conf.append("  (64512..65534, *, *),")
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
                routes["4"].append("%s %s" % (prefix, info))
            elif ":" in prefix:
                routes["6"].append("%s %s" % (prefix, info))
            else:
                raise BirdPlanError(f"The BGP originate route '{prefix}' is odd")
        # Loop with IPv4 and IPv6
        self.tables.conf.append("# BGP Origination Tables")
        for ipv in ["4", "6"]:
            self.tables.conf.append(f"ipv{ipv} table t_bgp_originate{ipv};")

            # FIXME - use common filter for both now?
            filter_name = f"f_bgp_originate{ipv}_import"
            self.conf.add(f"filter {filter_name}")
            self.conf.add("string filter_name;")
            self.conf.add("{")
            self.conf.add(f'  filter_name = "{filter_name}";')
            self.conf.add("  # Origination import")
            self.conf.add(f"  {self.bgp_functions.import_own(20)};")
            self.conf.add("  accept;")
            self.conf.add("};")
            self.conf.add("")

            self.conf.add(f"protocol static bgp_originate{ipv} {{")
            self.conf.add(f'  description "BGP route origination for IPv{ipv}";')
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
        filter_name = f"f_bgp{ipv}_master{ipv}_import"
        self.conf.add("# Import filter FROM master table TO BGP table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # Redistribute kernel routes
        if self.route_policy_import.kernel:
            self.conf.add("  # Import kernel routes into BGP")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add(f"    {self.bgp_functions.import_own(5)};")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Redistribute kernel routes
        if self.route_policy_import.static:
            self.conf.add("  # Import static routes into BGP")
            self.conf.add("  if (source = RTS_STATIC) then {")
            self.conf.add(f"    {self.bgp_functions.import_own(10)};")
            self.conf.add("    accept;")
            self.conf.add("  }")
        # Else accept
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _bgp_to_direct_import_filter(self, ipv: str) -> None:
        # Configure import filter to direct

        filter_name = f"f_bgp{ipv}_direct{ipv}_import"
        self.conf.add("# Import filter FROM master table TO BGP table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        self.conf.add("  # Origination import")
        self.conf.add(f"  {self.bgp_functions.import_own(10)};")
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
        self.functions.need_functions = True

    @property
    def graceful_shutdown(self) -> bool:
        """Return our the value of graceful_shutdown."""
        return self.bgp_attributes.graceful_shutdown

    @graceful_shutdown.setter
    def graceful_shutdown(self, graceful_shutdown: bool) -> None:
        """Set the value of graceful_shutdown."""
        self.bgp_attributes.graceful_shutdown = graceful_shutdown

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

    # IPV4 BLACKHOLE PREFIX LENGTHS

    @property
    def blackhole_maxlen4(self) -> int:
        """Return the current value of blackhole_maxlen4."""
        return self.bgp_attributes.blackhole_maxlen4

    @blackhole_maxlen4.setter
    def blackhole_maxlen4(self, blackhole_maxlen4: int) -> None:
        """Setter for blackhole_maxlen4."""
        self.bgp_attributes.blackhole_maxlen4 = blackhole_maxlen4

    @property
    def blackhole_minlen4(self) -> int:
        """Return the current value of blackhole_minlen4."""
        return self.bgp_attributes.blackhole_minlen4

    @blackhole_minlen4.setter
    def blackhole_minlen4(self, blackhole_minlen4: int) -> None:
        """Setter for blackhole_minlen4."""
        self.bgp_attributes.blackhole_minlen4 = blackhole_minlen4

    # IPV6 BLACKHOLE PREFIX LENGTHS

    @property
    def blackhole_maxlen6(self) -> int:
        """Return the current value of blackhole_maxlen6."""
        return self.bgp_attributes.blackhole_maxlen6

    @blackhole_maxlen6.setter
    def blackhole_maxlen6(self, blackhole_maxlen6: int) -> None:
        """Setter for blackhole_maxlen6."""
        self.bgp_attributes.blackhole_maxlen6 = blackhole_maxlen6

    @property
    def blackhole_minlen6(self) -> int:
        """Return the current value of blackhole_minlen6."""
        return self.bgp_attributes.blackhole_minlen6

    @blackhole_minlen6.setter
    def blackhole_minlen6(self, blackhole_minlen6: int) -> None:
        """Setter for blackhole_minlen6."""
        self.bgp_attributes.blackhole_minlen6 = blackhole_minlen6

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
    def aspath_import_minlen(self) -> int:
        """Return the current value of aspath_import_minlen."""
        return self.bgp_attributes.aspath_import_minlen

    @aspath_import_minlen.setter
    def aspath_import_minlen(self, aspath_import_minlen: int) -> None:
        """Set the AS path minlen."""
        self.bgp_attributes.aspath_import_minlen = aspath_import_minlen

    @property
    def aspath_import_maxlen(self) -> int:
        """Return the current value of aspath_import_maxlen."""
        return self.bgp_attributes.aspath_import_maxlen

    @aspath_import_maxlen.setter
    def aspath_import_maxlen(self, aspath_import_maxlen: int) -> None:
        """Set the AS path maxlen."""
        self.bgp_attributes.aspath_import_maxlen = aspath_import_maxlen

    # COMMUNITY LENGTHS

    @property
    def community_import_maxlen(self) -> int:
        """Return the current value of community_import_maxlen."""
        return self.bgp_attributes.community_import_maxlen

    @community_import_maxlen.setter
    def community_import_maxlen(self, community_import_maxlen: int) -> None:
        """Set the value of community_import_maxlen."""
        self.bgp_attributes.community_import_maxlen = community_import_maxlen

    @property
    def extended_community_import_maxlen(self) -> int:
        """Return the current value of extended_community_import_maxlen."""
        return self.bgp_attributes.extended_community_import_maxlen

    @extended_community_import_maxlen.setter
    def extended_community_import_maxlen(self, extended_community_import_maxlen: int) -> None:
        """Set the value of extended_community_import_maxlen."""
        self.bgp_attributes.extended_community_import_maxlen = extended_community_import_maxlen

    @property
    def large_community_import_maxlen(self) -> int:
        """Return the current value of large_community_import_maxlen."""
        return self.bgp_attributes.large_community_import_maxlen

    @large_community_import_maxlen.setter
    def large_community_import_maxlen(self, large_community_import_maxlen: int) -> None:
        """Set the value of large_community_import_maxlen."""
        self.bgp_attributes.large_community_import_maxlen = large_community_import_maxlen
