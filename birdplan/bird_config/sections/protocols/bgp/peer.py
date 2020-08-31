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

from typing import Any, Dict, List, Optional, Union
import requests
from .bgp_attributes import BGPAttributes
from .typing import BGPPeerConfig
from ..pipe import ProtocolPipe
from ..base import SectionProtocolBase
from .... import util
from .....bgpq3 import BGPQ3
from .....exceptions import BirdPlanError


BGPPeerRedistributeItem = Union[bool, Dict]
BGPPeerRedistribute = Dict[str, BGPPeerRedistributeItem]
BGPPeerFilterItem = Union[str, List[str]]
BGPPeerFilter = Dict[str, BGPPeerFilterItem]
BGPPeerPeeringDB = Dict[str, Any]
BGPPeerPrefixLimit = Optional[str]


class ProtocolBGPPeer(SectionProtocolBase):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """BIRD BGP protocol peer configuration."""

    _bgp_attributes: BGPAttributes

    _name: str
    _description: str
    _type: str
    _asn: int

    _neighbor4: Optional[str]
    _neighbor6: Optional[str]
    _source_address4: Optional[str]
    _source_address6: Optional[str]

    _connect_delay_time: Optional[str]
    _connect_retry_time: Optional[str]
    _error_wait_time: Optional[str]
    _multihop: Optional[str]
    _password: Optional[str]

    _cost: int

    _incoming_large_communities: List[str]
    _outgoing_large_communities: List[str]

    _passive: bool

    _redistribute: BGPPeerRedistribute
    _accept: Dict[str, bool]
    _filter: BGPPeerFilter

    _peeringdb: Optional[BGPPeerPeeringDB]
    _prefix_limit4: BGPPeerPrefixLimit
    _prefix_limit6: BGPPeerPrefixLimit

    def __init__(
        self, bgp_attributes: BGPAttributes, peer_name: str, peer_config: BGPPeerConfig, **kwargs
    ):  # pylint: disable=too-many-branches,too-many-statements
        """Initialize the object."""
        super().__init__(**kwargs)

        # Check if we have a peer description
        if "description" not in peer_config:
            raise BirdPlanError("BGP peers need a 'description' field")
        self._description = peer_config["description"]

        # Check if we have a peer type
        if "type" not in peer_config:
            raise BirdPlanError("BGP peers need a 'type' field")
        self._type = peer_config["type"]

        # Check if we have a peer asn
        if "asn" not in peer_config:
            raise BirdPlanError("BGP peers need a 'asn' field")
        self._asn = peer_config["asn"]

        # Save the BGP protocol attributes
        self._bgp_attributes = bgp_attributes

        # Save our name and configuration
        self._name = peer_name
        # Dynamically set the section
        self._section = f"BGP Peer: {self.asn} - {self.name}"

        # Check for neighbor addresses
        self._neighbor4 = None
        self._neighbor6 = None
        if "neighbor4" in peer_config:
            self._neighbor4 = peer_config["neighbor4"]
        if "neighbor6" in peer_config:
            self._neighbor6 = peer_config["neighbor6"]
        # Check if we have a source address
        self._source_address4 = None
        self._source_address6 = None
        if "source_address4" in peer_config:
            self._source_address4 = peer_config["source_address4"]
        if "source_address6" in peer_config:
            self._source_address6 = peer_config["source_address6"]
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
        self._connect_delay_time = None
        self._connect_retry_time = None
        self._error_wait_time = None
        self._multihop = None
        self._password = None
        if "connect_delay_time" in peer_config:
            self._connect_delay_time = peer_config["connect_delay_time"]
        if "connect_retry_time" in peer_config:
            self._connect_retry_time = peer_config["connect_retry_time"]
        if "error_wait_time" in peer_config:
            self._error_wait_time = peer_config["error_wait_time"]
        if "multihop" in peer_config:
            self._multihop = peer_config["multihop"]
        if "password" in peer_config:
            self._password = peer_config["password"]

        self._cost = 0
        if "cost" in peer_config:
            self._cost = peer_config["cost"]

        # Check if we are adding a large community to outgoing routes
        self._incoming_large_communities = []
        if "incoming-large-communities" in peer_config:
            for large_community in sorted(peer_config["incoming-large-communities"]):
                self._incoming_large_communities.append(util.sanitize_large_community(large_community))
        # Check if we are adding a large community to outgoing routes
        self._outgoing_large_communities = []
        if "outgoing-large-communities" in peer_config:
            for large_community in sorted(peer_config["outgoing-large-communities"]):
                self._outgoing_large_communities.append(util.sanitize_large_community(large_community))

        # Turn on passive mode for route reflectors
        self._passive = False
        if self.type in ("customer", "rrclient"):
            self._passive = True

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
        if self.type in ("rrclient", "rrserver", "rrserver-rrserver"):
            self._redistribute["bgp"] = True
        # If this is an transit, peer, customer, routecollector or routeserver, we need to redistribute our own routes and
        # customer routes
        if self.type in ("customer", "routecollector", "routeserver", "peer", "transit"):
            self._redistribute["bgp_own"] = True
            self._redistribute["bgp_customer"] = True
        # If this is an customer, we need to redistribute peer and transit routes too
        if self.type == "customer":
            self._redistribute["bgp_peering"] = True
            self._redistribute["bgp_transit"] = True
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
                self._redistribute[redistribute_type] = redistribute_config

        # We don't have peeringdb info yet
        self._peeringdb = None
        self._prefix_limit4 = None
        self._prefix_limit6 = None
        # If the peer is a customer or peer, check if we have a prefix limit, if not add it from peeringdb
        # For routecollector and routeservers we filter, not block
        if self.type in ("customer", "peer"):
            if self.has_ipv4 and ("prefix_limit4" not in peer_config):
                self.prefix_limit4 = "peeringdb"
            if self.has_ipv6 and ("prefix_limit6" not in peer_config):
                self.prefix_limit6 = "peeringdb"
        # Work out the prefix limits...
        if self.has_ipv4 and self.prefix_limit4 and self.prefix_limit4 == "peeringdb":
            self.prefix_limit4 = self.peeringdb["info_prefixes4"]
        if self.has_ipv6 and self.prefix_limit6 and self.prefix_limit6 == "peeringdb":
            self.prefix_limit6 = self.peeringdb["info_prefixes6"]

        # Default to accepting nothing
        self._accept = {
            "default": False,
        }
        # Work out what we're going to be accepting
        if "accept" in peer_config:
            for accept_type, accept_config in peer_config["accept"].items():
                if accept_type != "default":
                    raise BirdPlanError(f"The BGP accept type '{accept_type}' is not known")
                self._accept[accept_type] = accept_config

        # Check for filters we need to setup
        self._filter = {"prefixes": [], "asns": [], "as_sets": []}
        if "filter" in peer_config:
            for filter_type, filter_config in peer_config["filter"].items():
                if filter_type not in ("prefixes", "asns", "as_sets"):
                    raise BirdPlanError(f"The BGP filter type '{filter_type}' is not known")
                self._filter[filter_type] = filter_config

        # Check if we're quarantined
        self._quarantined = False
        if "quarantine" in peer_config and peer_config["quarantine"]:
            self._quarantined = True

    def configure(self):
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
            birdconf_globals=self.birdconf_globals,
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

    def protocol_name(self, ipv: int) -> str:
        """Return the IP versioned protocol name."""
        return f"bgp{ipv}_AS{self.asn}_{self.name}"

    def bgp_table_name(self, ipv: int) -> str:
        """Return the IP versioned BGP table name."""
        return f"t_bgp{ipv}_AS{self.asn}_{self.name}_peer"

    def filter_name_export(self, ipv: int) -> str:
        """Return the IP versioned peer export filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_export"

    def filter_name_import(self, ipv: int) -> str:
        """Return the IP versioned peer import filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_import"

    def filter_name_export_bgp(self, ipv: int) -> str:
        """Return the IP versioned BGP export filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_bgp{ipv}_export"

    def filter_name_import_bgp(self, ipv: int) -> str:
        """Return the IP versioned BGP import filter name."""
        return f"f_bgp{ipv}_AS{self.asn}_{self.name}_peer_bgp{ipv}_import"

    def prefix_list_name(self, ipv: int) -> str:
        """Return our prefix list name."""
        return f"bgp{ipv}_AS{self.asn}_{self.name}_prefixes"

    def _setup_peer_tables(self):
        """Peering routing table setup."""
        self.tables.conf.append(f"# BGP Peer Tables: {self.asn} - {self.name}")
        if self.has_ipv4:
            self.tables.conf.append(f"ipv4 table {self.bgp_table_name(4)};")
        if self.has_ipv6:
            self.tables.conf.append(f"ipv6 table {self.bgp_table_name(6)};")
        self.tables.conf.append("")

    def _setup_peer_asns(self):
        """ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_asn_filter:
            return

        # Grab IRR prefixes
        irr_asns = []
        if self.filter_as_sets:
            bgpq3 = BGPQ3()
            irr_asns = bgpq3.get_asns([self.filter_as_sets])

        self.conf.add(f"define {self.asn_list_name} = [")
        asns = []
        # Add ASN list with comments
        if self.filter_asns:
            asns.append(f"# {len(self.filter_asns)} statically defined")
            for asn in self.filter_asns:
                asns.append(f"{asn}")
        if irr_asns:
            asns.append(f"# {len(irr_asns)} from IRR with object '{self.filter_as_sets}'")
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

    def _setup_peer_prefixes(self):
        """Prefix list setup."""
        # Short circuit and exit if we have none
        if not self.has_prefix_filter:
            return

        # Work out prefixes
        prefix_lists = {"4": [], "6": []}
        for prefix in sorted(self.filter_prefixes):
            if ":" in prefix:
                prefix_lists["4"].append(prefix)
            else:
                prefix_lists["6"].append(prefix)

        # Grab IRR prefixes
        irr_prefixes = {"ipv4": [], "ipv6": []}
        if self.filter_as_sets:
            bgpq3 = BGPQ3()
            irr_prefixes = bgpq3.get_prefixes([self.filter_as_sets])

        # Output prefix definitions
        for ipv in ["4", "6"]:
            self.conf.add(f"define {self.prefix_list_name(ipv)} = [")
            prefix_list = prefix_lists[ipv]
            prefix_list_irr = irr_prefixes[f"ipv{ipv}"]
            prefixes = []
            # Add statically defined prefix list
            if prefix_list:
                prefixes.append(f"# {len(prefix_list)} statically defined")
                prefixes.extend(prefix_list)
            # Add prefix list from IRR
            if prefix_list_irr:
                prefixes.append(f"# {len(prefix_list_irr)} from IRR with object '{self.filter_as_sets}'")
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

    def _add_redistribute_properties(self, redistribute: BGPPeerRedistributeItem):
        """Redistribution properties to add to the route."""
        if isinstance(redistribute, dict):
            if "redistribute-large-communities" in redistribute:
                for large_community in sorted(redistribute["redistribute-large-communities"]):
                    bird_lc = util.sanitize_large_community(large_community)
                    self.conf.add(f'    print "[redistribute-large-communities] Adding {bird_lc} to ", net;', debug=True)
                    self.conf.add(f"    bgp_large_community.add({bird_lc});")

    def _peer_to_bgp_export_filter(self, ipv: int):
        """Export filters into our main BGP routing table from the BGP peer table."""

        # Configure export filter to our main BGP table
        self.conf.add("# Export filter TO the main BGP table from the BGP peer table")
        self.conf.add(f"filter {self.filter_name_export_bgp((ipv))}")
        self.conf.add("int accept_route;")
        self.conf.add("{")
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

    def _peer_to_bgp_import_filter(self, ipv: int):  # pylint: disable=too-many-branches,too-many-statements
        """Import filter FROM the main BGP table to the BGP peer table."""

        # Configure import filter from our main BGP table
        self.conf.add("# Import filter FROM the main BGP table to the BGP peer table")
        self.conf.add(f"filter {self.filter_name_import_bgp((ipv))}")
        self.conf.add("int accept_route;")
        self.conf.add("{")
        self.conf.add("  accept_route = 0;")

        # Check that we have static routes imported first
        if self.redistribute_connected and not self.bgp_attributes.route_policy_import.connected:
            raise BirdPlanError("BGP needs connected routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.redistribute_kernel and not self.bgp_attributes.route_policy_import.kernel:
            raise BirdPlanError("BGP needs kernel routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.redistribute_static and not self.bgp_attributes.route_policy_import.static:
            raise BirdPlanError("BGP needs static routes to be imported before they can be redistributed to a peer")

        # Override exports if this is a customer peer and we don't export to customers
        if self.type == "customer":
            self.conf.add("  # Check for large community to prevent export to customers")
            self.conf.add("  if (BGP_LC_EXPORT_NOCUSTOMER ~ bgp_large_community) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOCUSTOMER";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Override exports if this is a peer, routecollector or routeserver and we don't export to peers
        if self.type in ("peer", "routecollector", "routeserver"):
            self.conf.add(f"  # Check for large community to prevent export to {self.type}")
            self.conf.add("  if (BGP_LC_EXPORT_NOPEER ~ bgp_large_community) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOPEER";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Override exports if this is a transit and we don't export to transits
        if self.type == "transit":
            self.conf.add("  # Check for large community to prevent export to transit")
            self.conf.add("  if (BGP_LC_EXPORT_NOTRANSIT ~ bgp_large_community) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOTRANSIT";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")

        # Redistribute connected
        if self.redistribute_connected:
            self.conf.add("  # Redistribute connected routes")
            self.conf.add("  if (source = RTS_DEVICE) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_DEVICE '
                '(redistribute connected)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_connected)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        else:
            self.conf.add("  # Do not redistribute connected routes")
            self.conf.add("  if (source = RTS_DEVICE) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on RTS_DEVICE '
                '(no redistribute connected)";',
                debug=True,
            )
            self.conf.add("    reject;")
            self.conf.add("  }")
        # Redistribute static routes
        if self.redistribute_static:
            self.conf.add("  # Redistribute static routes")
            self.conf.add(f'  if (proto = "static{ipv}") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on proto static{ipv} '
                '(redistribute static)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_static)
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
        if self.redistribute_kernel:
            self.conf.add("  # Redistribute kernel routes")
            self.conf.add("  if (source = RTS_INHERIT) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_INHERIT '
                '(redistribute kernel)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_kernel)
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
        if self.redistribute_originated:
            self.conf.add("  # Redistribute originated routes")
            self.conf.add(f'  if (proto = "bgp_originate{ipv}") then {{')
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on proto bgp_originate{ipv}'
                ' (redistribute originated)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_originated)
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
        if self.redistribute_default:
            # Make sure this is an allowed peer type for the default route to be exported
            if self.type not in ["customer", "rrclient", "rrserver", "rrserver-rrserver"]:
                raise BirdPlanError(f"Having 'redistribute[default]' as True for a '{self.type}' makes no sense")
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
        if self.redistribute_bgp:
            self.conf.add("  # Redistribute BGP routes (which is everything in our table)")
            self.conf.add("  if (source = RTS_BGP) then {")
            self.conf.add(
                f'    print "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_BGP";', debug=True
            )
            self._add_redistribute_properties(self.redistribute_bgp)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")

        # Redistribute our own BGP routes
        if self.redistribute_bgp_own:
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
            self._add_redistribute_properties(self.redistribute_bgp_own)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        # Redistribute customer BGP routes
        if self.redistribute_bgp_customer:
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
            self._add_redistribute_properties(self.redistribute_bgp_customer)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        # Redistribute peering BGP routes
        if self.redistribute_bgp_peering:
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
            self._add_redistribute_properties(self.redistribute_bgp_peering)
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
            self._add_redistribute_properties(self.redistribute_bgp_peering)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")
        # Redistribute transit BGP routes
        if self.redistribute_bgp_transit:
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
            self._add_redistribute_properties(self.redistribute_bgp_transit)
            self.conf.add("    accept_route = 1;")
            self.conf.add("  }")

        # Check if we're accepting the route...
        self.conf.add("  if (accept_route > 0) then {")
        # Do large community prepending if the peer is a customer, peer, routeserver or transit
        if self.type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we are adding a large community to outgoing routes
            for large_community in sorted(self.outgoing_large_communities):
                self.conf.add(
                    f'    print "[{self.filter_name_import_bgp((ipv))}] Adding LC {large_community} to ", net;', debug=True
                )
                self.conf.add(f"    bgp_large_community.add({large_community});")
            # Check if we're doing prepending
            self.conf.add("    # Do prepend if we have any LCs set")
            self.conf.add(f"    bgp_export_prepend({self.asn});")
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

    def _peer_export_filter(self, ipv: int):
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

    def _peer_import_filter(self, ipv: int):  # pylint: disable=too-many-branches,too-many-statements
        """Peer import filter setup from peer to peer table."""

        # Configure import filter from the BGP peer
        self.conf.add("# Import filter FROM the BGP peer TO the peer BGP table")
        self.conf.add(f"filter {self.filter_name_import(ipv)} {{")

        # If this is the route from our peer, we need to check what type it is
        type_lines = []

        # Clients
        if self.type == "customer":
            type_lines.append("    bgp_lc_remove_internal();")
            type_lines.append(f"    bgp_import_customer({self.asn}, {self.cost});")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'customer' makes no sense")
            type_lines.append(f"    bgp_filter_default_v{ipv}();")
            type_lines.append(f"    bgp_filter_bogons_v{ipv}();")
            type_lines.append(f"    bgp_filter_size_v{ipv}();")
            type_lines.append("    bgp_filter_asn_bogons();")
            type_lines.append("    bgp_filter_asn_long();")
            type_lines.append("    bgp_filter_asn_short();")
            type_lines.append("    bgp_filter_nexthop_not_peerip();")
            type_lines.append(f"    bgp_filter_asn_invalid({self.asn});")
            type_lines.append("    bgp_filter_asn_transit();")
        # Peers
        elif self.type == "peer":
            type_lines.append("    bgp_lc_remove_all();")
            type_lines.append(f"    bgp_import_peer({self.asn}, {self.cost});")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'peer' makes no sense")
            type_lines.append(f"    bgp_filter_default_v{ipv}();")
            type_lines.append(f"    bgp_filter_bogons_v{ipv}();")
            type_lines.append(f"    bgp_filter_size_v{ipv}();")
            type_lines.append("    bgp_filter_asn_bogons();")
            type_lines.append("    bgp_filter_asn_long();")
            type_lines.append("    bgp_filter_asn_short();")
            type_lines.append("    bgp_filter_nexthop_not_peerip();")
            type_lines.append(f"    bgp_filter_asn_invalid({self.asn});")
            type_lines.append("    bgp_filter_asn_transit();")
        # Routecollector
        elif self.type == "routecollector":
            type_lines.append("    bgp_lc_remove_all();")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'routecollector' makes no sense")
            type_lines.append("    bgp_filter_routecollector();")
        # Routeserver
        elif self.type == "routeserver":
            type_lines.append("    bgp_lc_remove_all();")
            type_lines.append(f"    bgp_import_routeserver({self.asn}, {self.cost});")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'routeserver' makes no sense")
            type_lines.append(f"    bgp_filter_default_v{ipv}();")
            type_lines.append(f"    bgp_filter_bogons_v{ipv}();")
            type_lines.append(f"    bgp_filter_size_v{ipv}();")
            type_lines.append("    bgp_filter_asn_bogons();")
            type_lines.append("    bgp_filter_asn_long();")
            type_lines.append("    bgp_filter_asn_short();")
            type_lines.append("    bgp_filter_asn_transit();")
        # Route reflector client
        elif self.type == "rrclient":
            if not self.accept_default:
                type_lines.append(f"    bgp_filter_default_v{ipv}();")
        # Route reflector server
        elif self.type == "rrserver":
            if not self.accept_default:
                type_lines.append(f"    bgp_filter_default_v{ipv}();")
        # Route reflector server to route reflector server
        elif self.type == "rrserver-rrserver":
            if not self.accept_default:
                type_lines.append(f"    bgp_filter_default_v{ipv}();")
        # Transit providers
        elif self.type == "transit":
            type_lines.append("    bgp_lc_remove_all();")
            type_lines.append(f"    bgp_import_transit({self.asn}, {self.cost});")
            if self.accept_default:
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
            type_lines.append("    bgp_filter_nexthop_not_peerip();")
            type_lines.append(f"    bgp_filter_asn_invalid({self.asn});")
        else:
            raise BirdPlanError(f"The BGP peer type '{self.type}' is not supported")

        # Check if we're filtering allowed ASNs
        if self.filter_asns:
            type_lines.append("    # Filter on the allowed ASNs")
            type_lines.append(f"    bgp_filter_asns({self.asn_list_name});")

        # Check if we're filtering allowed prefixes
        if self.filter_prefixes:
            type_lines.append("    # Filter on the allowed prefixes")
            type_lines.append(f"    bgp_filter_prefixes_v{ipv}({self.prefix_list_name(ipv)});")

        # Quarantine mode...
        if self.quarantined:
            type_lines.append("    bgp_filter_quarantine();")

        # Check if we are adding a large community to incoming routes
        for large_community in sorted(self.incoming_large_communities):
            if self.birdconf_globals.debug:
                type_lines.append(f'    print "[{self.filter_name_import(ipv)}] Adding LC {large_community} to ", net;')
            type_lines.append(f"    bgp_large_community.add({large_community});")

        # If we have lines from the above add them
        if type_lines:
            self.conf.add("  # Process routes from our peer")
            self.conf.add(f'  if (proto = "{self.protocol_name(ipv)}") then {{')
            self.conf.add(type_lines)
            self.conf.add("  }")

        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _setup_peer_protocol(self, ipv: int):
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
        if self.type == "rrclient":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrclient
            if not self.bgp_attributes.rr_cluster_id:
                raise BirdPlanError("BGP route reflectors require a 'cluster_id' set if they have 'rrclient' peers")
            # Set this peer as a route reflector client
            self.conf.add("  rr client;")
            self.conf.add(f"  rr cluster id {self.bgp_attributes.rr_cluster_id};")

        # Handle route reflector server-to-server
        if self.type == "rrserver-rrserver":
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
        # Setup import and export table so we can do soft reconfiguration
        self.conf.add("    import table;")
        self.conf.add("    export table;")
        # Setup prefix limit
        prefix_limit = getattr(self, f"prefix_limit{ipv}")
        if prefix_limit:
            self.conf.add(f"    import limit {prefix_limit};")
        # Setup filters
        self.conf.add(f"    import filter {self.filter_name_import(ipv)};")
        self.conf.add(f"    export filter {self.filter_name_export(ipv)};")
        self.conf.add("  };")
        self.conf.add("}")
        self.conf.add("")

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
    def bgp_attributes(self) -> BGPAttributes:
        """Return the BGP protocol attributes."""
        return self._bgp_attributes

    @property
    def name(self) -> str:
        """Return our name."""
        return self._name

    @property
    def description(self) -> str:
        """Return our description."""
        return self._description

    @property
    def type(self) -> str:
        """Return our type."""
        return self._type

    @property
    def asn(self) -> int:
        """Return our ASN."""
        return self._asn

    @property
    def neighbor4(self) -> Optional[str]:
        """Return our IPv4 neighbor address."""
        return self._neighbor4

    @property
    def neighbor6(self) -> Optional[str]:
        """Return our IPv6 neighbor address."""
        return self._neighbor6

    @property
    def source_address4(self) -> Optional[str]:
        """Return our IPv4 source address."""
        return self._source_address4

    @property
    def source_address6(self) -> Optional[str]:
        """Return our IPv6 source address."""
        return self._source_address6

    @property
    def connect_delay_time(self) -> Optional[str]:
        """Return the value of our connect_delay_time option."""
        return self._connect_delay_time

    @property
    def connect_retry_time(self) -> Optional[str]:
        """Return the value of our connect_retry_time option."""
        return self._connect_retry_time

    @property
    def error_wait_time(self) -> Optional[str]:
        """Return the value of our error_wait_time option."""
        return self._error_wait_time

    @property
    def multihop(self) -> Optional[str]:
        """Return the value of our multihop option."""
        return self._multihop

    @property
    def password(self) -> Optional[str]:
        """Return the value of our password option."""
        return self._password

    @property
    def cost(self) -> int:
        """Return our prefix cost."""
        return self._cost

    @property
    def incoming_large_communities(self) -> List[str]:
        """Return our incoming large communities."""
        return self._incoming_large_communities

    @property
    def outgoing_large_communities(self) -> List[str]:
        """Return our outgoing large communities."""
        return self._outgoing_large_communities

    @property
    def passive(self) -> bool:
        """Return if we only accept connections, not make them."""
        return self._passive

    @property
    def redistribute_default(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["default"] value."""
        return self._redistribute["default"]

    @property
    def redistribute_connected(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["connected"] value."""
        return self._redistribute["connected"]

    @property
    def redistribute_kernel(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["kernel"] value."""
        return self._redistribute["kernel"]

    @property
    def redistribute_static(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["static"] value."""
        return self._redistribute["static"]

    @property
    def redistribute_originated(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["originated"] value."""
        return self._redistribute["originated"]

    @property
    def redistribute_bgp(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["bgp"] value."""
        return self._redistribute["bgp"]

    @property
    def redistribute_bgp_own(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["bgp_own"] value."""
        return self._redistribute["bgp_own"]

    @property
    def redistribute_bgp_customer(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["bgp_customer"] value."""
        return self._redistribute["bgp_customer"]

    @property
    def redistribute_bgp_peering(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["bgp_peering"] value."""
        return self._redistribute["bgp_peering"]

    @property
    def redistribute_bgp_transit(self) -> BGPPeerRedistributeItem:
        """Return our redistribute["bgp_transit"] value."""
        return self._redistribute["bgp_transit"]

    @property
    def accept_default(self) -> bool:
        """Return if we're accepting the default route or not."""
        return self._accept["default"]

    @property
    def filter_asns(self) -> BGPPeerFilterItem:
        """Return the asns we filter on."""
        return self._filter["asns"]

    @property
    def filter_prefixes(self) -> BGPPeerFilterItem:
        """Return the prefixes we filter on."""
        return self._filter["prefixes"]

    @property
    def filter_as_sets(self) -> BGPPeerFilterItem:
        """Return the AS-SETs we filter on."""
        return self._filter["as_sets"]

    @property
    def peeringdb(self) -> BGPPeerPeeringDB:
        """Return our peeringdb entry, if there is one."""
        if self.asn > 64512 and self.asn < 65534:
            return {"info_prefixes4": None, "info_prefixes6": None}
        # If we don't having peerindb info, grab it
        if not self._peeringdb:
            self._peeringdb = requests.get(f"https://www.peeringdb.com/api/net?asn__in={self.asn}").json()["data"][0]
        # Check the result of peeringdb is not empty
        if not self._peeringdb:
            raise BirdPlanError("PeeringDB returned and empty result")
        # Lastly return it
        return self._peeringdb

    @property
    def prefix_limit4(self) -> BGPPeerPrefixLimit:
        """Return our IPv4 prefix limit."""
        return self._prefix_limit4

    @prefix_limit4.setter
    def prefix_limit4(self, prefix_limit4: str):
        """Set our IPv4 prefix limit."""
        self._prefix_limit4 = prefix_limit4

    @property
    def prefix_limit6(self) -> BGPPeerPrefixLimit:
        """Return our IPv4 prefix limit."""
        return self._prefix_limit6

    @prefix_limit6.setter
    def prefix_limit6(self, prefix_limit6: str):
        """Set our IPv6 prefix limit."""
        self._prefix_limit6 = prefix_limit6

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
        return self.filter_asns or self.filter_as_sets

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
        return self.filter_prefixes or self.filter_as_sets

    @property
    def quarantined(self) -> bool:
        """Return if we're quarantined."""
        return self._quarantined
