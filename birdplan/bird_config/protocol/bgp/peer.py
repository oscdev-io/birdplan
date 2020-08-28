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

"""BIRD BGP protocol peer configuration."""

import requests
from ..pipe import BirdConfigProtocolPipe
from ...base import BirdConfigBase
from ... import util
from ....bgpq3 import BGPQ3
from ....exceptions import BirdPlanError


class BirdConfigProtocolBGPPeer(BirdConfigBase):
    """BIRD BGP protocol peer configuration."""

    def __init__(self, parent, peer_name, peer_config, **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Save our name and configuration
        self._peer_name = peer_name
        self._peer_config = peer_config

        # Work out our peer table name
        self._peer_table = f"bgp_AS{self.peer_asn}_{self.peer_name}_peer"

        # Work out our prefix list name
        self._prefix_list = f"bgp_AS{self.peer_asn}_{self.peer_name}_prefixes"

        # Work out our ASN list name
        self._asn_list = f"bgp_AS{self.peer_asn}_{self.peer_name}_asns"

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
        # If this is an transit, peer, customer, routecollector or routeserver, we need to redistribute our own routes and
        # customer routes
        if self.peer_type in ("customer", "routecollector", "routeserver", "peer", "transit"):
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
                if "prefix_limit4" not in self.peer_config:
                    self.peer_config["prefix_limit4"] = "peeringdb"
            if self.has_ipv6:
                if "prefix_limit6" not in self.peer_config:
                    self.peer_config["prefix_limit6"] = "peeringdb"
        # Work out the prefix limits...
        if self.has_ipv4:
            if ("prefix_limit4" in self.peer_config) and (self.peer_config["prefix_limit4"] == "peeringdb"):
                self.peer_config["prefix_limit4"] = self.peeringdb["info_prefixes4"]
        if self.has_ipv6:
            if ("prefix_limit6" in self.peer_config) and (self.peer_config["prefix_limit6"] == "peeringdb"):
                self.peer_config["prefix_limit6"] = self.peeringdb["info_prefixes6"]

        # Work out what we're going to be redistributing
        if "redistribute" in self.peer_config:
            for redistribute_type, redistribute_config in self.peer_config["redistribute"].items():
                if redistribute_type not in ("default", "connected", "static", "kernel", "originated"):
                    raise BirdPlanError(f"The BGP redistribute type '{redistribute_type}' is not known")
                self.redistribute[redistribute_type] = redistribute_config

        # Default to accepting nothing
        self._accept = {
            "default": False,
        }
        # Work out what we're going to be accepting
        if "accept" in self.peer_config:
            for accept_type, accept_config in self.peer_config["accept"].items():
                if accept_type != "default":
                    raise BirdPlanError(f"The BGP accept type '{accept_type}' is not known")
                self.accept[accept_type] = accept_config

        # Check for filters we need to setup
        self._filter = {"prefixes": [], "asns": [], "as-set": []}
        if "filter" in self.peer_config:
            for filter_type, filter_config in self.peer_config["filter"].items():
                if filter_type not in ("prefixes", "asns", "as-set"):
                    raise BirdPlanError(f"The BGP filter type '{filter_type}' is not known")
                self._filter[filter_type] = filter_config

        # Check if we're quarantined
        if "quarantine" in self.peer_config and self.peer_config["quarantine"]:
            self._quarantined = True
        else:
            self._quarantined = False

    def _setup_peer_tables(self):
        """Peering routing table setup."""
        if self.has_ipv4:
            self._addline(f"ipv4 table t_{self.peer_table}4;")
        if self.has_ipv6:
            self._addline(f"ipv6 table t_{self.peer_table}6;")

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

        self._addline(f"define {self.asn_list} = [")
        asns = []
        # Add ASN list with comments
        if self.filter_asns:
            asns.append(f"# {len(self.filter_asns)} statically defined")
            for asn in self.filter_asns:
                asns.append(f"{asn}")
        if irr_asns:
            asns.append(f"# {len(irr_asns)} from IRR with object '{self.filter_as_set}'")
            for asn in irr_asns:
                asns.append(f"{asn}")
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
                prefixes.append(f"# {len(ipv4_prefixes)} statically defined")
                prefixes.extend(ipv4_prefixes)
            if irr_prefixes["ipv4"]:
                prefixes.append("# %s from IRR with object '%s'" % (len(irr_prefixes["ipv4"]), self.filter_as_set))
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
            self._addline(f"define {self.prefix_list}6 = [")
            prefixes = []
            # Add prefix lists with comments
            if ipv6_prefixes:
                prefixes.append(f"# {len(ipv6_prefixes)} statically defined")
                prefixes.extend(ipv6_prefixes)
            if irr_prefixes["ipv6"]:
                prefixes.append("# %s from IRR with object '%s'" % (len(irr_prefixes["ipv6"]), self.filter_as_set))
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
                    self._addline(f'\t\tprint "[redistribute-large-communities] Adding {bird_lc} to ", net;', debug=True)
                    self._addline(f"\t\tbgp_large_community.add({bird_lc});")

    def _peer_to_bgp_export_filter(self, ipv):
        """Export filters into our main BGP routing table from the BGP peer table."""

        # Configure export filter to our main BGP table
        self._addline("# Export filter TO the main BGP table from the BGP peer table")
        self._addline(f"filter f_{self.peer_table}_bgp{ipv}_export")
        self._addline("int accept_route;")
        self._addline("{")
        # Check if we're accepting the route...
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then {")
        self._addline(f'\t\tprint "[f_{self.peer_table}_bgp{ipv}_export] Filtered ", net, " to main BGP table";', debug=True)
        self._addline("\t\treject;")
        self._addline("\t}")
        # Else reject
        self._addline(f'\tprint "[f_{self.peer_table}_bgp{ipv}_export] Exporting ", net, " to main BGP table";', debug=True)
        self._addline("\taccept;")
        self._addline("};")

    def _peer_to_bgp_import_filter(self, ipv):
        """Import filter FROM the main BGP table to the BGP peer table."""

        filter_name = f"f_{self.peer_table}_bgp{ipv}_import"

        # Configure import filter from our main BGP table
        self._addline("# Import filter FROM the main BGP table to the BGP peer table")
        self._addline(f"filter {filter_name}")
        self._addline("int accept_route;")
        self._addline("{")
        self._addline("\taccept_route = 0;")

        # Check that we have static routes imported first
        if self.redistribute["connected"] and not self.parent.import_connected:
            raise BirdPlanError("BGP needs connected routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.redistribute["kernel"] and not self.parent.import_kernel:
            raise BirdPlanError("BGP needs kernel routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.redistribute["static"] and not self.parent.import_static:
            raise BirdPlanError("BGP needs static routes to be imported before they can be redistributed to a peer")

        # Override exports if this is a customer peer and we don't export to customers
        if self.peer_type == "customer":
            self._addline("\t# Check for large community to prevent export to customers")
            self._addline("\tif (BGP_LC_EXPORT_NOCUSTOMER ~ bgp_large_community) then {")
            self._addline(
                f'\t\tprint "[{filter_name}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOCUSTOMER";', debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Override exports if this is a peer, routecollector or routeserver and we don't export to peers
        if self.peer_type in ("peer", "routecollector", "routeserver"):
            self._addline(f"\t# Check for large community to prevent export to {self.peer_type}")
            self._addline("\tif (BGP_LC_EXPORT_NOPEER ~ bgp_large_community) then {")
            self._addline(
                f'\t\tprint "[{filter_name}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOPEER";', debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Override exports if this is a transit and we don't export to transits
        if self.peer_type == "transit":
            self._addline("\t# Check for large community to prevent export to transit")
            self._addline("\tif (BGP_LC_EXPORT_NOTRANSIT ~ bgp_large_community) then {")
            self._addline(
                f'\t\tprint "[{filter_name}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOTRANSIT";', debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")

        # Redistribute connected
        if self.redistribute["connected"]:
            self._addline("\t# Redistribute connected routes")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on RTS_DEVICE (redistribute connected)";', debug=True,
            )
            self._add_redistribute_properties(self.redistribute["connected"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute connected routes")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline(
                f'\t\tprint "[{filter_name}] Rejecting ", net, " due to match on RTS_DEVICE (no redistribute connected)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute["static"]:
            self._addline("\t# Redistribute static routes")
            self._addline(f'\tif (proto = "static{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on proto static{ipv} (redistribute static)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["static"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute static routes")
            self._addline(f'\tif (proto = "static{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{filter_name}] Rejecting ", net, " due to match on proto static{ipv} (no redistribute static)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute["kernel"]:
            self._addline("\t# Redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on RTS_INHERIT (redistribute kernel)";', debug=True,
            )
            self._add_redistribute_properties(self.redistribute["kernel"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline(
                f'\t\tprint "[{filter_name}] Rejecting ", net, " due to match on RTS_INHERIT (no redistribute kernel)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute originated routes
        if self.redistribute["originated"]:
            self._addline("\t# Redistribute originated routes")
            self._addline(f'\tif (proto = "bgp_originate{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on proto bgp_originate{ipv}'
                ' (redistribute originated)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute["originated"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute originated routes")
            self._addline(f'\tif (proto = "bgp_originate{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{filter_name}] Rejecting ", net, " due to match on proto bgp_originate{ipv}'
                ' (no redistribute originated)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")

        # Do not redistribute the default route, no matter where we get it from
        if self.redistribute["default"]:
            # Make sure this is an allowed peer type for the default route to be exported
            if self.peer_type not in ["customer", "rrclient", "rrserver", "rrserver-rrserver"]:
                raise BirdPlanError(f"Having 'redistribute[default]' as True for a '{self.peer_type}' makes no sense")
            # Proceed with exporting...
            self._addline("\t# Accept the default route as we're redistributing, but only if, its been accepted above")
            self._addline(f"\tif (net = DEFAULT_ROUTE_V{ipv} && accept_route > 0) then {{")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting default route ", net, " due to match on accept_route>0'
                ' (redistribute default)";',
                debug=True,
            )
            self._addline("\t\taccept;")
        # Else explicitly reject it
        else:
            self._addline("\t# Reject the default route as we are not redistributing it")
            self._addline(f"\tif (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self._addline(f'\t\tprint "[{filter_name}] Rejecting default route ", net, " export";')
            self._addline("\t\treject;")
        self._addline("\t}")

        # Redistribute BGP routes
        if self.redistribute["bgp"]:
            self._addline("\t# Redistribute BGP routes (which is everything in our table)")
            self._addline("\tif (source = RTS_BGP) then {")
            self._addline(f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on RTS_BGP";', debug=True)
            self._add_redistribute_properties(self.redistribute["bgp"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")

        # Redistribute our own BGP routes
        if self.redistribute["bgp_own"]:
            self._addline("\t# Redistribute our own BGP routes")
            self._addline("\tif (BGP_LC_RELATION_OWN ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.peer_asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{filter_name}] Cannot export ", net, " with match on BGP_LC_RELATION_OWN";', debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on BGP_LC_RELATION_OWN";', debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_own"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute customer BGP routes
        if self.redistribute["bgp_customer"]:
            self._addline("\t# Redistribute customer BGP routes")
            self._addline("\tif (BGP_LC_RELATION_CUSTOMER ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.peer_asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{filter_name}] Cannot export ", net, " with match on BGP_LC_RELATION_CUSTOMER";', debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on BGP_LC_RELATION_CUSTOMER";', debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_customer"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute peering BGP routes
        if self.redistribute["bgp_peering"]:
            self._addline("\t# Redistribute peering BGP routes")
            self._addline("\tif (BGP_LC_RELATION_PEER ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.peer_asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{filter_name}] Cannot export ", net, " with match on BGP_LC_RELATION_PEER";', debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on BGP_LC_RELATION_PEER";', debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_peering"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
            self._addline("\tif (BGP_LC_RELATION_ROUTESERVER ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.peer_asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{filter_name}] Cannot export ", net, " with match on BGP_LC_RELATION_ROUTESERVER";', debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on BGP_LC_RELATION_ROUTESERVER";', debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_peering"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute transit BGP routes
        if self.redistribute["bgp_transit"]:
            self._addline("\t# Redistribute transit BGP routes")
            self._addline("\tif (BGP_LC_RELATION_TRANSIT ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.peer_asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{filter_name}] Cannot export ", net, " with match on BGP_LC_RELATION_TRANSIT";', debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{filter_name}] Accepting ", net, " due to match on BGP_LC_RELATION_TRANSIT";', debug=True,
            )
            self._add_redistribute_properties(self.redistribute["bgp_transit"])
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")

        # Check if we're accepting the route...
        self._addline("\tif (accept_route > 0) then {")
        # Do large community prepending if the peer is a customer, peer, routeserver or transit
        if self.peer_type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we are adding a large community to outgoing routes
            if "outgoing-large-communities" in self.peer_config:
                for large_community in sorted(self.peer_config["outgoing-large-communities"]):
                    bird_lc = util.sanitize_large_community(large_community)
                    self._addline(f'\t\tprint "[{filter_name}] Adding LC {bird_lc} to ", net;', debug=True)
                    self._addline(f"\t\tbgp_large_community.add({bird_lc});")
            # Check if we're doing prepending
            self._addline("\t\t# Do prepend if we have any LCs set")
            self._addline(f"\t\tbgp_export_prepend({self.peer_asn});")
        # Finally accept
        self._addline("\t\t# Finally accept")
        self._addline(f'\t\tprint "[{filter_name}] Accepting ", net, " to peer";', debug=True)
        self._addline("\t\taccept;")
        self._addline("\t}")

        # By default reject all routes
        self._addline("\t# Reject by default")
        self._addline(f'\tprint "[{filter_name}] Rejecting ", net, " to peer (fallthrough)";', debug=True)
        self._addline("\treject;")
        self._addline("};")

    def _peer_export_filter(self, ipv):
        """Peer export filter setup from peer table to peer."""

        filter_name = f"f_{self.peer_table}{ipv}_export"
        protocol_name = f"{self.peer_table}{ipv}"

        # Configure export filter to the BGP peer
        self._addline("# Export filter TO the BGP peer from the peer BGP table")
        self._addline(f"filter {filter_name}")
        self._addline("{")
        # Check if we're quarantined, if we are reject routes to the peer
        if self.quarantined:
            self._addline("\t# Peer is quarantined so reject exporting of routes")
            self._addline(f'\tprint "[{filter_name}] Rejecting ", net, " to peer (quarantined)";', debug=True)
            self._addline("\treject;")
        # If we're not quarantined, then export routes
        else:
            self._addline("\t# We accept all routes going to the peer that are in the peer BGP table")
            self._addline(f'\tif (proto != "{protocol_name}") then accept;')
        self._addline("};")

    def _peer_import_filter(self, ipv):
        """Peer import filter setup from peer to peer table."""

        filter_name = f"f_{self.peer_table}{ipv}_import"

        # Configure import filter from the BGP peer
        self._addline("# Import filter FROM the BGP peer TO the peer BGP table")
        self._addline(f"filter {filter_name} {{")

        # If this is the route from our peer, we need to check what type it is
        type_lines = []

        # Clients
        if self.peer_type == "customer":
            type_lines.append("\t\tbgp_lc_remove_internal();")
            type_lines.append(f"\t\tbgp_import_customer({self.peer_asn}, {self.cost});")
            if self.accept["default"]:
                raise BirdPlanError("Having 'accept[default]' as True for a 'customer' makes no sense")
            type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append(f"\t\tbgp_filter_asn_invalid({self.peer_asn});")
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Peers
        elif self.peer_type == "peer":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append(f"\t\tbgp_import_peer({self.peer_asn}, {self.cost});")
            if self.accept["default"]:
                raise BirdPlanError("Having 'accept[default]' as True for a 'peer' makes no sense")
            type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append(f"\t\tbgp_filter_asn_invalid({self.peer_asn});")
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Routecollector
        elif self.peer_type == "routecollector":
            type_lines.append("\t\tbgp_lc_remove_all();")
            if self.accept["default"]:
                raise BirdPlanError("Having 'accept[default]' as True for a 'routecollector' makes no sense")
            type_lines.append("\t\tbgp_filter_routecollector();")
        # Routeserver
        elif self.peer_type == "routeserver":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append(f"\t\tbgp_import_routeserver({self.peer_asn}, {self.cost});")
            if self.accept["default"]:
                raise BirdPlanError("Having 'accept[default]' as True for a 'routeserver' makes no sense")
            type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Route reflector client
        elif self.peer_type == "rrclient":
            if not self.accept["default"]:
                type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
        # Route reflector server
        elif self.peer_type == "rrserver":
            if not self.accept["default"]:
                type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
        # Route reflector server to route reflector server
        elif self.peer_type == "rrserver-rrserver":
            if not self.accept["default"]:
                type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
        # Transit providers
        elif self.peer_type == "transit":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append(f"\t\tbgp_import_transit({self.peer_asn}, {self.cost});")
            if self.accept["default"]:
                type_lines.append("\t\t# Bypass bogon and size filters for the default route")
                type_lines.append(f"\t\tif (net != DEFAULT_ROUTE_V{ipv}) then {{")
                type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
                type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
                type_lines.append("\t\t}")
            else:
                type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
                type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
                type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append(f"\t\tbgp_filter_asn_invalid({self.peer_asn});")
        else:
            raise BirdPlanError(f"The BGP peer type '{self.peer_type}' is not supported")

        # Check if we're filtering allowed ASNs
        if self.filter_asns:
            type_lines.append("\t\t# Filter on the allowed ASNs")
            type_lines.append(f"\t\tbgp_filter_asns({self.asn_list});")

        # Check if we're filtering allowed prefixes
        if self.filter_prefixes:
            type_lines.append("\t\t# Filter on the allowed prefixes")
            type_lines.append(f"\t\tbgp_filter_prefixes_v{ipv}({self.prefix_list}{ipv});")

        # Quarantine mode...
        if self.quarantined:
            type_lines.append("\t\tbgp_filter_quarantine();")

        # Check if we are adding a large community to incoming routes
        if "incoming-large-communities" in self.peer_config:
            for large_community in sorted(self.peer_config["incoming-large-communities"]):
                bird_lc = util.sanitize_large_community(large_community)
                if self.root.debug:
                    type_lines.append(f'\t\tprint "[{filter_name}] Adding LC {bird_lc} to ", net;')
                type_lines.append(f"\t\tbgp_large_community.add({bird_lc});")

        # If we have lines from the above add them
        if type_lines:
            self._addline("\t# Process routes from our peer")
            self._addline(f'\tif (proto = "{self.peer_table}{ipv}") then {{')
            self._addlines(type_lines)
            self._addline("\t}")

        self._addline("\taccept;")
        self._addline("};")

    def _setup_peer_protocol(self, ipv):
        """Peer protocol setup for a single protocol."""

        protocol_name = f"{self.peer_table}{ipv}"

        self._addline(f"protocol bgp {protocol_name} {{")
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
                raise BirdPlanError("BGP route reflectors require a 'cluster_id' set if they have 'rrclient' peers")
            # Set this peer as a route reflector client
            self._addline("\trr client;")
            self._addline(f"\trr cluster id {self.parent.rr_cluster_id};")

        # Handle route reflector server-to-server
        if self.peer_type == "rrserver-rrserver":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrserver-rrserver peer
            if not self.parent.rr_cluster_id:
                raise BirdPlanError("BGP route reflectors require a 'cluster_id' if they have 'rrserver-rrserver' peers")
            # Set this peer as a route reflector client
            self._addline("\trr client;")
            self._addline(f"\trr cluster id {self.parent.rr_cluster_id};")

        # Setup peer table
        self._addline(f"\tipv{ipv} {{")
        self._addline(f"\t\ttable t_{protocol_name};")
        self._addline(f"\t\tigp table master{ipv};")
        # Setup import and export table so we can do soft reconfiguration
        self._addline("\t\timport table;")
        self._addline("\t\texport table;")
        # Setup prefix limit
        prefix_limit_name = f"prefix_limit{ipv}"
        if prefix_limit_name in self.peer_config and (self.peer_config[prefix_limit_name] is not None):
            self._addline("\t\timport limit %s;" % self.peer_config[prefix_limit_name])
        # Setup filters
        self._addline(f"\t\timport filter f_{protocol_name}_import;")
        self._addline(f"\t\texport filter f_{protocol_name}_export;")
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
    def accept(self):
        """Return our accept structure."""
        return self._accept

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
        """Return our redistribute structure."""
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
        self._setup_peer_to_bgp_filters()

        # BGP peer filters
        self._setup_peer_filters()

        # BGP peer protocols
        self._setup_peer_protocols()

        # Configure pipe from the BGP peer table to the main BGP table
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
