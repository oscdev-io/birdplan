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

"""Bird configuration package."""

# pylint:disable=too-many-lines

from typing import List, Optional
import requests
from ..bgpq3 import BGPQ3
from . import util


class BirdConfigBase:
    """Base for our bird configuration."""

    _root: Optional["BirdConfig"]
    _parent: Optional["BirdConfigBase"]
    _config_lines: List[str]

    # pylint: disable=unused-argument
    def __init__(self, parent: Optional["BirdConfigBase"] = None, root: Optional["BirdConfig"] = None, **kwargs):
        """Initialize the object."""
        self._parent = parent

        # Setup our config lines
        if self.parent:
            self._config_lines = self.parent.config_lines
        else:
            self._config_lines = []

        # Set the root
        self._root = root
        if not self._root and parent:
            # If we didn't get anything, set it as the parent root
            self._root = parent.root

    def _addline(self, line: str, debug: bool = False):
        """
        Add line to config output.

        Parameters
        ----------
        line : str
            Line to add.
        debug : bool, optional
            Is this a debugging line? (default: False)

        """
        if debug and (not self.root or not self.root.debug):
            return
        self.config_lines.append(line)

    def _addlines(self, lines: List[str], debug: bool = False):
        """Add a list of lines."""
        if debug and (not self.root or not self.root.debug):
            return
        self.config_lines.extend(lines)

    def _addtitle(self, title: str):
        """Configure a title for a block of configuration."""
        self._addline("#")
        self._addline(f"# {title}")
        self._addline("#")
        self._addline("")

    def is_test_mode(self) -> bool:
        """Return if we're in test mode or not."""
        if self.root and self.root.test_mode:
            return True
        return False

    @property
    def root(self) -> Optional["BirdConfig"]:
        """Return our root configuration object."""
        return self._root

    @property
    def parent(self) -> Optional["BirdConfigBase"]:
        """Return our parent configuration object."""
        return self._parent

    @property
    def config_lines(self) -> List[str]:
        """Return the configuration lines."""
        return self._config_lines


class BirdConfigMain(BirdConfigBase):
    """Bird main configuration."""

    def configure(self):
        """Configure main part of the config."""
        self._addtitle("Main")

        self._addline("# Set time format for compatibility with 3rd-party programs")
        self._addline("timeformat base iso long;")
        self._addline("timeformat log iso long;")
        self._addline("timeformat protocol iso long;")
        self._addline("timeformat route iso long;")
        self._addline("")


class BirdConfigLogging(BirdConfigBase):
    """Bird logging configuration."""

    def configure(self):
        """Configure logging."""
        self._addtitle("Logging")
        # Grab logfile if we have one
        log_file = self.parent.log_file
        if log_file:
            self._addline('log "%s" all;' % log_file)
        else:
            self._addline("log stderr all;")
        # Check if we're in debug mode
        if self.parent.debug:
            self._addline("debug protocols { states, routes, filters, interfaces, events };")
        self._addline("")


class BirdConfigRouterID(BirdConfigBase):
    """Bird router ID configuration."""

    def configure(self):
        """Configure routing id."""
        self._addtitle("Router ID")
        self._addline("router id %s;" % self.parent.router_id)
        self._addline("")


