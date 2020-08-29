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

"""BIRD constants configuration."""

from .base import BirdConfigBase


class BirdConfigConstants(BirdConfigBase):
    """BIRD constants configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Add bogon constants to output
        self._need_bogons = False
        # Add functions to output
        self._need_functions = False
        # BGP constants output
        self._bgp = {
            "asn": None,
            "prefix_maxlen4_import": 24,
            "prefix_maxlen4_export": 24,
            "prefix_minlen4_import": 8,
            "prefix_minlen4_export": 8,
            "prefix_maxlen6_import": 48,
            "prefix_maxlen6_export": 48,
            "prefix_minlen6_import": 16,
            "prefix_minlen6_export": 16,
        }

    def _configure_defaults(self):
        """Configure default routes."""
        self._addline("# Default routes")
        self._addline("define DEFAULT_ROUTE_V4 = 0.0.0.0/0; # IPv4 default route")
        self._addline("define DEFAULT_ROUTE_V6 = ::/0; # IPv6 default route")
        self._addline("")

    def _configure_bogons_ipv4(self):
        """Configure IPv4 bogons."""
        self._addline("# As per http://bgpfilterguide.nlnog.net/guides/bogon_prefixes/")
        self._addline("define BOGONS_V4 = [")
        self._addline("\t0.0.0.0/8+, # RFC 1122 'this' network")
        self._addline("\t10.0.0.0/8+, # RFC 1918 private space")
        if self.test_mode:
            self._addline("\t# EXCLUDING DUE TO TESTING: 100.64.0.0/10+, # RFC 6598 Carrier grade nat space")
        else:
            self._addline("\t100.64.0.0/10+, # RFC 6598 Carrier grade nat space")
        self._addline("\t127.0.0.0/8+, # RFC 1122 localhost")
        self._addline("\t169.254.0.0/16+, # RFC 3927 link local")
        self._addline("\t172.16.0.0/12+, # RFC 1918 private space")
        self._addline("\t192.0.2.0/24+, # RFC 5737 TEST-NET-1")
        self._addline("\t192.88.99.0/24+, # RFC 7526 6to4 anycast relay")
        self._addline("\t192.168.0.0/16+, # RFC 1918 private space")
        self._addline("\t198.18.0.0/15+, # RFC 2544 benchmarking")
        self._addline("\t198.51.100.0/24+, # RFC 5737 TEST-NET-2")
        self._addline("\t203.0.113.0/24+, # RFC 5737 TEST-NET-3")
        self._addline("\t224.0.0.0/4+, # multicast")
        self._addline("\t240.0.0.0/4+ # reserved")
        self._addline("];")
        self._addline("")

    def _configure_bogons_ipv6(self):
        """Configure IPv6 bogons."""
        self._addline("# As per http://bgpfilterguide.nlnog.net/guides/bogon_prefixes/")
        self._addline("define BOGONS_V6 = [")
        self._addline("\t::/8+, # RFC 4291 IPv4-compatible, loopback, et al")
        self._addline("\t0100::/64+, # RFC 6666 Discard-Only")
        self._addline("\t2001:2::/48+, # RFC 5180 BMWG")
        self._addline("\t2001:10::/28+, # RFC 4843 ORCHID")
        self._addline("\t2001:db8::/32+, # RFC 3849 documentation")
        self._addline("\t2002::/16+, # RFC 7526 6to4 anycast relay")
        self._addline("\t3ffe::/16+, # RFC 3701 old 6bone")
        if self.test_mode:
            self._addline("\t# EXCLUDING DUE TO TESTING: fc00::/7+, # RFC 4193 unique local unicast")
        else:
            self._addline("\tfc00::/7+, # RFC 4193 unique local unicast")
        self._addline("\tfe80::/10+, # RFC 4291 link local unicast")
        self._addline("\tfec0::/10+, # RFC 3879 old site local unicast")
        self._addline("\tff00::/8+ # RFC 4291 multicast")
        self._addline("];")
        self._addline("")

    def _configure_bogons_asn(self):
        """Configure ASN bogons."""

        self._addline("# Ref http://bgpfilterguide.nlnog.net/guides/bogon_asns/")
        self._addline("define BOGON_ASNS = [")
        self._addline("\t0, # RFC 7607")
        self._addline("\t23456, # RFC 4893 AS_TRANS")
        self._addline("\t64496..64511, # RFC 5398 and documentation/example ASNs")
        if self.test_mode:
            self._addline("\t# EXCLUDING DUE TO TESTING: 64512..65534, # RFC 6996 Private ASNs")
        else:
            self._addline("\t64512..65534, # RFC 6996 Private ASNs")
        self._addline("\t65535, # RFC 7300 Last 16 bit ASN")
        self._addline("\t65536..65551, # RFC 5398 and documentation/example ASNs")
        self._addline("\t65552..131071, # RFC IANA reserved ASNs")
        self._addline("\t4200000000..4294967294, # RFC 6996 Private ASNs")
        self._addline("\t4294967295 # RFC 7300 Last 32 bit ASN")
        self._addline("];")

    def _configure_functions(self):
        """Configure functions."""
        self._addtitle("Global Functions")
        self._addline('# Match a prefix longer than "size".')
        self._addline("function prefix_is_longer(int size) {")
        self._addline("\tif (net.len > size) then {")
        self._addline('\t\tprint "[prefix_is_longer] Matched ", net, " against size ", size;', debug=True)
        self._addline("\t\treturn true;")
        self._addline("\t} else {")
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")
        self._addline('# Match a prefix shorter than "size".')
        self._addline("function prefix_is_shorter(int size) {")
        self._addline("\tif (net.len < size) then {")
        self._addline('\t\tprint "[prefix_is_shorter] Matched ", net, " against size ", size;', debug=True)
        self._addline("\t\treturn true;")
        self._addline("\t} else {")
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")
        self._addline("# Match on bogons for IPv4")
        self._addline("function is_bogon4() {")
        self._addline("\tif (net ~ BOGONS_V4) then {")
        self._addline('\t\tprint "[is_bogon4] Matched ", net;', debug=True)
        self._addline("\t\treturn true;")
        self._addline("\t} else {")
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")
        self._addline("# Match on bogons for IPv6")
        self._addline("function is_bogon6() {")
        self._addline("\tif (net ~ BOGONS_V6) then {")
        self._addline('\t\tprint "[is_bogon6] Matched ", net;', debug=True)
        self._addline("\t\treturn true;")
        self._addline("\t} else {")
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

    def _configure_constants_bgp(self):
        """Configure BGP constants."""
        self._addtitle("BGP Constants")

        self._addline("# Our BGP ASN")
        self._addline(f"define BGP_ASN = {self.bgp_asn};")
        self._addline("")

        self._addline("# Prefix sizes we will be using")
        self._addline(f"define BGP_PREFIX_MAXLEN4_IMPORT = {self.bgp_prefix_maxlen4_import};")
        self._addline(f"define BGP_PREFIX_MAXLEN4_EXPORT = {self.bgp_prefix_maxlen4_export};")
        self._addline(f"define BGP_PREFIX_MINLEN4_IMPORT = {self.bgp_prefix_minlen4_import};")
        self._addline(f"define BGP_PREFIX_MINLEN4_EXPORT = {self.bgp_prefix_minlen4_export};")
        # If we're in test mode, allow smaller prefixes
        if self.test_mode:
            self._addline("define BGP_PREFIX_MAXLEN6_IMPORT = 64;")
            self._addline("define BGP_PREFIX_MAXLEN6_EXPORT = 64;")
        else:
            self._addline(f"define BGP_PREFIX_MAXLEN6_IMPORT = {self.bgp_prefix_maxlen6_import};")
            self._addline(f"define BGP_PREFIX_MAXLEN6_EXPORT = {self.bgp_prefix_maxlen6_export};")
        self._addline(f"define BGP_PREFIX_MINLEN6_IMPORT = {self.bgp_prefix_minlen6_import};")
        self._addline(f"define BGP_PREFIX_MINLEN6_EXPORT = {self.bgp_prefix_minlen6_export};")

        self._addline("# Preferences")
        self._addline("define BGP_PREF_OWN = 950;")  # -20 = Originate, -10 = static, -5 = kernel
        self._addline("define BGP_PREF_CUSTOMER = 750;")
        self._addline("define BGP_PREF_PEER = 470;")
        self._addline("define BGP_PREF_ROUTESERVER = 450;")
        self._addline("define BGP_PREF_TRANSIT = 150;")
        self._addline("")

        self._addline("# Large community functions")
        # NK: IMPORTANT IF YOU CHANGE THE BELOW, UPDATE BGP_LC_STRIP
        self._addline("define BGP_LC_FUNCTION_LOCATION_ISO = 1;")
        self._addline("define BGP_LC_FUNCTION_LOCATION_UN = 2;")
        self._addline("define BGP_LC_FUNCTION_RELATION = 3;")
        self._addline("define BGP_LC_FUNCTION_NOEXPORT = 4;")
        self._addline("define BGP_LC_FUNCTION_PREPEND_ONE = 6;")
        self._addline("define BGP_LC_FUNCTION_PREPEND_TWO = 62;")
        self._addline("define BGP_LC_FUNCTION_PREPEND_THREE = 63;")
        self._addline("define BGP_LC_FUNCTION_FILTERED = 1101;")
        # NK: IMPORTANT IF THE ABOVE CHANGES UPDATE THE BELOW
        self._addline(
            "define BGP_LC_STRIP = [ (BGP_ASN, 5, *), (BGP_ASN, 7..61, *), (BGP_ASN, 64..1100, *), (BGP_ASN, 1102..65535) ];"
        )
        self._addline("")

        self._addline("# Large community noexport")
        self._addline("define BGP_LC_EXPORT_NOTRANSIT = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65412);")
        self._addline("define BGP_LC_EXPORT_NOPEER = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65413);")
        self._addline("define BGP_LC_EXPORT_NOCUSTOMER = (BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, 65414);")
        self._addline("")

        self._addline("# Large community relations")
        self._addline("define BGP_LC_RELATION_OWN = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 1);")
        self._addline("define BGP_LC_RELATION_CUSTOMER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 2);")
        self._addline("define BGP_LC_RELATION_PEER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 3);")
        self._addline("define BGP_LC_RELATION_TRANSIT = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 4);")
        self._addline("define BGP_LC_RELATION_ROUTESERVER = (BGP_ASN, BGP_LC_FUNCTION_RELATION, 5);")
        self._addline("")

        self._addline("# Large community filtered")
        self._addline("define BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 1);")
        self._addline("define BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 2);")
        self._addline("define BGP_LC_FILTERED_BOGON = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 3);")
        self._addline("define BGP_LC_FILTERED_BOGON_ASN = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 4);")
        self._addline("define BGP_LC_FILTERED_AS_PATH_TOO_LONG = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 5);")
        self._addline("define BGP_LC_FILTERED_AS_PATH_TOO_SHORT = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 6);")
        self._addline("define BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 7);")
        self._addline("define BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 8);")
        self._addline("define BGP_LC_FILTERED_PREFIX_FILTERED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 9);")
        self._addline("define BGP_LC_FILTERED_ORIGIN_AS_FILTERED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 10);")
        #        self._addline('define BGP_LC_FILTERED_PREFIX_NOT_IN_ORIGIN_AS = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 11);')
        self._addline("define BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 12);")
        self._addline("define BGP_LC_FILTERED_RPKI_UNKNOWN = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 13);")
        self._addline("define BGP_LC_FILTERED_RPKI_INVALID = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 14);")
        self._addline("define BGP_LC_FILTERED_TRANSIT_FREE_ASN = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 15);")
        self._addline("define BGP_LC_FILTERED_TOO_MANY_COMMUNITIES = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 16);")
        self._addline("define BGP_LC_FILTERED_ROUTECOLLECTOR = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 17);")
        self._addline("define BGP_LC_FILTERED_QUARANTINED = (BGP_ASN, BGP_LC_FUNCTION_FILTERED, 18);")
        self._addline("")

        self._addline("# Transit ASNs")
        self._addline("define BGP_ASNS_TRANSIT = [")
        self._addline("\t174, # Cogent")
        self._addline("\t209, # Qwest (HE carries this on IXPs IPv6 (Jul 12 2018))")
        self._addline("\t701, # UUNET")
        self._addline("\t702, # UUNET")
        self._addline("\t1239, # Sprint")
        self._addline("\t1299, # Telia")
        self._addline("\t2914, # NTT Communications")
        self._addline("\t3257, # GTT Backbone")
        self._addline("\t3320, # Deutsche Telekom AG (DTAG)")
        self._addline("\t3356, # Level3")
        self._addline("\t3549, # Level3")
        self._addline("\t3561, # Savvis / CenturyLink")
        self._addline("\t4134, # Chinanet")
        self._addline("\t5511, # Orange opentransit")
        self._addline("\t6453, # Tata Communications")
        self._addline("\t6461, # Zayo Bandwidth")
        self._addline("\t6762, # Seabone / Telecom Italia")
        self._addline("\t7018 # AT&T")
        self._addline("];")
        self._addline("")

    def _configure_functions_bgp(self):
        """Configure BGP functions."""
        self._addtitle("BGP Functions")

        self._addline("# Clear all our own BGP large communities")
        self._addline("function bgp_lc_remove_all() {")
        self._addline("\t# Remove all our own")
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, *, *)]) then {")
        self._addline('\t\tprint "[bgp_lc_remove_all] Removing own communities from ", net;', debug=True)
        self._addline("\t\tbgp_large_community.delete([(BGP_ASN, *, *)]);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Clear internal large communities")
        self._addline("function bgp_lc_remove_internal() {")
        self._addline("\t# Remove location ISO")
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_LOCATION_ISO, *)]) then {")
        self._addline('\t\tprint "[bgp_lc_remove_internal] Removing location ISO communities from ", net;', debug=True)
        self._addline("\t\tbgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_LOCATION_ISO, *)]);")
        self._addline("\t}")
        self._addline("\t# Remove location UN")
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_LOCATION_UN, *)]) then {")
        self._addline('\t\tprint "[bgp_lc_remove_internal] Removing location UN communities from ", net;', debug=True)
        self._addline("\t\tbgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_LOCATION_UN, *)]);")
        self._addline("\t}")
        self._addline("\t# Remove relations")
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_RELATION, *)]) then {")
        self._addline('\t\tprint "[bgp_lc_remove_internal] Removing relation communities from ", net;', debug=True)
        self._addline("\t\tbgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_RELATION, *)]);")
        self._addline("\t}")
        self._addline("\t# Remove filtered")
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then {")
        self._addline('\t\tprint "[bgp_lc_remove_internal] Removing filtered communities from ", net;', debug=True)
        self._addline("\t\tbgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]);")
        self._addline("\t}")
        self._addline("\t# Remove stripped communities")
        self._addline("\tif (bgp_large_community ~ BGP_LC_STRIP) then {")
        self._addline('\t\tprint "[bgp_lc_remove_internal] Removing stripped communities from ", net;', debug=True)
        self._addline("\t\tbgp_large_community.delete(BGP_LC_STRIP);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Import own routes")
        self._addline("function bgp_import_own(int local_pref_cost) {")
        self._addline(
            '\tprint "[bgp_import_own] Adding BGP_LC_RELATION_OWN to ", net, " with local pref ", '
            "BGP_PREF_OWN - local_pref_cost;",
            debug=True,
        )
        self._addline("\t# Tag route as a our own (originated and static) route")
        self._addline("\tbgp_large_community.add(BGP_LC_RELATION_OWN);")
        self._addline("\t# Set local preference")
        self._addline("\tbgp_local_pref = BGP_PREF_OWN - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import customer routes")
        self._addline("function bgp_import_customer(int peeras; int local_pref_cost) {")
        self._addline(
            '\tprint "[bgp_import_customer] Adding BGP_LC_RELATION_CUSTOMER to ", net, " with local pref ", '
            "BGP_PREF_CUSTOMER - local_pref_cost;",
            debug=True,
        )
        self._addline("\t# Tag route as a customer route")
        self._addline("\tbgp_large_community.add(BGP_LC_RELATION_CUSTOMER);")
        self._addline("\t# Set local preference")
        self._addline("\tbgp_local_pref = BGP_PREF_CUSTOMER - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import peer routes")
        self._addline("function bgp_import_peer(int peeras; int local_pref_cost) {")
        self._addline(
            '\tprint "[bgp_import_peer] Adding BGP_LC_RELATION_PEER to ", net, " with local pref ", '
            "BGP_PREF_PEER - local_pref_cost;",
            debug=True,
        )
        self._addline("\t# Tag route as a peer route")
        self._addline("\tbgp_large_community.add(BGP_LC_RELATION_PEER);")
        self._addline("\t# Set local preference")
        self._addline("\tbgp_local_pref = BGP_PREF_PEER - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import transit routes")
        self._addline("function bgp_import_transit(int peeras; int local_pref_cost) {")
        self._addline(
            '\tprint "[bgp_import_transit] Adding BGP_LC_RELATION_TRANSIT to ", net, " with local pref ", '
            "BGP_PREF_TRANSIT - local_pref_cost;",
            debug=True,
        )
        self._addline("\t# Tag route as a transit route")
        self._addline("\tbgp_large_community.add(BGP_LC_RELATION_TRANSIT);")
        self._addline("\t# Set local preference")
        self._addline("\tbgp_local_pref = BGP_PREF_TRANSIT - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import routeserver routes")
        self._addline("function bgp_import_routeserver(int peeras; int local_pref_cost) {")
        self._addline(
            '\tprint "[bgp_import_routeserver] Adding BGP_LC_RELATION_ROUTESERVER to ", net, " with local pref ", '
            "BGP_PREF_ROUTESERVER - local_pref_cost;",
            debug=True,
        )
        self._addline("\t# Tag route as a routeserver route")
        self._addline("\tbgp_large_community.add(BGP_LC_RELATION_ROUTESERVER);")
        self._addline("\t# Set local preference")
        self._addline("\tbgp_local_pref = BGP_PREF_ROUTESERVER - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Filter routecollector routes")
        self._addline("function bgp_filter_routecollector() {")
        self._addline('\tprint "[bgp_filter_routecollector] Adding BGP_FILTERED_ROUTECOLLECTOR to ", net;', debug=True)
        self._addline("\tbgp_large_community.add(BGP_LC_FILTERED_ROUTECOLLECTOR);")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 prefix size")
        self._addline("function bgp_filter_size_v4() {")
        self._addline("\tif prefix_is_longer(BGP_PREFIX_MAXLEN4_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN4_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 prefix size")
        self._addline("function bgp_filter_size_v6() {")
        self._addline("\tif prefix_is_longer(BGP_PREFIX_MAXLEN6_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN6_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 bogons")
        self._addline("function bgp_filter_bogons_v4() {")
        self._addline("\tif is_bogon4() then {")
        self._addline('\t\tprint "[bgp_filter_bogons_v4] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 bogons")
        self._addline("function bgp_filter_bogons_v6() {")
        self._addline("\tif is_bogon6() then {")
        self._addline('\t\tprint "[bgp_filter_bogons_v6] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 prefixes")
        self._addline("function bgp_filter_prefixes_v4(prefix set prefix_list) {")
        self._addline("\tif (net !~ prefix_list) then {")
        self._addline('\t\tprint "[bgp_filter_prefixes_v4] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 prefixes")
        self._addline("function bgp_filter_prefixes_v6(prefix set prefix_list) {")
        self._addline("\tif (net !~ prefix_list) then {")
        self._addline('\t\tprint "[bgp_filter_prefixes_v6] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 default route")
        self._addline("function bgp_filter_default_v4() {")
        self._addline("\tif (net = DEFAULT_ROUTE_V4) then {")
        self._addline('\t\tprint "[bgp_filter_default_v4] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 default route")
        self._addline("function bgp_filter_default_v6() {")
        self._addline("\tif (net = DEFAULT_ROUTE_V6) then {")
        self._addline('\t\tprint "[bgp_filter_default_v6] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter ASNs")
        self._addline("function bgp_filter_asns(int set asns) {")
        self._addline("\tif (bgp_path.last_nonaggregated !~ asns) then {")
        self._addline('\t\tprint "[bgp_filter_asns] Adding BGP_LC_FILTERED_ORIGIN_AS_FILTERED to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS_FILTERED);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter transit ASNs")
        self._addline("function bgp_filter_asn_transit() {")
        self._addline("\t# Filter transit ASNs")
        self._addline("\tif (bgp_path ~ BGP_ASNS_TRANSIT) then {")
        self._addline('\t\tprint "[bgp_filter_asn_transit] Adding BGP_LC_FILTERED_TRANSIT_FREE_ASN to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_TRANSIT_FREE_ASN);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter short AS paths")
        self._addline("function bgp_filter_asn_short() {")
        self._addline("\tif (bgp_path.len < 1) then {")
        self._addline('\t\tprint "[bgp_filter_asn_short] Adding BGP_LC_FILTERED_AS_PATH_TOO_SHORT to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_AS_PATH_TOO_SHORT);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter peer ASN != route first ASN")
        self._addline("function bgp_filter_asn_invalid(int peeras) {")
        self._addline("\tif (bgp_path.first != peeras) then {")
        self._addline('\t\tprint "[bgp_filter_asn_invalid] Adding BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter for QUARANTINE mode")
        self._addline("function bgp_filter_quarantine() {")
        self._addline('\tprint "[bgp_filter_quarantine] Adding BGP_LC_FILTERED_QUARANTINED to ", net;', debug=True)
        self._addline("\tbgp_large_community.add(BGP_LC_FILTERED_QUARANTINED);")
        self._addline("}")
        self._addline("")

        self._addline("# Can we export this IPv4 BGP route to the peeras?")
        self._addline("function bgp_can_export_v4(int peeras) {")
        self._addline("\t# Check for NOEXPORT large community")
        self._addline("\tif ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peeras) ~ bgp_large_community) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v4] Not exporting due to BGP_LC_FUNCTION_NOEXPORT for AS", peeras ," for ",' "net;",
            debug=True,
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\t# Validate route before export")
        self._addline("\tif prefix_is_longer(BGP_PREFIX_MAXLEN4_EXPORT) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v4] Not exporting due to prefix length > BGP_PREFIX_MAXLEN4_EXPORT for ", net;', debug=True
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN4_EXPORT) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v4] Not exporting due to prefix length < BGP_PREFIX_MINLEN4_EXPORT for ", net;', debug=True
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\tif is_bogon4() then {")
        self._addline('\t\tprint "[bgp_can_export_v4] Not exporting due to (is_bogon4 == True) for ", net;', debug=True)
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\t# If all above tests are ok, then we can")
        self._addline("\treturn true;")
        self._addline("}")
        self._addline("")

        self._addline("# Can we export this IPv6 BGP route to the peeras?")
        self._addline("function bgp_can_export_v6(int peeras) {")
        self._addline("\t# Check for NOEXPORT large community")
        self._addline("\tif ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peeras) ~ bgp_large_community) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v6] Not exporting due to BGP_LC_FUNCTION_NOEXPORT for AS", peeras ," for ",' "net;",
            debug=True,
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\t# Validate route before export")
        self._addline("\tif prefix_is_longer(BGP_PREFIX_MAXLEN6_EXPORT) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v6] Not exporting due to prefix length > BGP_PREFIX_MAXLEN6_EXPORT for ", net;', debug=True
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN6_EXPORT) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v6] Not exporting due to prefix length < BGP_PREFIX_MINLEN6_EXPORT for ", net;', debug=True
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\tif is_bogon6() then {")
        self._addline('\t\tprint "[bgp_can_export_v6] Not exporting due to (is_bogon6 == True) for ", net;', debug=True)
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\t# If all above tests are ok, then we can")
        self._addline("\treturn true;")
        self._addline("}")
        self._addline("")

        self._addline("# BGP export prepending")
        self._addline("function bgp_export_prepend(int peeras) {")
        self._addline("\t# If we are prepending three times")
        self._addline("\tif ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_THREE, peeras) ~ bgp_large_community) then {")
        self._addline('\t\tprint "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_THREE for ", net;', debug=True)
        self._addline("\t\tbgp_path.prepend(bgp_path.first);")
        self._addline("\t\tbgp_path.prepend(bgp_path.first);")
        self._addline("\t\tbgp_path.prepend(bgp_path.first);")
        self._addline("\t# If we are prepending two times")
        self._addline("\t} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_TWO, peeras) ~ bgp_large_community) then {")
        self._addline('\t\tprint "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_TWO for ", net;', debug=True)
        self._addline("\t\tbgp_path.prepend(bgp_path.first);")
        self._addline("\t\tbgp_path.prepend(bgp_path.first);")
        self._addline("\t# If we are prepending one time")
        self._addline("\t} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_ONE, peeras) ~ bgp_large_community) then {")
        self._addline('\t\tprint "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_ONE for ", net;', debug=True)
        self._addline("\t\tbgp_path.prepend(bgp_path.first);")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

    def configure(self):
        """Configure global constants."""
        self._addtitle("Global Constants")
        self._configure_defaults()
        # Check if we're adding bogons constants
        if self.need_bogons or self.need_functions:
            self._addline("")
            self._configure_bogons_asn()
            self._configure_bogons_ipv4()
            self._configure_bogons_ipv6()
        # Check if we're adding functions
        if self.need_functions:
            self._addline("")
            self._configure_functions()
        # Check if we're adding BGP constants
        if self.need_bgp:
            self._addline("")
            self._configure_constants_bgp()
            self._addline("")
            self._configure_functions_bgp()
        self._addline("")

    @property
    def need_functions(self):
        """Return if functions should be added to our output constants block."""
        return self._need_functions

    @need_functions.setter
    def need_functions(self, value):
        """Set if functions should be added to our output constants block."""
        self._need_functions = value

    @property
    def need_bogons(self):
        """Return if we need bogons or not."""
        return self._need_bogons

    @need_bogons.setter
    def need_bogons(self, value):
        """Add bogons to our output."""
        self._need_bogons = value

    @property
    def bgp(self):
        """Return BGP configuration."""
        return self._bgp

    @property
    def need_bgp(self):
        """Return BGP configuration."""
        return self.bgp["asn"] is not None

    @property
    def bgp_asn(self):
        """BGP ASN."""
        return self.bgp["asn"]

    @bgp_asn.setter
    def bgp_asn(self, value):
        """Set BGP ASN."""
        self._bgp["asn"] = value

    # PREFIX_MAXLEN4

    @property
    def bgp_prefix_maxlen4_import(self):
        """BGP PREFIX_MAXLEN4_IMPORT."""
        return self.bgp["prefix_maxlen4_import"]

    @bgp_prefix_maxlen4_import.setter
    def bgp_prefix_maxlen4_import(self, value):
        """Set BGP PREFIX_MAXLEN4_IMPORT."""
        self._bgp["prefix_maxlen4_import"] = value

    @property
    def bgp_prefix_maxlen4_export(self):
        """BGP PREFIX_MAXLEN4_EXPORT."""
        return self.bgp["prefix_maxlen4_export"]

    @bgp_prefix_maxlen4_export.setter
    def bgp_prefix_maxlen4_export(self, value):
        """Set BGP PREFIX_MAXLEN4_EXPORT."""
        self._bgp["prefix_maxlen4_export"] = value

    # PREFIX_MINLEN4

    @property
    def bgp_prefix_minlen4_import(self):
        """BGP PREFIX_MINLEN4_IMPORT."""
        return self.bgp["prefix_minlen4_import"]

    @bgp_prefix_minlen4_import.setter
    def bgp_prefix_minlen4_import(self, value):
        """SET BGP PREFIX_MINLEN4_IMPORT."""
        self._bgp["prefix_minlen4_import"] = value

    @property
    def bgp_prefix_minlen4_export(self):
        """BGP PREFIX_MINLEN4_EXPORT."""
        return self.bgp["prefix_minlen4_export"]

    @bgp_prefix_minlen4_export.setter
    def bgp_prefix_minlen4_export(self, value):
        """SET BGP PREFIX_MINLEN4_EXPORT."""
        self._bgp["prefix_minlen4_export"] = value

    # PREFIX_MAXLEN6

    @property
    def bgp_prefix_maxlen6_import(self):
        """BGP PREFIX_MAXLEN6_IMPORT."""
        return self.bgp["prefix_maxlen6_import"]

    @bgp_prefix_maxlen6_import.setter
    def bgp_prefix_maxlen6_import(self, value):
        """Set BGP PREFIX_MAXLEN6_IMPORT."""
        self._bgp["prefix_maxlen6_import"] = value

    @property
    def bgp_prefix_maxlen6_export(self):
        """BGP PREFIX_MAXLEN6_EXPORT."""
        return self.bgp["prefix_maxlen6_export"]

    @bgp_prefix_maxlen6_export.setter
    def bgp_prefix_maxlen6_export(self, value):
        """Set BGP PREFIX_MAXLEN6_EXPORT."""
        self._bgp["prefix_maxlen6_export"] = value

    # PREFIX_MINLEN6

    @property
    def bgp_prefix_minlen6_import(self):
        """BGP PREFIX_MINLEN6_IMPORT."""
        return self.bgp["prefix_minlen6_import"]

    @bgp_prefix_minlen6_import.setter
    def bgp_prefix_minlen6_import(self, value):
        """SET BGP PREFIX_MINLEN6_IMPORT."""
        self._bgp["prefix_minlen6_import"] = value

    @property
    def bgp_prefix_minlen6_export(self):
        """BGP PREFIX_MINLEN6_EXPORT."""
        return self.bgp["prefix_minlen6_export"]

    @bgp_prefix_minlen6_export.setter
    def bgp_prefix_minlen6_export(self, value):
        """SET BGP PREFIX_MINLEN6_EXPORT."""
        self._bgp["prefix_minlen6_export"] = value
