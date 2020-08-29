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
        self._addline("  0.0.0.0/8+, # RFC 1122 'this' network")
        self._addline("  10.0.0.0/8+, # RFC 1918 private space")
        if self.test_mode:
            self._addline("  # EXCLUDING DUE TO TESTING: 100.64.0.0/10+, # RFC 6598 Carrier grade nat space")
        else:
            self._addline("  100.64.0.0/10+, # RFC 6598 Carrier grade nat space")
        self._addline("  127.0.0.0/8+, # RFC 1122 localhost")
        self._addline("  169.254.0.0/16+, # RFC 3927 link local")
        self._addline("  172.16.0.0/12+, # RFC 1918 private space")
        self._addline("  192.0.2.0/24+, # RFC 5737 TEST-NET-1")
        self._addline("  192.88.99.0/24+, # RFC 7526 6to4 anycast relay")
        self._addline("  192.168.0.0/16+, # RFC 1918 private space")
        self._addline("  198.18.0.0/15+, # RFC 2544 benchmarking")
        self._addline("  198.51.100.0/24+, # RFC 5737 TEST-NET-2")
        self._addline("  203.0.113.0/24+, # RFC 5737 TEST-NET-3")
        self._addline("  224.0.0.0/4+, # multicast")
        self._addline("  240.0.0.0/4+ # reserved")
        self._addline("];")
        self._addline("")

    def _configure_bogons_ipv6(self):
        """Configure IPv6 bogons."""
        self._addline("# As per http://bgpfilterguide.nlnog.net/guides/bogon_prefixes/")
        self._addline("define BOGONS_V6 = [")
        self._addline("  ::/8+, # RFC 4291 IPv4-compatible, loopback, et al")
        self._addline("  0100::/64+, # RFC 6666 Discard-Only")
        self._addline("  2001:2::/48+, # RFC 5180 BMWG")
        self._addline("  2001:10::/28+, # RFC 4843 ORCHID")
        self._addline("  2001:db8::/32+, # RFC 3849 documentation")
        self._addline("  2002::/16+, # RFC 7526 6to4 anycast relay")
        self._addline("  3ffe::/16+, # RFC 3701 old 6bone")
        if self.test_mode:
            self._addline("  # EXCLUDING DUE TO TESTING: fc00::/7+, # RFC 4193 unique local unicast")
        else:
            self._addline("  fc00::/7+, # RFC 4193 unique local unicast")
        self._addline("  fe80::/10+, # RFC 4291 link local unicast")
        self._addline("  fec0::/10+, # RFC 3879 old site local unicast")
        self._addline("  ff00::/8+ # RFC 4291 multicast")
        self._addline("];")
        self._addline("")

    def _configure_bogons_asn(self):
        """Configure ASN bogons."""

        self._addline("# Ref http://bgpfilterguide.nlnog.net/guides/bogon_asns/")
        self._addline("define BOGON_ASNS = [")
        self._addline("  0, # RFC 7607")
        self._addline("  23456, # RFC 4893 AS_TRANS")
        self._addline("  64496..64511, # RFC 5398 and documentation/example ASNs")
        if self.test_mode:
            self._addline("  # EXCLUDING DUE TO TESTING: 64512..65534, # RFC 6996 Private ASNs")
        else:
            self._addline("  64512..65534, # RFC 6996 Private ASNs")
        self._addline("  65535, # RFC 7300 Last 16 bit ASN")
        self._addline("  65536..65551, # RFC 5398 and documentation/example ASNs")
        self._addline("  65552..131071, # RFC IANA reserved ASNs")
        self._addline("  4200000000..4294967294, # RFC 6996 Private ASNs")
        self._addline("  4294967295 # RFC 7300 Last 32 bit ASN")
        self._addline("];")

    def _configure_functions(self):
        """Configure functions."""
        self._addtitle("Global Functions")
        self._addline('# Match a prefix longer than "size".')
        self._addline("function prefix_is_longer(int size) {")
        self._addline("  if (net.len > size) then {")
        self._addline('    print "[prefix_is_longer] Matched ", net, " against size ", size;', debug=True)
        self._addline("    return true;")
        self._addline("  } else {")
        self._addline("    return false;")
        self._addline("  }")
        self._addline("}")
        self._addline("")
        self._addline('# Match a prefix shorter than "size".')
        self._addline("function prefix_is_shorter(int size) {")
        self._addline("  if (net.len < size) then {")
        self._addline('    print "[prefix_is_shorter] Matched ", net, " against size ", size;', debug=True)
        self._addline("    return true;")
        self._addline("  } else {")
        self._addline("    return false;")
        self._addline("  }")
        self._addline("}")
        self._addline("")
        self._addline("# Match on bogons for IPv4")
        self._addline("function is_bogon4() {")
        self._addline("  if (net ~ BOGONS_V4) then {")
        self._addline('    print "[is_bogon4] Matched ", net;', debug=True)
        self._addline("    return true;")
        self._addline("  } else {")
        self._addline("    return false;")
        self._addline("  }")
        self._addline("}")
        self._addline("")
        self._addline("# Match on bogons for IPv6")
        self._addline("function is_bogon6() {")
        self._addline("  if (net ~ BOGONS_V6) then {")
        self._addline('    print "[is_bogon6] Matched ", net;', debug=True)
        self._addline("    return true;")
        self._addline("  } else {")
        self._addline("    return false;")
        self._addline("  }")
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
        # If we're in test mode, we need to restrict the minimum length so we can trigger tests with 100.64.0.0/X<16
        if self.test_mode:
            self._addline("define BGP_PREFIX_MINLEN4_IMPORT = 16;")
            self._addline("define BGP_PREFIX_MINLEN4_EXPORT = 16;")
        else:
            self._addline(f"define BGP_PREFIX_MINLEN4_IMPORT = {self.bgp_prefix_minlen4_import};")
            self._addline(f"define BGP_PREFIX_MINLEN4_EXPORT = {self.bgp_prefix_minlen4_export};")

        # If we're in test mode, allow smaller prefixes
        if self.test_mode:
            self._addline("define BGP_PREFIX_MAXLEN6_IMPORT = 64;")
            self._addline("define BGP_PREFIX_MAXLEN6_EXPORT = 64;")
            self._addline("define BGP_PREFIX_MINLEN6_IMPORT = 32;")
            self._addline("define BGP_PREFIX_MINLEN6_EXPORT = 32;")
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
        self._addline("  174, # Cogent")
        self._addline("  209, # Qwest (HE carries this on IXPs IPv6 (Jul 12 2018))")
        self._addline("  701, # UUNET")
        self._addline("  702, # UUNET")
        self._addline("  1239, # Sprint")
        self._addline("  1299, # Telia")
        self._addline("  2914, # NTT Communications")
        self._addline("  3257, # GTT Backbone")
        self._addline("  3320, # Deutsche Telekom AG (DTAG)")
        self._addline("  3356, # Level3")
        self._addline("  3549, # Level3")
        self._addline("  3561, # Savvis / CenturyLink")
        self._addline("  4134, # Chinanet")
        self._addline("  5511, # Orange opentransit")
        self._addline("  6453, # Tata Communications")
        self._addline("  6461, # Zayo Bandwidth")
        self._addline("  6762, # Seabone / Telecom Italia")
        self._addline("  7018 # AT&T")
        self._addline("];")
        self._addline("")

    def _configure_functions_bgp(self):
        """Configure BGP functions."""
        self._addtitle("BGP Functions")

        self._addline("# Clear all our own BGP large communities")
        self._addline("function bgp_lc_remove_all() {")
        self._addline("  # Remove all our own")
        self._addline("  if (bgp_large_community ~ [(BGP_ASN, *, *)]) then {")
        self._addline('    print "[bgp_lc_remove_all] Removing own communities from ", net;', debug=True)
        self._addline("    bgp_large_community.delete([(BGP_ASN, *, *)]);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Clear internal large communities")
        self._addline("function bgp_lc_remove_internal() {")
        self._addline("  # Remove location ISO")
        self._addline("  if (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_LOCATION_ISO, *)]) then {")
        self._addline('    print "[bgp_lc_remove_internal] Removing location ISO communities from ", net;', debug=True)
        self._addline("    bgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_LOCATION_ISO, *)]);")
        self._addline("  }")
        self._addline("  # Remove location UN")
        self._addline("  if (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_LOCATION_UN, *)]) then {")
        self._addline('    print "[bgp_lc_remove_internal] Removing location UN communities from ", net;', debug=True)
        self._addline("    bgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_LOCATION_UN, *)]);")
        self._addline("  }")
        self._addline("  # Remove relations")
        self._addline("  if (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_RELATION, *)]) then {")
        self._addline('    print "[bgp_lc_remove_internal] Removing relation communities from ", net;', debug=True)
        self._addline("    bgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_RELATION, *)]);")
        self._addline("  }")
        self._addline("  # Remove filtered")
        self._addline("  if (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then {")
        self._addline('    print "[bgp_lc_remove_internal] Removing filtered communities from ", net;', debug=True)
        self._addline("    bgp_large_community.delete([(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]);")
        self._addline("  }")
        self._addline("  # Remove stripped communities")
        self._addline("  if (bgp_large_community ~ BGP_LC_STRIP) then {")
        self._addline('    print "[bgp_lc_remove_internal] Removing stripped communities from ", net;', debug=True)
        self._addline("    bgp_large_community.delete(BGP_LC_STRIP);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Import own routes")
        self._addline("function bgp_import_own(int local_pref_cost) {")
        self._addline(
            '  print "[bgp_import_own] Adding BGP_LC_RELATION_OWN to ", net, " with local pref ", '
            "BGP_PREF_OWN - local_pref_cost;",
            debug=True,
        )
        self._addline("  # Tag route as a our own (originated and static) route")
        self._addline("  bgp_large_community.add(BGP_LC_RELATION_OWN);")
        self._addline("  # Set local preference")
        self._addline("  bgp_local_pref = BGP_PREF_OWN - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import customer routes")
        self._addline("function bgp_import_customer(int peeras; int local_pref_cost) {")
        self._addline(
            '  print "[bgp_import_customer] Adding BGP_LC_RELATION_CUSTOMER to ", net, " with local pref ", '
            "BGP_PREF_CUSTOMER - local_pref_cost;",
            debug=True,
        )
        self._addline("  # Tag route as a customer route")
        self._addline("  bgp_large_community.add(BGP_LC_RELATION_CUSTOMER);")
        self._addline("  # Set local preference")
        self._addline("  bgp_local_pref = BGP_PREF_CUSTOMER - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import peer routes")
        self._addline("function bgp_import_peer(int peeras; int local_pref_cost) {")
        self._addline(
            '  print "[bgp_import_peer] Adding BGP_LC_RELATION_PEER to ", net, " with local pref ", '
            "BGP_PREF_PEER - local_pref_cost;",
            debug=True,
        )
        self._addline("  # Tag route as a peer route")
        self._addline("  bgp_large_community.add(BGP_LC_RELATION_PEER);")
        self._addline("  # Set local preference")
        self._addline("  bgp_local_pref = BGP_PREF_PEER - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import transit routes")
        self._addline("function bgp_import_transit(int peeras; int local_pref_cost) {")
        self._addline(
            '  print "[bgp_import_transit] Adding BGP_LC_RELATION_TRANSIT to ", net, " with local pref ", '
            "BGP_PREF_TRANSIT - local_pref_cost;",
            debug=True,
        )
        self._addline("  # Tag route as a transit route")
        self._addline("  bgp_large_community.add(BGP_LC_RELATION_TRANSIT);")
        self._addline("  # Set local preference")
        self._addline("  bgp_local_pref = BGP_PREF_TRANSIT - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Import routeserver routes")
        self._addline("function bgp_import_routeserver(int peeras; int local_pref_cost) {")
        self._addline(
            '  print "[bgp_import_routeserver] Adding BGP_LC_RELATION_ROUTESERVER to ", net, " with local pref ", '
            "BGP_PREF_ROUTESERVER - local_pref_cost;",
            debug=True,
        )
        self._addline("  # Tag route as a routeserver route")
        self._addline("  bgp_large_community.add(BGP_LC_RELATION_ROUTESERVER);")
        self._addline("  # Set local preference")
        self._addline("  bgp_local_pref = BGP_PREF_ROUTESERVER - local_pref_cost;")
        self._addline("}")
        self._addline("")

        self._addline("# Filter routecollector routes")
        self._addline("function bgp_filter_routecollector() {")
        self._addline('  print "[bgp_filter_routecollector] Adding BGP_FILTERED_ROUTECOLLECTOR to ", net;', debug=True)
        self._addline("  bgp_large_community.add(BGP_LC_FILTERED_ROUTECOLLECTOR);")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 prefix size")
        self._addline("function bgp_filter_size_v4() {")
        self._addline("  if prefix_is_longer(BGP_PREFIX_MAXLEN4_IMPORT) then {")
        self._addline('    print "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self._addline("  }")
        self._addline("  if prefix_is_shorter(BGP_PREFIX_MINLEN4_IMPORT) then {")
        self._addline('    print "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 prefix size")
        self._addline("function bgp_filter_size_v6() {")
        self._addline("  if prefix_is_longer(BGP_PREFIX_MAXLEN6_IMPORT) then {")
        self._addline('    print "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self._addline("  }")
        self._addline("  if prefix_is_shorter(BGP_PREFIX_MINLEN6_IMPORT) then {")
        self._addline('    print "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 bogons")
        self._addline("function bgp_filter_bogons_v4() {")
        self._addline("  if is_bogon4() then {")
        self._addline('    print "[bgp_filter_bogons_v4] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 bogons")
        self._addline("function bgp_filter_bogons_v6() {")
        self._addline("  if is_bogon6() then {")
        self._addline('    print "[bgp_filter_bogons_v6] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 prefixes")
        self._addline("function bgp_filter_prefixes_v4(prefix set prefix_list) {")
        self._addline("  if (net !~ prefix_list) then {")
        self._addline('    print "[bgp_filter_prefixes_v4] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 prefixes")
        self._addline("function bgp_filter_prefixes_v6(prefix set prefix_list) {")
        self._addline("  if (net !~ prefix_list) then {")
        self._addline('    print "[bgp_filter_prefixes_v6] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 default route")
        self._addline("function bgp_filter_default_v4() {")
        self._addline("  if (net = DEFAULT_ROUTE_V4) then {")
        self._addline('    print "[bgp_filter_default_v4] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);")
        self._addline("    accept;")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 default route")
        self._addline("function bgp_filter_default_v6() {")
        self._addline("  if (net = DEFAULT_ROUTE_V6) then {")
        self._addline('    print "[bgp_filter_default_v6] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);")
        self._addline("    accept;")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter ASNs")
        self._addline("function bgp_filter_asns(int set asns) {")
        self._addline("  if (bgp_path.last_nonaggregated !~ asns) then {")
        self._addline('    print "[bgp_filter_asns] Adding BGP_LC_FILTERED_ORIGIN_AS_FILTERED to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS_FILTERED);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter transit ASNs")
        self._addline("function bgp_filter_asn_transit() {")
        self._addline("  # Filter transit ASNs")
        self._addline("  if (bgp_path ~ BGP_ASNS_TRANSIT) then {")
        self._addline('    print "[bgp_filter_asn_transit] Adding BGP_LC_FILTERED_TRANSIT_FREE_ASN to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_TRANSIT_FREE_ASN);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter long AS paths")
        self._addline("function bgp_filter_asn_long() {")
        self._addline("  if (bgp_path.len > 100) then {")
        self._addline('    print "[bgp_filter_asn_long] Adding BGP_LC_FILTERED_AS_PATH_TOO_LONG to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_AS_PATH_TOO_LONG);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter short AS paths")
        self._addline("function bgp_filter_asn_short() {")
        self._addline("  if (bgp_path.len < 1) then {")
        self._addline('    print "[bgp_filter_asn_short] Adding BGP_LC_FILTERED_AS_PATH_TOO_SHORT to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_AS_PATH_TOO_SHORT);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter peer ASN != route first ASN")
        self._addline("function bgp_filter_asn_invalid(int peeras) {")
        self._addline("  if (bgp_path.first != peeras) then {")
        self._addline('    print "[bgp_filter_asn_invalid] Adding BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS to ", net;', debug=True)
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter peer != next_hop")
        self._addline("function bgp_filter_nexthop_not_peerip() {")
        self._addline("  if (from != bgp_next_hop) then {")
        self._addline(
            '    print "[bgp_filter_nexthop_not_peerip] Adding BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP to ", net;', debug=True
        )
        self._addline("    bgp_large_community.add(BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP);")
        self._addline("  }")
        self._addline("}")
        self._addline("")

        self._addline("# Filter for QUARANTINE mode")
        self._addline("function bgp_filter_quarantine() {")
        self._addline('  print "[bgp_filter_quarantine] Adding BGP_LC_FILTERED_QUARANTINED to ", net;', debug=True)
        self._addline("  bgp_large_community.add(BGP_LC_FILTERED_QUARANTINED);")
        self._addline("}")
        self._addline("")

        self._addline("# Can we export this IPv4 BGP route to the peeras?")
        self._addline("function bgp_can_export_v4(int peeras) {")
        self._addline("  # Check for NOEXPORT large community")
        self._addline("  if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peeras) ~ bgp_large_community) then {")
        self._addline(
            '    print "[bgp_can_export_v4] Not exporting due to BGP_LC_FUNCTION_NOEXPORT for AS", peeras ," for ",' "net;",
            debug=True,
        )
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  # Validate route before export")
        self._addline("  if prefix_is_longer(BGP_PREFIX_MAXLEN4_EXPORT) then {")
        self._addline(
            '    print "[bgp_can_export_v4] Not exporting due to prefix length > BGP_PREFIX_MAXLEN4_EXPORT for ", net;', debug=True
        )
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  if prefix_is_shorter(BGP_PREFIX_MINLEN4_EXPORT) then {")
        self._addline(
            '    print "[bgp_can_export_v4] Not exporting due to prefix length < BGP_PREFIX_MINLEN4_EXPORT for ", net;', debug=True
        )
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  if is_bogon4() then {")
        self._addline('    print "[bgp_can_export_v4] Not exporting due to (is_bogon4 == True) for ", net;', debug=True)
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  # If all above tests are ok, then we can")
        self._addline("  return true;")
        self._addline("}")
        self._addline("")

        self._addline("# Can we export this IPv6 BGP route to the peeras?")
        self._addline("function bgp_can_export_v6(int peeras) {")
        self._addline("  # Check for NOEXPORT large community")
        self._addline("  if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peeras) ~ bgp_large_community) then {")
        self._addline(
            '    print "[bgp_can_export_v6] Not exporting due to BGP_LC_FUNCTION_NOEXPORT for AS", peeras ," for ",' "net;",
            debug=True,
        )
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  # Validate route before export")
        self._addline("  if prefix_is_longer(BGP_PREFIX_MAXLEN6_EXPORT) then {")
        self._addline(
            '    print "[bgp_can_export_v6] Not exporting due to prefix length > BGP_PREFIX_MAXLEN6_EXPORT for ", net;', debug=True
        )
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  if prefix_is_shorter(BGP_PREFIX_MINLEN6_EXPORT) then {")
        self._addline(
            '    print "[bgp_can_export_v6] Not exporting due to prefix length < BGP_PREFIX_MINLEN6_EXPORT for ", net;', debug=True
        )
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  if is_bogon6() then {")
        self._addline('    print "[bgp_can_export_v6] Not exporting due to (is_bogon6 == True) for ", net;', debug=True)
        self._addline("    return false;")
        self._addline("  }")
        self._addline("  # If all above tests are ok, then we can")
        self._addline("  return true;")
        self._addline("}")
        self._addline("")

        self._addline("# BGP export prepending")
        self._addline("function bgp_export_prepend(int peeras) {")
        self._addline("  # If we are prepending three times")
        self._addline("  if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_THREE, peeras) ~ bgp_large_community) then {")
        self._addline('    print "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_THREE for ", net;', debug=True)
        self._addline("    bgp_path.prepend(bgp_path.first);")
        self._addline("    bgp_path.prepend(bgp_path.first);")
        self._addline("    bgp_path.prepend(bgp_path.first);")
        self._addline("  # If we are prepending two times")
        self._addline("  } else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_TWO, peeras) ~ bgp_large_community) then {")
        self._addline('    print "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_TWO for ", net;', debug=True)
        self._addline("    bgp_path.prepend(bgp_path.first);")
        self._addline("    bgp_path.prepend(bgp_path.first);")
        self._addline("  # If we are prepending one time")
        self._addline("  } else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_ONE, peeras) ~ bgp_large_community) then {")
        self._addline('    print "[bgp_export_prepend] Matched BGP_LC_FUNCTION_PREPEND_ONE for ", net;', debug=True)
        self._addline("    bgp_path.prepend(bgp_path.first);")
        self._addline("  }")
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
