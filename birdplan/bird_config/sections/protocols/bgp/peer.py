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

# pylint: disable=too-many-lines

from typing import Dict, List, Optional

from .bgp_attributes import BGPAttributes
from .peer_attributes import (
    BGPPeerAttributes,
    BGPPeerFilterPolicy,
    BGPPeerFilterItem,
    BGPPeerPeeringDB,
    BGPPeerPrefixLimit,
    BGPPeerRoutePolicyAccept,
    BGPPeerRoutePolicyRedistribute,
    BGPPeerRoutePolicyRedistributeItem,
    BGPPeerLargeCommunities,
)
from .typing import BGPPeerConfig
from ..pipe import ProtocolPipe
from ..base import SectionProtocolBase
from ...constants import SectionConstants
from ...functions import SectionFunctions
from ...tables import SectionTables
from .... import util
from ....globals import BirdConfigGlobals
from .....bgpq3 import BGPQ3
from .....exceptions import BirdPlanError


class ProtocolBGPPeer(SectionProtocolBase):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """BIRD BGP protocol peer configuration."""

    _bgp_attributes: BGPAttributes
    _peer_attributes: BGPPeerAttributes

    def __init__(
        self,
        birdconfig_globals: BirdConfigGlobals,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
        bgp_attributes: BGPAttributes,
        peer_name: str,
        peer_config: BGPPeerConfig,
    ):  # pylint: disable=too-many-branches,too-many-statements,too-many-arguments
        """Initialize the object."""
        super().__init__(birdconfig_globals, constants, functions, tables)

        # Initialize our attributes
        self._bgp_attributes = bgp_attributes
        self._peer_attributes = BGPPeerAttributes()

        # Save our name and configuration
        self.name = peer_name

        # Check if we have a peer description
        if "description" not in peer_config:
            raise BirdPlanError(f"BGP peer '{self.name}' need a 'description' field")
        self.description = peer_config["description"]

        # Check if we have a peer type
        if "type" not in peer_config:
            raise BirdPlanError(f"BGP peer '{self.name}' need a 'type' field")
        self.peer_type = peer_config["type"]

        # Check if we have a peer asn
        if "asn" not in peer_config:
            raise BirdPlanError(f"BGP peer '{self.name}' need a 'asn' field")
        self.asn = peer_config["asn"]

        # If the peer type is of internal nature, but doesn't match our peer type, throw an exception
        if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.asn != self.bgp_attributes.asn:
                raise BirdPlanError(f"BGP peer '{self.name}' is of internal nature, but has a different ASN")

        # INTERNAL: Dynamically set the section
        self._section = f"BGP Peer: {self.asn} - {self.name}"

        # Check for neighbor addresses
        if "neighbor4" in peer_config:
            self.neighbor4 = peer_config["neighbor4"]
        if "neighbor6" in peer_config:
            self.neighbor6 = peer_config["neighbor6"]
        # Check if we have a source address
        if "source_address4" in peer_config:
            self.source_address4 = peer_config["source_address4"]
        if "source_address6" in peer_config:
            self.source_address6 = peer_config["source_address6"]
        # Sanity test the neighbor and source addresses
        if self.neighbor4 and not self.source_address4:
            raise BirdPlanError(f"BGP peer '{self.name}' has 'neighbor4' specified but no 'source_address4'")
        if self.neighbor6 and not self.source_address6:
            raise BirdPlanError(f"BGP peer '{self.name}' has 'neighbor6' specified but no 'source_address6'")
        if self.source_address4 and not self.neighbor4:
            raise BirdPlanError(f"BGP peer '{self.name}' has 'source_address4' specified but no 'neighbor4'")
        if self.source_address6 and not self.neighbor6:
            raise BirdPlanError(f"BGP peer '{self.name}' has 'source_address6' specified but no 'neighbor6'")

        # Check additional options we may have
        if "connect_delay_time" in peer_config:
            self.connect_delay_time = peer_config["connect_delay_time"]
        if "connect_retry_time" in peer_config:
            self.connect_retry_time = peer_config["connect_retry_time"]
        if "error_wait_time" in peer_config:
            self.error_wait_time = peer_config["error_wait_time"]
        if "multihop" in peer_config:
            self.multihop = peer_config["multihop"]
        if "password" in peer_config:
            self.password = peer_config["password"]

        if "cost" in peer_config:
            # Raise an exception if peer cost does not make sense for a specific peer type
            if self.peer_type in ("internal", "routecollector", "rrclient", "rrserver", "rrserver-rrserver"):
                raise BirdPlanError(f"BGP peer '{self.name}' has 'cost' specified but makes no sense for this peer type")
            self.cost = peer_config["cost"]

        # Check if we're in graceful_shutdown mode
        if self.bgp_attributes.graceful_shutdown:
            self.graceful_shutdown = True
        if "graceful_shutdown" in peer_config:
            self.graceful_shutdown = peer_config["graceful_shutdown"]

        # Check if we are adding a large community to outgoing routes
        if "incoming_large_communities" in peer_config:
            for large_community in sorted(peer_config["incoming_large_communities"]):
                self.large_communities.incoming.append(util.sanitize_large_community(large_community))
        # Check if we are adding a large community to outgoing routes
        if "outgoing_large_communities" in peer_config:
            for large_community in sorted(peer_config["outgoing_large_communities"]):
                self.large_communities.outgoing.append(util.sanitize_large_community(large_community))

        # Turn on passive mode for route reflectors and customers
        if self.peer_type in ("customer", "rrclient"):
            self.passive = True
        # But allow it to be set manually
        if "passive" in peer_config:
            self.passive = peer_config["passive"]

        # If this involves an internal peer, send our entire BGP table
        if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.route_policy_redistribute.bgp = True
        # If this is an transit, peer, customer, routecollector or routeserver, we need to redistribute our own routes and
        # customer routes
        if self.peer_type in ("customer", "routecollector", "routeserver", "peer", "transit"):
            self.route_policy_redistribute.bgp_own = True
            self.route_policy_redistribute.bgp_customer = True
        # If this is an customer, we need to redistribute peer and transit routes too
        if self.peer_type == "customer":
            self.route_policy_redistribute.bgp_peering = True
            self.route_policy_redistribute.bgp_transit = True
        # Work out what we're going to be redistributing
        if "redistribute" in peer_config:
            for redistribute_type, redistribute_config in peer_config["redistribute"].items():
                if redistribute_type not in (
                    "default",
                    "connected",
                    "static",
                    "kernel",
                    "originated",
                    "bgp",
                    "bgp_own",
                    "bgp_customer",
                    "bgp_peering",
                    "bgp_transit",
                ):
                    raise BirdPlanError(f"The BGP redistribute type '{redistribute_type}' is not known")
                setattr(self.route_policy_redistribute, redistribute_type, redistribute_config)

        # If the peer is a customer or peer, check if we have a prefix limit, if not add it from peeringdb
        if self.peer_type in ("customer", "peer"):
            if self.has_ipv4 and ("prefix_limit4" not in peer_config):
                self.prefix_limit4 = "peeringdb"
            if self.has_ipv6 and ("prefix_limit6" not in peer_config):
                self.prefix_limit6 = "peeringdb"
        # Check for peer config, this should override the above
        if self.has_ipv4 and "prefix_limit4" in peer_config:
            self.prefix_limit4 = peer_config["prefix_limit4"]
        if self.has_ipv6 and "prefix_limit6" in peer_config:
            self.prefix_limit6 = peer_config["prefix_limit6"]
        # Work out the prefix limits...
        if self.has_ipv4 and self.prefix_limit4 and self.prefix_limit4 == "peeringdb":
            self.prefix_limit4 = self.peeringdb["info_prefixes4"]
        if self.has_ipv6 and self.prefix_limit6 and self.prefix_limit6 == "peeringdb":
            self.prefix_limit6 = self.peeringdb["info_prefixes6"]

        # If this is a rrserver to rrserver peer, we need to by default redistribute the default route (if we have one)
        if self.peer_type == "rrserver-rrserver":
            self.route_policy_accept.default = True
        # Work out what we're going to be accepting
        if "accept" in peer_config:
            for accept_type, accept_config in peer_config["accept"].items():
                if accept_type != "default":
                    raise BirdPlanError(f"The BGP accept type '{accept_type}' is not known")
                setattr(self.route_policy_accept, accept_type, accept_config)

        # Check for filters we need to setup
        if "filter" in peer_config:
            for filter_type, filter_config in peer_config["filter"].items():
                if filter_type not in ("prefixes", "asns", "as_sets"):
                    raise BirdPlanError(f"The BGP filter type '{filter_type}' is not known")
                setattr(self.filter_policy, filter_type, filter_config)

        # Check if we're quarantined
        if "quarantine" in peer_config and peer_config["quarantine"]:
            self.quarantined = True

    def configure(self) -> None:
        """Configure BGP peer."""
        super().configure()

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
        bgp_peer_pipe = ProtocolPipe(
            birdconfig_globals=self.birdconfig_globals,
            table_from=self.bgp_table_name,
            table_to="bgp",
            table_export_filtered=True,
            table_import_filtered=True,
            has_ipv4=self.has_ipv4,
            has_ipv6=self.has_ipv6,
        )
        self.conf.add(bgp_peer_pipe)

        # End of peer
        self.conf.add("")

    def protocol_name(self, ipv: str) -> str:
        """Return the IP versioned protocol name."""
        return f"bgp{ipv}_AS{self.asn}_{self.name}"

    def bgp_table_name(self, ipv: str) -> str:
        """Return the IP versioned BGP table name."""
        return f"t_bgp{ipv}_AS{self.asn}_{self.name}_peer"

    def filter_name_export(self, ipv: str) -> str:
        """Return the IP versioned peer export filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_export"

    def filter_name_import(self, ipv: str) -> str:
        """Return the IP versioned peer import filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_import"

    def filter_name_export_bgp(self, ipv: str) -> str:
        """Return the IP versioned BGP export filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_bgp{ipv}_export"

    def filter_name_import_bgp(self, ipv: str) -> str:
        """Return the IP versioned BGP import filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_bgp{ipv}_import"

    def prefix_list_name(self, ipv: str) -> str:
        """Return our prefix list name."""
        return f"bgp{ipv}_AS{self.asn}_{self.name}_prefixes"

    def _setup_peer_tables(self) -> None:
        """Peering routing table setup."""
        self.tables.conf.append(f"# BGP Peer Tables: {self.asn} - {self.name}")
        if self.has_ipv4:
            self.tables.conf.append(f"ipv4 table {self.bgp_table_name('4')};")
        if self.has_ipv6:
            self.tables.conf.append(f"ipv6 table {self.bgp_table_name('6')};")
        self.tables.conf.append("")

    def _setup_peer_asns(self) -> None:
        """ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_asn_filter:
            return

        # Grab IRR prefixes
        irr_asns = []
        if self.filter_policy.as_sets:
            bgpq3 = BGPQ3()
            irr_asns = bgpq3.get_asns(self.filter_policy.as_sets)

        self.conf.add(f"define {self.asn_list_name} = [")
        asns = []
        # Add ASN list with comments
        if self.filter_policy.asns:
            asns.append(f"# {len(self.filter_policy.asns)} statically defined")
            for asn in self.filter_policy.asns:
                asns.append(f"{asn}")
        if irr_asns:
            asns.append(f"# {len(irr_asns)} from IRR with object '{self.filter_policy.as_sets}'")
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
            self.conf.add("  " + line)
        self.conf.add("];")
        self.conf.add("")

    def _setup_peer_prefixes(self) -> None:
        """Prefix list setup."""
        # Short circuit and exit if we have none
        if not self.has_prefix_filter:
            return

        # Work out prefixes
        prefix_lists: Dict[str, List[str]] = {"4": [], "6": []}
        for prefix in sorted(self.filter_policy.prefixes):
            if ":" in prefix:
                prefix_lists["6"].append(prefix)
            else:
                prefix_lists["4"].append(prefix)

        # Grab IRR prefixes
        irr_prefixes: Dict[str, List[str]] = {"ipv4": [], "ipv6": []}
        if self.filter_policy.as_sets:
            bgpq3 = BGPQ3()
            irr_prefixes = bgpq3.get_prefixes(self.filter_policy.as_sets)

        # Output prefix definitions
        for ipv in ["4", "6"]:
            self.conf.add(f"define {self.prefix_list_name(ipv)} = [")
            prefix_list = prefix_lists[ipv]
            prefix_list_irr = irr_prefixes[f"ipv{ipv}"]
            prefixes = []
            # Add statically defined prefix list
            if prefix_list:
                prefixes.append(f"# {len(prefix_list)} explicitly defined")
                prefixes.extend(prefix_list)
            # Add prefix list from IRR
            if prefix_list_irr:
                prefixes.append(f"# {len(prefix_list_irr)} from IRR with object '{self.filter_policy.as_sets}'")
                prefixes.extend(prefix_list_irr)
            # Join into one string, so we get the commas
            prefixes_str = ",\n".join(prefixes)
            # Loop with each line
            for line in prefixes_str.splitlines():
                # Remove comma from the comments
                if "#" in line:
                    line = line[:-1]
                # Add line to our output
                self.conf.add("  " + line)
            self.conf.add("];")
            self.conf.add("")

    def _add_redistribute_properties(self, redistribute: BGPPeerRoutePolicyRedistributeItem) -> None:
        """Redistribution properties to add to the route."""
        if isinstance(redistribute, dict):
            if "large_communities" in redistribute:
                for large_community in sorted(redistribute["large_communities"]):
                    bird_lc = util.sanitize_large_community(large_community)
                    self.conf.add(f'    print "[redistribute:large_communities] Adding {bird_lc} to ", net;', debug=True)
                    self.conf.add(f"    bgp_large_community.add({bird_lc});")

    def _peer_to_bgp_export_filter(self, ipv: str) -> None:
        """Export filters into our main BGP routing table from the BGP peer table."""

        # Configure export filter to our main BGP table
        self.conf.add("# Export filter TO the main BGP table from the BGP peer table")
        self.conf.add(f"filter {self.filter_name_export_bgp((ipv))} {{")
        # Check if we're accepting the route...
        self.conf.add("  if (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then {")
        self.conf.add(f'    print "[{self.filter_name_export_bgp((ipv))}] Filtered ", net, " to main BGP table";', debug=True)
        self.conf.add("    reject;")
        self.conf.add("  }")
        # Else reject
        self.conf.add(f'  print "[{self.filter_name_export_bgp((ipv))}] Exporting ", net, " to main BGP table";', debug=True)
        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _peer_to_bgp_import_filter(self, ipv: str) -> None:  # pylint: disable=too-many-branches,too-many-statements
        """Import filter FROM the main BGP table to the BGP peer table."""

        # Configure import filter from our main BGP table
        self.conf.add("# Import filter FROM the main BGP table to the BGP peer table")
        self.conf.add(f"filter {self.filter_name_import_bgp((ipv))}")
        self.conf.add("int accept_route;")
        self.conf.add("{")
        self.conf.add("  accept_route = 0;")

        # Check that we have static routes imported first
        if self.route_policy_redistribute.connected and not self.bgp_attributes.route_policy_import.connected:
            raise BirdPlanError("BGP needs connected routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.route_policy_redistribute.kernel and not self.bgp_attributes.route_policy_import.kernel:
            raise BirdPlanError("BGP needs kernel routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.route_policy_redistribute.static and not self.bgp_attributes.route_policy_import.static:
            raise BirdPlanError("BGP needs static routes to be imported before they can be redistributed to a peer")

        # Override exports if this is a customer peer and we don't export to customers
        if self.peer_type == "customer":
            self.conf.add("  # Check for large community to prevent export to customers")
            self.conf.add("  if (BGP_LC_EXPORT_NOCUSTOMER ~ bgp_large_community) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOCUSTOMER";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Override exports if this is a peer, routecollector or routeserver and we don't export to peers
        if self.peer_type in ("peer", "routecollector", "routeserver"):
            self.conf.add(f"  # Check for large community to prevent export to {self.peer_type}")
            self.conf.add("  if (BGP_LC_EXPORT_NOPEER ~ bgp_large_community) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOPEER";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Override exports if this is a transit and we don't export to transits
        if self.peer_type == "transit":
            self.conf.add("  # Check for large community to prevent export to transit")
            self.conf.add("  if (BGP_LC_EXPORT_NOTRANSIT ~ bgp_large_community) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOTRANSIT";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")

        # Redistribute connected
        if self.route_policy_redistribute.connected:
            self.conf.add("  # Redistribute connected routes")
            self.conf.add(f'  if (proto = "direct{ipv}_bgp") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on direct{ipv}_bgp '
                '(redistribute connected)";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.connected)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        else:
            self.conf.add("  # Do not redistribute connected routes")
            self.conf.add(f'  if (proto = "direct{ipv}_bgp") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on direct{ipv}_bgp '
                '(no redistribute connected)";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Redistribute static routes
        if self.route_policy_redistribute.static:
            self.conf.add("  # Redistribute static routes")
            self.conf.add(f'  if (proto = "static{ipv}") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on proto static{ipv} '
                '(redistribute static)";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.static)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        else:
            self.conf.add("  # Do not redistribute static routes")
            self.conf.add(f'  if (proto = "static{ipv}") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on proto static{ipv} '
                '(no redistribute static)";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Redistribute kernel routes
        if self.route_policy_redistribute.kernel:
            self.conf.add("  # Redistribute kernel routes")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_INHERIT '
                '(redistribute kernel)";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.kernel)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        else:
            self.conf.add("  # Do not redistribute kernel routes")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on RTS_INHERIT '
                '(no redistribute kernel)";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Redistribute originated routes
        if self.route_policy_redistribute.originated:
            self.conf.add("  # Redistribute originated routes")
            self.conf.add(f'  if (proto = "bgp_originate{ipv}") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on proto bgp_originate{ipv}'
                ' (redistribute originated)";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.originated)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        else:
            self.conf.add("  # Do not redistribute originated routes")
            self.conf.add(f'  if (proto = "bgp_originate{ipv}") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on proto bgp_originate{ipv}'
                ' (no redistribute originated)";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")

        # Do not redistribute the default route, no matter where we get it from
        if self.route_policy_redistribute.default:
            # Make sure this is an allowed peer type for the default route to be exported
            if self.peer_type not in ["customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"]:
                raise BirdPlanError(
                    f"Having 'redistribute[default]' as True for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            # Proceed with exporting...
            self.conf.add("  # Accept the default route as we're redistributing, but only if, its been accepted above")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv} && accept_route > 0) then {{")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting default route ", net, " due to match on '
                ' accept_route>0 (redistribute default)";',
                debug=True,
            )
            self.conf.add("    accept;")
        # Else explicitly reject it
        else:
            self.conf.add("  # Reject the default route as we are not redistributing it")
            self.conf.add(f"  if (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self.conf.add(f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting default route ", net, " export";')
            self.conf.add("    reject;")
        self.conf.add("  }")

        # Redistribute BGP routes
        if self.route_policy_redistribute.bgp:
            self.conf.add("  # Redistribute BGP routes (which is everything in our table)")
            self.conf.add("  if (source = RTS_BGP) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_BGP";', debug=True
            )
            self._add_redistribute_properties(self.route_policy_redistribute.bgp)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")

        # Redistribute our own BGP routes
        if self.route_policy_redistribute.bgp_own:
            self.conf.add("  # Redistribute our own BGP routes")
            self.conf.add("  if (BGP_LC_RELATION_OWN ~ bgp_large_community) then {")
            self.conf.add(f"    if !bgp_can_export_v{ipv}({self.asn}) then {{")
            self.conf.add(
                f'      print "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on BGP_LC_RELATION_OWN";',
                debug=True,
            )
            self.conf.add("      reject;")
            self.conf.add("    }")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on BGP_LC_RELATION_OWN";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.bgp_own)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        # Redistribute customer BGP routes
        if self.route_policy_redistribute.bgp_customer:
            self.conf.add("  # Redistribute customer BGP routes")
            self.conf.add("  if (BGP_LC_RELATION_CUSTOMER ~ bgp_large_community) then {")
            self.conf.add(f"    if !bgp_can_export_v{ipv}({self.asn}) then {{")
            self.conf.add(
                f'      print "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on '
                'BGP_LC_RELATION_CUSTOMER";',
                debug=True,
            )
            self.conf.add("      reject;")
            self.conf.add("    }")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on '
                'BGP_LC_RELATION_CUSTOMER";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.bgp_customer)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        # Redistribute peering BGP routes
        if self.route_policy_redistribute.bgp_peering:
            self.conf.add("  # Redistribute peering BGP routes")
            self.conf.add("  if (BGP_LC_RELATION_PEER ~ bgp_large_community) then {")
            self.conf.add(f"    if !bgp_can_export_v{ipv}({self.asn}) then {{")
            self.conf.add(
                f'      print "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on BGP_LC_RELATION_PEER";',
                debug=True,
            )
            self.conf.add("      reject;")
            self.conf.add("    }")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on BGP_LC_RELATION_PEER";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.bgp_peering)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
            self.conf.add("  if (BGP_LC_RELATION_ROUTESERVER ~ bgp_large_community) then {")
            self.conf.add(f"    if !bgp_can_export_v{ipv}({self.asn}) then {{")
            self.conf.add(
                f'      print "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on '
                'BGP_LC_RELATION_ROUTESERVER";',
                debug=True,
            )
            self.conf.add("      reject;")
            self.conf.add("    }")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on '
                'BGP_LC_RELATION_ROUTESERVER";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.bgp_peering)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        # Redistribute transit BGP routes
        if self.route_policy_redistribute.bgp_transit:
            self.conf.add("  # Redistribute transit BGP routes")
            self.conf.add("  if (BGP_LC_RELATION_TRANSIT ~ bgp_large_community) then {")
            self.conf.add(f"    if !bgp_can_export_v{ipv}({self.asn}) then {{")
            self.conf.add(
                f'      print "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on '
                'BGP_LC_RELATION_TRANSIT";',
                debug=True,
            )
            self.conf.add("      reject;")
            self.conf.add("    }")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on '
                'BGP_LC_RELATION_TRANSIT";',
                debug=True,
            )
            self._add_redistribute_properties(self.route_policy_redistribute.bgp_transit)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")

        # Check if we're accepting the route...
        self.conf.add("  if (accept_route > 0) then {")
        # Check if we are adding a large community to outgoing routes
        for large_community in sorted(self.large_communities.outgoing):
            self.conf.add(f'    print "[{self.filter_name_import_bgp((ipv))}] Adding LC {large_community} to ", net;', debug=True)
            self.conf.add(f"    bgp_large_community.add({large_community});")
        # Do large community prepending if the peer is a customer, peer, routeserver or transit
        if self.peer_type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we're doing prepending
            self.conf.add("    # Do prepend if we have any LCs set")
            self.conf.add(f"    bgp_export_prepend({self.asn});")
        # If we have graceful_shutdown set, add the community
        if self.graceful_shutdown:
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Adding GRACEFUL_SHUTDOWN community to ", net;', debug=True
            )
            self.conf.add("    bgp_community.add(BGP_COMMUNITY_GRACEFUL_SHUTDOWN);")
        # Finally accept
        self.conf.add("    # Finally accept")
        self.conf.add(f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " to peer";', debug=True)
        self.conf.add("    accept;")
        self.conf.add("  }")

        # By default reject all routes
        self.conf.add("  # Reject by default")
        self.conf.add(f'  print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " to peer (fallthrough)";', debug=True)
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _peer_export_filter(self, ipv: str) -> None:
        """Peer export filter setup from peer table to peer."""

        # Configure export filter to the BGP peer
        self.conf.add("# Export filter TO the BGP peer from the peer BGP table")
        self.conf.add(f"filter {self.filter_name_export(ipv)}")
        self.conf.add("{")
        # Check if we're quarantined, if we are reject routes to the peer
        if self.quarantined:
            self.conf.add("  # Peer is quarantined so reject exporting of routes")
            self.conf.add(f'  print "[{self.filter_name_export(ipv)}] Rejecting ", net, " to peer (quarantined)";', debug=True)
            self.conf.add("  reject;")
        # If we're not quarantined, then export routes
        else:
            self.conf.add("  # We accept all routes going to the peer that are in the peer BGP table")
            self.conf.add(f'  if (proto != "{self.protocol_name(ipv)}") then accept;')
        self.conf.add("};")
        self.conf.add("")

    def _peer_import_filter(self, ipv: str) -> None:  # pylint: disable=too-many-branches,too-many-statements
        """Peer import filter setup from peer to peer table."""

        # Configure import filter from the BGP peer
        self.conf.add("# Import filter FROM the BGP peer TO the peer BGP table")
        self.conf.add(f"filter {self.filter_name_import(ipv)} {{")

        # If this is the route from our peer, we need to check what type it is
        type_lines = []

        # Check accept default is valid
        if self.route_policy_accept.default and self.peer_type not in (
            "internal",
            "rrclient",
            "rrserver",
            "rrserver-rrserver",
            "transit",
        ):
            raise BirdPlanError(
                f"Having 'accept[default]' as True for peer '{self.name}' with type '{self.peer_type}' makes no sense"
            )

        # Clients
        if self.peer_type == "customer":
            type_lines.append("    bgp_communities_strip_internal();")
            type_lines.append(f"    bgp_import_customer({self.asn}, {self.cost});")
            type_lines.append(f"    bgp_filter_default_v{ipv}();")
            type_lines.append(f"    bgp_filter_bogons_v{ipv}();")
            type_lines.append(f"    bgp_filter_size_v{ipv}();")
            type_lines.append("    bgp_filter_asn_bogons();")
            type_lines.append("    bgp_filter_asn_long();")
            type_lines.append("    bgp_filter_asn_short();")
            type_lines.append(f"    bgp_filter_asn_invalid({self.asn});")
            type_lines.append("    bgp_filter_asn_transit();")
            type_lines.append("    bgp_filter_nexthop_not_peerip();")
            type_lines.append("    bgp_filter_community_length();")
        # Peers
        elif self.peer_type == "peer":
            type_lines.append("    bgp_communities_strip_all();")
            type_lines.append(f"    bgp_import_peer({self.asn}, {self.cost});")
            type_lines.append(f"    bgp_filter_default_v{ipv}();")
            type_lines.append(f"    bgp_filter_bogons_v{ipv}();")
            type_lines.append(f"    bgp_filter_size_v{ipv}();")
            type_lines.append("    bgp_filter_asn_bogons();")
            type_lines.append("    bgp_filter_asn_long();")
            type_lines.append("    bgp_filter_asn_short();")
            type_lines.append("    bgp_filter_nexthop_not_peerip();")
            type_lines.append(f"    bgp_filter_asn_invalid({self.asn});")
            type_lines.append("    bgp_filter_asn_transit();")
            type_lines.append("    bgp_filter_community_length();")
        # Routecollector
        elif self.peer_type == "routecollector":
            type_lines.append("    bgp_communities_strip_all();")
            type_lines.append("    bgp_filter_routecollector();")
        # Routeserver
        elif self.peer_type == "routeserver":
            type_lines.append("    bgp_communities_strip_all();")
            type_lines.append(f"    bgp_import_routeserver({self.asn}, {self.cost});")
            type_lines.append(f"    bgp_filter_default_v{ipv}();")
            type_lines.append(f"    bgp_filter_bogons_v{ipv}();")
            type_lines.append(f"    bgp_filter_size_v{ipv}();")
            type_lines.append("    bgp_filter_asn_bogons();")
            type_lines.append("    bgp_filter_asn_long();")
            type_lines.append("    bgp_filter_asn_short();")
            type_lines.append("    bgp_filter_asn_transit();")
            type_lines.append("    bgp_filter_community_length();")
        # Internal router peer types
        elif self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if not self.route_policy_accept.default:
                type_lines.append(f"    bgp_filter_default_v{ipv}();")
        # Transit providers
        elif self.peer_type == "transit":
            type_lines.append("    bgp_communities_strip_all();")
            type_lines.append(f"    bgp_import_transit({self.asn}, {self.cost});")
            if self.route_policy_accept.default:
                type_lines.append("    # Bypass bogon and size filters for the default route")
                type_lines.append(f"    if (net != DEFAULT_ROUTE_V{ipv}) then {{")
                type_lines.append(f"      bgp_filter_bogons_v{ipv}();")
                type_lines.append(f"      bgp_filter_size_v{ipv}();")
                type_lines.append("    }")
            else:
                type_lines.append(f"    bgp_filter_default_v{ipv}();")
                type_lines.append(f"    bgp_filter_bogons_v{ipv}();")
                type_lines.append(f"    bgp_filter_size_v{ipv}();")
            type_lines.append("    bgp_filter_asn_bogons();")
            type_lines.append("    bgp_filter_asn_long();")
            type_lines.append("    bgp_filter_asn_short();")
            type_lines.append(f"    bgp_filter_asn_invalid({self.asn});")
            type_lines.append("    bgp_filter_nexthop_not_peerip();")
            type_lines.append("    bgp_filter_community_length();")
        else:
            raise BirdPlanError(f"The BGP peer type '{self.peer_type}' is not supported")

        # Flip around the meaning of filters depending on peer type
        # For customer and peer, it is an ALLOW list
        if self.peer_type in ("customer", "peer"):
            # Check if we're filtering allowed ASNs
            if self.filter_policy.asns:
                type_lines.append("    # Filter on the allowed ASNs")
                type_lines.append(f"    bgp_filter_allow_asns({self.asn_list_name});")
            # Check if we're filtering allowed prefixes
            if self.filter_policy.prefixes:
                type_lines.append("    # Filter on the allowed prefixes")
                type_lines.append(f"    bgp_filter_allow_prefixes({self.prefix_list_name(ipv)});")
        # For everything else it is a DENY list
        elif self.peer_type != "routecollector":
            # Check if we're filtering allowed ASNs
            if self.filter_policy.asns:
                type_lines.append("    # Filter on the allowed ASNs")
                type_lines.append(f"    bgp_filter_deny_asns({self.asn_list_name});")
            # Check if we're filtering allowed prefixes
            if self.filter_policy.prefixes:
                type_lines.append("    # Filter on the allowed prefixes")
                type_lines.append(f"    bgp_filter_deny_prefixes({self.prefix_list_name(ipv)});")

        # Quarantine mode...
        if self.quarantined:
            # Quarantining a routecollector makes no sense at all
            if self.peer_type == "routecollector":
                raise BirdPlanError(f"Having 'quarantine' as True for a '{self.peer_type}' makes no sense")
            # Quarantine prefixes
            type_lines.append("    # Quarantine all prefixes received")
            type_lines.append("    bgp_filter_quarantine();")

        # Check if we are adding a large community to incoming routes
        if self.large_communities.incoming:
            # Adding an incoming large community to a routecollector makes no sense at all
            if self.peer_type == "routecollector":
                raise BirdPlanError(
                    f"Having 'incoming_large_communities' set for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            # Loop with large communities and add to the prefix
            for large_community in sorted(self.large_communities.incoming):
                if self.birdconfig_globals.debug:
                    type_lines.append(f'    print "[{self.filter_name_import(ipv)}] Adding LC {large_community} to ", net;')
                type_lines.append(f"    bgp_large_community.add({large_community});")

        # Support for changing incoming local_pref
        if self.peer_type == "customer":
            type_lines.append("    bgp_import_localpref();")

        # Enable graceful_shutdown for this prefix
        if self.graceful_shutdown:
            type_lines.append("    bgp_graceful_shutdown_enable();")
        # Set local_pref to 0 (GRACEFUL_SHUTDOWN) for the peer in graceful_shutdown
        type_lines.append("    bgp_graceful_shutdown();")

        # If we have lines from the above add them
        if type_lines:
            self.conf.add("  # Process routes from our peer")
            self.conf.add(f'  if (proto = "{self.protocol_name(ipv)}") then {{')
            self.conf.add(type_lines)
            self.conf.add("  }")

        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _setup_peer_protocol(self, ipv: str) -> None:
        """Peer protocol setup for a single protocol."""

        # Get our source and neighbor addresses
        source_address = getattr(self, f"source_address{ipv}")
        neighbor = getattr(self, f"neighbor{ipv}")

        self.conf.add(f"protocol bgp {self.protocol_name(ipv)} {{")
        self.conf.add(f'  description "AS{self.asn} {self.name} - {self.description}";')

        self.conf.add("  local as BGP_ASN;")
        self.conf.add(f"  source address {source_address};")
        self.conf.add("  strict bind;")
        self.conf.add(f"  neighbor {neighbor} as {self.asn};")
        # Check if this is a passive peer
        if self.passive:
            self.conf.add("  passive;")

        # Add various tunables
        if self.connect_delay_time:
            self.conf.add(f"  connect delay time {self.connect_delay_time};")
        if self.connect_retry_time:
            self.conf.add(f"  connect retry time {self.connect_retry_time};")
        if self.error_wait_time:
            self.conf.add(f"  error wait time {self.error_wait_time};")
        if self.multihop:
            self.conf.add(f"  multihop {self.multihop};")
        if self.password:
            self.conf.add(f'  password "{self.password}";')

        # Handle route reflector clients
        if self.peer_type == "rrclient":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrclient
            if not self.bgp_attributes.rr_cluster_id:
                raise BirdPlanError("BGP route reflectors require a 'cluster_id' set if they have 'rrclient' peers")
            # Set this peer as a route reflector client
            self.conf.add("  rr client;")
            self.conf.add(f"  rr cluster id {self.bgp_attributes.rr_cluster_id};")

        # Handle route reflector server-to-server
        if self.peer_type == "rrserver-rrserver":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrserver-rrserver peer
            if not self.bgp_attributes.rr_cluster_id:
                raise BirdPlanError("BGP route reflectors require a 'cluster_id' if they have 'rrserver-rrserver' peers")
            # Set this peer as a route reflector client
            self.conf.add("  rr client;")
            self.conf.add(f"  rr cluster id {self.bgp_attributes.rr_cluster_id};")

        # Setup peer table
        self.conf.add(f"  ipv{ipv} {{")
        self.conf.add(f"    table {self.bgp_table_name(ipv)};")
        self.conf.add(f"    igp table master{ipv};")
        # Set the nexthop to ourselves for external peers
        if self.peer_type in ("customer", "peer", "transit", "routecollector", "routeserver"):
            self.conf.add("    next hop self;")
        # Setup import and export table so we can do soft reconfiguration
        self.conf.add("    import table;")
        self.conf.add("    export table;")
        # Setup prefix limit
        prefix_limit = getattr(self, f"prefix_limit{ipv}")
        if prefix_limit:
            self.conf.add(f"    import limit {prefix_limit} action restart;")
        # Setup filters
        self.conf.add(f"    import filter {self.filter_name_import(ipv)};")
        self.conf.add(f"    export filter {self.filter_name_export(ipv)};")
        self.conf.add("  };")
        self.conf.add("}")
        self.conf.add("")

    def _setup_peer_protocols(self) -> None:
        """Peer protocols setup."""
        if self.has_ipv4:
            self._setup_peer_protocol("4")
        if self.has_ipv6:
            self._setup_peer_protocol("6")

    def _setup_peer_to_bgp_filters(self) -> None:
        """Peer filters to the main BGP table."""
        # Setup peer to main BGP table export filter
        if self.has_ipv4:
            self._peer_to_bgp_export_filter("4")
        if self.has_ipv6:
            self._peer_to_bgp_export_filter("6")
        # Setup peer to main BGP table import filter
        if self.has_ipv4:
            self._peer_to_bgp_import_filter("4")
        if self.has_ipv6:
            self._peer_to_bgp_import_filter("6")

    def _setup_peer_filters(self) -> None:
        """Peer filter setup."""
        # Setup export filters
        if self.has_ipv4:
            self._peer_export_filter("4")
        if self.has_ipv6:
            self._peer_export_filter("6")

        # Setup import filters
        if self.has_ipv4:
            self._peer_import_filter("4")
        if self.has_ipv6:
            self._peer_import_filter("6")

    @property
    def bgp_attributes(self) -> BGPAttributes:
        """Return the BGP protocol attributes."""
        return self._bgp_attributes

    @property
    def peer_attributes(self) -> BGPPeerAttributes:
        """Return our attributes."""
        return self._peer_attributes

    @property
    def name(self) -> str:
        """Return our name."""
        return self.peer_attributes.name

    @name.setter
    def name(self, name: str) -> None:
        """Set our name."""
        self.peer_attributes.name = name

    @property
    def description(self) -> str:
        """Return our description."""
        return self.peer_attributes.description

    @description.setter
    def description(self, description: str) -> None:
        """Set our description."""
        self.peer_attributes.description = description

    @property
    def peer_type(self) -> str:
        """Return our type."""
        return self.peer_attributes.peer_type

    @peer_type.setter
    def peer_type(self, peer_type: str) -> None:
        """Set our peer_type."""
        self.peer_attributes.peer_type = peer_type

    @property
    def asn(self) -> int:
        """Return our ASN."""
        return self.peer_attributes.asn

    @asn.setter
    def asn(self, asn: int) -> None:
        """Set our asn."""
        self.peer_attributes.asn = asn

    @property
    def neighbor4(self) -> Optional[str]:
        """Return our IPv4 neighbor address."""
        return self.peer_attributes.neighbor4

    @neighbor4.setter
    def neighbor4(self, neighbor4: str) -> None:
        """Set our IPv4 neighbor address."""
        self.peer_attributes.neighbor4 = neighbor4

    @property
    def neighbor6(self) -> Optional[str]:
        """Return our IPv4 neighbor address."""
        return self.peer_attributes.neighbor6

    @neighbor6.setter
    def neighbor6(self, neighbor6: str) -> None:
        """Set our IPv4 neighbor address."""
        self.peer_attributes.neighbor6 = neighbor6

    @property
    def source_address4(self) -> Optional[str]:
        """Return our IPv4 source_address4 address."""
        return self.peer_attributes.source_address4

    @source_address4.setter
    def source_address4(self, source_address4: str) -> None:
        """Set our IPv4 source_address4 address."""
        self.peer_attributes.source_address4 = source_address4

    @property
    def source_address6(self) -> Optional[str]:
        """Return our IPv4 source_address6 address."""
        return self.peer_attributes.source_address6

    @source_address6.setter
    def source_address6(self, source_address6: str) -> None:
        """Set our IPv4 source_address6 address."""
        self.peer_attributes.source_address6 = source_address6

    @property
    def connect_delay_time(self) -> Optional[str]:
        """Return the value of our connect_delay_time option."""
        return self.peer_attributes.connect_delay_time

    @connect_delay_time.setter
    def connect_delay_time(self, connect_delay_time: str) -> None:
        """Set the value of our connect_delay_time option."""
        self.peer_attributes.connect_delay_time = connect_delay_time

    @property
    def connect_retry_time(self) -> Optional[str]:
        """Return the value of our connect_retry_time option."""
        return self.peer_attributes.connect_retry_time

    @connect_retry_time.setter
    def connect_retry_time(self, connect_retry_time: str) -> None:
        """Set the value of our connect_retry_time option."""
        self.peer_attributes.connect_retry_time = connect_retry_time

    @property
    def error_wait_time(self) -> Optional[str]:
        """Return the value of our error_wait_time option."""
        return self.peer_attributes.error_wait_time

    @error_wait_time.setter
    def error_wait_time(self, error_wait_time: str) -> None:
        """Set the value of our error_wait_time option."""
        self.peer_attributes.error_wait_time = error_wait_time

    @property
    def multihop(self) -> Optional[str]:
        """Return the value of our multihop option."""
        return self.peer_attributes.multihop

    @multihop.setter
    def multihop(self, multihop: str) -> None:
        """Set the value of our multihop option."""
        self.peer_attributes.multihop = multihop

    @property
    def password(self) -> Optional[str]:
        """Return the value of our password option."""
        return self.peer_attributes.password

    @password.setter
    def password(self, password: str) -> None:
        """Set the value of our password option."""
        self.peer_attributes.password = password

    @property
    def cost(self) -> int:
        """Return our prefix cost."""
        return self.peer_attributes.cost

    @cost.setter
    def cost(self, cost: int) -> None:
        """Set our prefix cost."""
        self.peer_attributes.cost = cost

    @property
    def graceful_shutdown(self) -> bool:
        """Return the value of graceful_shutdown."""
        return self.peer_attributes.graceful_shutdown

    @graceful_shutdown.setter
    def graceful_shutdown(self, graceful_shutdown: bool) -> None:
        """Set the value of graceful_shutdown."""
        self.peer_attributes.graceful_shutdown = graceful_shutdown

    @property
    def large_communities(self) -> BGPPeerLargeCommunities:
        """Return our large communities."""
        return self.peer_attributes.large_communities

    @property
    def passive(self) -> bool:
        """Return if we only accept connections, not make them."""
        return self.peer_attributes.passive

    @passive.setter
    def passive(self, passive: bool) -> None:
        """Set our passive mode."""
        self.peer_attributes.passive = passive

    @property
    def route_policy_redistribute(self) -> BGPPeerRoutePolicyRedistribute:
        """Return our route redistribute policy."""
        return self.peer_attributes.route_policy_redistribute

    @property
    def route_policy_accept(self) -> BGPPeerRoutePolicyAccept:
        """Return if we're accepting the default route or not."""
        return self.peer_attributes.route_policy_accept

    @property
    def filter_policy(self) -> BGPPeerFilterPolicy:
        """Return the our filter policy."""
        return self.peer_attributes.filter_policy

    @property
    def prefix_limit4(self) -> BGPPeerPrefixLimit:
        """Return our IPv4 prefix limit."""
        return self.peer_attributes.prefix_limit4

    @prefix_limit4.setter
    def prefix_limit4(self, prefix_limit4: str) -> None:
        """Set our IPv4 prefix limit."""
        self.peer_attributes.prefix_limit4 = prefix_limit4

    @property
    def prefix_limit6(self) -> BGPPeerPrefixLimit:
        """Return our IPv4 prefix limit."""
        return self.peer_attributes.prefix_limit6

    @prefix_limit6.setter
    def prefix_limit6(self, prefix_limit6: str) -> None:
        """Set our IPv6 prefix limit."""
        self.peer_attributes.prefix_limit6 = prefix_limit6

    @property
    def peeringdb(self) -> BGPPeerPeeringDB:
        """Return our peeringdb entry."""
        return self.peer_attributes.peeringdb

    #
    # Helper properties
    #

    @property
    def asn_list_name(self) -> str:
        """Return our ASN list name."""
        return f"bgp_AS{self.asn}_{self.name}_asns"

    @property
    def has_asn_filter(self) -> BGPPeerFilterItem:
        """Return if we filter on ASNs."""
        return self.filter_policy.asns or self.filter_policy.as_sets

    @property
    def has_ipv4(self) -> bool:
        """Return if we have IPv4."""
        return self.neighbor4 is not None

    @property
    def has_ipv6(self) -> bool:
        """Return if we have IPv6."""
        return self.neighbor6 is not None

    @property
    def has_prefix_filter(self) -> BGPPeerFilterItem:
        """Return if we filter on prefixes."""
        return self.filter_policy.prefixes or self.filter_policy.as_sets

    @property
    def quarantined(self) -> bool:
        """Return if we're quarantined."""
        return self.peer_attributes.quarantined

    @quarantined.setter
    def quarantined(self, quarantined: bool) -> None:
        """Set quarantined status."""
        self.peer_attributes.quarantined = quarantined