class BirdConfigConstants(BirdConfigBase):
    """Bird constants configuration."""

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
        if self.root and self.root.test_mode:
            self._bgp["prefix_maxlen6_import"] = 64
            self._bgp["prefix_maxlen6_export"] = 64

    def _configure_defaults(self):
        """Configure default routes."""
        self._addline("# Default routes")
        self._addline("define DEFAULT_ROUTE_V4 = 0.0.0.0/0; # IPv4 default route")
        self._addline("define DEFAULT_ROUTE_V6 = ::/0; # IPv6 default route")
        self._addline("")

    def _configure_bogons_ipv4(self):
        """Configure IPv4 bogons."""
        self._addline("# Ref https://tools.ietf.org/html/rfc6890")
        self._addline("define BOGONS_V4 = [")
        self._addline("\t0.0.0.0/31-, # Match anything which has a shorter default route prefix")
        self._addline("\t10.0.0.0/8+, # Private range")
        if self.is_test_mode():
            self._addline("\t100.64.0.0/10+, # Carrier NAT range")
        else:
            self._addline("\t# Excluding 100.64.0.0/10+ Carrier NAT range: EXCLUDED DUE TO TESTING")
        self._addline("\t127.0.0.0/8+, # Local loopback")
        self._addline("\t169.254.0.0/16+, # Link-local")
        self._addline("\t172.16.0.0/12+, # Private range")
        self._addline("\t192.0.0.0/24+, # Reserved for IANA")
        self._addline("\t192.0.2.0/24+, # Reserved for TEST-NET-1")
        self._addline("\t192.168.0.0/16+, # Private range")
        self._addline("\t198.18.0.0/15+, # Benchmarking range")
        self._addline("\t198.51.100.0/24+, # Reserved for TEST-NET-2")
        self._addline("\t203.0.113.0/24+, # Reserved for TEST-NET-3")
        self._addline("\t224.0.0.0/4+, # Multicast reserved")
        self._addline("\t240.0.0.0/4+ # Reserved host group addresses")
        self._addline("];")
        self._addline("")

    def _configure_bogons_ipv6(self):
        """Configure IPv6 bogons."""
        self._addline("define BOGONS_V6 = [")
        self._addline("\t::/96, # IPv4-compatible IPv6 address - deprecated by RFC4291")
        self._addline("\t::/128, # Unspecified address")
        self._addline("\t::1/128, # Local host loopback address")
        self._addline("\t::ffff:0.0.0.0/96+, # IPv4-mapped addresses")
        self._addline("\t::224.0.0.0/100+, # Compatible address (IPv4 format)")
        self._addline("\t::127.0.0.0/104+, # Compatible address (IPv4 format)")
        self._addline("\t::0.0.0.0/104+, # Compatible address (IPv4 format)")
        self._addline("\t::255.0.0.0/104+, # Compatible address (IPv4 format)")
        self._addline("\t0000::/8+, # Pool used for unspecified, loopback and embedded IPv4 addresses")
        self._addline("\t0200::/7+, # OSI NSAP-mapped prefix set (RFC4548) - deprecated by RFC4048")
        self._addline("\t3ffe::/16+, # Former 6bone, now decommissioned")
        self._addline("\t2001:db8::/32+, # Reserved by IANA for special purposes and documentation")
        self._addline("\t2002:e000::/20+, # Invalid 6to4 packets (IPv4 multicast)")
        self._addline("\t2002:7f00::/24+, # Invalid 6to4 packets (IPv4 loopback)")
        self._addline("\t2002:0000::/24+, # Invalid 6to4 packets (IPv4 default)")
        self._addline("\t2002:ff00::/24+, # Invalid 6to4 packets")
        self._addline("\t2002:0a00::/24+, # Invalid 6to4 packets (IPv4 private 10.0.0.0/8 network)")
        self._addline("\t2002:ac10::/28+, # Invalid 6to4 packets (IPv4 private 172.16.0.0/12 network)")
        self._addline("\t2002:c0a8::/32+, # Invalid 6to4 packets (IPv4 private 192.168.0.0/16 network)")
        if self.is_test_mode():
            self._addline("\tfc00::/7+, # Unicast Unique Local Addresses (ULA) - RFC 4193")
        else:
            self._addline("\t# Excluding fc00::/7+ Unicast Unique Local Addresses (ULA) - RFC 4193: EXCLUDED DUE TO TESTING")
        self._addline("\tfe80::/10+, # Link-local Unicast")
        self._addline("\tfec0::/10+, # Site-local Unicast - deprecated by RFC 3879 (replaced by ULA)")
        self._addline("\tff00::/8+ # Multicast")
        self._addline("];")
        self._addline("")

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
        self._addline("define BGP_ASN = %s;" % self.bgp_asn)
        self._addline("")

        self._addline("# Prefix sizes we will be using")
        self._addline("define BGP_PREFIX_MAXLEN4_IMPORT = %s;" % self.bgp_prefix_maxlen4_import)
        self._addline("define BGP_PREFIX_MAXLEN4_EXPORT = %s;" % self.bgp_prefix_maxlen4_export)
        self._addline("define BGP_PREFIX_MINLEN4_IMPORT = %s;" % self.bgp_prefix_minlen4_import)
        self._addline("define BGP_PREFIX_MINLEN4_EXPORT = %s;" % self.bgp_prefix_minlen4_export)
        self._addline("define BGP_PREFIX_MAXLEN6_IMPORT = %s;" % self.bgp_prefix_maxlen6_import)
        self._addline("define BGP_PREFIX_MAXLEN6_EXPORT = %s;" % self.bgp_prefix_maxlen6_export)
        self._addline("define BGP_PREFIX_MINLEN6_IMPORT = %s;" % self.bgp_prefix_minlen6_import)
        self._addline("define BGP_PREFIX_MINLEN6_EXPORT = %s;" % self.bgp_prefix_minlen6_export)

        self._addline("# Preferences")
        self._addline("define BGP_PREF_OWN = 950;")  # -20 = Originate, -10 = static, -5 = kernel
        self._addline("define BGP_PREF_CUSTOMER = 750;")
        self._addline("define BGP_PREF_PEER = 450;")
        self._addline("define BGP_PREF_ROUTESERVER = 450;")
        self._addline("define BGP_PREF_TRANSIT = 150;")
        self._addline("")

        self._addline("# Large community functions")
        self._addline("define BGP_LC_FUNCTION_RELATION = 3;")
        self._addline("define BGP_LC_FUNCTION_NOEXPORT = 4;")
        self._addline("define BGP_LC_FUNCTION_PREPEND_ONE = 61;")
        self._addline("define BGP_LC_FUNCTION_PREPEND_TWO = 62;")
        self._addline("define BGP_LC_FUNCTION_PREPEND_THREE = 63;")
        self._addline("define BGP_LC_FUNCTION_FILTERED = 1101;")
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
        self._addline("\taccept;")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 prefix size")
        self._addline("function bgp_filter_size_v4() {")
        self._addline("\tif prefix_is_longer(BGP_PREFIX_MAXLEN4_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN4_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v4] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 prefix size")
        self._addline("function bgp_filter_size_v6() {")
        self._addline("\tif prefix_is_longer(BGP_PREFIX_MAXLEN6_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN6_IMPORT) then {")
        self._addline('\t\tprint "[bgp_filter_size_v6] Adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 bogons")
        self._addline("function bgp_filter_bogons_v4() {")
        self._addline("\tif is_bogon4() then {")
        self._addline('\t\tprint "[bgp_filter_bogons_v4] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 bogons")
        self._addline("function bgp_filter_bogons_v6() {")
        self._addline("\tif is_bogon6() then {")
        self._addline('\t\tprint "[bgp_filter_bogons_v6] Adding BGP_FILTERED_BOGON to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_BOGON);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv4 prefixes")
        self._addline("function bgp_filter_prefixes_v4(prefix set prefix_list) {")
        self._addline("\tif (net !~ prefix_list) then {")
        self._addline('\t\tprint "[bgp_filter_prefixes_v4] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter IPv6 prefixes")
        self._addline("function bgp_filter_prefixes_v6(prefix set prefix_list) {")
        self._addline("\tif (net !~ prefix_list) then {")
        self._addline('\t\tprint "[bgp_filter_prefixes_v6] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);")
        self._addline("\t\taccept;")
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
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter transit ASNs")
        self._addline("function bgp_filter_asn_transit() {")
        self._addline("\t# Filter transit ASNs")
        self._addline("\tif (bgp_path ~ BGP_ASNS_TRANSIT) then {")
        self._addline('\t\tprint "[bgp_filter_asn_transit] Adding BGP_LC_FILTERED_TRANSIT_FREE_ASN to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_TRANSIT_FREE_ASN);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter short AS paths")
        self._addline("function bgp_filter_asn_short() {")
        self._addline("\tif (bgp_path.len < 1) then {")
        self._addline('\t\tprint "[bgp_filter_asn_short] Adding BGP_LC_FILTERED_AS_PATH_TOO_SHORT to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_AS_PATH_TOO_SHORT);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter peer ASN != route first ASN")
        self._addline("function bgp_filter_asn_invalid(int peeras) {")
        self._addline("\tif (bgp_path.first != peeras) then {")
        self._addline('\t\tprint "[bgp_filter_asn_invalid] Adding BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS to ", net;', debug=True)
        self._addline("\t\tbgp_large_community.add(BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS);")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("}")
        self._addline("")

        self._addline("# Filter for QUARANTINE mode")
        self._addline("function bgp_filter_quarantine() {")
        self._addline('\tprint "[bgp_filter_quarantine] Adding BGP_LC_FILTERED_QUARANTINED to ", net;', debug=True)
        self._addline("\tbgp_large_community.add(BGP_LC_FILTERED_QUARANTINED);")
        self._addline("\taccept;")
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
            '\t\tprint "[bgp_can_export_v4] Not exporting due to prefix lengh > BGP_PREFIX_MAXLEN4_EXPORT for ", net;', debug=True
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN4_EXPORT) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v4] Not exporting due to prefix lengh < BGP_PREFIX_MINLEN4_EXPORT for ", net;', debug=True
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
            '\t\tprint "[bgp_can_export_v6] Not exporting due to prefix lengh > BGP_PREFIX_MAXLEN6_EXPORT for ", net;', debug=True
        )
        self._addline("\t\treturn false;")
        self._addline("\t}")
        self._addline("\tif prefix_is_shorter(BGP_PREFIX_MINLEN6_EXPORT) then {")
        self._addline(
            '\t\tprint "[bgp_can_export_v6] Not exporting due to prefix lengh < BGP_PREFIX_MINLEN6_EXPORT for ", net;', debug=True
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


class BirdConfigMaster(BirdConfigBase):
    """BIRD master table configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Are we going to export routes to the kernel
        self._export_kernel = {
            "static": True,
            "rip": True,
            "ospf": True,
            "bgp": True,
        }

    def configure(self):
        """Configure the master tables."""
        self._addtitle("Master Tables")

        # Setup filters
        self._master_to_kernel_export_filter(4)
        self._master_to_kernel_export_filter(6)

        self._master_to_kernel_import_filter(4)
        self._master_to_kernel_import_filter(6)

        # Configure pipe from kernel table to master table
        kernel_master_pipe = BirdConfigProtocolPipe(
            self, table_from="master", table_to="kernel", table_export_filtered=True, table_import_filtered=True
        )
        kernel_master_pipe.configure()
        self._addline("")

    def _master_to_kernel_import_filter(self, ipv):
        """Master to kernel import filter setup."""
        # Configure import filter to master table
        self._addline("filter f_master_kernel%s_import {" % ipv)
        self._addline("\t# Accept all routes from the kernel, always")
        self._addline("\tif (source = RTS_INHERIT) then {")
        self._addline("\t\taccept;")
        self._addline("\t}")
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _master_to_kernel_export_filter(self, ipv):
        """Master to kernel export filter setup."""
        # Configure export filter to master table
        self._addline("filter f_master_kernel%s_export {" % ipv)

        if self.export_kernel_static:
            self._addline("\t# Export static routes to kernel")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        if self.export_kernel_rip:
            self._addline("\t# Export RIP routes to kernel")
            self._addline("\tif (source = RTS_RIP) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        if self.export_kernel_ospf:
            self._addline("\t# Export OSPF routes to kernel")
            # NK: We cannot seem to filter out the device routes
            self._addline("\tif (source ~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2]) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        if self.export_kernel_bgp:
            self._addline("\t# Export BGP routes to kernel")
            self._addline("\tif (source = RTS_BGP) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")

        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    @property
    def export_kernel_static(self):
        """Return if we're exporting static to kernel."""
        return self._export_kernel["static"]

    @export_kernel_static.setter
    def export_kernel_static(self, value):
        """Set if we're exporting static routes to kernel."""
        self._export_kernel["static"] = value

    @property
    def export_kernel_rip(self):
        """Return if we're exporting RIP to kernel."""
        return self._export_kernel["rip"]

    @export_kernel_rip.setter
    def export_kernel_rip(self, value):
        """Set if we're exporting RIP routes to kernel."""
        self._export_kernel["rip"] = value

    @property
    def export_kernel_ospf(self):
        """Return if we're exporting OSPF to kernel."""
        return self._export_kernel["ospf"]

    @export_kernel_ospf.setter
    def export_kernel_ospf(self, value):
        """Set if we're exporting OSPF routes to kernel."""
        self._export_kernel["ospf"] = value

    @property
    def export_kernel_bgp(self):
        """Return if we're exporting BGP to kernel."""
        return self._export_kernel["bgp"]

    @export_kernel_bgp.setter
    def export_kernel_bgp(self, value):
        """Set if we're exporting BGP routes to kernel."""
        self._export_kernel["bgp"] = value


class BirdConfigProtocolDevice(BirdConfigBase):
    """Bird device protocol configuration."""

    def configure(self):
        """Configure the device protocol."""
        self._addtitle("Device Protocol")
        self._addline("protocol device {")
        self._addline('\tdescription "Device protocol";')
        self._addline("")
        self._addline("\tscan time 10;")
        self._addline("};")
        self._addline("")


class BirdConfigProtocolKernel(BirdConfigBase):
    """Bird kernel protocol configuration."""

    def configure(self):
        """Configure the kernel protocol."""
        self._addtitle("Kernel Protocol")

        # Setup kernel tables
        self._addline("ipv4 table t_kernel4;")
        self._addline("ipv6 table t_kernel6;")

        # Configure the kernel protocol
        self._configure_protocol_kernel(4)
        self._configure_protocol_kernel(6)

        self._addline("")

    def _configure_protocol_kernel(self, ipv):
        """Protocol configuration."""
        self._addline("")
        self._addline("protocol kernel kernel%s {" % ipv)
        self._addline('\tdescription "Kernel protocol for IPv%s";' % ipv)
        self._addline("")
        self._addline("\tmetric 600; # Set the BIRD metric to be used when creating kernel routes to fall in line with our OS")
        self._addline("\tlearn; # Learn routes from the kernel")
        self._addline("\tpersist; # Dont remove routes on BIRD shutdown")
        self._addline("\tmerge paths on; # Merge similar BGP paths into a multi-hop")
        self._addline("")
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_kernel%s;" % ipv)
        self._addline("")
        self._addline("\t\texport all;")
        self._addline("\t\timport all;")
        self._addline("\t};")
        self._addline("};")


class BirdConfigProtocolStatic(BirdConfigBase):
    """Bird static protocol configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Initialize our route list
        self._static_routes = {}

    def add_route(self, route):
        """Add static route."""
        (prefix, route_info) = route.split(" ", 1)
        self._static_routes[prefix] = route_info

    def configure(self):
        """Configure the static protocol."""
        # Work out static v4 and v6 routes
        routes_ipv4 = []
        routes_ipv6 = []
        for prefix in sorted(self.static_routes.keys()):
            info = self.static_routes[prefix]
            if "." in prefix:
                routes_ipv4.append("%s %s" % (prefix, info))
            elif ":" in prefix:
                routes_ipv6.append("%s %s" % (prefix, info))
            else:
                raise RuntimeError('The static route "%s" is odd' % prefix)

        self._addtitle("Static Protocol")

        self._addline("ipv4 table t_static4;")
        self._addline("ipv6 table t_static6;")
        self._addline("")
        self._addline("protocol static static4 {")
        self._addline('\tdescription "Static protocol for IPv4";')
        self._addline("")
        # FIXME - remove at some stage # pylint:disable=fixme
        self._addline("debug all;")
        self._addline("")
        self._addline("\tipv4 {")
        self._addline("\t\ttable t_static4;")
        self._addline("\t\texport none;")
        self._addline("\t\timport all;")
        self._addline("\t};")
        # If we have IPv4 routes
        if routes_ipv4:
            self._addline("")
            # Output the routes
            for route in routes_ipv4:
                self._addline("\troute %s;" % route)
        self._addline("};")
        self._addline("")
        self._addline("protocol static static6 {")
        self._addline('\tdescription "Static protocol for IPv6";')
        self._addline("")
        self._addline("\tipv6 {")
        self._addline("\t\ttable t_static6;")
        self._addline("\t\texport none;")
        self._addline("\t\timport all;")
        self._addline("\t};")
        # If we have IPv6 routes
        if routes_ipv6:
            self._addline("")
            # Output the routes
            for route in routes_ipv6:
                self._addline("\troute %s;" % route)
        self._addline("};")
        self._addline("")

        # Configure static route pipe to the kernel
        static_kernel_pipe = BirdConfigProtocolPipe(
            self, table_from="static", table_to="master", table_export="all", table_import="none"
        )
        static_kernel_pipe.configure()

    @property
    def static_routes(self):
        """Return our static routes."""
        return self._static_routes


class BirdConfigProtocolPipe(BirdConfigBase):
    """Bird pipe protocol configuration."""

    def __init__(self, parent, name="", **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Add a suffix if we have a name
        if name:
            self._name_suffix = "_%s" % name
        else:
            self._name_suffix = ""

        # Grab table information
        self._table_from = kwargs.get("table_from")
        self._table_to = kwargs.get("table_to")
        self._table_export = kwargs.get("table_export", None)
        self._table_import = kwargs.get("table_import", None)
        self._table_export_filtered = kwargs.get("table_export_filtered", False)
        self._table_import_filtered = kwargs.get("table_import_filtered", False)

        # Are we excluding anything?
        self._has_ipv4 = kwargs.get("has_ipv4", True)
        self._has_ipv6 = kwargs.get("has_ipv6", True)

    def configure(self):
        """Create a pipe protocol."""

        if self.has_ipv4:
            self._addline("protocol pipe p_%s4_to_%s4%s {" % (self.table_from, self.table_to, self.name_suffix))
            self._addline('\tdescription "Pipe from %s4 to %s4%s";' % (self.t_table_from, self.t_table_to, self.name_suffix))
            self._addline("")
            self._addline("\ttable %s4;" % self.t_table_from)
            self._addline("\tpeer table %s4%s;" % (self.t_table_to, self.name_suffix))
            self._addline("")
            # Check if we're doing export filtering
            if self.table_export_filtered:
                self._addline("\texport filter f_%s_%s4_export;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\texport %s;" % self.table_export)
            # Check if we're doing import filtering
            if self.table_import_filtered:
                self._addline("\timport filter f_%s_%s4_import;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\timport %s;" % self.table_import)
            self._addline("};")
            self._addline("")

        if self.has_ipv6:
            self._addline("protocol pipe p_%s6_to_%s6%s {" % (self.table_from, self.table_to, self.name_suffix))
            self._addline('\tdescription "Pipe from %s6 to %s6%s";' % (self.t_table_from, self.t_table_to, self.name_suffix))
            self._addline("")
            self._addline("\ttable %s6;" % self.t_table_from)
            self._addline("\tpeer table %s6%s;" % (self.t_table_to, self.name_suffix))
            self._addline("")
            # Check if we're doing export filtering
            if self.table_export_filtered:
                self._addline("\texport filter f_%s_%s6_export;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\texport %s;" % self.table_export)
            # Check if we're doing import filtering
            if self.table_import_filtered:
                self._addline("\timport filter f_%s_%s6_import;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\timport %s;" % self.table_import)
            self._addline("};")
            self._addline("")

    @property
    def has_ipv4(self):
        """Return if we have IPv4."""
        return self._has_ipv4

    @property
    def has_ipv6(self):
        """Return if we have IPv6."""
        return self._has_ipv6

    @property
    def name_suffix(self):
        """Return our name suffix."""
        return self._name_suffix

    @property
    def t_table_from(self):
        """Return table_from, some tables don't have t_ prefixes."""
        if self._table_from == "master":
            return self._table_from
        return "t_%s" % self._table_from

    @property
    def t_table_to(self):
        """Return table_to, some tables don't have t_ prefixes."""
        if self._table_to == "master":
            return self._table_to
        return "t_%s" % self._table_to

    @property
    def table_from(self):
        """Return table_from, raw."""
        return self._table_from

    @property
    def table_to(self):
        """Return table_to, raw."""
        return self._table_to

    @property
    def table_export(self):
        """Return that state of us exporting the table."""
        return self._table_export

    @property
    def table_import(self):
        """Return that state of us importing the table."""
        return self._table_import

    @property
    def table_export_filtered(self):
        """Return that state of us exporting the table filtered."""
        return self._table_export_filtered

    @property
    def table_import_filtered(self):
        """Return that state of us importing the table filtered."""
        return self._table_import_filtered


class BirdConfigProtocolDirect(BirdConfigBase):
    """Bird direct protocol configuration."""

    def __init__(self, parent, name="", **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Add a suffix if we have a name
        if name:
            self._name_suffix = "_%s" % name
        else:
            self._name_suffix = ""

        # Grab the list of interfaces we need
        self._interfaces = kwargs.get("interfaces", [])

    def configure(self):
        """Configure the direct protocol."""
        # If we're not handling a specific direct protocol, add a title
        if not self.name_suffix:
            self._addtitle("Direct Protocol")

        # If we have a list of interfaces, create the config lines
        interface_lines = []
        if self.interfaces:
            # Create list of quoted interfaces
            interface_list = []
            for interface in self.interfaces:
                interface_list.append('"%s"' % interface)
            # Drop in a comma between them
            interface_str = ", ".join(interface_list)
            interface_lines.append("")
            interface_lines.append("\tinterface %s;" % interface_str)

        self._addline("ipv4 table t_direct4%s;" % self.name_suffix)
        self._addline("ipv6 table t_direct6%s;" % self.name_suffix)
        self._addline("")

        self._setup_protocol(4, interface_lines)
        self._setup_protocol(6, interface_lines)

    def _setup_protocol(self, ipv, lines):
        self._addline("protocol direct direct%s%s {" % (ipv, self.name_suffix))
        self._addline('\tdescription "Direct protocol for IPv%s";' % ipv)
        self._addline("")
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_direct%s%s;" % (ipv, self.name_suffix))
        self._addline("")
        self._addline("\t\texport none;")
        self._addline("\t\timport all;")
        self._addline("\t};")
        self._addlines(lines)
        self._addline("};")
        self._addline("")

    @property
    def name_suffix(self):
        """Return our name suffix."""
        return self._name_suffix

    @property
    def interfaces(self):
        """Return our interfaces."""
        return self._interfaces


class BirdConfigProtocolRIP(BirdConfigBase):
    """Bird RIP protocol configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Interfaces
        self._rip_interfaces = {}

        # Some tunables...
        self._rip_accept = {
            "default": False,
        }

        # RIP route redistribution
        self._rip_redistribute = {
            "connected": {},
            "static": False,
            "kernel": False,
            "default": False,
            "rip": True,
        }

    def _interface_config(self):
        """Generate interface configuration."""

        interface_lines = []
        # Loop with interfaces
        for interface_name in sorted(self.interfaces.keys()):
            interface = self.interfaces[interface_name]
            interface_lines.append('\tinterface "%s" {' % interface_name)
            # Loop with config items
            for config_item in interface:
                # Loop with key-value pairs
                for key, value in config_item.items():
                    if (key == "update-time") and value:
                        interface_lines.append("\t\tupdate time %s;" % value)
                    else:
                        interface_lines.append("\t\t%s %s;" % (key, value))
            interface_lines.append("\t};")

        return interface_lines

    def _setup_protocol(self, ipv):
        """Set up RIP protocol."""
        if ipv == 4:
            self._addline("protocol rip rip%s {" % ipv)
        elif ipv == 6:
            self._addline("protocol rip ng rip%s {" % ipv)
        self._addline('\tdescription "RIP protocol for IPv%s";' % ipv)
        self._addline("")
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_rip%s;" % ipv)
        self._addline("")
        self._addline("\t\texport filter f_rip_export%s;" % ipv)
        self._addline("\t\timport filter f_rip_import%s;" % ipv)
        self._addline("")
        self._addline("\t};")
        self._addline("")
        self._addlines(self._interface_config())
        self._addline("};")

    def _rip_export_filter(self, ipv):
        """RIP export filter setup."""
        self._addline("filter f_rip_export%s {" % ipv)
        # Redistribute the default route
        if not self.redistribute_default:
            self._addline("\t# Reject redistribution of the default route")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute connected
        if self.redistribute_connected:
            self._addline("\t# Redistribute connected")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute_static:
            self._addline("\t# Redistribute static routes")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self._addline("\t# Redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute RIP routes
        if self.redistribute_rip:
            self._addline("\t# Redistribute RIP routes")
            self._addline("\tif (source = RTS_RIP) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else reject
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _rip_import_filter(self, ipv):
        """RIP import filter setup."""
        # Configure import filter
        self._addline("filter f_rip_import%s {" % ipv)
        # Accept all inbound routes into the table
        self._addline("\t# Import all RIP routes by default")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

    def _rip_to_master_export_filter(self, ipv):
        """RIP to master export filter setup."""
        # Configure export filter to master4
        self._addline("filter f_rip_master%s_export {" % ipv)
        # Check if we accept the default route, if not block it
        if not self.accept_default:
            self._addline("\t# Do not export default route to master (no accept:default)")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Accept only RIP routes into the master table
        self._addline("\t# Only export RIP routes to the master table")
        self._addline("\tif (source = RTS_RIP) then {")
        self._addline("\t\taccept;")
        self._addline("\t}")
        # Default to reject
        self._addline("\t# Reject everything else;")
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _rip_to_master_import_filter(self, ipv):
        """RIP to master import filter setup."""
        # Configure import filter to master table
        self._addline("filter f_rip_master%s_import {" % ipv)
        # Redistribute the default route
        if not self.redistribute_default:
            self._addline("\t# Deny import of default route into RIP (no redistribute_default)")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute connected
        if self.redistribute_connected:
            self._addline("\t# Import RTS_DEVICE routes into RIP (redistribute_connected)")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute_static:
            self._addline("\t# Import RTS_STATIC routes into RIP (redistribute_static)")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self._addline("\t# Import RTS_INHERIT routes (kernel routes) into RIP (redistribute_kernel)")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else accept
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def configure(self):
        """Configure the RIP protocol."""

        # If we don't have any configuration, just abort
        if not self.interfaces:
            return

        self._addtitle("RIP Protocol")
        self._addline("# RIP Tables")
        self._addline("ipv4 table t_rip4;")
        self._addline("ipv6 table t_rip6;")
        self._addline("")

        # RIP export filters
        self._rip_export_filter(4)
        self._rip_export_filter(6)

        # RIP import filters
        self._rip_import_filter(4)
        self._rip_import_filter(6)

        # RIP to master export filters
        self._rip_to_master_export_filter(4)
        self._rip_to_master_export_filter(6)

        # RIP to master import filters
        self._rip_to_master_import_filter(4)
        self._rip_to_master_import_filter(6)

        # Setup the protocol
        self._setup_protocol(4)
        self._setup_protocol(6)

        # Configure pipe from RIP to the master routing table
        rip_master_pipe = BirdConfigProtocolPipe(
            self, table_from="rip", table_to="master", table_export_filtered=True, table_import_filtered=True
        )
        rip_master_pipe.configure()

        # Check if we're redistributing connected routes, if we are, create the protocol and pipe
        if self.redistribute_connected:
            if "interfaces" not in self.redistribute_connected:
                raise RuntimeError('RIP redistribute connected requires a list in item "interfaces" to match interface names')
            # Add direct protocol for redistribution of connected routes
            rip_direct_protocol = BirdConfigProtocolDirect(self, name="rip", interfaces=self.redistribute_connected["interfaces"])
            rip_direct_protocol.configure()
            # Add pipe
            rip_direct_pipe = BirdConfigProtocolPipe(
                self, name="rip", description="RIP", table_from="rip", table_to="direct", table_export="none", table_import="all"
            )
            rip_direct_pipe.configure()

    def add_interface(self, interface_name, interface_config):
        """Add interface to RIP."""
        # Make sure the interface exists
        if interface_name not in self.interfaces:
            self._rip_interfaces[interface_name] = []
        # Grab the config so its easier to work with below
        config = self.interfaces[interface_name]
        # Work through supported configuration
        for item in interface_config:
            for key, value in item.items():
                if key in ("metric", "update-time"):
                    config.append({key: value})
                else:
                    raise RuntimeError(
                        'The RIP config for interface "%s" item "%s" hasnt been added to Salt yet' % (interface_name, key)
                    )

    @property
    def accept_default(self):
        """Return if we will accept the default route if we get it via RIP."""
        return self._rip_accept["default"]

    @accept_default.setter
    def accept_default(self, value):
        """Set we will accept the default route if we get it via RIP."""
        self._rip_accept["default"] = value

    @property
    def redistribute_connected(self):
        """Return if we redistribute connected routes."""
        return self._rip_redistribute["connected"]

    @redistribute_connected.setter
    def redistribute_connected(self, value):
        """Set redistribute connected routes."""
        self._rip_redistribute["connected"] = value

    @property
    def redistribute_static(self):
        """Return if we redistribute static routes."""
        return self._rip_redistribute["static"]

    @redistribute_static.setter
    def redistribute_static(self, value):
        """Set redistribute static routes."""
        self._rip_redistribute["static"] = value

    @property
    def redistribute_kernel(self):
        """Return if we redistribute kernel routes."""
        return self._rip_redistribute["kernel"]

    @redistribute_kernel.setter
    def redistribute_kernel(self, value):
        """Set redistribute kernel routes."""
        self._rip_redistribute["kernel"] = value

    @property
    def redistribute_default(self):
        """Return if we redistribute the default route."""
        return self._rip_redistribute["default"]

    @redistribute_default.setter
    def redistribute_default(self, value):
        """Set redistribute the default route."""
        self._rip_redistribute["default"] = value

    @property
    def redistribute_rip(self):
        """Return if we redistribute RIP routes."""
        return self._rip_redistribute["rip"]

    @redistribute_rip.setter
    def redistribute_rip(self, value):
        """Set redistribute RIP routes."""
        self._rip_redistribute["rip"] = value

    @property
    def interfaces(self):
        """Return RIP interfaces."""
        return self._rip_interfaces


class BirdConfigProtocolOSPF(BirdConfigBase):
    """Bird OSPF protocol configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Areas and interfaces
        self._ospf_areas = {}
        self._ospf_interfaces = {}

        # Some tunables...
        self._ospf_accept = {
            "default": False,
        }

        # OSPF route redistribution
        self._ospf_redistribute = {
            "connected": {},
            "static": False,
            "kernel": False,
            "default": False,
        }

    def _area_config(self):
        """Generate area configuration."""

        area_lines = []
        for area_name in self.interfaces:
            area_lines.append("\tarea %s {" % area_name)
            # Loop with area config items
            for config_item in self.areas[area_name]:
                # Loop with key-value pairs
                for key, value in config_item.items():
                    area_lines.append("\t\t%s %s;" % (key, value))
            # Loop with interfaces
            for interface_name in sorted(self.interfaces[area_name].keys()):
                interface = self.interfaces[area_name][interface_name]
                area_lines.append('\t\tinterface "%s" {' % interface_name)
                # Loop with config items
                for config_item in interface:
                    # Loop with key-value pairs
                    for key, value in config_item.items():
                        if (key == "stub") and value:
                            area_lines.append("\t\t\t%s;" % key)
                        else:
                            area_lines.append("\t\t\t%s %s;" % (key, value))
                area_lines.append("\t\t};")
            # End off area
            area_lines.append("\t};")

        return area_lines

    def _setup_protocol(self, ipv):
        self._addline("protocol ospf v3 ospf%s {" % ipv)
        self._addline('\tdescription "OSPF protocol for IPv%s";' % ipv)
        self._addline("")
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_ospf%s;" % ipv)
        self._addline("")
        self._addline("\t\texport filter f_ospf_export%s;" % ipv)
        self._addline("\t\timport filter f_ospf_import%s;" % ipv)
        self._addline("")
        self._addline("\t};")
        self._addline("")
        self._addlines(self._area_config())
        self._addline("};")
        self._addline("")

    def _ospf_export_filter(self, ipv):
        """OSPF export filter setup."""

        self._addline("filter f_ospf_export%s {" % ipv)
        # Redistribute the default route
        if not self.redistribute_default:
            self._addline("\t# Reject redistribution of the default route")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute connected
        if self.redistribute_connected:
            self._addline("\t# Redistribute connected")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute_static:
            self._addline("\t# Redistribute static routes")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self._addline("\t# Redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else reject
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _ospf_import_filter(self, ipv):
        """OSPF import filter setup."""
        # Configure import4 filter
        self._addline("filter f_ospf_import%s {" % ipv)
        # Accept all inbound routes into the t_ospf4 table
        self._addline("\t# Import all OSPF routes by default")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

    def _ospf_to_master_export_filter(self, ipv):
        """OSPF to master export filter setup."""
        # Configure export filter to master table
        self._addline("filter f_ospf_master%s_export {" % ipv)
        # Check if we accept the default route, if not block it
        if not self.accept_default:
            self._addline("\t# Do not export default route to master (no accept:default)")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Accept only OSPF routes into the master table
        self._addline("\t# Only export OSPF routes to the master table")
        # NK: We cannot seem to filter out the device routes
        self._addline("\tif (source ~ [RTS_OSPF, RTS_OSPF_IA, RTS_OSPF_EXT1, RTS_OSPF_EXT2]) then {")
        self._addline("\t\taccept;")
        self._addline("\t}")
        # Default to reject
        self._addline("\t# Reject everything else;")
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _ospf_to_master_import_filter(self, ipv):
        """OSPF to master import filter setup."""
        # Configure import filter to master table
        self._addline("filter f_ospf_master%s_import {" % ipv)
        # Redistribute the default route
        if not self.redistribute_default:
            self._addline("\t# Deny import of default route into OSPF (no redistribute_default)")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute connected
        if self.redistribute_connected:
            self._addline("\t# Import RTS_DEVICE routes into OSPF (redistribute_connected)")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute_static:
            self._addline("\t# Import RTS_STATIC routes into OSPF (redistribute_static)")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self._addline("\t# Import RTS_INHERIT routes (kernel routes) into OSPF (redistribute_kernel)")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else accept
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def configure(self):
        """Configure the OSPF protocol."""

        # If we don't have any configuration, just abort
        if not self.areas:
            return

        self._addtitle("OSPF Protocol")
        self._addline("# OSPF Tables")
        self._addline("ipv4 table t_ospf4;")
        self._addline("ipv6 table t_ospf6;")
        self._addline("")

        # OSPF export filters
        self._ospf_export_filter(4)
        self._ospf_export_filter(6)

        # OSPF import filters
        self._ospf_import_filter(4)
        self._ospf_import_filter(6)

        # OSPF to master export filters
        self._ospf_to_master_export_filter(4)
        self._ospf_to_master_export_filter(6)

        # OSPF to master import filters
        self._ospf_to_master_import_filter(4)
        self._ospf_to_master_import_filter(6)

        # OSPF protocol configuration
        # FIXME - assigned but not used?  # pylint:disable=fixme
        # area_lines = self._area_config()
        self._setup_protocol(4)
        self._setup_protocol(6)

        # Configure pipe from OSPF to the master routing table
        ospf_master_pipe = BirdConfigProtocolPipe(
            self, table_from="ospf", table_to="master", table_export_filtered=True, table_import_filtered=True
        )
        ospf_master_pipe.configure()

        # Check if we're redistributing connected routes, if we are, create the protocol and pipe
        if self.redistribute_connected:
            if "interfaces" not in self.redistribute_connected:
                raise RuntimeError('OSPF redistribute connected requires a list in item "interfaces" to match interface names')
            # Add direct protocol for redistribution of connected routes
            ospf_direct_protocol = BirdConfigProtocolDirect(self, name="ospf", interfaces=self.redistribute_connected["interfaces"])
            ospf_direct_protocol.configure()
            # Add pipe
            ospf_direct_pipe = BirdConfigProtocolPipe(
                self,
                name="ospf",
                descospftion="ospf",
                table_from="ospf",
                table_to="direct",
                table_export="none",
                table_import="all",
            )
            ospf_direct_pipe.configure()

    def add_area(self, area_name, area_config=None):
        """Add area to OSPF."""
        # Make sure the area exists
        if area_name not in self.areas:
            self._ospf_areas[area_name] = area_config

    def add_interface(self, area_name, interface_name, interface_config):
        """Add interface to OSPF."""
        # Make sure the area exists
        if area_name not in self.interfaces:
            self._ospf_interfaces[area_name] = {}
        # Make sure the interface exists
        if interface_name not in self.interfaces[area_name]:
            self._ospf_interfaces[area_name][interface_name] = []
        # Grab the config so its easier to work with below
        config = self.interfaces[area_name][interface_name]
        # Work through supported configuration
        for key, value in interface_config.items():
            if key in ("hello", "wait"):
                config.append({key: value})
            elif key == "stub":
                if not value:
                    RuntimeError('The OSPF default config for interface "%s" item "stub" is "false".' % interface_name)
                config.append({key: value})
            else:
                raise RuntimeError(
                    'The OSPF config for interface "%s" item "%s" hasnt been added to Salt yet' % (interface_name, key)
                )

    @property
    def accept_default(self):
        """Return if we accept the default route if we get it via OSPF."""
        return self._ospf_accept["default"]

    @accept_default.setter
    def accept_default(self, value):
        """Set if we accept the default route if we get it via OSPF."""
        self._ospf_accept["default"] = value

    @property
    def redistribute_connected(self):
        """Return if we redistribute connected routes."""
        return self._ospf_redistribute["connected"]

    @redistribute_connected.setter
    def redistribute_connected(self, value):
        """Set redistribute connected routes."""
        self._ospf_redistribute["connected"] = value

    @property
    def redistribute_static(self):
        """Return if we redistribute static routes."""
        return self._ospf_redistribute["static"]

    @redistribute_static.setter
    def redistribute_static(self, value):
        """Set if we redistribute static routes."""
        self._ospf_redistribute["static"] = value

    @property
    def redistribute_kernel(self):
        """Return if we redistribute kernel routes."""
        return self._ospf_redistribute["kernel"]

    @redistribute_kernel.setter
    def redistribute_kernel(self, value):
        """Set if we redistribute kernel routes."""
        self._ospf_redistribute["kernel"] = value

    @property
    def redistribute_default(self):
        """Return if we redistribute the default route."""
        return self._ospf_redistribute["default"]

    @redistribute_default.setter
    def redistribute_default(self, value):
        """Set if we redistribute the default route."""
        self._ospf_redistribute["default"] = value

    @property
    def areas(self):
        """Return OSPF areas."""
        return self._ospf_areas

    @property
    def interfaces(self):
        """Return OSPF interfaces."""
        return self._ospf_interfaces


class BirdConfigProtocolBGP(BirdConfigBase):
    """Bird BGP protocol configuration."""

    def __init__(self, parent, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # BGP
        self._bgp_asn = None
        self._bgp_peers = {}
        # Route reflector cluster ID
        self._bgp_rr_cluster_id = None
        # Routes originated from BGP
        self._bgp_originate_routes = {}
        # Some tunables...
        self._bgp_accept = {
            "default": False,
        }
        # BGP route redistribution
        self._bgp_import = {
            "connected": {},
            "static": False,
            "kernel": False,
        }

    def _configure_originate(self):
        # Work out static v4 and v6 routes
        routes_ipv4 = []
        routes_ipv6 = []
        for prefix in sorted(self._bgp_originate_routes.keys()):
            info = self._bgp_originate_routes[prefix]
            if "." in prefix:
                routes_ipv4.append("%s %s" % (prefix, info))
            elif ":" in prefix:
                routes_ipv6.append("%s %s" % (prefix, info))
            else:
                raise RuntimeError('The BGP originate route "%s" is odd' % prefix)

        self._addline("# BGP Origination")
        self._addline("ipv4 table t_bgp_originate4;")
        self._addline("ipv6 table t_bgp_originate6;")
        self._addline("")

        #
        # Setup BGP Origination
        #

        self._addline("filter f_bgp_originate4_import {")
        self._addline("\t# Origination import")
        self._addline("\tbgp_import_own(20);")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")
        self._addline("filter f_bgp_originate6_import {")
        self._addline("\t# Origination import")
        self._addline("\tbgp_import_own(20);")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

        self._addline("protocol static bgp_originate4 {")
        self._addline('\tdescription "BGP route origination for IPv4";')
        self._addline("")
        self._addline("\tipv4 {")
        self._addline("\t\ttable t_bgp_originate4;")
        self._addline("\t\texport none;")
        self._addline("\t\timport filter f_bgp_originate4_import;")
        self._addline("\t};")
        # If we have IPv4 routes
        if routes_ipv4:
            self._addline("")
            # Output the routes
            for route in routes_ipv4:
                self._addline("\troute %s;" % route)
        self._addline("};")
        self._addline("")
        self._addline("protocol static bgp_originate6 {")
        self._addline('\tdescription "BGP route origination for IPv6";')
        self._addline("")
        self._addline("\tipv6 {")
        self._addline("\t\ttable t_bgp_originate6;")
        self._addline("\t\texport none;")
        self._addline("\t\timport filter f_bgp_originate6_import;")
        self._addline("\t};")
        # If we have IPv6 routes
        if routes_ipv6:
            self._addline("")
            # Output the routes
            for route in routes_ipv6:
                self._addline("\troute %s;" % route)
        self._addline("};")
        self._addline("")

        # Configure BGP origination route pipe to the kernel
        originate_pipe = BirdConfigProtocolPipe(
            self, table_from="bgp_originate", table_to="bgp", table_export="all", table_import="none"
        )
        originate_pipe.configure()

    def _bgp_to_master_export_filter(self, ipv):
        """BGP to master filter."""

        # Configure export filter to master
        self._addline("filter f_bgp_master%s_export {" % ipv)
        # Check if we accept the default route, if not block it
        if not self.accept_default:
            self._addline("\t# Do not export default routes to the master")

            if ipv == 4:
                self._addline("\tif (net = 0.0.0.0/0) then {")
            elif ipv == 6:
                self._addline("\tif (net = ::/0) then {")

            self._addline("\t\treject;")
            self._addline("\t}")
        # Else accept
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

    def _bgp_to_master_import_filter(self, ipv):
        # Configure import filter to master
        self._addline("filter f_bgp_master%s_import" % ipv)
        self._addline("{")
        # Redistribute kernel routes
        if self.import_kernel:
            self._addline("\t# Import kernel routes into BGP")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline("\t\tbgp_import_own(5);")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.import_static:
            self._addline("\t# Import static routes into BGP")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline("\t\tbgp_import_own(10);")
            self._addline("\t\taccept;")
            self._addline("\t}")
        # Else accept
        self._addline("\treject;")
        self._addline("};")
        self._addline("")

    def _bgp_to_direct_import_filter(self, ipv):
        # Configure import filter to direct
        self._addline("filter f_bgp_direct%s_import" % ipv)
        self._addline("{")
        self._addline("\t# Origination import")
        self._addline("\tbgp_import_own(10);")
        self._addline("\taccept;")
        self._addline("};")
        self._addline("")

    def _setup_bgp_to_master_export_filters(self):
        """BGP main table to master export filters setup."""
        self._bgp_to_master_export_filter(4)
        self._bgp_to_master_export_filter(6)

    def _setup_bgp_to_master_import_filters(self):
        """BGP main table to master import filters setup."""
        self._bgp_to_master_import_filter(4)
        self._bgp_to_master_import_filter(6)

    def _setup_bgp_to_direct_import_filters(self):
        """BGP main table to direct import filters setup."""
        self._bgp_to_direct_import_filter(4)
        self._bgp_to_direct_import_filter(6)

    def configure(self):
        """Configure the BGP protocol."""

        self._addline("# BGP Tables")
        self._addline("ipv4 table t_bgp4;")
        self._addline("ipv6 table t_bgp6;")
        self._addline("")

        # Setup BGP origination
        self._configure_originate()

        # BGP to master export filters
        self._setup_bgp_to_master_export_filters()

        # BGP to master import filters
        self._setup_bgp_to_master_import_filters()

        # Configure pipe from BGP to the master routing table
        bgp_master_pipe = BirdConfigProtocolPipe(
            self, table_from="bgp", table_to="master", table_export_filtered=True, table_import_filtered=True
        )
        bgp_master_pipe.configure()

        # Check if we're importing connected routes, if we are, create the protocol and pipe
        if self.import_connected:
            if "interfaces" not in self.import_connected:
                raise RuntimeError('BGP import connected requires a list in item "interfaces" to match interface names')
            # Add direct protocol for redistribution of connected routes
            bgp_direct_protocol = BirdConfigProtocolDirect(self, name="bgp", interfaces=self.import_connected["interfaces"])
            bgp_direct_protocol.configure()
            # Add pipe
            self._setup_bgp_to_direct_import_filters()
            bgp_direct_pipe = BirdConfigProtocolPipe(
                self,
                name="bgp",
                description="BGP",
                table_from="bgp",
                table_to="direct",
                table_export="none",
                table_import_filtered=True,
            )
            bgp_direct_pipe.configure()

        # Loop with BGP peers and configure them
        for peer_name in sorted(self._bgp_peers.keys()):
            peer = BirdConfigProtocolBGPPeer(self, peer_name=peer_name, peer_config=self._bgp_peers[peer_name])
            peer.configure()

    def set_asn(self, asn):
        """Set our ASN."""
        self._bgp_asn = asn

        # Turn on bogons and functions output in our constants block
        self.parent.constants.need_bogons = True
        self.parent.constants.bgp_asn = self._bgp_asn
        self.parent.constants.need_functions = True

    def add_originate_route(self, route):
        """Add static route."""
        (prefix, route_info) = route.split(" ", 1)
        self._bgp_originate_routes[prefix] = route_info

    def add_peer(self, peer_name, peer_config=None):
        """Add peer to BGP."""
        if peer_name not in self._bgp_peers:
            self._bgp_peers[peer_name] = peer_config

    # PREFIX_MAXLEN4

    @property
    def prefix_maxlen4_import(self):
        """Return the current value of prefix_maxlen4_import."""
        return self.parent.constants.bgp_prefix_maxlen4_import

    @prefix_maxlen4_import.setter
    def prefix_maxlen4_import(self, value):
        """Setter for prefix_maxlen4_import."""
        self.parent.constants.bgp_prefix_maxlen4_import = value

    @property
    def prefix_maxlen4_export(self):
        """Return the current value of prefix_maxlen4_export."""
        return self.parent.constants.bgp_prefix_maxlen4_export

    @prefix_maxlen4_export.setter
    def prefix_maxlen4_export(self, value):
        """Setter for prefix_maxlen4_export."""
        self.parent.constants.bgp_prefix_maxlen4_export = value

    # PREFIX_MINLEN4

    @property
    def prefix_minlen4_import(self):
        """Return the current value of prefix_minlen4_import."""
        return self.parent.constants.bgp_prefix_minlen4_import

    @prefix_minlen4_import.setter
    def prefix_minlen4_import(self, value):
        """Setter for prefix_minlen4_import."""
        self.parent.constants.bgp_prefix_minlen4_import = value

    @property
    def prefix_minlen4_export(self):
        """Return the current value of prefix_minlen4_export."""
        return self.parent.constants.bgp_prefix_minlen4_export

    @prefix_minlen4_export.setter
    def prefix_minlen4_export(self, value):
        """Setter for prefix_minlen4_export."""
        self.parent.constants.bgp_prefix_minlen4_export = value

    # PREFIX_MAXLEN6

    @property
    def prefix_maxlen6_import(self):
        """Return the current value of prefix_maxlen6_import."""
        return self.parent.constants.bgp_prefix_maxlen6_import

    @prefix_maxlen6_import.setter
    def prefix_maxlen6_import(self, value):
        """Setter for prefix_maxlen6_import."""
        self.parent.constants.bgp_prefix_maxlen6_import = value

    @property
    def prefix_maxlen6_export(self):
        """Return the current value of prefix_maxlen6_export."""
        return self.parent.constants.bgp_prefix_maxlen6_export

    @prefix_maxlen6_export.setter
    def prefix_maxlen6_export(self, value):
        """Setter for prefix_maxlen6_export."""
        self.parent.constants.bgp_prefix_maxlen6_export = value

    # PREFIX_MINLEN6

    @property
    def prefix_minlen6_import(self):
        """Return the current value of prefix_minlen6_import."""
        return self.parent.constants.bgp_prefix_minlen6_import

    @prefix_minlen6_import.setter
    def prefix_minlen6_import(self, value):
        """Setter for prefix_minlen6_import."""
        self.parent.constants.bgp_prefix_minlen6_import = value

    @property
    def prefix_minlen6_export(self):
        """Return the current value of prefix_minlen6_export."""
        return self.parent.constants.bgp_prefix_minlen6_export

    @prefix_minlen6_export.setter
    def prefix_minlen6_export(self, value):
        """Setter for prefix_minlen6_export."""
        self.parent.constants.bgp_prefix_minlen6_export = value

    # OTHER SETTINGS

    @property
    def accept_default(self):
        """Accept the default route if we get it via BGP."""
        return self._bgp_accept["default"]

    @accept_default.setter
    def accept_default(self, value):
        """Setter for accept_default."""
        self._bgp_accept["default"] = value

    @property
    def import_connected(self):
        """Import connected routes into the main BGP table."""
        return self._bgp_import["connected"]

    @import_connected.setter
    def import_connected(self, value):
        """Setter for import_connected."""
        self._bgp_import["connected"] = value

    @property
    def import_static(self):
        """Import static routes into the main BGP table."""
        return self._bgp_import["static"]

    @import_static.setter
    def import_static(self, value):
        """Setter for import_static."""
        self._bgp_import["static"] = value

    @property
    def import_kernel(self):
        """Import kernel routes into the main BGP table."""
        return self._bgp_import["kernel"]

    @import_kernel.setter
    def import_kernel(self, value):
        """Setter for import_kernel."""
        self._bgp_import["kernel"] = value

    @property
    def peers(self):
        """Return BGP peers."""
        return self._bgp_peers

    @property
    def rr_cluster_id(self):
        """Return route reflector cluster ID."""
        return self._bgp_rr_cluster_id

    @rr_cluster_id.setter
    def rr_cluster_id(self, value):
        """Set our route reflector cluster ID."""
        self._bgp_rr_cluster_id = value


class BirdConfigProtocolBGPPeer(BirdConfigBase):
    """Bird BGP protocol peer configuration."""

    def __init__(self, parent, peer_name, peer_config, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Save our name and configuration
        self._peer_name = peer_name
        self._peer_config = peer_config

        # Work out our peer table name
        self._peer_table = "bgp_AS%s_%s_peer" % (self.peer_asn, self.peer_name)

        # Work out our prefix list name
        self._prefix_list = "bgp_AS%s_%s_prefixes" % (self.peer_asn, self.peer_name)

        # Work out our ASN list name
        self._asn_list = "bgp_AS%s_%s_asns" % (self.peer_asn, self.peer_name)

        # Turn on passive mode for route reflectors
        if self.peer_type in ("customer", "rrclient"):
            self._passive = True
        else:
            self._passive = False

        # We don't have peeringdb info yet
        self._peeringdb = None

        # Default to redistributing nothing
        self._redistribute = {
            "default": False,
            "connected": False,
            "kernel": False,
            "static": False,
            "originated": False,
            "bgp": False,
            "bgp_own": False,
            "bgp_customer": False,
            "bgp_peering": False,
            "bgp_transit": False,
        }
        # If this is a rrserver, send our entire BGP table
        if self.peer_type in ("rrclient", "rrserver", "rrserver-rrserver"):
            self.redistribute["bgp"] = True
        # If this is an upstream, peer, customer, routecollector or routeserver, we need to redistribute our own routes and
        # customer routes
        if self.peer_type in ("customer", "routecollector", "routeserver", "peer", "upstream"):
            self.redistribute["bgp_own"] = True
            self.redistribute["bgp_customer"] = True
        # If this is an customer, we need to redistribute peer and transit routes too
        if self.peer_type == "customer":
            self.redistribute["bgp_peering"] = True
            self.redistribute["bgp_transit"] = True

        # If the peer is a customer or peer, check if we have a prefix limit, if not add it from peeringdb
        # For routecollector and routeservers we filter, not block
        if self.peer_type in ("customer", "peer"):
            if self.has_ipv4:
                if "prefix_limit_ipv4" not in self.peer_config:
                    self.peer_config["prefix_limit_ipv4"] = "peeringdb"
            if self.has_ipv6:
                if "prefix_limit_ipv6" not in self.peer_config:
                    self.peer_config["prefix_limit_ipv6"] = "peeringdb"
        # Work out the prefix limits...
        if self.has_ipv4:
            if ("prefix_limit_ipv4" in self.peer_config) and (self.peer_config["prefix_limit_ipv4"] == "peeringdb"):
                self.peer_config["prefix_limit_ipv4"] = self.peeringdb["info_prefixes4"]
        if self.has_ipv6:
            if ("prefix_limit_ipv6" in self.peer_config) and (self.peer_config["prefix_limit_ipv6"] == "peeringdb"):
                self.peer_config["prefix_limit_ipv6"] = self.peeringdb["info_prefixes6"]

        # Work out what we're going to be redistributing
        if "redistribute" in self.peer_config:
            for redistribute_type, redistribute_config in self.peer_config["redistribute"].items():
                if redistribute_type not in ("default", "connected", "static", "kernel", "originated"):
                    raise ValueError('The BGP redistribute type "%s" is not known' % redistribute_type)
                self.redistribute[redistribute_type] = redistribute_config

        # Default to accepting nothing
        self._accept = {
            "default": False,
        }
        # Work out what we're going to be accepting
        if "accept" in self.peer_config:
            for accept_type, accept_config in self.peer_config["accept"].items():
                if accept_type != "default":
                    raise ValueError('The BGP accept type "%s" is not known' % accept_type)
                self._accept[accept_type] = accept_config

        # Check for filters we need to setup
        self._filter = {"prefixes": [], "asns": [], "as-set": []}
        if "filter" in self.peer_config:
            for filter_type, filter_config in self.peer_config["filter"].items():
                if filter_type not in ("prefixes", "asns", "as-set"):
                    raise ValueError('The BGP filter type "%s" is not known' % filter_type)
                self._filter[filter_type] = filter_config

        # Check if we're quarantined
        if "quarantine" in self.peer_config and self.peer_config["quarantine"]:
            self._quarantined = True
        else:
            self._quarantined = False

    def _setup_peer_tables(self):
        """Peering routing table setup."""
        if self.has_ipv4:
            self._addline("ipv4 table t_%s4;" % self.peer_table)
        if self.has_ipv6:
            self._addline("ipv6 table t_%s6;" % self.peer_table)

    def _setup_peer_asns(self):
        """ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_asn_filter:
            return

        # Grab IRR prefixes
        irr_asns = []
        if self.filter_as_set:
            bgpq3 = BGPQ3()
            irr_asns = bgpq3.get_asns([self.filter_as_set])

        self._addline("define %s = [" % self.asn_list)
        asns = []
        # Add ASN list with comments
        if self.filter_asns:
            asns.append("# {} statically defined".format(len(self.filter_asns)))
            for asn in self.filter_asns:
                asns.append("%s" % asn)
        if irr_asns:
            asns.append('# {} from IRR with object "{}"'.format(len(irr_asns), self.filter_as_set))
            for asn in irr_asns:
                asns.append("%s" % asn)
        # Join into one string, so we get the commas
        asns_str = ",\n".join(asns)
        # Loop with each line
        for line in asns_str.splitlines():
            # Remove comma from the comments
            if "#" in line:
                line = line[:-1]
            # Add line to our output
            self._addline("\t" + line)
        self._addline("];")

    def _setup_peer_prefixes(self):
        """Prefix list setup."""
        # Short circuit and exit if we have none
        if not self.has_prefix_filter:
            return

        # Work out prefixes
        ipv4_prefixes = []
        ipv6_prefixes = []
        for prefix in sorted(self.filter_prefixes):
            if ":" in prefix:
                ipv6_prefixes.append(prefix)
            else:
                ipv4_prefixes.append(prefix)

        # Grab IRR prefixes
        irr_prefixes = {"ipv4": [], "ipv6": []}
        if self.filter_as_set:
            bgpq3 = BGPQ3()
            irr_prefixes = bgpq3.get_prefixes([self.filter_as_set])

        # Output prefix definitions
        if self.has_ipv4:
            self._addline("define %s4 = [" % self.prefix_list)
            prefixes = []
            # Add prefix lists with comments
            if ipv4_prefixes:
                prefixes.append("# {} statically defined".format(len(ipv4_prefixes)))
                prefixes.extend(ipv4_prefixes)
            if irr_prefixes["ipv4"]:
                prefixes.append('# {} from IRR with object "{}"'.format(len(irr_prefixes["ipv4"]), self.filter_as_set))
                prefixes.extend(irr_prefixes["ipv4"])
            # Join into one string, so we get the commas
            prefixes_str = ",\n".join(prefixes)
            # Loop with each line
            for line in prefixes_str.splitlines():
                # Remove comma from the comments
                if "#" in line:
                    line = line[:-1]
                # Add line to our output
                self._addline("\t" + line)
            self._addline("];")
        # and output for IPv6
        if self.has_ipv6:
            self._addline("define %s6 = [" % self.prefix_list)
            prefixes = []
            # Add prefix lists with comments
            if ipv6_prefixes:
                prefixes.append("# {} statically defined".format(len(ipv6_prefixes)))
                prefixes.extend(ipv6_prefixes)
            if irr_prefixes["ipv6"]:
                prefixes.append('# {} from IRR with object "{}"'.format(len(irr_prefixes["ipv6"]), self.filter_as_set))
                prefixes.extend(irr_prefixes["ipv6"])
            # Join into one string, so we get the commas
            prefixes_str = ",\n".join(prefixes)
            # Loop with each line
            for line in prefixes_str.splitlines():
                # Remove comma from the comments
                if "#" in line:
                    line = line[:-1]
                # Add line to our output
                self._addline("\t" + line)
            self._addline("];")

    def _add_redistribute_properties(self, config):
        """Redistribution properties to add to the route."""
        if isinstance(config, dict):
            if "redistribute-large-communities" in config:
                for large_community in sorted(config["redistribute-large-communities"]):
                    bird_lc = util.sanitize_large_community(large_community)
                    self._addline('\t\tprint "[redistribute-large-communities] Adding %s to ", net;' % bird_lc, debug=True)
                    self._addline("\t\tbgp_large_community.add(%s);" % bird_lc)

    def _peer_to_bgp_export_filter(self, ipv):
        """Export filters into our main BGP routing table from the BGP peer table."""

        # Configure export filter to our main BGP table
        self._addline("# Export filter TO the main BGP table from the BGP peer table")
        self._addline("filter f_%s_bgp%s_export" % (self.peer_table, ipv))
        self._addline("int accept_route;")
        self._addline("{")
        # Check if we're accepting the route...
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then {")
        self._addline('\t\tprint "[f_%s_bgp%s_export] Filtered ", net, " to main BGP table";' % (self.peer_table, ipv), debug=True)
        self._addline("\t\treject;")
        self._addline("\t}")
        # Else reject
        self._addline('\tprint "[f_%s_bgp%s_export] Exporting ", net, " to main BGP table";' % (self.peer_table, ipv), debug=True)
        self._addline("\taccept;")
        self._addline("};")

    def _peer_to_bgp_import_filter(self, ipv):
        """Import filter FROM the main BGP table to the BGP peer table."""

        # Configure import filter from our main BGP table
        self._addline("# Import filter FROM the main BGP table to the BGP peer table")
        self._addline("filter f_%s_bgp%s_import" % (self.peer_table, ipv))
        self._addline("int accept_route;")
        self._addline("{")
        self._addline("\taccept_route = 0;")

        # Check that we have static routes imported first
        if self.redistribute["static"] and not self.parent.import_static:
            raise RuntimeError("BGP needs static routes to be imported before they can be redistributed to a peer")

        # Do not redistribute the default route, no matter where we get it from
        if not self.redistribute["default"]:
            self._addline("\t# Reject the default route as we are not redistributing it")
            self._addline("\tif (net = DEFAULT_ROUTE_V%s) then {" % ipv)
            self._addline('\t\tprint "[f_%s_bgp%s_import] Rejecting default route ", net, " export";' % (self.peer_table, ipv))
            self._addline("\t\treject;")
            self._addline("\t}")

        # Override exports if this is a customer peer and we don't export to customers
        if self.peer_type == "customer":
            self._addline("\t# Check for large community to prevent export to customers")
            self._addline("\tif (BGP_LC_EXPORT_NOCUSTOMER ~ bgp_large_community) then {")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOCUSTOMER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Override exports if this is a peer, routecollector or routeserver and we don't export to peers
        if self.peer_type in ("peer", "routecollector", "routeserver"):
            self._addline("\t# Check for large community to prevent export to %s" % self.peer_type)
            self._addline("\tif (BGP_LC_EXPORT_NOPEER ~ bgp_large_community) then {")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOPEER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Override exports if this is a transit and we don't export to transits
        if self.peer_type == "transit":
            self._addline("\t# Check for large community to prevent export to transit")
            self._addline("\tif (BGP_LC_EXPORT_NOTRANSIT ~ bgp_large_community) then {")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOTRANSIT";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")

        # Redistribute connected
        if self.redistribute["connected"]:
            self._addline("\t# Redistribute connected")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on RTS_DEVICE";' % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["connected"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute["static"]:
            self._addline("\t# Redistribute static routes")
            self._addline("\tif (source = RTS_STATIC) then {")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on RTS_STATIC";' % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["static"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute["kernel"]:
            self._addline("\t# Redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on RTS_INHERIT";' % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["kernel"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute originated routes
        if self.redistribute["originated"]:
            self._addline("\t# Redistribute originated routes")
            self._addline('\tif (proto = "bgp_originate%s") then {' % ipv)
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on bgp_originate%s";'
                % (self.peer_table, ipv, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["originated"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute BGP routes
        if self.redistribute["bgp"]:
            self._addline("\t# Redistribute BGP routes (which is everything in our table)")
            self._addline("\tif (source = RTS_BGP) then {")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on RTS_BGP";' % (self.peer_table, ipv), debug=True
            )
            self._add_redistribute_properties(self.redistribute["bgp"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")

        # Redistribute our own BGP routes
        if self.redistribute["bgp_own"]:
            self._addline("\t# Redistribute our own BGP routes")
            self._addline("\tif (BGP_LC_RELATION_OWN ~ bgp_large_community) then {")
            self._addline("\t\tif !bgp_can_export_v%s(%s) then {" % (ipv, self.peer_asn))
            self._addline(
                '\t\t\tprint "[f_%s_bgp%s_import] Cannot export ", net, " with match on BGP_LC_RELATION_OWN";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on BGP_LC_RELATION_OWN";' % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_own"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute customer BGP routes
        if self.redistribute["bgp_customer"]:
            self._addline("\t# Redistribute customer BGP routes")
            self._addline("\tif (BGP_LC_RELATION_CUSTOMER ~ bgp_large_community) then {")
            self._addline("\t\tif !bgp_can_export_v%s(%s) then {" % (ipv, self.peer_asn))
            self._addline(
                '\t\t\tprint "[f_%s_bgp%s_import] Cannot export ", net, " with match on BGP_LC_RELATION_CUSTOMER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on BGP_LC_RELATION_CUSTOMER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_customer"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute peering BGP routes
        if self.redistribute["bgp_peering"]:
            self._addline("\t# Redistribute peering BGP routes")
            self._addline("\tif (BGP_LC_RELATION_PEER ~ bgp_large_community) then {")
            self._addline("\t\tif !bgp_can_export_v%s(%s) then {" % (ipv, self.peer_asn))
            self._addline(
                '\t\t\tprint "[f_%s_bgp%s_import] Cannot export ", net, " with match on BGP_LC_RELATION_PEER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on BGP_LC_RELATION_PEER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_peering"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
            self._addline("\tif (BGP_LC_RELATION_ROUTESERVER ~ bgp_large_community) then {")
            self._addline("\t\tif !bgp_can_export_v%s(%s) then {" % (ipv, self.peer_asn))
            self._addline(
                '\t\t\tprint "[f_%s_bgp%s_import] Cannot export ", net, " with match on BGP_LC_RELATION_ROUTESERVER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on BGP_LC_RELATION_ROUTESERVER";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_peering"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute transit BGP routes
        if self.redistribute["bgp_transit"]:
            self._addline("\t# Redistribute transit BGP routes")
            self._addline("\tif (BGP_LC_RELATION_TRANSIT ~ bgp_large_community) then {")
            self._addline("\t\tif !bgp_can_export_v%s(%s) then {" % (ipv, self.peer_asn))
            self._addline(
                '\t\t\tprint "[f_%s_bgp%s_import] Cannot export ", net, " with match on BGP_LC_RELATION_TRANSIT";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                '\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " due to match on BGP_LC_RELATION_TRANSIT";'
                % (self.peer_table, ipv),
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_transit"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")

        # Check if we're accepting the route...
        self._addline("\tif (accept_route > 0) then {")
        # Do large community prepending if the peer is a customer, peer, routeserver or upstream
        if self.peer_type in ("customer", "peer", "routeserver", "routecollector", "upstream"):
            # Check if we are adding a large community to outgoing routes
            if "outgoing-large-communities" in self.peer_config:
                for large_community in sorted(self.peer_config["outgoing-large-communities"]):
                    bird_lc = util.sanitize_large_community(large_community)
                    self._addline(
                        '\t\tprint "[f_%s_bgp%s_import] Adding LC %s to ", net;' % (self.peer_table, ipv, bird_lc), debug=True
                    )
                    self._addline("\t\tbgp_large_community.add(%s);" % bird_lc)
            # Check if we're doing prepending
            self._addline("\t\t# Do prepend if we have any LCs set")
            self._addline("\t\tbgp_export_prepend(%s);" % self.peer_asn)
        # Finally accept
        self._addline("\t\t# Finally accept")
        self._addline('\t\tprint "[f_%s_bgp%s_import] Accepting ", net, " to peer";' % (self.peer_table, ipv), debug=True)
        self._addline("\t\taccept;")
        self._addline("\t}")

        # By default reject all routes
        self._addline("\t# Reject by default")
        self._addline(
            '\tprint "[f_%s_bgp%s_import] Rejecting ", net, " to peer (fallthrough)";' % (self.peer_table, ipv), debug=True
        )
        self._addline("\treject;")
        self._addline("};")

    def _peer_export_filter(self, ipv):
        """Peer export filter setup from peer table to peer."""
        # Configure export filter to the BGP peer
        self._addline("# Export filter TO the BGP peer from the peer BGP table")
        self._addline("filter f_%s%s_export" % (self.peer_table, ipv))
        self._addline("{")
        self._addline("\t# We accept all routes going to the peer that are in the peer BGP table")
        self._addline('\tif (proto != "%s%s") then accept;' % (self.peer_table, ipv))
        self._addline("};")

    def _peer_import_filter(self, ipv):
        """Peer import filter setup from peer to peer table."""
        # Configure import filter from the BGP peer
        self._addline("# Import filter FROM the BGP peer TO the peer BGP table")
        self._addline("filter f_%s%s_import {" % (self.peer_table, ipv))

        # If this is the route from our peer, we need to check what type it is
        type_lines = []

        # Clients
        if self.peer_type == "customer":
            type_lines.append("\t\tbgp_lc_remove_internal();")
            type_lines.append("\t\tbgp_import_customer(%s, %s);" % (self.peer_asn, self.cost))
            if self._accept["default"]:
                raise RuntimeError('Having "accept[default]" as True for a "customer" makes no sense')
            type_lines.append("\t\tbgp_filter_default_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_bogons_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_size_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append("\t\tbgp_filter_asn_invalid(%s);" % self.peer_asn)
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Peers
        elif self.peer_type == "peer":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append("\t\tbgp_import_peer(%s, %s);" % (self.peer_asn, self.cost))
            if self._accept["default"]:
                raise RuntimeError('Having "accept[default]" as True for a "peer" makes no sense')
            type_lines.append("\t\tbgp_filter_default_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_bogons_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_size_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append("\t\tbgp_filter_asn_invalid(%s);" % self.peer_asn)
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Routecollector
        elif self.peer_type == "routecollector":
            type_lines.append("\t\tbgp_lc_remove_all();")
            if self._accept["default"]:
                raise RuntimeError('Having "accept[default]" as True for a "routecollector" makes no sense')
            type_lines.append("\t\tbgp_filter_routecollector();")
        # Routeserver
        elif self.peer_type == "routeserver":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append("\t\tbgp_import_routeserver(%s, %s);" % (self.peer_asn, self.cost))
            if self._accept["default"]:
                raise RuntimeError('Having "accept[default]" as True for a "routeserver" makes no sense')
            type_lines.append("\t\tbgp_filter_default_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_bogons_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_size_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Route reflector client
        elif self.peer_type == "rrclient":
            if not self._accept["default"]:
                type_lines.append("\t\tbgp_filter_default_v%s();" % ipv)
        # Route reflector server
        elif self.peer_type == "rrserver":
            if not self._accept["default"]:
                type_lines.append("\t\tbgp_filter_default_v%s();" % ipv)
        # Route reflector server to route reflector server
        elif self.peer_type == "rrserver-rrserver":
            if not self._accept["default"]:
                type_lines.append("\t\tbgp_filter_default_v%s();" % ipv)
        # Upstreams
        elif self.peer_type == "upstream":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append("\t\tbgp_import_transit(%s, %s);" % (self.peer_asn, self.cost))
            if not self._accept["default"]:
                type_lines.append("\t\tbgp_filter_default_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_bogons_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_size_v%s();" % ipv)
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append("\t\tbgp_filter_asn_invalid(%s);" % self.peer_asn)
        else:
            raise RuntimeError('The BGP peer type "%s" is not supported' % self.peer_type)

        # Check if we're filtering allowed ASNs
        if self.filter_asns:
            type_lines.append("\t\t# Filter on the allowed ASNs")
            type_lines.append("\t\tbgp_filter_asns(%s);" % self.asn_list)

        # Check if we're filtering allowed prefixes
        if self.filter_prefixes:
            type_lines.append("\t\t# Filter on the allowed prefixes")
            type_lines.append("\t\tbgp_filter_prefixes_v%s(%s%s);" % (ipv, self.prefix_list, ipv))

        # Quarantine mode...
        if self.quarantined:
            type_lines.append("\t\tbgp_filter_quarantine();")

        # Check if we are adding a large community to incoming routes
        if "incoming-large-communities" in self.peer_config:
            for large_community in sorted(self.peer_config["incoming-large-communities"]):
                bird_lc = util.sanitize_large_community(large_community)
                if self.root.debug:
                    type_lines.append('\t\tprint "[f_%s%s_import] Adding LC %s to ", net;' % (self.peer_table, ipv, bird_lc))
                type_lines.append("\t\tbgp_large_community.add(%s);" % bird_lc)

        # If we have lines from the above add them
        if type_lines:
            self._addline("\t# Process routes from our peer")
            self._addline('\tif (proto = "%s%s") then {' % (self.peer_table, ipv))
            self._addlines(type_lines)
            self._addline("\t}")

        self._addline("\taccept;")
        self._addline("};")

    def _setup_peer_protocol(self, ipv):
        """Peer protocol setup for a single protocol."""

        self._addline("protocol bgp %s%s {" % (self.peer_table, ipv))
        self._addline('\tdescription "AS%s %s - %s";' % (self.peer_asn, self.peer_name, self.peer_config["description"]))

        self._addline("\tlocal as BGP_ASN;")
        self._addline("\tsource address %s;" % (self.peer_config["source_address%s" % ipv]))
        self._addline("\tstrict bind;")
        self._addline("\tneighbor %s as %s;" % (self.peer_config["neighbor%s" % ipv], self.peer_asn))
        # Check if this is a passive peer
        if self.is_passive:
            self._addline("\tpassive;")

        # Add various tunables
        if "connect_delay_time" in self.peer_config:
            self._addline("\tconnect delay time %s;" % self.peer_config["connect_delay_time"])
        if "connect_retry_time" in self.peer_config:
            self._addline("\tconnect retry time %s;" % self.peer_config["connect_retry_time"])
        if "error_wait_time" in self.peer_config:
            self._addline("\terror wait time %s;" % self.peer_config["error_wait_time"])
        if "multihop" in self.peer_config:
            self._addline("\tmultihop %s;" % self.peer_config["multihop"])
        if "password" in self.peer_config:
            self._addline('\tpassword "%s";' % self.peer_config["password"])

        # Handle route reflector clients
        if self.peer_type == "rrclient":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrclient
            if not self.parent.rr_cluster_id:
                raise RuntimeError('BGP route reflectors require a "cluster_id set" if they have "rrclient" peers')
            # Set this peer as a route reflector client
            self._addline("\trr client;")
            self._addline("\trr cluster id %s;" % self.parent.rr_cluster_id)

        # Handle route reflector server-to-server
        if self.peer_type == "rrserver-rrserver":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrserver-rrserver peer
            if not self.parent.rr_cluster_id:
                raise RuntimeError('BGP route reflectors require a "cluster_id" if they have "rrserver-rrserver" peers')
            # Set this peer as a route reflector client
            self._addline("\trr client;")
            self._addline("\trr cluster id %s;" % self.parent.rr_cluster_id)

        # Setup peer table
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_%s%s;" % (self.peer_table, ipv))
        self._addline("\t\tigp table master%s;" % ipv)
        # Setup import and export table so we can do soft reconfiguration
        self._addline("\t\timport table;")
        self._addline("\t\texport table;")
        # Setup prefix limit
        prefix_limit_name = "prefix_limit_ipv%s" % ipv
        if prefix_limit_name in self.peer_config and (self.peer_config[prefix_limit_name] is not None):
            self._addline("\t\timport limit %s;" % self.peer_config[prefix_limit_name])
        # Setup filters
        self._addline("\t\timport filter f_%s%s_import;" % (self.peer_table, ipv))
        self._addline("\t\texport filter f_%s%s_export;" % (self.peer_table, ipv))
        self._addline("\t};")
        self._addline("}")

    def _setup_peer_protocols(self):
        """Peer protocols setup."""
        if self.has_ipv4:
            self._setup_peer_protocol(4)
        if self.has_ipv6:
            self._setup_peer_protocol(6)

    def _setup_peer_to_bgp_filters(self):
        """Peer filters to the main BGP table."""
        # Setup peer to main BGP table export filter
        if self.has_ipv4:
            self._peer_to_bgp_export_filter(4)
        if self.has_ipv6:
            self._peer_to_bgp_export_filter(6)
        # Setup peer to main BGP table import filter
        if self.has_ipv4:
            self._peer_to_bgp_import_filter(4)
        if self.has_ipv6:
            self._peer_to_bgp_import_filter(6)

    def _setup_peer_filters(self):
        """Peer filter setup."""
        # Setup export filters
        if self.has_ipv4:
            self._peer_export_filter(4)
        if self.has_ipv6:
            self._peer_export_filter(6)

        # Setup import filters
        if self.has_ipv4:
            self._peer_import_filter(4)
        if self.has_ipv6:
            self._peer_import_filter(6)

    @property
    def asn_list(self):
        """Return our ASN list name."""
        return self._asn_list

    @property
    def cost(self) -> int:
        """Return our route cost."""
        if "cost" in self.peer_config:
            return self.peer_config["cost"]
        return 0

    @property
    def has_asn_filter(self):
        """Return if we filter on ASNs."""
        return self.filter_asns or self.filter_as_set

    @property
    def has_prefix_filter(self):
        """Return if we filter on prefixes."""
        return self.filter_prefixes or self.filter_as_set

    @property
    def filter_asns(self):
        """Return the asns we filter on."""
        return self._filter["asns"]

    @property
    def filter_prefixes(self):
        """Return the prefixes we filter on."""
        return self._filter["prefixes"]

    @property
    def filter_as_set(self):
        """Return the as-set we filter on."""
        return self._filter["as-set"]

    @property
    def has_ipv4(self):
        """Return if we have IPv4."""
        return "neighbor4" in self.peer_config

    @property
    def has_ipv6(self):
        """Return if we have IPv6."""
        return "neighbor6" in self.peer_config

    @property
    def is_passive(self):
        """Return if we only accept connections, not make them."""
        return self._passive

    @property
    def peer_asn(self):
        """Return our ASN from the peer_config."""
        return self._peer_config["asn"]

    @property
    def peer_config(self):
        """Return our config."""
        return self._peer_config

    @property
    def peer_name(self):
        """Return our name."""
        return self._peer_name

    @property
    def peer_table(self):
        """Return our table."""
        return self._peer_table

    @property
    def peer_type(self):
        """Return our type."""
        return self._peer_config["type"]

    @property
    def peeringdb(self):
        """Return our peeringdb entry, if there is one."""
        if self.peer_asn > 64512 and self.peer_asn < 65534:
            return {"info_prefixes4": None, "info_prefixes6": None}
        # If we don't having peerindb info, grab it
        if not self._peeringdb:
            self._peeringdb = requests.get("https://www.peeringdb.com/api/net?asn__in=%s" % self.peer_asn).json()["data"][0]
        # Lastly return it
        return self._peeringdb

    @property
    def prefix_list(self):
        """Return our prefix list name."""
        return self._prefix_list

    @property
    def quarantined(self):
        """Return if we're quarantined."""
        return self._quarantined

    @property
    def redistribute(self):
        """Return our restribute structure."""
        return self._redistribute

    def configure(self):
        """Configure BGP peer."""
        #
        # BGP peer config
        #

        self._addline("# BGP Peer %s" % self.peer_name)

        # Setup routing tables
        self._setup_peer_tables()

        # Setup allowed ASNs
        self._setup_peer_asns()

        # Setup allowed prefixes
        self._setup_peer_prefixes()

        # BGP peer to main table
        if not self.quarantined:
            self._setup_peer_to_bgp_filters()

        # BGP peer filters
        self._setup_peer_filters()

        # BGP peer protocols
        self._setup_peer_protocols()

        # Configure pipe from the BGP peer table to the main BGP table
        if not self.quarantined:
            bgp_peer_pipe = BirdConfigProtocolPipe(
                self,
                table_from=self.peer_table,
                table_to="bgp",
                table_export_filtered=True,
                table_import_filtered=True,
                has_ipv4=self.has_ipv4,
                has_ipv6=self.has_ipv6,
            )
            bgp_peer_pipe.configure()

        # End of peer
        self._addline("")


class BirdConfig(BirdConfigBase):
    """BirdConfig is responsible for configuring Bird."""

    _router_id: str
    _log_file: Optional[str]
    _debug: bool

    _constants: BirdConfigConstants
    _master: BirdConfigMaster
    _static: BirdConfigProtocolStatic
    _rip: BirdConfigProtocolRIP
    _ospf: BirdConfigProtocolOSPF
    _bgp: BirdConfigProtocolBGP

    def __init__(self):
        """Initialize the object."""
        super().__init__(root=self)

        # Router ID
        self._router_id = "0.0.0.0"

        # Log file
        self._log_file = None

        # Debugging
        self._debug = False
        self._test_mode = False

        # Constants
        self._constants = BirdConfigConstants(parent=self)
        # Master tables
        self._master = BirdConfigMaster(parent=self)
        # Static protocol
        self._static = BirdConfigProtocolStatic(parent=self)
        # RIP protocol
        self._rip = BirdConfigProtocolRIP(parent=self)
        # OSPF protocol
        self._ospf = BirdConfigProtocolOSPF(parent=self)
        # BGP protocol
        self._bgp = BirdConfigProtocolBGP(parent=self)

    def static_add_route(self, route):
        """Add static route."""
        self.static.add_route(route)

    def get_config(self):
        """Return the Bird configuration."""

        main = BirdConfigMain(parent=self)
        main.configure()

        logging = BirdConfigLogging(parent=self)
        logging.configure()

        router_id = BirdConfigRouterID(parent=self)
        router_id.configure()

        self.constants.configure()

        protocol_device = BirdConfigProtocolDevice(parent=self)
        protocol_device.configure()

        protocol_kernel = BirdConfigProtocolKernel(parent=self)
        protocol_kernel.configure()

        self.master.configure()

        self.static.configure()

        if self.rip.interfaces:
            self.rip.configure()

        if self.ospf.areas:
            self.ospf.configure()

        if self.bgp.peers:
            self.bgp.configure()

        return self.config_lines

    @property
    def router_id(self) -> str:
        """Return our router_id."""
        return self._router_id

    @router_id.setter
    def router_id(self, router_id: str):
        """Set router_id."""
        self._router_id = router_id

    @property
    def log_file(self) -> Optional[str]:
        """Return the log file to use."""
        return self._log_file

    @log_file.setter
    def log_file(self, log_file: str):
        """Set the log file to use."""
        self._log_file = log_file

    @property
    def debug(self) -> bool:
        """Return debugging mode."""
        return self._debug

    @debug.setter
    def debug(self, debug: bool):
        """Set debugging mode."""
        self._debug = debug

    @property
    def test_mode(self) -> bool:
        """Return if we're running in test mode."""
        return self._test_mode

    @test_mode.setter
    def test_mode(self, test_mode: bool):
        """Set test mode."""
        self._test_mode = test_mode

    @property
    def constants(self) -> BirdConfigConstants:
        """Return our constants."""
        return self._constants

    @property
    def master(self) -> BirdConfigMaster:
        """Return our master config."""
        return self._master

    @property
    def static(self) -> BirdConfigProtocolStatic:
        """Return our static protocol config."""
        return self._static

    @property
    def rip(self) -> BirdConfigProtocolRIP:
        """Return our RIP protocol config."""
        return self._rip

    @property
    def ospf(self) -> BirdConfigProtocolOSPF:
        """Return our OSPF protocol config."""
        return self._ospf

    @property
    def bgp(self) -> BirdConfigProtocolBGP:
        """Return our BGP protocol config."""
        return self._bgp
