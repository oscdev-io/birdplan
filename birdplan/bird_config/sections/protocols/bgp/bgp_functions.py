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

"""BGP protocol specific functions class."""

# pylint: disable=too-many-lines

from typing import Any

from ....globals import BirdConfigGlobals
from ...functions import BirdFunction, BirdVariable, SectionFunctions
from ..base_protocol_functions import ProtocolFunctionsBase

__all__ = ["BGPFunctions"]


class BGPFunctions(ProtocolFunctionsBase):  # pylint: disable=too-many-public-methods
    """BGP protocol specific functions class."""

    def __init__(self, birdconfig_globals: BirdConfigGlobals, functions: SectionFunctions):
        """Initialize the object."""
        super().__init__(birdconfig_globals, functions)

        self._section = "BGP Functions"

    @BirdFunction("bgp_accept_bgp")
    def accept_bgp(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_accept_bgp function."""

        return f"""\
            # Accept bgp routes
            function bgp_accept_bgp(string filter_name) -> bool {{
                if (
                    !{self.functions.is_bgp()} ||
                    {self.is_blackhole()} ||
                    {self.is_originated()} ||
                    {self.functions.is_default()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_bgp] Accepting BGP route ", {self.functions.route_info()};
                accept;
            }}"""

    @BirdFunction("bgp_accept_customer_blackhole")
    def accept_customer_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_accept_customer_blackhole function."""

        return f"""\
            # Accept customer blackhole routes
            function bgp_accept_customer_blackhole(string filter_name) -> bool {{
                if (
                    !{self.functions.is_bgp()} ||
                    !{self.is_blackhole()} ||
                    !{self.is_bgp_customer()} ||
                    {self.functions.is_default()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_customer_blackhole] Accepting BGP customer blackhole route ", {self.functions.route_info()};
                accept;
            }}"""

    @BirdFunction("bgp_accept_own_blackhole")
    def accept_own_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_accept_own_blackhole function."""

        return f"""\
            # Accept own blackhole routes
            function bgp_accept_own_blackhole(string filter_name) -> bool {{
                if (
                    !{self.functions.is_bgp()} ||
                    !{self.is_blackhole()} ||
                    !{self.is_bgp_own()} ||
                    {self.functions.is_default()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_own_blackhole] Accepting BGP own blackhole route ", {self.functions.route_info()};
                accept;
            }}"""

    @BirdFunction("bgp_accept_bgp_own_default")
    def accept_bgp_own_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_accept_bgp_own_default function."""

        return f"""\
            # Accept BGP default routes
            function bgp_accept_bgp_own_default(string filter_name) -> bool {{
                if (
                    !{self.functions.is_bgp()} ||
                    !{self.is_bgp_own()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_bgp_own_default] Accepting BGP own default route ", {self.functions.route_info()};
                accept;
            }}"""

    @BirdFunction("bgp_accept_bgp_transit_default")
    def accept_bgp_transit_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_accept_bgp_transit_default function."""

        return f"""\
            # Accept BGP default routes
            function bgp_accept_bgp_transit_default(string filter_name) -> bool {{
                if (
                    !{self.functions.is_bgp()} ||
                    !{self.is_bgp_transit()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_bgp_transit_default] Accepting BGP transit default route ", {self.functions.route_info()};
                accept;
            }}"""

    @BirdFunction("bgp_accept_originated")
    def accept_originated(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_accept_originated function."""

        return f"""\
            # Accept originated routes
            function bgp_accept_originated(string filter_name) -> bool {{
                if (!{self.is_originated()} || {self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_originated] Accepting originated route ", {self.functions.route_info()};
                accept;
            }}"""

    @BirdFunction("bgp_accept_originated_default")
    def accept_originated_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_accept_originated_default function."""

        return f"""\
            # Accept originated default routes
            function bgp_accept_originated_default(string filter_name) -> bool {{
                if (!{self.is_originated()} || {self.is_blackhole()} || !{self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_accept_originated_default] Accepting originated default route ", {self.functions.route_info()};
                accept;
            }}"""

    @BirdFunction("bgp_is_connected")
    def is_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_connected function."""

        return """\
            # Check if this is an connected route
            function bgp_is_connected(string filter_name) -> bool {
                if (proto = "direct4_bgp" || proto = "direct6_bgp") then return true;
                return false;
            }"""

    @BirdFunction("bgp_is_originated")
    def is_originated(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_originated function."""

        return """\
            # Check if this is an originated route
            function bgp_is_originated(string filter_name) -> bool {
                if (proto = "bgp_originate4" || proto = "bgp_originate6") then return true;
                return false;
            }"""

    @BirdFunction("bgp_is_bgp_customer")
    def is_bgp_customer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_bgp_customer function."""

        return """\
            # Check if this is a route that originated from a customer
            function bgp_is_bgp_customer(string filter_name) -> bool {
                if (BGP_LC_RELATION_CUSTOMER ~ bgp_large_community) then return true;
                return false;
            }"""

    @BirdFunction("bgp_is_bgp_own")
    def is_bgp_own(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_bgp_own function."""

        return f"""\
            # Check if this is a route that originated within our federation
            function bgp_is_bgp_own(string filter_name) -> bool {{
                if ({self.functions.is_bgp()} && BGP_LC_RELATION_OWN ~ bgp_large_community) then return true;
                return false;
            }}"""

    @BirdFunction("bgp_is_bgp_peer")
    def is_bgp_peer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_bgp_peer function."""

        return """\
            # Check if this is a route that originated from a peer
            function bgp_is_bgp_peer(string filter_name) -> bool {
                if (BGP_LC_RELATION_PEER ~ bgp_large_community) then return true;
                return false;
            }"""

    @BirdFunction("bgp_is_bgp_peering")
    def is_bgp_peering(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_bgp_peering function."""

        return f"""\
            # Check if this is a route that originated from a peer or routeserver
            function bgp_is_bgp_peering(string filter_name) -> bool {{
                if ({self.is_bgp_peer()} || {self.is_bgp_routeserver()}) then return true;
                return false;
            }}"""

    @BirdFunction("bgp_is_bgp_routeserver")
    def is_bgp_routeserver(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_bgp_routeserver function."""

        return """\
            # Check if this is a route that originated from a routeserver
            function bgp_is_bgp_routeserver(string filter_name) -> bool {
                if (BGP_LC_RELATION_ROUTESERVER ~ bgp_large_community) then return true;
                return false;
            }"""

    @BirdFunction("bgp_is_bgp_transit")
    def is_bgp_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_bgp_transit function."""

        return """\
            # Check if this is a route that originated from a transit peer
            function bgp_is_bgp_transit(string filter_name) -> bool {
                if (BGP_LC_RELATION_TRANSIT ~ bgp_large_community) then return true;
                return false;
            }"""

    @BirdFunction("bgp_is_blackhole")
    def is_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_is_blackhole function."""

        return """\
            # Check if this is a blackhole route
            function bgp_is_blackhole(string filter_name) -> bool {
                if (BGP_COMMUNITY_BLACKHOLE ~ bgp_community) then return true;
                return false;
            }"""

    @BirdFunction("bgp_import_kernel")
    def import_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_kernel function."""

        return f"""\
            # Import kernel routes
            function bgp_import_kernel(string filter_name) -> bool {{
                if (!{self.functions.is_kernel()} || dest = RTD_BLACKHOLE || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_kernel] Importing kernel route ", {self.functions.route_info()};
                {self.import_own(5)};
                accept;
            }}"""

    @BirdFunction("bgp_import_kernel_blackhole")
    def import_kernel_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_kernel_blackhole function."""

        return f"""\
            # Import kernel blackhole routes
            function bgp_import_kernel_blackhole(string filter_name) -> bool {{
                if (!{self.functions.is_kernel()} || dest != RTD_BLACKHOLE || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_kernel_blackhole] Importing kernel blackhole route ", {self.functions.route_info()};
                {self.import_own(5)};
                bgp_community.add(BGP_COMMUNITY_BLACKHOLE);
                bgp_community.add(BGP_COMMUNITY_NOEXPORT);
                accept;
            }}"""

    @BirdFunction("bgp_import_kernel_default")
    def import_kernel_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_kernel_default function."""

        return f"""\
            # Import kernel default routes
            function bgp_import_kernel_default(string filter_name) -> bool {{
                if (!{self.functions.is_kernel()} || dest = RTD_BLACKHOLE || !{self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_kernel_default] Importing kernel default route ", {self.functions.route_info()};
                {self.import_own(5)};
                accept;
            }}"""

    @BirdFunction("bgp_import_own")
    def import_own(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_own function."""

        return f"""\
            # Import own routes
            function bgp_import_own(string filter_name; int local_pref_cost) {{
                if DEBUG then print filter_name,
                    " [bgp_import_own] Adding BGP_LC_RELATION_OWN to ", {self.functions.route_info()}, " with local pref ",
                    BGP_PREF_OWN - local_pref_cost;
                # Tag route as a our own (originated and static) route
                bgp_large_community.add(BGP_LC_RELATION_OWN);
                # Add our internal blackhole action to originated routes
                if ({self.is_originated()} && dest = RTD_BLACKHOLE) then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_own] Adding BGP_LC_ACTION_BLACKHOLE_ORIGINATE to ", {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_ACTION_BLACKHOLE_ORIGINATE);
                }}
                # Set local preference
                bgp_local_pref = BGP_PREF_OWN - local_pref_cost;
            }}"""

    @BirdFunction("bgp_import_static")
    def import_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_static function."""

        return f"""\
            # Import static routes
            function bgp_import_static(string filter_name) -> bool {{
                if (!{self.functions.is_static()} || dest = RTD_BLACKHOLE || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_static] Importing static route ", {self.functions.route_info()};
                {self.import_own(10)};
                accept;
            }}"""

    @BirdFunction("bgp_import_static_blackhole")
    def import_static_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_static_blackhole function."""

        return f"""\
            # Import static blackhole routes
            function bgp_import_static_blackhole(string filter_name) -> bool {{
                if (!{self.functions.is_static()} || dest != RTD_BLACKHOLE || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_static_blackhole] Importing static blackhole route ", {self.functions.route_info()};
                {self.import_own(10)};
                bgp_community.add(BGP_COMMUNITY_BLACKHOLE);
                bgp_community.add(BGP_COMMUNITY_NOEXPORT);
                accept;
            }}"""

    @BirdFunction("bgp_import_static_default")
    def import_static_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_static_default function."""

        return f"""\
            # Import static default routes
            function bgp_import_static_default(string filter_name) -> bool {{
                if (!{self.functions.is_static()} || dest = RTD_BLACKHOLE || !{self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_static_default] Importing static default route ", {self.functions.route_info()};
                {self.import_own(10)};
                accept;
            }}"""

    @BirdFunction("bgp_peer_reject_non_targetted_blackhole")
    def peer_reject_non_targetted_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_non_targetted_blackhole function."""

        return f"""\
            # Check if we're allowing blackholes tagged with the blackhole large community
            function bgp_peer_reject_non_targetted_blackhole(
                string filter_name;
                bool capable;
                bool allow_kernel_blackhole;
                bool allow_static_blackhole;
                int peer_asn;
                int type_asn
            ) -> bool {{
                # If this is not a route with a blackhole community, then just return false
                if !{self.is_blackhole()} then return false;
                # If this is a blackhole community, check if we're going to allow it
                if (
                    # ASN based ACL
                    ((BGP_ASN, 666, peer_asn) ~ bgp_large_community || (BGP_ASN, 666, type_asn) ~ bgp_large_community) ||
                    # Kernel blackholes
                    (allow_kernel_blackhole && {self.functions.is_kernel()}) ||
                    # Static blackholes
                    (allow_static_blackhole && {self.functions.is_static()})
                ) then {{
                    # Check if the peer is blackhole community capable
                    if (!capable) then {{
                        if DEBUG then print filter_name,
                            " [bgp_peer_reject_non_targetted_blackhole] Rejecting blackhole ", {self.functions.route_info()},
                            " due to peer not being blackhole community capable";
                        reject;
                    }}
                    # Check if we have a NOEXPORT community set, if we do strip it off")
                    if (BGP_COMMUNITY_NOEXPORT ~ bgp_community) then {{
                        if DEBUG then print filter_name,
                            " [bgp_peer_reject_non_targetted_blackhole] Removing community BGP_COMMUNITY_NOEXPORT from ",
                            {self.functions.route_info()}, " due to match on BGP blackhole advertise large community function";
                        bgp_community.delete(BGP_COMMUNITY_NOEXPORT);
                    }}
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_non_targetted_blackhole] Rejecting blackhole ", {self.functions.route_info()},
                    " due to no match on BGP blackhole advertise large community function";
                reject;
            }}"""

    @BirdFunction("bgp_peer_accept")
    def peer_accept(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_accept function."""

        return f"""\
            # Accept BGP route into the main BGP table
            function bgp_peer_accept(string filter_name) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_accept] Exporting ", {self.functions.route_info()}, " to main BGP table";
                accept;
            }}"""

    @BirdFunction("bgp_peer_accept_blackhole")
    def peer_accept_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_accept_blackhole function."""

        return f"""\
            # Accept BGP blackhole
            function bgp_peer_accept_blackhole(string filter_name) -> bool {{
                if !{self.is_blackhole()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_accept_blackhole] Enabling blackhole for ", {self.functions.route_info()};
                # Set destination as blackhole
                dest = RTD_BLACKHOLE;
                # Make sure we have our NOEXPORT community set
                if (BGP_COMMUNITY_NOEXPORT !~ bgp_community) then bgp_community.add(BGP_COMMUNITY_NOEXPORT);
            }}"""

    @BirdFunction("bgp_peer_accept_blackhole_originated")
    def peer_accept_blackhole_originated(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_accept_blackhole_originated function."""

        return f"""\
            # Origination blackhole action
            function bgp_peer_accept_blackhole_originated(string filter_name) -> bool {{
                if (BGP_LC_ACTION_BLACKHOLE_ORIGINATE !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_accept_blackhole_originated] Enabling origination blackhole for ",
                    {self.functions.route_info()};
                # Set destination as blackhole
                dest = RTD_BLACKHOLE;
            }}"""

    @BirdFunction("bgp_peer_communities_strip_all")
    def peer_communities_strip_all(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_communities_strip_all function."""

        return f"""\
            # Strip all communities we could interpret internally
            function bgp_peer_communities_strip_all(string filter_name)
            bool stripped_community;
            bool stripped_community_private;
            bool stripped_lc;
            bool stripped_lc_private;
            {{
                stripped_community = false;
                stripped_community_private = false;
                stripped_lc = false;
                stripped_lc_private = false;
                # Sanitize communities
                if (bgp_community ~ BGP_COMMUNITY_STRIP_ALL) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Sanitizing communities for ", {self.functions.route_info()};
                    bgp_community.delete(BGP_COMMUNITY_STRIP_ALL);
                    stripped_community = true;
                }}
                # Sanitize large communities
                if (bgp_large_community ~ BGP_LC_STRIP_ALL) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Sanitizing large communities for ", {self.functions.route_info()};
                    bgp_large_community.delete(BGP_LC_STRIP_ALL);
                    stripped_lc = true;
                }}
                # Sanitize private communities
                if (bgp_community ~ BGP_COMMUNITY_STRIP_PRIVATE) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Sanitizing private communities for ",
                        {self.functions.route_info()};
                    bgp_community.delete(BGP_COMMUNITY_STRIP_PRIVATE);
                    stripped_community_private = true;
                }}
                # Sanitize private large communities
                if (bgp_large_community ~ BGP_LC_STRIP_PRIVATE) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Sanitizing private large communities for ",
                        {self.functions.route_info()};
                    bgp_large_community.delete(BGP_LC_STRIP_PRIVATE);
                    stripped_lc_private = true;
                }}
                #
                # Output debug info and do the actual stripping
                #
                if (stripped_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY);
                }}
                if (stripped_community_private) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY_PRIVATE to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY_PRIVATE);
                }}
                if (stripped_lc) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Adding BGP_LC_INFORMATION_STRIPPED_LC to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC);
                }}
                if (stripped_lc_private) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_all] Adding BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE);
                }}
            }}"""

    @BirdFunction("bgp_peer_communities_strip_internal")
    def peer_communities_strip_internal(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_communities_strip_internal function."""

        return f"""\
            # Strip internal communities
            function bgp_peer_communities_strip_internal(string filter_name)
            bool stripped_community;
            bool stripped_community_private;
            bool stripped_lc;
            bool stripped_lc_private;
            {{
                stripped_community = false;
                stripped_community_private = false;
                stripped_lc = false;
                stripped_lc_private = false;
                # Remove stripped communities
                if (bgp_community ~ BGP_COMMUNITY_STRIP) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Removing stripped communities from ", {self.functions.route_info()};
                    bgp_community.delete(BGP_COMMUNITY_STRIP);
                    stripped_community = true;
                }}
                # Remove stripped large communities
                if (bgp_large_community ~ BGP_LC_STRIP) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Removing stripped large communities from ",
                        {self.functions.route_info()};
                    bgp_large_community.delete(BGP_LC_STRIP);
                    stripped_lc = true;
                }}
                # Remove stripped private communities
                if (bgp_community ~ BGP_COMMUNITY_STRIP_PRIVATE) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Removing stripped private communities from ",
                        {self.functions.route_info()};
                    bgp_community.delete(BGP_COMMUNITY_STRIP_PRIVATE);
                    stripped_community_private = true;
                }}
                # Remove stripped private large communities
                if (bgp_large_community ~ BGP_LC_STRIP_PRIVATE) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Removing stripped private large communities from ",
                        {self.functions.route_info()};
                    bgp_large_community.delete(BGP_LC_STRIP_PRIVATE);
                    stripped_lc_private = true;
                }}
                #
                # Output debug info and do the actual stripping
                #
                if (stripped_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY);
                }}
                if (stripped_lc) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC);
                }}
                if (stripped_community_private) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_COMMUNITY_PRIVATE to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_COMMUNITY_PRIVATE);
                }}
                if (stripped_lc_private) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_communities_strip_internal] Adding BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE to ",
                        {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_INFORMATION_STRIPPED_LC_PRIVATE);
                }}
            }}"""

    @BirdFunction("bgp_import_filter_asn_bogons")
    def import_filter_asn_bogons(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_asn_bogons function."""

        return f"""\
            # Import filter bogon ASNs
            function bgp_import_filter_asn_bogons(string filter_name) -> bool {{
                if (bgp_path !~ BOGON_ASNS) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_asn_bogons] Adding BGP_LC_FILTERED_BOGON_ASN to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_BOGON_ASN);
            }}"""

    @BirdFunction("bgp_import_filter_asn_invalid")
    def import_filter_asn_invalid(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_asn_invalid function."""

        return f"""\
            # Import filter peer ASN != route first ASN
            function bgp_import_filter_asn_invalid(string filter_name; int peer_asn) -> bool {{
                if (bgp_path.first = peer_asn) then return false;
                if DEBUG then print filter_name,
                        " [bgp_import_filter_asn_invalid] Adding BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS to ",
                        {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_FIRST_AS_NOT_PEER_AS);
            }}"""

    @BirdFunction("bgp_import_filter_aspath_allow")
    def import_filter_aspath_allow(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_aspath_allow function."""

        return f"""\
            function bgp_import_filter_aspath_allow(string filter_name; int set asn_list) -> bool {{
                if (bgp_path = filter(bgp_path, asn_list)) then return false;
                if (bgp_large_community ~ [BGP_LC_FILTERED_ORIGIN_AS, BGP_LC_FILTERED_PEER_AS]) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_aspath_allow] Adding BGP_LC_FILTERED_ASPATH_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_ASPATH_NOT_ALLOWED);
            }}"""

    @BirdFunction("bgp_import_filter_aspath_deny")
    def import_filter_aspath_deny(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_aspath_deny function."""

        return f"""\
            function bgp_import_filter_aspath_deny(string filter_name; int set asn_list) -> bool {{
                if (bgp_path !~ asn_list) then return false;
                if (bgp_large_community ~ [BGP_LC_FILTERED_ORIGIN_AS, BGP_LC_FILTERED_PEER_AS]) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_aspath_deny] Adding BGP_LC_FILTERED_ASPATH_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_ASPATH_NOT_ALLOWED);
            }}"""

    @BirdFunction("bgp_import_filter_deny_aspath")
    def import_filter_deny_aspath(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_deny_aspath function."""

        return f"""\
            function bgp_import_filter_deny_aspath(string filter_name; int set asn_list) -> bool {{
                if (bgp_path !~ asn_list) then return false;
                if (bgp_large_community ~ [BGP_LC_FILTERED_ORIGIN_AS, BGP_LC_FILTERED_PEER_AS]) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_deny_aspath] Adding BGP_LC_FILTERED_DENY_ASPATH to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_DENY_ASPATH);
            }}"""

    @BirdFunction("bgp_import_filter_asn_private")
    def import_filter_asn_private(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_asn_private function."""

        return f"""\
            # Import filter private ASN's
            function bgp_import_filter_asn_private(string filter_name; int set allowed_asns) -> bool {{
                if (bgp_path = filter(bgp_path, allowed_asns)) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_asn_private] Adding BGP_LC_FILTERED_ASPATH_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_ASPATH_NOT_ALLOWED);
            }}"""

    @BirdFunction("bgp_import_filter_asn_transit")
    def import_filter_asn_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_asn_transit function."""

        return f"""\
            # Import filter transit free ASNs
            function bgp_import_filter_asn_transit(string filter_name) -> bool {{
                if (bgp_path !~ BGP_ASNS_TRANSIT) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_asn_transit] Adding BGP_LC_FILTERED_TRANSIT_FREE_ASN to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_TRANSIT_FREE_ASN);
            }}"""

    @BirdFunction("bgp_import_filter_asns_allow")
    def import_filter_asns_allow(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_asns_allow function."""

        return f"""\
            # Import filter peer ASNs (ALLOW list)
            function bgp_import_filter_asns_allow(string filter_name; int set asns) -> bool {{
                if (bgp_path.first ~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_asns_allow] Adding BGP_LC_FILTERED_PEER_AS to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_PEER_AS);
            }}"""

    @BirdFunction("bgp_import_filter_asns_deny")
    def import_filter_asns_deny(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_asns_deny function."""

        return f"""\
            # Import filter peer ASNs (DENY list)
            function bgp_import_filter_asns_deny(string filter_name; int set asns) -> bool {{
                if (bgp_path.first !~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_asns_deny] Adding BGP_LC_FILTERED_PEER_AS to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_PEER_AS);
            }}"""

    @BirdFunction("bgp_import_filter_aspath_length")
    def import_filter_aspath_length(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_aspath_length function."""

        return f"""\
            # Import filter AS-PATH length
            function bgp_import_filter_aspath_length(string filter_name; int aspath_maxlen; int aspath_minlen) {{
                if (bgp_path.len > aspath_maxlen) then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_filter_aspath_length] AS-PATH length >", aspath_maxlen,
                        ", adding BGP_LC_FILTERED_ASPATH_TOO_LONG to ", {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_FILTERED_ASPATH_TOO_LONG);
                }}
                if (bgp_path.len < aspath_minlen) then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_filter_aspath_length] AS-PATH length <", aspath_minlen,
                        ", adding BGP_LC_FILTERED_ASPATH_TOO_SHORT to ", {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_FILTERED_ASPATH_TOO_SHORT);
                }}
            }}"""

    @BirdFunction("bgp_import_filter_blackhole")
    def import_filter_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_blackhole function."""

        return f"""\
            # Import filter blackhole routes
            function bgp_import_filter_blackhole(string filter_name) -> bool {{
                if !{self.is_blackhole()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_blackhole] Adding BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED);
            }}"""

    @BirdFunction("bgp_import_filter_blackhole_size")
    def import_filter_blackhole_size(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_blackhole_size function."""

        return f"""\
            # Import filter blackhole size
            function bgp_import_filter_blackhole_size(
                string filter_name;
                int ipv4_maxlen; int ipv4_minlen;
                int ipv6_maxlen; int ipv6_minlen
            ) -> bool
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
                # If this is not a blackhole then just return
                if !{self.is_blackhole()} then return false;
                # Check prefix is not longer than what we allow
                if {self.functions.prefix_is_longer(BirdVariable("prefix_maxlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_filter_prefix_size] Blackhole length >", prefix_maxlen,
                        ", adding BGP_FILTERED_BLACKHOLE_LEN_TOO_LONG to ", {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_LEN_TOO_LONG);
                }}
                # Check prefix is not shorter than what we allow
                if {self.functions.prefix_is_shorter(BirdVariable("prefix_minlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_filter_prefix_size] Blackhole length <", prefix_minlen,
                        ", adding BGP_FILTERED_BLACKHOLE_LEN_TOO_SHORT to ", {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_LEN_TOO_SHORT);
                }}
            }}"""

    @BirdFunction("bgp_import_filter_bogons")
    def import_filter_bogons(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_bogons function."""

        return f"""\
            # Import filter bogons
            function bgp_import_filter_bogons(string filter_name) -> bool {{
                if !{self.functions.is_bogon()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_bogons] Adding BGP_FILTERED_BOGON to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_BOGON);
            }}"""

    @BirdFunction("bgp_import_filter_community_lengths")
    def import_filter_community_lengths(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_community_lengths function."""

        return f"""\
            # Import filter too many communities
            function bgp_import_filter_community_lengths(
                string filter_name;
                int community_maxlen;
                int ext_maxlen;
                int large_maxlen
            ) {{
                if (bgp_community.len > community_maxlen) then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_filter_community_lengths] Community list length >", community_maxlen,
                        ", adding BGP_LC_FILTERED_TOO_MANY_COMMUNITIES to ", {self.functions.route_info()},
                        " counted ", bgp_community.len;
                    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_COMMUNITIES);
                }}
                if (bgp_ext_community.len > ext_maxlen) then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_filter_community_lengths] Extended community list length >", ext_maxlen,
                        ", adding BGP_LC_FILTERED_TOO_MANY_EXTENDED_COMMUNITIES to ", {self.functions.route_info()},
                        " counted ", bgp_ext_community.len;
                    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_EXTENDED_COMMUNITIES);
                }}
                if (bgp_large_community.len > large_maxlen) then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_filter_community_lengths] Large community list length >", large_maxlen,
                        ", adding BGP_LC_FILTERED_TOO_MANY_LARGE_COMMUNITIES to ", {self.functions.route_info()},
                        " counted ", bgp_large_community.len;
                    bgp_large_community.add(BGP_LC_FILTERED_TOO_MANY_LARGE_COMMUNITIES);
                }}
            }}"""

    @BirdFunction("bgp_import_filter_customer_blackhole")
    def import_filter_customer_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_customer_blackhole function."""

        return f"""\
            # Import filter customer blackhole routes
            function bgp_import_filter_customer_blackhole(string filter_name) -> bool {{
                if (!{self.is_blackhole()} || !{self.is_bgp_customer()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_customer_blackhole] Adding BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED);
                accept;
            }}"""

    @BirdFunction("bgp_import_filter_default")
    def import_filter_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_default function."""

        return f"""\
            # Import filter default routes
            function bgp_import_filter_default(string filter_name) -> bool {{
                if !{self.functions.is_default()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_default] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);
                accept;
            }}"""

    @BirdFunction("bgp_import_filter_invalid_blackhole")
    def import_filter_invalid_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_invalid_blackhole function."""

        return f"""\
            # Import filter invalid blackhole routes
            function bgp_import_filter_invalid_blackhole(string filter_name) -> bool {{
                if (!{self.is_blackhole()} || {self.is_bgp_customer()} || {self.is_bgp_own()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_invalid_blackhole] Adding BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED);
                accept;
            }}"""

    @BirdFunction("bgp_import_filter_invalid_default")
    def import_filter_invalid_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_invalid_default function."""

        return f"""\
            # Import filter invalid default routes
            function bgp_import_filter_invalid_default(string filter_name) -> bool {{
                if (!{self.functions.is_default()} || {self.is_bgp_own()} || {self.is_bgp_transit()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_invalid_default] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);
                accept;
            }}"""

    @BirdFunction("bgp_import_filter_lc_no_relation")
    def import_filter_lc_no_relation(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_lc_no_relation function."""

        return f"""\
            # Import filter prefixes without a large community relation set
            function bgp_import_filter_lc_no_relation(string filter_name) -> bool {{
                if (bgp_large_community ~ BGP_LC_RELATION) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_lc_no_relation] Adding BGP_LC_FILTERED_NO_RELATION_LC to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_NO_RELATION_LC);
            }}"""

    @BirdFunction("bgp_import_filter_nexthop_not_peerip")
    def import_filter_nexthop_not_peerip(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_nexthop_not_peerip function."""

        return f"""\
            # Import filter peer != next_hop
            function bgp_import_filter_nexthop_not_peerip(string filter_name) -> bool {{
                if (from = bgp_next_hop) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_nexthop_not_peerip] Adding BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_NEXT_HOP_NOT_PEER_IP);
            }}"""

    @BirdFunction("bgp_import_filter_origin_asns_allow")
    def import_filter_origin_asns_allow(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_origin_asns_allow function."""

        return f"""\
            # Import filter origin ASNs (ALLOW list)
            function bgp_import_filter_origin_asns_allow(string filter_name; int set asns) -> bool {{
                if (bgp_path.last_nonaggregated ~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_origin_asns_allow] Adding BGP_LC_FILTERED_ORIGIN_AS to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS);
            }}"""

    @BirdFunction("bgp_export_filter_origin_asns")
    def export_filter_origin_asns(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_export_filter_origin_asns function."""

        return f"""\
            # Export filter origin ASNs
            function bgp_export_filter_origin_asns(string filter_name; int set asns) -> bool {{
                if (bgp_path.last_nonaggregated !~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_export_filter_origin_asns] Dropping origin ASN filtered route ", {self.functions.route_info()};
                return true;
            }}"""

    @BirdFunction("bgp_import_filter_origin_asns_deny")
    def import_filter_origin_asns_deny(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_origin_asns_deny function."""

        return f"""\
            # Import filter origin ASNs (DENY list)
            function bgp_import_filter_origin_asns_deny(string filter_name; int set asns) -> bool {{
                if (bgp_path.last_nonaggregated !~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_origin_asns_deny] Adding BGP_LC_FILTERED_ORIGIN_AS to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_ORIGIN_AS);
            }}"""

    @BirdFunction("bgp_import_filter_deny_origin_asns")
    def import_filter_deny_origin_asns(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_deny_origin_asns function."""

        return f"""\
            # Import filter origin ASNs (import_filter_deny)
            function bgp_import_filter_deny_origin_asns(string filter_name; int set asns) -> bool {{
                if (bgp_path.last_nonaggregated !~ asns) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_deny_origin_asns] Adding BGP_LC_FILTERED_DENY_ORIGIN_AS to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_DENY_ORIGIN_AS);
            }}"""

    @BirdFunction("bgp_import_filter_own_blackhole")
    def import_filter_own_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_own_blackhole function."""

        return f"""\
            # Import filter own blackhole routes
            function bgp_import_filter_own_blackhole(string filter_name) -> bool {{
                if (!{self.is_blackhole()} || !{self.is_bgp_own()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_own_blackhole] Adding BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED);
                accept;
            }}"""

    @BirdFunction("bgp_import_filter_own_default")
    def import_filter_own_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_own_default function."""

        return f"""\
            # Import filter own default routes
            function bgp_import_filter_own_default(string filter_name) -> bool {{
                if (!{self.functions.is_default()} || !{self.is_bgp_own()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_own_default] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);
                accept;
            }}"""

    @BirdFunction("bgp_import_filter_prefix_size")
    def import_filter_prefix_size(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_prefix_size function."""

        return f"""\
            # Import filter prefix size
            function bgp_import_filter_prefix_size(
                string filter_name;
                int ipv4_maxlen; int ipv4_minlen;
                int ipv6_maxlen; int ipv6_minlen
            ) -> bool
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
                if {self.is_blackhole()} then return false;
                # Check prefix length is within the range we allow
                if {self.functions.prefix_is_longer(BirdVariable("prefix_maxlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_filter_prefix_size] Prefix length >", prefix_maxlen,
                        ", adding BGP_FILTERED_PREFIX_LEN_TOO_LONG to ", {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_LONG);
                }}
                # Check prefix length is within the range we allow
                if {self.functions.prefix_is_shorter(BirdVariable("prefix_minlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_import_filter_prefix_size] Prefix length <", prefix_minlen,
                        ", adding BGP_FILTERED_PREFIX_LEN_TOO_SHORT to ", {self.functions.route_info()};
                    bgp_large_community.add(BGP_LC_FILTERED_PREFIX_LEN_TOO_SHORT);
                }}
            }}"""

    @BirdFunction("bgp_import_filter_prefixes_allow")
    def import_filter_prefixes_allow(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_prefixes_allow function."""

        return f"""\
            # Import filter prefixes (ALLOW)
            function bgp_import_filter_prefixes_allow(
                string filter_name;
                prefix set prefix_list4; prefix set prefix_list6
            ) -> bool {{
                if {self.is_blackhole()} then return false;
                if (net.type = NET_IP4 && net ~ prefix_list4) then return false;
                if (net.type = NET_IP6 && net ~ prefix_list6) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_prefixes_allow] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);
            }}"""

    @BirdFunction("bgp_import_filter_prefixes_deny")
    def import_filter_prefixes_deny(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_prefixes_deny function."""

        return f"""\
            # Import filter prefixes (DENY)
            function bgp_import_filter_prefixes_deny(
                string filter_name;
                prefix set prefix_list4; prefix set prefix_list6
            ) -> bool {{
                if {self.is_blackhole()} then return false;
                if (net.type = NET_IP4 && net !~ prefix_list4) then return false;
                if (net.type = NET_IP6 && net !~ prefix_list6) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_prefixes_deny] Adding BGP_LC_FILTERED_PREFIX_FILTERED to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);
            }}"""

    @BirdFunction("bgp_import_filter_deny_prefixes")
    def import_filter_deny_prefixes(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_deny_prefixes function."""

        return f"""\
            # Import filter prefixes (DENY)
            function bgp_import_filter_deny_prefixes(
                string filter_name;
                prefix set prefix_list4; prefix set prefix_list6
            ) -> bool {{
                if {self.is_blackhole()} then return false;
                if (net.type = NET_IP4 && net !~ prefix_list4) then return false;
                if (net.type = NET_IP6 && net !~ prefix_list6) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_deny_prefixes] Adding BGP_LC_FILTERED_DENY_PREFIX to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_DENY_PREFIX);
            }}"""

    @BirdFunction("bgp_export_filter_prefixes")
    def export_filter_prefixes(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_export_filter_prefixes function."""

        return f"""\
            # Export filter prefixes
            function bgp_export_filter_prefixes(
                string filter_name;
                prefix set prefix_list4; prefix set prefix_list6
            ) -> bool {{
                if (net.type = NET_IP4 && net !~ prefix_list4) then return false;
                if (net.type = NET_IP6 && net !~ prefix_list6) then return false;
                if DEBUG then print filter_name,
                    " [bgp_export_filter_prefixes] Dropping filtered route ", {self.functions.route_info()};
                return true;
            }}"""

    @BirdFunction("bgp_import_filter_prefixes_blackhole_allow")
    def import_filter_prefixes_blackhole_allow(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_prefixes_blackhole_allow function."""

        return f"""\
            # Import filter prefixes blackholes (ALLOW)
            function bgp_import_filter_prefixes_blackhole_allow(
                string filter_name;
                prefix set prefix_list4; prefix set prefix_list6
            ) -> bool {{
                if !{self.is_blackhole()} then return false;
                if (net.type = NET_IP4 && net ~ prefix_list4) then return false;
                if (net.type = NET_IP6 && net ~ prefix_list6) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_prefixes_blackhole_allow] Adding BGP_LC_FILTERED_PREFIX_FILTERED, ",
                    "BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);
                bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED);
            }}"""

    @BirdFunction("bgp_import_filter_prefixes_blackhole_deny")
    def import_filter_prefixes_blackhole_deny(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_prefixes_blackhole_deny function."""

        return f"""\
            # Import filter blackholes (DENY)
            function bgp_import_filter_prefixes_blackhole_deny(
                string filter_name;
                prefix set prefix_list4; prefix set prefix_list6
            ) -> bool {{
                if !{self.is_blackhole()} then return false;
                if (net.type = NET_IP4 && net !~ prefix_list4) then return false;
                if (net.type = NET_IP6 && net !~ prefix_list6) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_prefixes_blackhole_deny] Adding BGP_LC_FILTERED_PREFIX_FILTERED, ",
                    "BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_PREFIX_FILTERED);
                bgp_large_community.add(BGP_LC_FILTERED_BLACKHOLE_NOT_ALLOWED);
            }}"""

    @BirdFunction("bgp_import_filter_routecollector_all")
    def import_filter_routecollector_all(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_routecollector_all function."""

        return f"""\
            # Import filter all incoming routecollector routes
            function bgp_import_filter_routecollector_all(string filter_name) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_import_routecollector] Adding BGP_FILTERED_ROUTECOLLECTOR to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_ROUTECOLLECTOR);
            }}"""

    @BirdFunction("bgp_import_filter_transit_default")
    def import_filter_transit_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_import_filter_transit_default function."""

        return f"""\
            # Import filter default route
            function bgp_import_filter_transit_default(string filter_name) -> bool {{
                if (!{self.functions.is_default()} || !{self.is_bgp_transit()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_import_filter_transit_default] Adding BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_DEFAULT_NOT_ALLOWED);
                accept;
            }}"""

    @BirdFunction("bgp_peer_graceful_shutdown")
    def peer_graceful_shutdown(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_graceful_shutdown function."""

        return f"""\
            # Enable graceful shutdown
            function bgp_peer_graceful_shutdown(string filter_name) {{
                if DEBUG then print filter_name,
                    " [peer_graceful_shutdown] Adding GRACEFUL_SHUTDOWN community to ", {self.functions.route_info()};
                bgp_community.add(BGP_COMMUNITY_GRACEFUL_SHUTDOWN);
            }}"""

    @BirdFunction("bgp_peer_import_customer")
    def peer_import_customer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_customer function."""

        return f"""\
            # Import customer routes
            function bgp_peer_import_customer(string filter_name; int peer_asn; int local_pref_cost) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_import_customer] Adding BGP_LC_RELATION_CUSTOMER to ", {self.functions.route_info()},
                    " with local pref ", BGP_PREF_CUSTOMER - local_pref_cost;
                # Tag route as a customer route
                bgp_large_community.add(BGP_LC_RELATION_CUSTOMER);
                # Set local preference
                bgp_local_pref = BGP_PREF_CUSTOMER - local_pref_cost;
            }}"""

    @BirdFunction("bgp_peer_import_graceful_shutdown")
    def peer_import_graceful_shutdown(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_graceful_shutdown function."""

        return f"""\
            # Import a graceful shutdown prefix
            function bgp_peer_import_graceful_shutdown(string filter_name) -> bool {{
                if (BGP_COMMUNITY_GRACEFUL_SHUTDOWN !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_import_graceful_shutdown] Setting LOCAL_PREF to 0 for ", {self.functions.route_info()};
                bgp_local_pref = 0;
            }}"""

    @BirdFunction("bgp_peer_import_location_iso3166")
    def peer_import_location_iso3166(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_location_iso3166 function."""

        return f"""\
            # Location-based prefix importing (ISO-3166 country codes)
            function bgp_peer_import_location_iso3166(string filter_name; int location) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_import_location_iso3166] Adding BGP_LC_FUNCTION_LOCATION_ISO3166 with ", location, " to ",
                    {self.functions.route_info()};
                bgp_large_community.add((BGP_ASN, BGP_LC_FUNCTION_LOCATION_ISO3166, location));
            }}"""

    @BirdFunction("bgp_peer_import_location_unm49")
    def peer_import_location_unm49(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_location_unm49 function."""

        return f"""\
            # Location-based prefix importing (UN.M49 country codes)
            function bgp_peer_import_location_unm49(string filter_name; int location) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_import_location_unm49] Adding BGP_LC_FUNCTION_LOCATION_UNM49 with ", location, " to ",
                    {self.functions.route_info()};
                bgp_large_community.add((BGP_ASN, BGP_LC_FUNCTION_LOCATION_UNM49, location));
            }}"""

    # Local pref manipulation
    @BirdFunction("bgp_peer_import_localpref")
    def peer_import_localpref(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_localpref function."""

        return f"""\
            # BGP import local_pref manipulation
            function bgp_peer_import_localpref(string filter_name) {{
                # If we are reducing local_pref by three
                if (BGP_LC_LOCALPREF_MINUS_THREE ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_import_localpref] Matched BGP_LC_LOCALPREF_MINUS_THREE for ", {self.functions.route_info()};
                    bgp_local_pref = bgp_local_pref - 3;
                # If we are reducing local_pref by two
                }} else if (BGP_LC_LOCALPREF_MINUS_TWO ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_import_localpref] Matched BGP_LC_LOCALPREF_MINUS_TWO for ", {self.functions.route_info()};
                    bgp_local_pref = bgp_local_pref - 2;
                # If we are reducing local_pref by one
                }} else if (BGP_LC_LOCALPREF_MINUS_ONE ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_import_localpref] Matched BGP_LC_LOCALPREF_MINUS_ONE for ", {self.functions.route_info()};
                    bgp_local_pref = bgp_local_pref - 1;
                }}
            }}"""

    @BirdFunction("bgp_peer_import_peer")
    def peer_import_peer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_peer function."""

        return f"""\
            # Import peer routes
            function bgp_peer_import_peer(string filter_name; int peer_asn; int local_pref_cost) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_import_peer] Adding BGP_LC_RELATION_PEER to ", {self.functions.route_info()}, " with local pref ",
                    BGP_PREF_PEER - local_pref_cost;
                # Tag route as a peer route
                bgp_large_community.add(BGP_LC_RELATION_PEER);
                # Set local preference
                bgp_local_pref = BGP_PREF_PEER - local_pref_cost;
            }}"""

    @BirdFunction("bgp_peer_import_routeserver")
    def peer_import_routeserver(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_routeserver function."""

        return f"""\
            # Import routeserver routes
            function bgp_peer_import_routeserver(string filter_name; int peer_asn; int local_pref_cost) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_import_routeserver] Adding BGP_LC_RELATION_ROUTESERVER to ", {self.functions.route_info()},
                    " with local pref ", BGP_PREF_ROUTESERVER - local_pref_cost;
                # Tag route as a routeserver route
                bgp_large_community.add(BGP_LC_RELATION_ROUTESERVER);
                # Set local preference
                bgp_local_pref = BGP_PREF_ROUTESERVER - local_pref_cost;
            }}"""

    @BirdFunction("bgp_peer_import_transit")
    def peer_import_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_import_transit function."""

        return f"""\
            # Import transit routes
            function bgp_peer_import_transit(string filter_name; int peer_asn; int local_pref_cost) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_import_transit] Adding BGP_LC_RELATION_TRANSIT to ", {self.functions.route_info()},
                    " with local pref ", BGP_PREF_TRANSIT - local_pref_cost;
                # Tag route as a transit route
                bgp_large_community.add(BGP_LC_RELATION_TRANSIT);
                # Set local preference
                bgp_local_pref = BGP_PREF_TRANSIT - local_pref_cost;
            }}"""

    #
    # Communities
    #

    @BirdFunction("bgp_peer_community_add_connected")
    def peer_community_add_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_connected function."""

        return f"""\
            function bgp_peer_community_add_connected(string filter_name; pair community) -> bool {{
                if !{self.is_connected()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_connected] Adding community ", community, " for type CONNECTED to ",
                    {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_kernel")
    def peer_community_add_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_kernel function."""

        return f"""\
            function bgp_peer_community_add_kernel(string filter_name; pair community) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_kernel] Adding community ", community, " for type KERNEL to ",
                    {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_kernel_blackhole")
    def peer_community_add_kernel_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_kernel_blackhole function."""

        return f"""\
            function bgp_peer_community_add_kernel_blackhole(string filter_name; pair community) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_kernel_blackhole] Adding community ", community,
                    " for type KERNEL BLACKHOLE to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_kernel_default")
    def peer_community_add_kernel_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_kernel_default function."""

        return f"""\
            function bgp_peer_community_add_kernel_default(string filter_name; pair community) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_kernel_default] Adding community ", community,
                    " for type KERNEL DEFAULT to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_originated")
    def peer_community_add_originated(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_originated function."""

        return f"""\
            # BGP originated route community adding
            function bgp_peer_community_add_originated(string filter_name; pair community) -> bool {{
                if (!{self.is_originated()} || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_originate] Adding community ", community,
                    " for type ORIGINATED to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_originated_blackhole")
    def peer_community_add_originated_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_originated_blackhole function."""

        return f"""\
            function bgp_peer_community_add_originated_blackhole(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_originated()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_originated_blackhole] Adding community ", community,
                    " for type ORIGINATED BLACKHOLE to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_originated_default")
    def peer_community_add_originated_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_originated_default function."""

        return f"""\
            function bgp_peer_community_add_originated_default(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_originated()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_originated_default] Adding community ", community,
                    " for type ORIGINATED DEFAULT to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_static")
    def peer_community_add_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_static function."""

        return f"""\
            function bgp_peer_community_add_static(string filter_name; pair community) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_static] Adding community ", community, " for type STATIC to ",
                    {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_static_blackhole")
    def peer_community_add_static_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_static_blackhole function."""

        return f"""\
            function bgp_peer_community_add_static_blackhole(string filter_name; pair community) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_static_blackhole] Adding community ", community,
                    " for type STATIC BLACKHOLE to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_static_default")
    def peer_community_add_static_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_static_default function."""

        return f"""\
            function bgp_peer_community_add_static_default(string filter_name; pair community) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_static_default] Adding community ", community,
                    " for type STATIC DEFAULT to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_own")
    def peer_community_add_bgp_own(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_own function."""

        return f"""\
            # BGP own route community adding
            function bgp_peer_community_add_bgp_own(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                )  then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_bgp_own] Adding community ", community, " for type BGP_OWN to ",
                    {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_own_blackhole")
    def peer_community_add_bgp_own_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_own_blackhole function."""

        return f"""\
            function bgp_peer_community_add_bgp_own_blackhole(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_bgp_own_blackhole] Adding community ", community,
                    " for type BGP_OWN BLACKHOLE to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_own_default")
    def peer_community_add_bgp_own_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_own_default function."""

        return f"""\
            function bgp_peer_community_add_bgp_own_default(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_bgp_own_default] Adding community ", community,
                    " for type BGP_OWN DEFAULT to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_customer")
    def peer_community_add_bgp_customer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_customer function."""

        return f"""\
            # BGP customer route community adding
            function bgp_peer_community_add_bgp_customer(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_bgp_customer()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_bgp_customer] Adding community ", community, " for type BGP_CUSTOMER to ",
                    {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_customer_blackhole")
    def peer_community_add_bgp_customer_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_customer_blackhole function."""

        return f"""\
            function bgp_peer_community_add_bgp_customer_blackhole(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_bgp_customer()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_bgp_customer_blackhole] Adding community ", community,
                    " for type BGP_CUSTOMER BLACKHOLE to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_peering")
    def peer_community_add_bgp_peering(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_peering function."""

        return f"""\
            # BGP peering route community adding
            function bgp_peer_community_add_bgp_peering(string filter_name; pair community) -> bool {{
                if (!{self.is_bgp_peer()} && !{self.is_bgp_routeserver()}) then return false;
                if DEBUG then print filter_name,
                        " [bgp_peer_community_add_bgp_peer] Adding community ", community, " for type BGP_PEER to ",
                        {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_transit")
    def peer_community_add_bgp_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_transit function."""

        return f"""\
            # BGP transit route community adding
            function bgp_peer_community_add_bgp_transit(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_bgp_transit()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_bgp_transit] Adding community ", community, " for type BGP_TRANSIT to ",
                    {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_bgp_transit_default")
    def peer_community_add_bgp_transit_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_bgp_transit_default function."""

        return f"""\
            function bgp_peer_community_add_bgp_transit_default(string filter_name; pair community) -> bool {{
                if (
                    !{self.is_bgp_transit()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_bgp_transit_default] Adding community ", community,
                    " for type BGP_TRANSIT DEFAULT to ", {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    @BirdFunction("bgp_peer_community_add_blackhole")
    def peer_community_add_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_community_add_blackhole function."""

        return f"""\
            # Add a community to a blackhole route (the check for a blackhole route needs to be done before calling this
            # function)
            function bgp_peer_community_add_blackhole(string filter_name; pair community) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_community_add_blackhole] Adding community ", community, " for type BLACKHOLE to ",
                    {self.functions.route_info()};
                bgp_community.add(community);
            }}"""

    #
    # Large Communities
    #

    @BirdFunction("bgp_peer_lc_add_connected")
    def peer_lc_add_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_connected function."""

        return f"""\
            function bgp_peer_lc_add_connected(string filter_name; lc large_community) -> bool {{
                if !{self.is_connected()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_connected] Adding large community ", large_community, " for type CONNECTED to ",
                    {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_kernel")
    def peer_lc_add_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_kernel function."""

        return f"""\
            function bgp_peer_lc_add_kernel(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_kernel] Adding large community ", large_community, " for type KERNEL to ",
                    {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_kernel_blackhole")
    def peer_lc_add_kernel_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_kernel_blackhole function."""

        return f"""\
            function bgp_peer_lc_add_kernel_blackhole(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_kernel_blackhole] Adding large community ", large_community,
                    " for type KERNEL BLACKHOLE to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_kernel_default")
    def peer_lc_add_kernel_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_kernel_default function."""

        return f"""\
            function bgp_peer_lc_add_kernel_default(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_kernel_default] Adding large community ", large_community,
                    " for type KERNEL DEFAULT to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_originated")
    def peer_lc_add_originated(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_originated function."""

        return f"""\
            # BGP originated route large community adding
            function bgp_peer_lc_add_originated(string filter_name; lc large_community) -> bool {{
                if (!{self.is_originated()} || {self.functions.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_originate] Adding large community ", large_community,
                    " for type ORIGINATED to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_originated_blackhole")
    def peer_lc_add_originated_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_originated_blackhole function."""

        return f"""\
            function bgp_peer_lc_add_originated_blackhole(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_originated()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_originated_blackhole] Adding large community ", large_community,
                    " for type ORIGINATED BLACKHOLE to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_originated_default")
    def peer_lc_add_originated_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_originated_default function."""

        return f"""\
            function bgp_peer_lc_add_originated_default(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_originated()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_originated_default] Adding large community ", large_community,
                    " for type ORIGINATED DEFAULT to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_static")
    def peer_lc_add_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_static function."""

        return f"""\
            function bgp_peer_lc_add_static(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_static] Adding large community ", large_community, " for type STATIC to ",
                    {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_static_blackhole")
    def peer_lc_add_static_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_static_blackhole function."""

        return f"""\
            function bgp_peer_lc_add_static_blackhole(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_static_blackhole] Adding large community ", large_community,
                    " for type STATIC BLACKHOLE to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_static_default")
    def peer_lc_add_static_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_static_default function."""

        return f"""\
            function bgp_peer_lc_add_static_default(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_static_default] Adding large community ", large_community,
                    " for type STATIC DEFAULT to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_own")
    def peer_lc_add_bgp_own(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_own function."""

        return f"""\
            # BGP own route large community adding
            function bgp_peer_lc_add_bgp_own(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                )  then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_bgp_own] Adding large community ", large_community, " for type BGP_OWN to ",
                    {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_own_blackhole")
    def peer_lc_add_bgp_own_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_own_blackhole function."""

        return f"""\
            function bgp_peer_lc_add_bgp_own_blackhole(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_bgp_own_blackhole] Adding large community ", large_community,
                    " for type BGP_OWN BLACKHOLE to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_own_default")
    def peer_lc_add_bgp_own_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_own_default function."""

        return f"""\
            function bgp_peer_lc_add_bgp_own_default(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_bgp_own_default] Adding large community ", large_community,
                    " for type BGP_OWN DEFAULT to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_customer")
    def peer_lc_add_bgp_customer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_customer function."""

        return f"""\
            # BGP customer route large community adding
            function bgp_peer_lc_add_bgp_customer(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_bgp_customer()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_bgp_customer] Adding large community ", large_community, " for type BGP_CUSTOMER to ",
                    {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_customer_blackhole")
    def peer_lc_add_bgp_customer_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_customer_blackhole function."""

        return f"""\
            function bgp_peer_lc_add_bgp_customer_blackhole(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_bgp_customer()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_bgp_customer_blackhole] Adding large community ", large_community,
                    " for type BGP_CUSTOMER BLACKHOLE to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_peering")
    def peer_lc_add_bgp_peering(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_peering function."""

        return f"""\
            # BGP peering route large community adding
            function bgp_peer_lc_add_bgp_peering(string filter_name; lc large_community) -> bool {{
                if (!{self.is_bgp_peer()} && !{self.is_bgp_routeserver()}) then return false;
                if DEBUG then print filter_name,
                        " [bgp_peer_lc_add_bgp_peer] Adding large community ", large_community, " for type BGP_PEER to ",
                        {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_transit")
    def peer_lc_add_bgp_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_transit function."""

        return f"""\
            # BGP transit route large community adding
            function bgp_peer_lc_add_bgp_transit(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_bgp_transit()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_bgp_transit] Adding large community ", large_community, " for type BGP_TRANSIT to ",
                    {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_bgp_transit_default")
    def peer_lc_add_bgp_transit_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_bgp_transit_default function."""

        return f"""\
            function bgp_peer_lc_add_bgp_transit_default(string filter_name; lc large_community) -> bool {{
                if (
                    !{self.is_bgp_transit()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_bgp_transit_default] Adding large community ", large_community,
                    " for type BGP_TRANSIT DEFAULT to ", {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_lc_add_blackhole")
    def peer_lc_add_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_lc_add_blackhole function."""

        return f"""\
            # Add a large community to a blackhole route (the check for a blackhole route needs to be done before calling this
            # function)
            function bgp_peer_lc_add_blackhole(string filter_name; lc large_community) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_lc_add_blackhole] Adding large community ", large_community, " for type BLACKHOLE to ",
                    {self.functions.route_info()};
                bgp_large_community.add(large_community);
            }}"""

    @BirdFunction("bgp_peer_peer_prepend")
    def peer_prepend(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_peer_prepend function."""

        return """\
            # BGP prepending
            function bgp_peer_peer_prepend(string filter_name; int peer_asn; int prepend_count) {
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

    @BirdFunction("bgp_peer_peer_prepend_default")
    def peer_prepend_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_peer_prepend_default function."""

        return f"""\
            function bgp_peer_prepend_default(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if !{self.functions.is_default()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_default] Prepending AS-PATH for type DEFAULT ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_connected")
    def peer_prepend_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_connected function."""

        return f"""\
            # BGP connected route prepending
            function bgp_peer_prepend_connected(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if !{self.is_connected()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_connected] Prepending AS-PATH for type CONNECTED ", prepend_count, "x to "
                    , {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_kernel")
    def peer_prepend_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_kernel function."""

        return f"""\
            function bgp_peer_prepend_kernel(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_kernel] Prepending AS-PATH for type KERNEL ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_kernel_blackhole")
    def peer_prepend_kernel_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_kernel_blackhole function."""

        return f"""\
            function bgp_peer_prepend_kernel_blackhole(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_kernel_blackhole] Prepending AS-PATH for type KERNEL BLACKHOLE ",
                    prepend_count, "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_kernel_default")
    def peer_prepend_kernel_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_kernel_default function."""

        return f"""\
            function bgp_peer_prepend_kernel_default(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.functions.is_kernel()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_kernel_default] Prepending AS-PATH for type KERNEL DEFAULT ",
                    prepend_count, "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_originated")
    def peer_prepend_originated(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_originated function."""

        return f"""\
            function bgp_peer_prepend_originated(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_originated()} ||
                    {self.functions.is_default()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_originated] Prepending AS-PATH for type ORIGINATED ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_originated_default")
    def peer_prepend_originated_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_originated_default function."""

        return f"""\
            function bgp_peer_prepend_originated_default(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_originated()} ||
                    !{self.functions.is_default()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_originated_default] Prepending AS-PATH for type ORIGINATED DEFAULT ", prepend_count,
                    "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_static")
    def peer_prepend_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_static function."""

        return f"""\
            function bgp_peer_prepend_static(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_static] Prepending AS-PATH for type STATIC ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_static_blackhole")
    def peer_prepend_static_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_static_blackhole function."""

        return f"""\
            function bgp_peer_prepend_static_blackhole(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_static_blackhole] Prepending AS-PATH for type STATIC BLACKHOLE ",
                    prepend_count, "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_static_default")
    def peer_prepend_static_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_static_default function."""

        return f"""\
            function bgp_peer_prepend_static_default(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.functions.is_static()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_static_default] Prepending AS-PATH for type STATIC DEFAULT ",
                    prepend_count, "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_own")
    def peer_prepend_bgp_own(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_own function."""

        return f"""\
            function bgp_peer_prepend_bgp_own(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_own] Prepending AS-PATH for type BGP_OWN ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_own_blackhole")
    def peer_prepend_bgp_own_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_own_blackhole function."""

        return f"""\
            function bgp_peer_prepend_bgp_own_blackhole(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_own_blackhole] Prepending AS-PATH for type BGP_OWN BLACKHOLE ", prepend_count,
                    "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_own_default")
    def peer_prepend_bgp_own_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_own_default function."""

        return f"""\
            function bgp_peer_prepend_bgp_own_default(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_bgp_own()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_own_default] Prepending AS-PATH for type BGP_OWN DEFAULT ", prepend_count,
                    "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_customer")
    def peer_prepend_bgp_customer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_customer function."""

        return f"""\
            function bgp_peer_prepend_bgp_customer(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_bgp_customer()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_customer] Prepending AS-PATH for type BGP_CUSTOMER ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_customer_blackhole")
    def peer_prepend_bgp_customer_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_customer_blackhole function."""

        return f"""\
            function bgp_peer_prepend_bgp_customer_blackhole(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_bgp_customer()} ||
                    {self.functions.is_default()} ||
                    !{self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_customer_blackhole] Prepending AS-PATH for type BGP_CUSTOMER BLACKHOLE ", prepend_count,
                    "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_peering")
    def peer_prepend_bgp_peering(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_peering function."""

        return f"""\
            function bgp_peer_prepend_bgp_peering(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (!{self.is_bgp_peer()} && !{self.is_bgp_routeserver()}) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_peer] Prepending AS-PATH for type BGP_PEER ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_transit")
    def peer_prepend_bgp_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_transit function."""

        return f"""\
            function bgp_peer_prepend_bgp_transit(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_bgp_transit()} ||
                    {self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_transit] Prepending AS-PATH for type BGP_TRANSIT ", prepend_count, "x to ",
                    {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_bgp_transit_default")
    def peer_prepend_bgp_transit_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_bgp_transit_default function."""

        return f"""\
            function bgp_peer_prepend_bgp_transit_default(string filter_name; int peer_asn; int prepend_count) -> bool {{
                if (
                    !{self.is_bgp_transit()} ||
                    !{self.functions.is_default()} ||
                    {self.is_blackhole()}
                ) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_prepend_bgp_transit_default] Prepending AS-PATH for type BGP_TRANSIT DEFAULT ", prepend_count,
                    "x to ", {self.functions.route_info()};
                {self.peer_prepend(BirdVariable("peer_asn"), BirdVariable("prepend_count"))};
            }}"""

    @BirdFunction("bgp_peer_prepend_lc")
    def peer_prepend_lc(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_lc function."""

        return f"""\
            # BGP large community based prepending
            function bgp_peer_prepend_lc(string filter_name; int peer_asn)
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
                        " [bgp_peer_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_THREE for ", {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 3)};
                # If we are prepending two times
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_TWO, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_TWO for ", {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 2)};
                # If we are prepending one time
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_ONE, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_ONE for ", {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 1)};
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_ONE_2, peer_asn) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_prepend_lc] Matched BGP_LC_FUNCTION_PREPEND_ONE_2 for ", {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 1)};
                }}
            }}"""

    @BirdFunction("bgp_peer_prepend_lc_location")
    def peer_prepend_lc_location(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_prepend_location function."""

        return f"""\
            # BGP large community location based prepending
            function bgp_peer_prepend_lc_location(string filter_name; int location)
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
                        " [bgp_peer_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_THREE for ",
                        {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 3)};
                # If we are prepending two times
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_LOCATION_TWO, location) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_TWO for ",
                        {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 2)};
                # If we are prepending one time
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_LOCATION_ONE, location) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_ONE for ",
                        {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 1)};
                }} else if ((BGP_ASN, BGP_LC_FUNCTION_PREPEND_LOCATION_ONE_2, location) ~ bgp_large_community) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_prepend_lc_location] Matched BGP_LC_FUNCTION_PREPEND_LOCATION_ONE_2 for ",
                        {self.functions.route_info()};
                    {self.peer_prepend(BirdVariable("prepend_asn"), 1)};
                }}
            }}"""

    @BirdFunction("bgp_peer_quarantine")
    def peer_quarantine(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_quarantine function."""

        return f"""\
            # Quarantine peer
            function bgp_peer_quarantine(string filter_name) {{
                if DEBUG then print filter_name,
                    " [bgp_peer_quarantine] Adding BGP_LC_FILTERED_QUARANTINED to ", {self.functions.route_info()};
                bgp_large_community.add(BGP_LC_FILTERED_QUARANTINED);
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_customer")
    def peer_redistribute_bgp_customer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_customer function."""

        return f"""\
            # Check for redistribution of customer routes for BGP
            function bgp_peer_redistribute_bgp_customer(string filter_name; bool redistribute) -> bool {{
                # Check for redistribute customer routes
                if (!{self.is_bgp_customer()} || {self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_customer] Accepting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_CUSTOMER route match (redistribute customer)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_bgp_customer] Rejecting ", {self.functions.route_info()},
                    " due to BGP_LC_RELATION_CUSTOMER route match (no redistribute customer)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_customer_blackhole")
    def peer_redistribute_bgp_customer_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_customer_blackhole function."""

        return f"""\
            # Check for redistribution of customer blackhole routes for BGP
            function bgp_peer_redistribute_bgp_customer_blackhole(string filter_name; bool redistribute) -> bool {{
                # Check for redistribute customer blackhole routes
                if (!{self.is_bgp_customer()} || !{self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_customer_blackhole] Accepting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_CUSTOMER and blackhole route match (redistribute customer blackhole)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_bgp_customer_blackhole] Rejecting ", {self.functions.route_info()},
                    " due to BGP_LC_RELATION_CUSTOMER and blackhole route match (no redistribute customer blackhole)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_own")
    def peer_redistribute_bgp_own(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_own function."""

        return f"""\
            # Check for redistribution of our own routes for BGP
            function bgp_peer_redistribute_bgp_own(string filter_name; bool redistribute) -> bool {{
                # Check for redistribute own routes
                if (!{self.is_bgp_own()} || {self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_own] Accepting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_OWN route match (redistribute own)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_bgp_own] Rejecting ", {self.functions.route_info()},
                    " due to BGP_LC_RELATION_OWN route match (no redistribute own)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_own_blackhole")
    def peer_redistribute_bgp_own_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_own_blackhole function."""

        return f"""\
            # Check for redistribution of our own blackhoole routes for BGP
            function bgp_peer_redistribute_bgp_own_blackhole(string filter_name; bool redistribute) -> bool {{
                # Check for redistribute own blackhole routes
                if (!{self.is_bgp_own()} || !{self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_own_blackhole] Accepting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_OWN and blackhole route match (redistribute own blackhole)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_bgp_own_blackhole] Rejecting ", {self.functions.route_info()},
                    " due to BGP_LC_RELATION_OWN and blackhole route match (no redistribute own blackhole)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_own_default")
    def peer_redistribute_bgp_own_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_own_default function."""

        return f"""\
            # Check for redistribution of our own default routes for BGP
            function bgp_peer_redistribute_bgp_own_default(string filter_name; bool redistribute) -> bool {{
                # Check for redistribute own default routes
                if (!{self.is_bgp_own()} || {self.is_blackhole()} || !{self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_own_default] Accepting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_OWN and default route match (redistribute own default)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_bgp_own_default] Rejecting ", {self.functions.route_info()},
                    " due to BGP_LC_RELATION_OWN and default route match (no redistribute own default)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_peering")
    def peer_redistribute_bgp_peering(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_peering function."""

        return f"""\
            # Check for redistribution of peering routes for BGP
            function bgp_peer_redistribute_bgp_peering(string filter_name; bool redistribute) -> bool {{
                if (!{self.is_bgp_peering()} || {self.is_blackhole()} || {self.functions.is_default()}) then return false;
                # Check for redistribute peering routes
                if {self.is_bgp_peer()} then {{
                    if (redistribute) then {{
                        if DEBUG then print filter_name,
                            " [bgp_peer_redistribute_bgp_peering] Accepting ", {self.functions.route_info()},
                            " due to BGP_LC_RELATION_PEER route match (redistribute peering)";
                        return true;
                    }}
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_peering] Rejecting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_PEER route match (no redistribute peering)";
                    reject;
                }}
                # Check for redistribute routeserver routes
                if {self.is_bgp_routeserver()} then {{
                    if (redistribute) then {{
                        if DEBUG then print filter_name,
                            " [bgp_peer_redistribute_bgp_peering] Accepting ", {self.functions.route_info()},
                            " due to BGP_LC_RELATION_ROUTESERVER route match (redistribute peering)";
                        return true;
                    }}
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_peering] Rejecting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_ROUTESERVER route match (no redistribute peering)";
                    reject;
                }}
                return false;
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_transit")
    def peer_redistribute_bgp_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_transit function."""

        return f"""\
            # Check for redistribution of transit routes for BGP
            function bgp_peer_redistribute_bgp_transit(string filter_name; bool redistribute) -> bool {{
                # Check for redistribute transit routes
                if (!{self.is_bgp_transit()} || {self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_transit] Accepting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_TRANSIT route match (redistribute transit)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_bgp_transit] Rejecting ", {self.functions.route_info()},
                    " due to BGP_LC_RELATION_TRANSIT route match (no redistribute transit)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_bgp_transit_default")
    def peer_redistribute_bgp_transit_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_bgp_transit_default function."""

        return f"""\
            # Check for redistribution of transit routes for BGP
            function bgp_peer_redistribute_bgp_transit_default(string filter_name; bool redistribute) -> bool {{
                # Check for redistribute transit routes
                if (!{self.is_bgp_transit()} || {self.is_blackhole()} || !{self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_bgp_transit_default] Accepting ", {self.functions.route_info()},
                        " due to BGP_LC_RELATION_TRANSIT and default route match (redistribute transit default)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_bgp_transit_default] Rejecting ", {self.functions.route_info()},
                    " due to BGP_LC_RELATION_TRANSIT and default route match (no redistribute transit default)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_connected")
    def peer_redistribute_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_connected function."""

        return f"""\
            # Check for redistribution of connected routes for BGP
            function bgp_peer_redistribute_connected(string filter_name; bool redistribute) -> bool {{
                # Check for connected routes
                if !{self.is_connected()} then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_connected] Accepting ", {self.functions.route_info()},
                        " due to direct route match (redistribute connected)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_connected] Rejecting ", {self.functions.route_info()},
                    " due to direct route match (no redistribute connected)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_kernel")
    def peer_redistribute_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_kernel function."""

        return f"""\
            # Check for redistribution of kernel routes for BGP
            function bgp_peer_redistribute_kernel(string filter_name; bool redistribute) -> bool {{
                if (!{self.functions.is_kernel()} || {self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_kernel] Accepting ", {self.functions.route_info()},
                        " due to kernel route match (redistribute kernel)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_kernel] Rejecting ", {self.functions.route_info()},
                    " due to kernel route match (no redistribute kernel)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_kernel_blackhole")
    def peer_redistribute_kernel_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_kernel_blackhole function."""

        return f"""\
            # Check for redistribution of kernel blackhole routes for BGP
            function bgp_peer_redistribute_kernel_blackhole(string filter_name; bool redistribute) -> bool {{
                if (!{self.functions.is_kernel()} || !{self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_kernel_blackhole] Accepting ", {self.functions.route_info()},
                        " due to kernel blackhole route match (redistribute kernel)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_kernel_blackhole] Rejecting ", {self.functions.route_info()},
                    " due to kernel blackhole route match (no redistribute kernel)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_kernel_default")
    def peer_redistribute_kernel_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_kernel_default function."""

        return f"""\
            # Check for redistribution of kernel default routes for BGP
            function bgp_peer_redistribute_kernel_default(string filter_name; bool redistribute) -> bool {{
                if (!{self.functions.is_kernel()} || {self.is_blackhole()} || !{self.functions.is_default()}) then
                    return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_kernel_default] Accepting ", {self.functions.route_info()},
                        " due to kernel default route match (redistribute kernel default) and accepted";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_kernel_default] Rejecting ", {self.functions.route_info()},
                    " due to kernel default route match";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_originated")
    def peer_redistribute_originated(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_originated function."""

        return f"""\
            # Check for redistribution of originated routes for BGP
            function bgp_peer_redistribute_originated(string filter_name; bool redistribute) -> bool {{
                if (!{self.is_originated()} || {self.is_blackhole()} || {self.functions.is_default()}) then
                    return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_originated] Accepting ", {self.functions.route_info()},
                        " due to originated route match (redistribute originated)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_originated] Rejecting ", {self.functions.route_info()},
                    " due to originated route match (no redistribute originated)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_originated_default")
    def peer_redistribute_originated_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_originated_default function."""

        return f"""\
            # Check for redistribution of originated default routes for BGP
            function bgp_peer_redistribute_originated_default(string filter_name; bool redistribute) -> bool {{
                if (!{self.is_originated()} || {self.is_blackhole()} || !{self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_originated_default] Accepting ", {self.functions.route_info()},
                        " due to originated default route match (redistribute originated default) and accepted";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_originated_default] Rejecting ", {self.functions.route_info()},
                    " due to originated default route match";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_static")
    def peer_redistribute_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_static function."""

        return f"""\
            # Check for redistribution of static routes for BGP
            function bgp_peer_redistribute_static(string filter_name; bool redistribute) -> bool {{
                if (!{self.functions.is_static()} || {self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_static] Accepting ", {self.functions.route_info()},
                        " due to static route match (redistribute static)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_static] Rejecting ", {self.functions.route_info()},
                    " due to static route match (no redistribute static)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_static_blackhole")
    def peer_redistribute_static_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_static_blackhole function."""

        return f"""\
            # Check for redistribution of static blackhole routes for BGP
            function bgp_peer_redistribute_static_blackhole(string filter_name; bool redistribute) -> bool {{
                if (!{self.functions.is_static()} || !{self.is_blackhole()} || {self.functions.is_default()}) then return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_static_blackhole] Accepting ", {self.functions.route_info()},
                        " due to static blackhole route match (redistribute static)";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_static_blackhole] Rejecting ", {self.functions.route_info()},
                    " due to static blackhole route match (no redistribute static)";
                reject;
            }}"""

    @BirdFunction("bgp_peer_redistribute_static_default")
    def peer_redistribute_static_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_redistribute_static_default function."""

        return f"""\
            # Check for redistribution of static default routes for BGP
            function bgp_peer_redistribute_static_default(string filter_name; bool redistribute) -> bool {{
                if (!{self.functions.is_static()} || {self.is_blackhole()} || !{self.functions.is_default()}) then
                    return false;
                if (redistribute) then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_redistribute_static_default] Accepting ", {self.functions.route_info()},
                        " due to static default route match (redistribute static default) and accepted";
                    return true;
                }}
                if DEBUG then print filter_name,
                    " [bgp_peer_redistribute_static_default] Rejecting ", {self.functions.route_info()},
                    " due to static default route match";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_blackholes")
    def peer_reject_blackholes(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_blackholes function."""

        return f"""\
            # Reject blackhole routes
            function bgp_peer_reject_blackholes(string filter_name) -> bool {{
                if !{self.is_blackhole()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_blackholes] Rejecting blackhole ", {self.functions.route_info()},
                    " due to match on BGP_COMMUNITY_BLACKHOLE";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_bogons")
    def peer_reject_bogons(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_bogons function."""

        return f"""\
            # Reject bogon routes
            function bgp_peer_reject_bogons(string filter_name) -> bool {{
                if !{self.functions.is_bogon()} then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_bogons] Rejecting bogon ", {self.functions.route_info()};
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_filtered")
    def peer_reject_filtered(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_filtered function."""

        return f"""\
            # Reject filtered routes to main BGP table
            function bgp_peer_reject_filtered(string filter_name) -> bool {{
                if (bgp_large_community !~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_filtered] Filtered ", {self.functions.route_info()}, " to main BGP table";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_noadvertise")
    def peer_reject_noadvertise(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_noadvertise function."""

        return f"""\
            # Reject NO_ADVERTISE routes
            function bgp_peer_reject_noadvertise(string filter_name) -> bool {{
                # Check for NO_ADVERTISE community
                if (BGP_COMMUNITY_NOADVERTISE !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_noadvertise] Rejecting ", {self.functions.route_info()},
                    " due to match on BGP_COMMUNITY_NOADVERTISE";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_noexport")
    def peer_reject_noexport(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_noexport function."""

        return f"""\
            # Reject NOEXPORT routes
            function bgp_peer_reject_noexport(string filter_name) -> bool {{
                if (BGP_COMMUNITY_NOEXPORT !~ bgp_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_noexport] Rejecting ", {self.functions.route_info()},
                    " due to match on BGP_COMMUNITY_NOEXPORT";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_noexport_asn")
    def peer_reject_noexport_asn(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_noexport_asn function."""

        return f"""\
            # Reject NOEXPORT ASN routes
            function bgp_peer_reject_noexport_asn(string filter_name; int peer_asn) -> bool {{
                # Check for NOEXPORT large community
                if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT, peer_asn) !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_noexport_asn] Rejecting ", {self.functions.route_info()},
                    " due to match on BGP_LC_FUNCTION_NOEXPORT for AS", peer_asn;
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_noexport_customer")
    def peer_reject_noexport_customer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_noexport_customer function."""

        return f"""\
            # Reject EXPORT_NOCUSTOMER routes
            function bgp_peer_reject_noexport_customer(string filter_name) -> bool {{
                # Check for large community to prevent export to customers
                if (BGP_LC_EXPORT_NOCUSTOMER !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_noexport_customer] Rejecting ", {self.functions.route_info()},
                    " due to match on BGP_LC_EXPORT_NOCUSTOMER";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_noexport_peer")
    def peer_reject_noexport_peer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_noexport_peer function."""

        return f"""\
            # Reject EXPORT_NOPEER routes
            function bgp_peer_reject_noexport_peer(string filter_name) -> bool {{
                # Check for large community to prevent export to peers
                if (BGP_LC_EXPORT_NOPEER !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_noexport_peer] Rejecting ", {self.functions.route_info()},
                    " due to match on BGP_LC_EXPORT_NOPEER";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_noexport_transit")
    def peer_reject_noexport_transit(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_noexport_transit function."""

        return f"""\
            # Reject EXPORT_NOTRANSIT routes
            function bgp_peer_reject_noexport_transit(string filter_name) -> bool {{
                # Check for large community to prevent export to transit
                if (BGP_LC_EXPORT_NOTRANSIT !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_noexport_transit] Rejecting ", {self.functions.route_info()},
                    " due to match on BGP_LC_EXPORT_NOTRANSIT";
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_noexport_location")
    def peer_reject_noexport_location(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_noexport_location function."""

        return f"""\
            # Reject NOEXPORT_LOCATION routes
            function bgp_peer_reject_noexport_location(string filter_name; int location) -> bool {{
                # Check for large community to prevent export to a location
                if ((BGP_ASN, BGP_LC_FUNCTION_NOEXPORT_LOCATION, location) !~ bgp_large_community) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_reject_noexport_location] Rejecting ", {self.functions.route_info()},
                    " due to match on BGP_LC_FUNCTION_NOEXPORT_LOCATION with location ", location;
                reject;
            }}"""

    @BirdFunction("bgp_peer_reject_non_exportable")
    def peer_reject_non_exportable(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_non_exportable function."""

        return f"""\
            # Can we export this route to the peer_asn?
            function bgp_peer_reject_non_exportable(
                string filter_name;
                int ipv4_maxlen; int ipv4_minlen;
                int ipv6_maxlen; int ipv6_minlen
            ) -> bool
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
                # Validate route before export
                if {self.functions.prefix_is_longer(BirdVariable("prefix_maxlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_reject_non_exportable] Not exporting due to prefix length >", prefix_maxlen," for ",
                        {self.functions.route_info()};
                    reject;
                }}
                if {self.functions.prefix_is_shorter(BirdVariable("prefix_minlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_reject_non_exportable] Not exporting due to prefix length <", prefix_minlen, " for ",
                        {self.functions.route_info()};
                    reject;
                }}
                # If all above tests are ok, then we can
                return true;
            }}"""

    @BirdFunction("bgp_peer_reject_non_exportable_blackhole")
    def peer_reject_non_exportable_blackhole(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_reject_non_exportable_blackhole function."""

        return f"""\
            # Can we export this route to the peer_asn?
            function bgp_peer_reject_non_exportable_blackhole(
                string filter_name;
                int ipv4_maxlen; int ipv4_minlen;
                int ipv6_maxlen; int ipv6_minlen
            ) -> bool
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
                # Validate route before export
                if {self.functions.prefix_is_longer(BirdVariable("prefix_maxlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_reject_non_exportable_blackhole] Not exporting due to prefix length >", prefix_maxlen," for ",
                        net;
                    reject;
                }}
                if {self.functions.prefix_is_shorter(BirdVariable("prefix_minlen"))} then {{
                    if DEBUG then print filter_name,
                        " [bgp_peer_reject_non_exportable_blackhole] Not exporting due to prefix length <", prefix_minlen, " for ",
                        net;
                    reject;
                }}
                # If all above tests are ok, then we can
                return true;
            }}"""

    @BirdFunction("bgp_peer_replace_aspath")
    def peer_replace_aspath(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_replace_aspath function."""

        return f"""\
            # Check if we need to replace the AS-PATH
            function bgp_peer_replace_aspath(string filter_name) -> bool
            int path_len;
            {{
                # Check for replace AS-PATH large community action
                if (BGP_LC_ACTION_REPLACE_ASPATH !~ bgp_large_community) then return false;
                # Grab current path length
                path_len = bgp_path.len;
                if DEBUG then print filter_name,
                    " [bgp_peer_replace_aspath] Replacing AS-PATH [", bgp_path, "] for ", {self.functions.route_info()},
                    " with ", path_len, "x ", BGP_ASN;
                # Empty the path, as we cannot assign a sequence
                bgp_path.empty;
                # Prepend our own ASN the number of times there was an ASN in the path
                path_len = path_len - 1;
                {self.peer_prepend(BirdVariable("BGP_ASN"), BirdVariable("path_len"))};
            }}"""

    @BirdFunction("bgp_peer_remove_lc_private")
    def peer_remove_lc_private(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD bgp_peer_remove_lc_private function."""

        return f"""\
            # Remove private large communities
            function bgp_peer_remove_lc_private(string filter_name) -> bool {{
                # Remove private large communities
                if (bgp_large_community !~ BGP_LC_STRIP_PRIVATE) then return false;
                if DEBUG then print filter_name,
                    " [bgp_peer_remove_lc_private] Removing private large communities from ", {self.functions.route_info()};
                bgp_large_community.delete(BGP_LC_STRIP_PRIVATE);
            }}"""

    @property
    def functions(self) -> SectionFunctions:
        """Return the functions section."""
        return self._functions
