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

"""BGP protocol specific functions class."""

# pylint: disable=too-many-lines

from typing import Any
from ..base_protocol_functions import ProtocolFunctionsBase
from ...functions import BirdVariable, SectionFunctions, bird_function


class BGPFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """BGP protocol specific functions class."""

    _section: str = "BGP Functions"

    @bird_function("bgp_graceful_shutdown")
    def graceful_shutdown(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_graceful_shutdown function."""

        return """\
            # Enable graceful shutdown
            function bgp_graceful_shutdown(string filter_name) {
                if DEBUG then print filter_name,
                    " [graceful_shutdown] Adding GRACEFUL_SHUTDOWN community to ", net;
                bgp_community.add(BGP_COMMUNITY_GRACEFUL_SHUTDOWN);
            }"""

    @bird_function("bgp_quarantine_peer")
    def quarantine_peer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_quarantine_peer function."""

        return """\
            # Quarantine peer
            function bgp_quarantine_peer(string filter_name) {
                if DEBUG then print filter_name,
                    " [bgp_quarantine_peer] Adding BGP_LC_FILTERED_QUARANTINED to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_QUARANTINED);
            }"""

    @bird_function("bgp_import_customer")
    def import_customer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_customer function."""

        return """\
            # Import customer routes
            function bgp_import_customer(string filter_name; int peer_asn; int local_pref_cost) {
                if DEBUG then print filter_name,
                    " [bgp_import_customer] Adding BGP_LC_RELATION_CUSTOMER to ", net, " with local pref ",
                    BGP_PREF_CUSTOMER - local_pref_cost;
                # Tag route as a customer route
                bgp_large_community.add(BGP_LC_RELATION_CUSTOMER);
                # Set local preference
                bgp_local_pref = BGP_PREF_CUSTOMER - local_pref_cost;
            }"""

    @bird_function("bgp_import_own")
    def import_own(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_own function."""

        return """\
            # Import own routes
            function bgp_import_own(string filter_name; int local_pref_cost) {
                if DEBUG then print filter_name,
                    " [bgp_import_own] Adding BGP_LC_RELATION_OWN to ", net, " with local pref ",
                    BGP_PREF_OWN - local_pref_cost;
                # Tag route as a our own (originated and static) route
                bgp_large_community.add(BGP_LC_RELATION_OWN);
                # Add our internal blackhole action to originated routes
                if ((proto = "bgp_originate4" || proto = "bgp_originate6") && dest = RTD_BLACKHOLE) then {
                    if DEBUG then print filter_name,
                        " [bgp_import_own] Adding BGP_LC_ACTION_BLACKHOLE_ORIGINATE to ", net;
                    bgp_large_community.add(BGP_LC_ACTION_BLACKHOLE_ORIGINATE);
                }
                # Set local preference
                bgp_local_pref = BGP_PREF_OWN - local_pref_cost;
            }"""

    @bird_function("bgp_import_routecollector")
    def import_routecollector(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_routecollector function."""

        return """\
            # Import routecollector routes (we add a LC to filter them)
            function bgp_import_routecollector(string filter_name) {
                if DEBUG then print filter_name,
                    " [bgp_import_routecollector] Adding BGP_FILTERED_ROUTECOLLECTOR to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_ROUTECOLLECTOR);
            }"""

    @bird_function("bgp_import_routeserver")
    def import_routeserver(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_routeserver function."""

        return """\
            # Import routeserver routes
            function bgp_import_routeserver(string filter_name; int peer_asn; int local_pref_cost) {
                if DEBUG then print filter_name,
                    " [bgp_import_routeserver] Adding BGP_LC_RELATION_ROUTESERVER to ", net, " with local pref ",
                    BGP_PREF_ROUTESERVER - local_pref_cost;
                # Tag route as a routeserver route
                bgp_large_community.add(BGP_LC_RELATION_ROUTESERVER);
                # Set local preference
                bgp_local_pref = BGP_PREF_ROUTESERVER - local_pref_cost;
            }"""

    @bird_function("bgp_import_peer")
    def import_peer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_peer function."""

        return """\
            # Import peer routes
            function bgp_import_peer(string filter_name; int peer_asn; int local_pref_cost) {
                if DEBUG then print filter_name,
                    " [bgp_import_peer] Adding BGP_LC_RELATION_PEER to ", net, " with local pref ",
                    BGP_PREF_PEER - local_pref_cost;
                # Tag route as a peer route
                bgp_large_community.add(BGP_LC_RELATION_PEER);
                # Set local preference
                bgp_local_pref = BGP_PREF_PEER - local_pref_cost;
            }"""

    @bird_function("bgp_import_transit")
    def import_transit(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_transit function."""

        return """\
            # Import transit routes
            function bgp_import_transit(string filter_name; int peer_asn; int local_pref_cost) {
                if DEBUG then print filter_name,
                    " [bgp_import_transit] Adding BGP_LC_RELATION_TRANSIT to ", net, " with local pref ",
                    BGP_PREF_TRANSIT - local_pref_cost;
                # Tag route as a transit route
                bgp_large_community.add(BGP_LC_RELATION_TRANSIT);
                # Set local preference
                bgp_local_pref = BGP_PREF_TRANSIT - local_pref_cost;
            }"""

    @bird_function("bgp_import_location_iso3166")
    def import_location_iso3166(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_location_iso3166 function."""

        return """\
            # Location-based prefix importing (ISO-3166 country codes)
            function bgp_import_location_iso3166(string filter_name; int location) {
                if DEBUG then print filter_name,
                    " [bgp_import_location_iso3166] Adding BGP_LC_FUNCTION_LOCATION_ISO3166 with ", location, " to ", net;
                bgp_large_community.add((BGP_ASN, BGP_LC_FUNCTION_LOCATION_ISO3166, location));
            }"""

    @bird_function("bgp_import_location_unm49")
    def import_location_unm49(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_location_unm49 function."""

        return """\
            # Location-based prefix importing (UN.M49 country codes)
            function bgp_import_location_unm49(string filter_name; int location) {
                if DEBUG then print filter_name,
                    " [bgp_import_location_unm49] Adding BGP_LC_FUNCTION_LOCATION_UNM49 with ", location, " to ", net;
                bgp_large_community.add((BGP_ASN, BGP_LC_FUNCTION_LOCATION_UNM49, location));
            }"""

    # Local pref manipulation
    @bird_function("bgp_import_localpref")
    def import_localpref(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_localpref function."""

        return """\
            # BGP import local_pref manipulation
            function bgp_import_localpref(string filter_name) {
                # If we are reducing local_pref by three
                if (BGP_LC_LOCALPREF_MINUS_THREE ~ bgp_large_community) then {
                    if DEBUG then print filter_name,
                        " [bgp_import_localpref] Matched BGP_LC_LOCALPREF_MINUS_THREE for ", net;
                    bgp_local_pref = bgp_local_pref - 3;
                # If we are reducing local_pref by two
                } else if (BGP_LC_LOCALPREF_MINUS_TWO ~ bgp_large_community) then {
                    if DEBUG then print filter_name,
                        " [bgp_import_localpref] Matched BGP_LC_LOCALPREF_MINUS_TWO for ", net;
                    bgp_local_pref = bgp_local_pref - 2;
                # If we are reducing local_pref by one
                } else if (BGP_LC_LOCALPREF_MINUS_ONE ~ bgp_large_community) then {
                    if DEBUG then print filter_name,
                        " [bgp_import_localpref] Matched BGP_LC_LOCALPREF_MINUS_ONE for ", net;
                    bgp_local_pref = bgp_local_pref - 1;
                }
            }"""

    @bird_function("bgp_import_graceful_shutdown")
    def import_graceful_shutdown(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_import_graceful_shutdown function."""

        return """\
            function bgp_import_graceful_shutdown(string filter_name) {
                if (BGP_COMMUNITY_GRACEFUL_SHUTDOWN !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_graceful_shutdown] Setting LOCAL_PREF to 0 for ", net;
                bgp_local_pref = 0;
            }"""

    @bird_function("bgp_export_ok")
    def export_ok(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_export_ok function."""

        return f"""\
            # Can we export this route to the peer_asn?
            function bgp_export_ok(
                string filter_name; int peer_asn;
                int ipv4_maxlen; int ipv4_minlen;
                int ipv6_maxlen; int ipv6_minlen
            )
            int prefix_maxlen;
            int prefix_minlen;
            {{
                # Work out what prefix lenghts we're going to use
                if (net.type = NET_IP4) then {{
                    prefix_maxlen = ipv4_maxlen;
                    prefix_minlen = ipv4_minlen;
                }}
                if (net.type = NET_IP6) then {{
                    prefix_maxlen = ipv6_maxlen;
                    prefix_minlen = ipv6_minlen;
                }}
                # Check for NOEXPORT large community
                if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_export_ok] Not exporting due to BGP_LC_FUNCTION_NOEXPORT for AS", peer_asn ," for ", net;
                    return false;
                }}
                # Validate route before export
                if {self.functions.prefix_is_longer(BirdVariable("prefix_maxlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_export_ok] Not exporting due to prefix length >", prefix_maxlen," for ", net;
                    return false;
                }}
                if {self.functions.prefix_is_shorter(BirdVariable("prefix_minlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_export_ok] Not exporting due to prefix length <", prefix_minlen, " for ", net;
                    return false;
                }}
                # Check if this is a bogon
                if {self.functions.is_bogon()} then {{
                    if DEBUG then print filter_name,
                        " [bgp_export_ok] Not exporting due to ", net, " being a bogon";
                    return false;
                }}
                # If all above tests are ok, then we can
                return true;
            }}"""

    @bird_function("bgp_accept")
    def accept(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_accept function."""

        return """\
            # Accept BGP route into the main BGP table
            function bgp_accept(string filter_name) {
                if DEBUG then print filter_name,
                    " [bgp_accept] Exporting ", net, " to main BGP table";
                accept;
            }"""

    @bird_function("bgp_accept_blackhole")
    def accept_blackhole(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_accept_blackhole function."""

        return """\
            # Accept BGP blackhole
            function bgp_accept_blackhole(string filter_name) {
                if (BGP_COMMUNITY_BLACKHOLE !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_blackhole] Enabling blackhole for ", net;
                # Set destination as blackhole
                dest = RTD_BLACKHOLE;
                # Make sure we have our NOEXPORT community set
                if (BGP_COMMUNITY_NOEXPORT !~ bgp_community) then bgp_community.add(BGP_COMMUNITY_NOEXPORT);
            }"""

    @bird_function("bgp_accept_blackhole_originated")
    def accept_blackhole_originated(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_accept_blackhole_originated function."""

        return """\
            # Origination blackhole action
            function bgp_accept_blackhole_originated(string filter_name) {
                if (BGP_LC_ACTION_BLACKHOLE_ORIGINATE !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_blackhole_originated] Enabling origination blackhole for ", net;
                # Set destination as blackhole
                dest = RTD_BLACKHOLE;
            }"""

    @bird_function("bgp_filter_default")
    def filter_default(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_default function."""

        return f"""\
            # Filter default route
            function bgp_filter_default(string filter_name) {{
                if !{self.functions.is_default()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_default] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);
                accept;
            }}"""

    @bird_function("bgp_filter_nexthop_not_peerip")
    def filter_nexthop_not_peerip(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_nexthop_not_peerip function."""

        return """\
            # Filter peer != next_hop
            function bgp_filter_nexthop_not_peerip(string filter_name) {
                if (from = bgp_next_hop) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_nexthop_not_peerip] Adding BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP);
            }"""

    @bird_function("bgp_filter_aspath_length")
    def filter_aspath_length(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_aspath_length function."""

        return """\
            # Filter AS-PATH length
            function bgp_filter_aspath_length(string filter_name; int aspath_maxlen; int aspath_minlen) {
                if (bgp_path.len > aspath_maxlen) then {
                    if DEBUG then print filter_name,
                        " [bgp_filter_aspath_length] AS-PATH length >", aspath_maxlen,
                        ", adding BGP_LC_FILTERED_ASPATH_TOO_LONG to ", net;
                    bgp_large_community.add(BGP_LC_FILTERED_ASPATH_TOO_LONG);
                }
                if (bgp_path.len < aspath_minlen) then {
                    if DEBUG then print filter_name,
                        " [bgp_filter_aspath_length] AS-PATH length <", aspath_minlen,
                        ", adding BGP_LC_FILTERED_ASPATH_TOO_SHORT to ", net;
                    bgp_large_community.add(BGP_LC_FILTERED_ASPATH_TOO_SHORT);
                }
            }"""

    @bird_function("bgp_filter_bogons")
    def filter_bogons(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_bogons function."""

        return f"""\
            # Filter bogons
            function bgp_filter_bogons(string filter_name) {{
                if !{self.functions.is_bogon()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_bogons] Adding BGP_FILTERED_BOGON to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_BOGON);
            }}"""

    @bird_function("bgp_filter_asn_bogons")
    def filter_asn_bogons(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_asn_bogons function."""

        return """\
            # Filter bogon ASNs
            function bgp_filter_asn_bogons(string filter_name) {
                if (bgp_path !~ BOGON_ASNS) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_asn_bogons] Adding BGP_LC_FILTERED_BOGON_ASN to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_BOGON_ASN);
            }"""

    @bird_function("bgp_filter_asn_private")
    def filter_asn_private(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_asn_private function."""

        return """\
            # Filter private ASN's
            function bgp_filter_asn_private(string filter_name; int set allowed_asns) {
                if (bgp_path = filter(bgp_path, allowed_asns)) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_asn_private] Adding BGP_LC_FILTERED_ASPATH_NOT_ALLOWED to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_ASPATH_NOT_ALLOWED);
            }"""

    @bird_function("bgp_filter_asn_invalid")
    def filter_asn_invalid(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_asn_invalid function."""

        return """\
            # Filter peer ASN != route first ASN
            function bgp_filter_asn_invalid(string filter_name; int peer_asn) {
                if (bgp_path.first = peer_asn) then return false;
                if DEBUG then print filter_name,
                        " [bgp_filter_asn_invalid] Adding BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS);
            }"""

    @bird_function("bgp_filter_asn_transit")
    def filter_asn_transit(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_asn_transit function."""

        return """\
            # Filter transit free ASNs
            function bgp_filter_asn_transit(string filter_name) {
                if (bgp_path !~ BGP_ASNS_TRANSIT) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_asn_transit] Adding BGP_LC_FILTERED_TRANSIT_FREE_ASN to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_TRANSIT_FREE_ASN);
            }"""

    @bird_function("bgp_filter_blackhole")
    def filter_blackhole(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_blackhole function."""

        return """\
            # Filter blackhole routes
            function bgp_filter_blackhole(string filter_name) {
                if (BGP_COMMUNITY_BLACKHOLE !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_blackhole] Adding BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED);
            }"""

    @bird_function("bgp_filter_blackhole_size")
    def filter_blackhole_size(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_blackhole_size function."""

        return f"""\
            # Filter blackhole size
            function bgp_filter_blackhole_size(
                string filter_name;
                int ipv4_maxlen; int ipv4_minlen;
                int ipv6_maxlen; int ipv6_minlen
            )
            int prefix_maxlen;
            int prefix_minlen;
            {{
                # Work out what prefix lenghts we're going to use
                if (net.type = NET_IP4) then {{
                    prefix_maxlen = ipv4_maxlen;
                    prefix_minlen = ipv4_minlen;
                }}
                if (net.type = NET_IP6) then {{
                    prefix_maxlen = ipv6_maxlen;
                    prefix_minlen = ipv6_minlen;
                }}
                # If this is not a blackhole prefix then just return
                if (BGP_COMMUNITY_BLACKHOLE !~ bgp_community) then return false;
                # Check prefix is not longer than what we allow
                if {self.functions.prefix_is_longer(BirdVariable("prefix_maxlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_filter_prefix_size] Blackhole length >", prefix_maxlen,
                        ", adding BGP_FILTERED_BLACKHOLE_LEN_TOO_LONG to ", net;
                    bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_LEN_TOO_LONG);
                }}
                # Check prefix is not shorter than what we allow
                if {self.functions.prefix_is_shorter(BirdVariable("prefix_minlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_filter_prefix_size] Blackhole length <", prefix_minlen,
                        ", adding BGP_FILTERED_BLACKHOLE_LEN_TOO_SHORT to ", net;
                    bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_LEN_TOO_SHORT);
                }}
            }}"""

    @bird_function("bgp_filter_prefix_size")
    def filter_prefix_size(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_prefix_size function."""

        return f"""\
            # Filter prefix size
            function bgp_filter_prefix_size(
                string filter_name;
                int ipv4_maxlen; int ipv4_minlen;
                int ipv6_maxlen; int ipv6_minlen
            )
            int prefix_maxlen;
            int prefix_minlen;
            {{
                # Work out what prefix lenghts we're going to use
                if (net.type = NET_IP4) then {{
                    prefix_maxlen = ipv4_maxlen;
                    prefix_minlen = ipv4_minlen;
                }}
                if (net.type = NET_IP6) then {{
                    prefix_maxlen = ipv6_maxlen;
                    prefix_minlen = ipv6_minlen;
                }}
                # If this is a blackhole prefix then just return, it will be caught later
                if (BGP_COMMUNITY_BLACKHOLE ~ bgp_community) then return false;
                # Check prefix length is within the range we allow
                if {self.functions.prefix_is_longer(BirdVariable("prefix_maxlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_filter_prefix_size] Prefix length >", prefix_maxlen,
                        ", adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", net;
                    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);
                }}
                # Check prefix length is within the range we allow
                if {self.functions.prefix_is_shorter(BirdVariable("prefix_minlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_filter_prefix_size] Prefix length <", prefix_minlen,
                        ", adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", net;
                    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);
                }}
            }}"""

    @bird_function("bgp_filter_community_lengths")
    def filter_community_lengths(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_community_lengths function."""

        return """\
            # Filter too many communities
            function bgp_filter_community_lengths(string filter_name; int community_maxlen; int ext_maxlen; int large_maxlen) {
                if (bgp_community.len > community_maxlen) then {
                    if DEBUG then print filter_name,
                        " [bgp_filter_community_lengths] Community list length >", community_maxlen,
                        ", adding BGP_LC_FILTERED_TOO_MANY_COMMUNITIES to ", net, " counted ", bgp_community.len;
                    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_COMMUNITIES);
                }
                if (bgp_ext_community.len > ext_maxlen) then {
                    if DEBUG then print filter_name,
                        " [bgp_filter_community_lengths] Extended community list length >", ext_maxlen,
                        ", adding BGP_LC_FILTERED_TOO_MANY_EXTENDED_COMMUNITIES to ", net, " counted ", bgp_ext_community.len;
                    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_EXTENDED_COMMUNITIES);
                }
                if (bgp_large_community.len > large_maxlen) then {
                    if DEBUG then print filter_name,
                        " [bgp_filter_community_lengths] Large community list length >", large_maxlen,
                        ", adding BGP_LC_FILTERED_TOO_MANY_LARGE_COMMUNITIES to ", net, " counted ", bgp_large_community.len;
                    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_LARGE_COMMUNITIES);
                }
            }"""

    @bird_function("bgp_filter_lc_no_relation")
    def filter_lc_no_relation(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_lc_no_relation function."""

        return """\
            # Filter prefixes without a large community relation set
            function bgp_filter_lc_no_relation(string filter_name) {
                if (bgp_large_community ~ BGP_LC_RELATION) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_lc_no_relation] Adding BGP_LC_FILTERED_NO_RELATION_LC to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_NO_RELATION_LC);
            }"""

    @bird_function("bgp_filter_origin_asns_allow")
    def filter_origin_asns_allow(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_origin_asns_allow function."""

        return """\
            # Filter origin ASNs (ALLOW list)
            function bgp_filter_origin_asns_allow(string filter_name; int set asns) {
                if (bgp_path.last_nonaggregated ~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_origin_asns_allow] Adding BGP_LC_FILTERED_ORIGIN_AS to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS);
            }"""

    @bird_function("bgp_filter_origin_asns_deny")
    def filter_origin_asns_deny(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_origin_asns_deny function."""

        return """\
            # Filter origin ASNs (DENY list)
            function bgp_filter_origin_asns_deny(string filter_name; int set asns) {
                if (bgp_path.last_nonaggregated !~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_origin_asns_deny] Adding BGP_LC_FILTERED_ORIGIN_AS to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS);
            }"""

    @bird_function("bgp_filter_peer_asns_allow")
    def filter_peer_asns_allow(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_peer_asns_allow function."""

        return """\
            # Filter peer ASNs (ALLOW list)
            function bgp_filter_peer_asns_allow(string filter_name; int set asns) {
                if (bgp_path.first ~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_peer_asns_allow] Adding BGP_LC_FILTERED_PEER_AS to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_PEER_AS);
            }"""

    @bird_function("bgp_filter_peer_asns_deny")
    def filter_peer_asns_deny(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_peer_asns_deny function."""

        return """\
            # Filter peer ASNs (DENY list)
            function bgp_filter_peer_asns_deny(string filter_name; int set asns) {
                if (bgp_path.first !~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_peer_asns_deny] Adding BGP_LC_FILTERED_PEER_AS to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_PEER_AS);
            }"""

    @bird_function("bgp_filter_prefixes_allow")
    def filter_prefixes_allow(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_prefixes_allow function."""

        return """\
            # Filter prefixes (ALLOW)
            function bgp_filter_prefixes_allow(string filter_name; prefix set prefix_list) {
                if (net ~ prefix_list) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_prefixes_allow] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);
            }"""

    @bird_function("bgp_filter_prefixes_deny")
    def filter_prefixes_deny(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_filter_prefixes_deny function."""

        return """\
            # Filter prefixes (DENY)
            function bgp_filter_prefixes_deny(string filter_name; prefix set prefix_list) {
                if (net !~ prefix_list) then return false;
                if DEBUG then print filter_name,
                    " [bgp_filter_prefixes_deny] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", net;
                bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);
            }"""

    @bird_function("bgp_redistribute_connected")
    def redistribute_connected(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_connected function."""

        return """\
            # Check for redistribution of connected routes for BGP
            # - Reject routes that are not redistributable
            # - Return true when routes are redistributable
            # - Return false otherwise
            function bgp_redistribute_connected(string filter_name; bool redistribute) {
                # Check for connected routes
                if (proto != "direct4_bgp" && proto != "direct6_bgp") then return false;
                if (redistribute) then {
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_connected] Accepting ", net, " due to direct route match",
                        " (redistribute connected)";
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_redistribute_connected] Rejecting ", net, " due to direct route match",
                    " (no redistribute connected)";
                reject;
            }"""

    @bird_function("bgp_redistribute_static")
    def redistribute_static(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_static function."""

        return """\
            # Check for redistribution of static routes for BGP
            # - Reject routes that are not redistributable
            # - Return true when routes are redistributable
            # - Return false otherwise
            function bgp_redistribute_static(string filter_name; bool redistribute) {
                # Check for static routes
                if (proto != "static4" && proto != "static6") then return false;
                if (redistribute) then {
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_static] Accepting ", net, " due to static route match (redistribute static)";
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_redistribute_static] Rejecting ", net, " due to static route match (no redistribute static)";
                reject;
            }"""

    @bird_function("bgp_redistribute_kernel")
    def redistribute_kernel(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_kernel function."""

        return """\
            # Check for redistribution of kernel routes for BGP
            # - Reject routes that are not redistributable
            # - Return true when routes are redistributable
            # - Return false otherwise
            function bgp_redistribute_kernel(string filter_name; bool redistribute) {
                # Check for kernel routes
                if (source != RTS_INHERIT) then return false;
                if (redistribute) then {
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_kernel] Accepting ", net, " due to kernel route match (redistribute kernel)";
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_redistribute_kernel] Rejecting ", net, " due to kernel route match (no redistribute kernel)";
                reject;
            }"""

    @bird_function("bgp_redistribute_originated")
    def redistribute_originated(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_originated function."""

        return """\
            # Check for redistribution of originated routes for BGP
            # - Reject routes that are not redistributable
            # - Return true when routes are redistributable
            # - Return false otherwise
            function bgp_redistribute_originated(string filter_name; bool redistribute) {
                # Check for originated routes
                if (proto != "bgp_originate4" && proto != "bgp_originate6") then return false;
                if (redistribute) then {
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_originated] Accepting ", net, " due to originated route match ",
                        " (redistribute originated)";
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_redistribute_originated] Rejecting ", net, " due to originated route match ",
                    " (no redistribute originated)";
                reject;
            }"""

    @bird_function("bgp_redistribute_default")
    def redistribute_default(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_default function."""

        return f"""\
            # Check for redistribution of default IPv4 routes for BGP
            # - Reject routes that are not redistributable
            # - Return true when routes are redistributable and accepted
            # - Return false otherwise
            function bgp_redistribute_default(string filter_name; bool redistribute; bool accepted) {{
                # If this is not a default route or is not accepted, return false
                if (!{self.functions.is_default()} || !accepted) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_default] Accepting ", net, " due to default route match",
                        " (redistribute default) and accepted";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_redistribute_default] Rejecting ", net, " due to default route match",
                    " (no redistribute default)";
                reject;
            }}"""

    @bird_function("bgp_redistribute_bgp")
    def redistribute_bgp(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_bgp function."""

        return """\
            # Check for redistribution of all BGP routes
            # - Return true when routes match RTS_BGP
            # - Return false otherwise
            function bgp_redistribute_bgp(string filter_name) {
                # Check for BGP routes
                if (source != RTS_BGP) then return false;
                if DEBUG then print filter_name,
                    " [bgp_redistribute_bgp] Accepting ", net, " due to RTS_BGP route match (redistribute BGP)";
                return true;
            }"""

    @bird_function("bgp_redistribute_bgp_own")
    def redistribute_bgp_own(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_bgp_own function."""

        return """\
            # Check for redistribution of our own routes for BGP
            # - Reject routes that are not exportable
            # - Return true when routes match BGP_LC_RELATION_OWN and are exportable
            # - Return false otherwise
            function bgp_redistribute_bgp_own(string filter_name; bool exportable) {
                # Check for exportable own routes
                if (BGP_LC_RELATION_OWN !~ bgp_large_community) then return false;
                if (exportable) then {
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_bgp_own] Accepting ", net, " due to BGP_LC_RELATION_OWN route match",
                        " (redistribute own) and exportable";
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_redistribute_bgp_own] Rejecting ", net, " due to BGP_LC_RELATION_OWN route match",
                    " (redistribute own) and not exportable";
                reject;
            }"""

    @bird_function("bgp_redistribute_bgp_customer")
    def redistribute_bgp_customer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_bgp_customer function."""

        return """\
            # - Reject routes that are not exportable
            # - Return true when routes match BGP_LC_RELATION_CUSTOMER and are exportable
            # - Return false otherwise
            function bgp_redistribute_bgp_customer(string filter_name; bool exportable) {
                # Check for exportable customer routes
                if (BGP_LC_RELATION_CUSTOMER !~ bgp_large_community) then return false;
                if (exportable) then {
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_bgp_customer] Accepting ", net, " due to BGP_LC_RELATION_CUSTOMER route match",
                        " (redistribute customer) and exportable";
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_redistribute_bgp_customer] Rejecting ", net, " due to BGP_LC_RELATION_CUSTOMER route match",
                    " (redistribute customer) and not exportable";
                reject;
            }"""

    @bird_function("bgp_redistribute_bgp_peering")
    def redistribute_bgp_peering(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_bgp_peering function."""

        return """\
            # Check for redistribution of peering routes for BGP
            # - Reject routes that are not exportable
            # - Return true when routes match BGP_LC_RELATION_PEER and are exportable
            # - Return false otherwise
            function bgp_redistribute_bgp_peering(string filter_name; bool exportable) {
                # Check for exportable peering routes
                if (BGP_LC_RELATION_PEER ~ bgp_large_community) then {
                    if (exportable) then {
                        if DEBUG then print filter_name,
                            " [bgp_redistribute_bgp_peering] Accepting ", net, " due to BGP_LC_RELATION_PEER route match",
                            " (redistribute peering) and exportable";
                        return true;
                    }
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_bgp_peering] Rejecting ", net, " due to BGP_LC_RELATION_PEER route match",
                        " (redistribute peering) and not exportable";
                    reject;
                }
                # Check for exportable routeserver routes
                if (BGP_LC_RELATION_ROUTESERVER ~ bgp_large_community) then {
                    if (exportable) then {
                        if DEBUG then print filter_name,
                            " [bgp_redistribute_bgp_peering] Accepting ", net, " due to BGP_LC_RELATION_ROUTESERVER route match",
                            " (redistribute peering) and exportable";
                        return true;
                    }
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_bgp_peering] Rejecting ", net, " due to BGP_LC_RELATION_ROUTESERVER route match",
                        " (redistribute peering) and not exportable";
                    reject;
                }
                return false;
            }"""

    @bird_function("bgp_redistribute_bgp_transit")
    def redistribute_bgp_transit(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_redistribute_bgp_transit function."""

        return """\
            # - Reject routes that are not exportable
            # - Return true when routes match BGP_LC_RELATION_TRANSIT and are exportable
            # - Return false otherwise
            function bgp_redistribute_bgp_transit(string filter_name; bool exportable) {
                # Check for exportable transit routes
                if (BGP_LC_RELATION_TRANSIT !~ bgp_large_community) then return false;
                if (exportable) then {
                    if DEBUG then print filter_name,
                        " [bgp_redistribute_bgp_transit] Accepting ", net, " due to BGP_LC_RELATION_TRANSIT route match",
                        " (redistribute transit) and exportable";
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_redistribute_bgp_transit] Rejecting ", net, " due to BGP_LC_RELATION_TRANSIT route match",
                    " (redistribute transit) and not exportable";
                reject;
            }"""

    @bird_function("bgp_strip_communities_all")
    def strip_communities_all(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_strip_communities_all function."""

        return """\
            # Strip all communities we could interpret internally
            function bgp_strip_communities_all(string filter_name)
            bool stripped_community;
            bool stripped_lc;
            bool stripped_lc_private;
            {
                stripped_community = false;
                stripped_lc = false;
                stripped_lc_private = false;
                # Sanitize communities
                if (bgp_community ~ BGP_COMMUNITY_STRIP_ALL) then {
                    if DEBUG then print filter_name,
                        " [bgp_strip_communities_all] Sanitizing communities for ", net;
                    bgp_community.delete(BGP_COMMUNITY_STRIP_ALL);
                    stripped_community = true;
                }
                # Sanitize large communities
                if (bgp_large_community ~ BGP_LC_STRIP_ALL) then {
                    if DEBUG then print filter_name,
                        " [bgp_strip_communities_all] Sanitizing large communities for ", net;
                    bgp_large_community.delete(BGP_LC_STRIP_ALL);
                    stripped_lc = true;
                }
                # Sanitize private large communities
                if (bgp_large_community ~ BGP_LC_STRIP_PRIVATE) then {
                    if DEBUG then print filter_name,
                        " [bgp_strip_communities_all] Sanitizing private large communities for ", net;
                    bgp_large_community.delete(BGP_LC_STRIP_PRIVATE);
                    stripped_lc_private = true;
                }
                if (stripped_community) then {
                    if DEBUG then print filter_name,
                        " [bgp_strip_communities_all] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ", net;
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY);
                }
                if (stripped_lc) then {
                    if DEBUG then print filter_name,
                        " [bgp_strip_communities_all] Adding BGP_LC_INFORMATION_STRIPPED_LC to ", net;
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC);
                }
                if (stripped_lc_private) then {
                    if DEBUG then print filter_name,
                        " [bgp_strip_communities_all] Adding BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE to ", net;
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE);
                }
            }"""

    @bird_function("bgp_lc_add_default")
    def lc_add_default(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_default function."""

        return f"""\
            function bgp_lc_add_default(string filter_name; lc large_community) {{
                if !{self.functions.is_default()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_default] Adding large community ", large_community, " for type DEFAULT to ", net;
                bgp_large_community.add(large_community);
            }}"""

    @bird_function("bgp_lc_add_connected")
    def lc_add_connected(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_connected function."""

        return """\
            function bgp_lc_add_connected(string filter_name; lc large_community) {
                if (proto != "direct4_bgp" && proto != "direct6_bgp") then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_connected] Adding large community ", large_community, " for type CONNECTED to ", net;
                bgp_large_community.add(large_community);
            }"""

    @bird_function("bgp_lc_add_static")
    def lc_add_static(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_static function."""

        return f"""\
            function bgp_lc_add_static(string filter_name; lc large_community) {{
                if ((proto != "static4" && proto != "static6") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_static] Adding large community ", large_community, " for type STATIC to ", net;
                bgp_large_community.add(large_community);
            }}"""

    @bird_function("bgp_lc_add_kernel")
    def lc_add_kernel(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_kernel function."""

        return f"""\
            function bgp_lc_add_kernel(string filter_name; lc large_community) {{
                if (source != RTS_INHERIT || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_kernel] Adding large community ", large_community, " for type KERNEL to ", net;
                bgp_large_community.add(large_community);
            }}"""

    @bird_function("bgp_lc_add_originated")
    def lc_add_originated(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_originated function."""

        return f"""\
            # BGP originated route large community adding
            function bgp_lc_add_originated(string filter_name; lc large_community) {{
                if ((proto != "bgp_originate4" && proto != "bgp_originate6") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_originate] Adding large community ", large_community, " for type ORIGINATED to ", net;
                bgp_large_community.add(large_community);
            }}"""

    @bird_function("bgp_lc_add_bgp")
    def lc_add_bgp(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_bgp function."""

        return """\
            # BGP large community adding
            function bgp_lc_add_bgp(string filter_name; lc large_community) {
                if DEBUG then print filter_name,
                    " [bgp_lc_add_bgp] Adding large community ", large_community, " for type BGP to ", net;
                bgp_large_community.add(large_community);
            }"""

    @bird_function("bgp_lc_add_bgp_own")
    def lc_add_bgp_own(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_bgp_own function."""

        return """\
            # BGP own route large community adding
            function bgp_lc_add_bgp_own(string filter_name; lc large_community) {
                if (BGP_LC_RELATION_OWN !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_bgp_own] Adding large community ", large_community, " for type BGP_OWN to ", net;
                bgp_large_community.add(large_community);
            }"""

    @bird_function("bgp_lc_add_bgp_customer")
    def lc_add_bgp_customer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_bgp_customer function."""

        return """\
            # BGP customer route large community adding
            function bgp_lc_add_bgp_customer(string filter_name; lc large_community) {
                if (BGP_LC_RELATION_CUSTOMER !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_bgp_customer] Adding large community ", large_community, " for type BGP_CUSTOMER to ", net;
                bgp_large_community.add(large_community);
            }"""

    @bird_function("bgp_lc_add_bgp_peering")
    def lc_add_bgp_peering(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_bgp_peering function."""

        return """\
            # BGP peering route large community adding
            function bgp_lc_add_bgp_peering(string filter_name; lc large_community) {
                if (
                    BGP_LC_RELATION_PEER !~ bgp_large_community
                    && BGP_LC_RELATION_ROUTESERVER !~ bgp_large_community
                ) then return false;
                if DEBUG then print filter_name,
                        " [bgp_lc_add_bgp_peer] Adding large community ", large_community, " for type BGP_PEER to ", net;
                bgp_large_community.add(large_community);
            }"""

    @bird_function("bgp_lc_add_bgp_transit")
    def lc_add_bgp_transit(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_lc_add_bgp_transit function."""

        return """\
            # BGP transit route large community adding
            function bgp_lc_add_bgp_transit(string filter_name; lc large_community) {
                if (BGP_LC_RELATION_TRANSIT !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_lc_add_bgp_transit] Adding large community ", large_community, " for type BGP_TRANSIT to ", net;
                bgp_large_community.add(large_community);
            }"""

    @bird_function("bgp_prepend")
    def prepend(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend function."""

        return """\
            # BGP prepending
            function bgp_prepend(string filter_name; int peer_asn; int prepend_count) {
                if (prepend_count > 0) then bgp_path.prepend(peer_asn);
                if (prepend_count > 1) then bgp_path.prepend(peer_asn);
                if (prepend_count > 2) then bgp_path.prepend(peer_asn);
                if (prepend_count > 3) then bgp_path.prepend(peer_asn);
                if (prepend_count > 4) then bgp_path.prepend(peer_asn);
                if (prepend_count > 5) then bgp_path.prepend(peer_asn);
                if (prepend_count > 6) then bgp_path.prepend(peer_asn);
                if (prepend_count > 7) then bgp_path.prepend(peer_asn);
                if (prepend_count > 8) then bgp_path.prepend(peer_asn);
                if (prepend_count > 9) then bgp_path.prepend(peer_asn);
            }"""

    @bird_function("bgp_prepend_default")
    def prepend_default(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_default function."""

        return f"""\
            function bgp_prepend_default(string filter_name; int peer_asn; int prepend_count) {{
                if !{self.functions.is_default()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_default] Prepending AS-PATH for type DEFAULT ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_connected")
    def prepend_connected(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_connected function."""

        return f"""\
            # BGP connected route prepending
            function bgp_prepend_connected(string filter_name; int peer_asn; int prepend_count) {{
                if (proto != "direct4_bgp" && proto != "direct6_bgp") then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_connected] Prepending AS-PATH for type CONNECTED ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_static")
    def prepend_static(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_static function."""

        return f"""\
            function bgp_prepend_static(string filter_name; int peer_asn; int prepend_count) {{
                if ((proto != "static4" && proto != "static6") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_static] Prepending AS-PATH for type STATIC ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_kernel")
    def prepend_kernel(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_kernel function."""

        return f"""\
            function bgp_prepend_kernel(string filter_name; int peer_asn; int prepend_count) {{
                if (source != RTS_INHERIT || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_kernel] Prepending AS-PATH for type KERNEL ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_originated")
    def prepend_originated(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_originated function."""

        return f"""\
            function bgp_prepend_originated(string filter_name; int peer_asn; int prepend_count) {{
                if ((proto != "bgp_originate4" && proto != "bgp_originate6") || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_originate] Prepending AS-PATH for type ORIGINATED ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_bgp")
    def prepend_bgp(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_bgp function."""

        return f"""\
            # BGP route prepending
            function bgp_prepend_bgp(string filter_name; int peer_asn; int prepend_count)
            {{
                if DEBUG then print filter_name,
                    " [bgp_prepend_bgp] Prepending AS-PATH for type BGP ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_bgp_own")
    def prepend_bgp_own(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_bgp_own function."""

        return f"""\
            # BGP own route prepending
            function bgp_prepend_bgp_own(string filter_name; int peer_asn; int prepend_count) {{
                if (BGP_LC_RELATION_OWN !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_bgp_own] Prepending AS-PATH for type BGP_OWN ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_bgp_customer")
    def prepend_bgp_customer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_bgp_customer function."""

        return f"""\
            # BGP customer route prepending
            function bgp_prepend_bgp_customer(string filter_name; int peer_asn; int prepend_count) {{
                if (BGP_LC_RELATION_CUSTOMER !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_bgp_customer] Prepending AS-PATH for type BGP_CUSTOMER ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_bgp_peering")
    def prepend_bgp_peering(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_bgp_peering function."""

        return f"""\
            # BGP peering route prepending
            function bgp_prepend_bgp_peering(string filter_name; int peer_asn; int prepend_count) {{
                if (
                    BGP_LC_RELATION_PEER !~ bgp_large_community
                    && BGP_LC_RELATION_ROUTESERVER !~ bgp_large_community
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_bgp_peer] Prepending AS-PATH for type BGP_PEER ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_bgp_transit")
    def prepend_bgp_transit(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_bgp_transit function."""

        return f"""\
            # BGP transit route prepending
            function bgp_prepend_bgp_transit(string filter_name; int peer_asn; int prepend_count) {{
                if (BGP_LC_RELATION_TRANSIT !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_prepend_bgp_transit] Prepending AS-PATH for type BGP_TRANSIT ", prepend_count, "x to ", net;
                {self.prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @bird_function("bgp_prepend_lc")
    def prepend_lc(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_lc function."""

        return f"""\
            # BGP large community based prepending
            function bgp_prepend_lc(string filter_name; int peer_asn)
            int prepend_asn;
            {{
                # Make sure we use the right ASN when prepending, and not 0 if bgp_path is empty
                if (bgp_path.len = 0) then {{
                    prepend_asn = BGP_ASN;
                }} else {{
                    prepend_asn = bgp_path.first;
                }}
                # If we are prepending three times
                if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_THREE, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_THREE for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 3)};
                # If we are prepending two times
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_TWO, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_TWO for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 2)};
                # If we are prepending one time
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_ONE, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_ONE for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 1)};
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_ONE_2, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_ONE_2 for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 1)};
                }}
            }}"""

    @bird_function("bgp_prepend_lc_location")
    def prepend_lc_location(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_prepend_location function."""

        return f"""\
            # BGP large community location based prepending
            function bgp_prepend_lc_location(string filter_name; int location)
            int prepend_asn;
            {{
                # Make sure we use the right ASN when prepending, and not 0 if bgp_path is empty
                if (bgp_path.len = 0) then {{
                    prepend_asn = BGP_ASN;
                }} else {{
                    prepend_asn = bgp_path.first;
                }}
                # If we are prepending three times
                if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_LOCATION_THREE, location) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_THREE for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 3)};
                # If we are prepending two times
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_LOCATION_TWO, location) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_TWO for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 2)};
                # If we are prepending one time
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_LOCATION_ONE, location) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_ONE for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 1)};
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_LOCATION_ONE_2, location) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_ONE_2 for ", net;
                    {self.prepend(BirdVariable("prepend_asn"), 1)};
                }}
            }}"""

    @bird_function("bgp_allow_blackholes")
    def allow_blackholes(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_allow_blackholes function."""

        return """\
            # Check if we're allowing blackholes tagged with the blackhole large community
            function bgp_allow_blackholes(string filter_name; bool capable; int peer_asn; int type_asn) {
                # If this is not a route with a blackhole community, then just return false
                if (BGP_COMMUNITY_BLACKHOLE !~ bgp_community) then return false;
                # If this is a blackhole community, check if we're going to allow it
                if (
                    (BGP_ASN, 666, peer_asn) ~ bgp_large_community ||
                    (BGP_ASN, 666, type_asn) ~ bgp_large_community
                ) then {
                    # Check if the peer is blackhole community capable
                    if (!capable) then {
                        if DEBUG then print filter_name,
                            " [bgp_allow_blackholes] Rejecting blackhole ", net,
                            " due to peer not being blackhole community capable";
                        reject;
                    }
                    # Check if we have a NOEXPORT community set, if we do strip it off")
                    if (BGP_COMMUNITY_NOEXPORT ~ bgp_community) then {
                        if DEBUG then print filter_name,
                            " [bgp_allow_blackholes] Removing community BGP_COMMUNITY_NOEXPORT from ", net,
                            " due to match on BGP blackhole advertise large community function";
                        bgp_community.delete(BGP_COMMUNITY_NOEXPORT);
                    }
                    return true;
                }
                if DEBUG then print filter_name,
                    " [bgp_allow_blackholes] Rejecting blackhole ", net,
                    " due to no match on BGP blackhole advertise large community function";
                reject;
            }"""

    @bird_function("bgp_reject_blackholes")
    def reject_blackholes(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_blackholes function."""

        return """\
            # Reject blackhole routes
            function bgp_reject_blackholes(string filter_name) {
                if (BGP_COMMUNITY_BLACKHOLE !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_blackholes] Rejecting blackhole ", net, " due to match on BGP_COMMUNITY_BLACKHOLE";
                reject;
            }"""

    @bird_function("bgp_reject_noexport")
    def reject_noexport(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_noexport function."""

        return """\
            # Reject NOEXPORT routes
            function bgp_reject_noexport(string filter_name) {
                if (BGP_COMMUNITY_NOEXPORT !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_noexport] Rejecting ", net, " due to match on BGP_COMMUNITY_NOEXPORT";
                reject;
            }"""

    @bird_function("bgp_reject_noexport_customer")
    def reject_noexport_customer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_noexport_customer function."""

        return """\
            # Reject EXPORT_NOCUSTOMER routes
            function bgp_reject_noexport_customer(string filter_name) {
                # Check for large community to prevent export to customers
                if (BGP_LC_EXPORT_NOCUSTOMER !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_noexport_customer] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOCUSTOMER";
                reject;
            }"""

    @bird_function("bgp_reject_noexport_peer")
    def reject_noexport_peer(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_noexport_peer function."""

        return """\
            # Reject EXPORT_NOPEER routes
            function bgp_reject_noexport_peer(string filter_name) {
                # Check for large community to prevent export to peers
                if (BGP_LC_EXPORT_NOPEER !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_noexport_peer] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOPEER";
                reject;
            }"""

    @bird_function("bgp_reject_noexport_transit")
    def reject_noexport_transit(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_noexport_transit function."""

        return """\
            # Reject EXPORT_NOTRANSIT routes
            function bgp_reject_noexport_transit(string filter_name) {
                # Check for large community to prevent export to transit
                if (BGP_LC_EXPORT_NOTRANSIT !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_noexport_transit] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOTRANSIT";
                reject;
            }"""

    @bird_function("bgp_reject_noexport_location")
    def reject_noexport_location(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_noexport_location function."""

        return """\
            # Reject NOEXPORT_LOCATION routes
            function bgp_reject_noexport_location(string filter_name; int location) {
                # Check for large community to prevent export to a location
                if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT_LOCATION, location) !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_noexport_location] Rejecting ", net, " due to match on BGP_LC_FUNCTION_NOEXPORT_LOCATION",
                    " with location ", location;
                reject;
            }"""

    @bird_function("bgp_reject_noadvertise")
    def reject_noadvertise(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_noadvertise function."""

        return """\
            # Reject NO_ADVERTISE routes
            function bgp_reject_noadvertise(string filter_name) {
                # Check for NO_ADVERTISE community
                if (BGP_COMMUNITY_NOADVERTISE !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_noadvertise] Rejecting ", net, " due to match on BGP_COMMUNITY_NOADVERTISE";
                reject;
            }"""

    @bird_function("bgp_reject_filtered")
    def reject_filtered(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_reject_filtered function."""

        return """\
            # Reject filtered routes to main BGP table
            function bgp_reject_filtered(string filter_name) {
                if (bgp_large_community !~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then return false;
                if DEBUG then print filter_name,
                    " [bgp_reject_filtered] Filtered ", net, " to main BGP table";
                reject;
            }"""

    @bird_function("bgp_replace_aspath")
    def replace_aspath(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_replace_aspath function."""

        return f"""\
            # Check if we need to replace the AS-PATH
            function bgp_replace_aspath(string filter_name)
            int path_len;
            {{
                # Check for replace AS-PATH large community action
                if (BGP_LC_ACTION_REPLACE_ASPATH !~ bgp_large_community) then return false;
                # Grab current path length
                path_len = bgp_path.len;
                if DEBUG then print filter_name,
                    " [bgp_replace_aspath] Replacing AS-PATH [", bgp_path, "] for ", net, " with ", path_len, "x ", BGP_ASN;
                # Empty the path, as we cannot assign a sequence
                bgp_path.empty;
                # Prepend our own ASN the number of times there was an ASN in the path
                path_len = path_len - 1;
                {self.prepend(BirdVariable("BGP_ASN"), BirdVariable("path_len"))};
            }}"""

    @bird_function("bgp_remove_lc_private")
    def remove_lc_private(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_remove_lc_private function."""

        return """\
            # Remove private large communities
            function bgp_remove_lc_private(string filter_name) {
                # Remove private large communities
                if (bgp_large_community !~ BGP_LC_STRIP_PRIVATE) then return false;
                if DEBUG then print filter_name,
                    " [bgp_strip_lc_private] Removing private large communities from ", net;
                bgp_large_community.delete(BGP_LC_STRIP_PRIVATE);
            }"""

    @bird_function("bgp_communities_strip_internal")
    def communities_strip_internal(self, *args: Any) -> str:  # pylint: disable=no-self-use,unused-argument
        """BIRD bgp_communities_strip_internal function."""

        return """\
            # Strip internal communities
            function bgp_communities_strip_internal(string filter_name)
            bool stripped_community;
            bool stripped_lc;
            bool stripped_lc_private;
            {
                stripped_community = false;
                stripped_lc = false;
                stripped_lc_private = false;
                # Remove stripped communities
                if (bgp_community ~ BGP_COMMUNITY_STRIP) then {
                    if DEBUG then print filter_name,
                        " [bgp_communities_strip_internal] Removing stripped communities from ", net;
                    bgp_community.delete(BGP_COMMUNITY_STRIP);
                    stripped_community = true;
                }
                # Remove stripped large communities
                if (bgp_large_community ~ BGP_LC_STRIP) then {
                    if DEBUG then print filter_name,
                        " [bgp_communities_strip_internal] Removing stripped large communities from ", net;
                    bgp_large_community.delete(BGP_LC_STRIP);
                    stripped_lc = true;
                }
                # Remove stripped private large communities
                if (bgp_large_community ~ BGP_LC_STRIP_PRIVATE) then {
                    if DEBUG then print filter_name,
                        " [bgp_communities_strip_internal] Removing stripped private large communities from ", net;
                    bgp_large_community.delete(BGP_LC_STRIP_PRIVATE);
                    stripped_lc_private = true;
                }
                if (stripped_community) then {
                    if DEBUG then print filter_name,
                        " [bgp_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ", net;
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY);
                }
                if (stripped_lc) then {
                    if DEBUG then print filter_name,
                        " [bgp_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ", net;
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC);
                }
                if (stripped_lc_private) then {
                    if DEBUG then print filter_name,
                        " [bgp_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE to ", net;
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE);
                }
            }"""

    @property
    def functions(self) -> SectionFunctions:
        """Return the functions section."""
        return self._functions
