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
from ..pipe import BirdConfigProtocolPipe
from ...base import BirdConfigBase
from ... import util
from ....bgpq3 import BGPQ3
from ....exceptions import BirdPlanError


class BirdConfigProtocolBGPPeer(BirdConfigBase):
    """BIRD BGP protocol peer configuration."""

    _name: str
    _description: str
    _type: str
    _asn: str

    _neighbor4: Optional[str]
    _neighbor6: Optional[str]
    _source_address4: Optional[str]
    _source_address6: Optional[str]

    _connect_delay_time: Optional[str]
    _connect_retry_time: Optional[str]
    _error_wait_time: Optional[str]
    _multihop: Optional[str]
    _password: Optional[str]

    _prefix_list_name: str
    _asn_list_name: str

    _cost: int

    _incoming_large_communities: List[str]
    _outgoing_large_communities: List[str]

    _passive: bool

    _redistribute: Dict[str, Union[bool, Dict]]
    _accept: Dict[str, bool]
    _filter: Dict[str, Any]

    _peering_db: Optional[Dict[str, Any]]
    _prefix_limit4: Optional[str]
    _prefix_limit6: Optional[str]

    def __init__(self, parent: BirdConfigBase, peer_name: str, peer_config: Dict[str, Any], **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Save our name and configuration
        self._name = peer_name

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

        # Work out our prefix list name
        self._prefix_list_name = f"bgp_AS{self.asn}_{self.name}_prefixes"
        # Work out our ASN list name
        self._asn_list_name = f"bgp_AS{self.asn}_{self.name}_asns"

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
            if self.has_ipv4:
                if "prefix_limit4" not in peer_config:
                    self._prefix_limit4 = "peeringdb"
            if self.has_ipv6:
                if "prefix_limit6" not in peer_config:
                    self._prefix_limit6 = "peeringdb"
        # Work out the prefix limits...
        if self.has_ipv4:
            if self.prefix_limit4 and (self.prefix_limit4 == "peeringdb"):
                self._prefix_limit4 = self.peeringdb["info_prefixes4"]
        if self.has_ipv6:
            if self.prefix_limit6 and (self.prefix_limit6 == "peeringdb"):
                self._prefix_limit6 = self.peeringdb["info_prefixes6"]

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

        self._addline(f"# BGP Peer {self.name}")

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
            table_from=self.bgp_table_name,
            table_to="bgp",
            table_export_filtered=True,
            table_import_filtered=True,
            has_ipv4=self.has_ipv4,
            has_ipv6=self.has_ipv6,
        )
        bgp_peer_pipe.configure()

        # End of peer
        self._addline("")

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

    def _setup_peer_tables(self):
        """Peering routing table setup."""
        if self.has_ipv4:
            self._addline(f"ipv4 table {self.bgp_table_name(4)};")
        if self.has_ipv6:
            self._addline(f"ipv6 table {self.bgp_table_name(6)};")

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

        self._addline(f"define {self.asn_list_name} = [")
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
            self._addline("\t" + line)
        self._addline("];")

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
            self._addline(f"define {self.prefix_list_name}{ipv} = [")
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
        self._addline(f"filter {self.filter_name_export_bgp((ipv))}")
        self._addline("int accept_route;")
        self._addline("{")
        # Check if we're accepting the route...
        self._addline("\tif (bgp_large_community ~ [(BGP_ASN, BGP_LC_FUNCTION_FILTERED, *)]) then {")
        self._addline(f'\t\tprint "[{self.filter_name_export_bgp((ipv))}] Filtered ", net, " to main BGP table";', debug=True)
        self._addline("\t\treject;")
        self._addline("\t}")
        # Else reject
        self._addline(f'\tprint "[{self.filter_name_export_bgp((ipv))}] Exporting ", net, " to main BGP table";', debug=True)
        self._addline("\taccept;")
        self._addline("};")

    def _peer_to_bgp_import_filter(self, ipv):
        """Import filter FROM the main BGP table to the BGP peer table."""

        # Configure import filter from our main BGP table
        self._addline("# Import filter FROM the main BGP table to the BGP peer table")
        self._addline(f"filter {self.filter_name_import_bgp((ipv))}")
        self._addline("int accept_route;")
        self._addline("{")
        self._addline("\taccept_route = 0;")

        # Check that we have static routes imported first
        if self.redistribute_connected and not self.parent.import_connected:
            raise BirdPlanError("BGP needs connected routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.redistribute_kernel and not self.parent.import_kernel:
            raise BirdPlanError("BGP needs kernel routes to be imported before they can be redistributed to a peer")

        # Check that we have static routes imported first
        if self.redistribute_static and not self.parent.import_static:
            raise BirdPlanError("BGP needs static routes to be imported before they can be redistributed to a peer")

        # Override exports if this is a customer peer and we don't export to customers
        if self.type == "customer":
            self._addline("\t# Check for large community to prevent export to customers")
            self._addline("\tif (BGP_LC_EXPORT_NOCUSTOMER ~ bgp_large_community) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOCUSTOMER";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Override exports if this is a peer, routecollector or routeserver and we don't export to peers
        if self.type in ("peer", "routecollector", "routeserver"):
            self._addline(f"\t# Check for large community to prevent export to {self.type}")
            self._addline("\tif (BGP_LC_EXPORT_NOPEER ~ bgp_large_community) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOPEER";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Override exports if this is a transit and we don't export to transits
        if self.type == "transit":
            self._addline("\t# Check for large community to prevent export to transit")
            self._addline("\tif (BGP_LC_EXPORT_NOTRANSIT ~ bgp_large_community) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on BGP_LC_EXPORT_NOTRANSIT";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")

        # Redistribute connected
        if self.redistribute_connected:
            self._addline("\t# Redistribute connected routes")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_DEVICE '
                '(redistribute connected)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_connected)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute connected routes")
            self._addline("\tif (source = RTS_DEVICE) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on RTS_DEVICE '
                '(no redistribute connected)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute static routes
        if self.redistribute_static:
            self._addline("\t# Redistribute static routes")
            self._addline(f'\tif (proto = "static{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on proto static{ipv} '
                '(redistribute static)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_static)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute static routes")
            self._addline(f'\tif (proto = "static{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on proto static{ipv} '
                '(no redistribute static)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute kernel routes
        if self.redistribute_kernel:
            self._addline("\t# Redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_INHERIT '
                '(redistribute kernel)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_kernel)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute kernel routes")
            self._addline("\tif (source = RTS_INHERIT) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on RTS_INHERIT '
                '(no redistribute kernel)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")
        # Redistribute originated routes
        if self.redistribute_originated:
            self._addline("\t# Redistribute originated routes")
            self._addline(f'\tif (proto = "bgp_originate{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on proto bgp_originate{ipv}'
                ' (redistribute originated)";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_originated)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        else:
            self._addline("\t# Do not redistribute originated routes")
            self._addline(f'\tif (proto = "bgp_originate{ipv}") then {{')
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " due to match on proto bgp_originate{ipv}'
                ' (no redistribute originated)";',
                debug=True,
            )
            self._addline("\t\treject;")
            self._addline("\t}")

        # Do not redistribute the default route, no matter where we get it from
        if self.redistribute_default:
            # Make sure this is an allowed peer type for the default route to be exported
            if self.type not in ["customer", "rrclient", "rrserver", "rrserver-rrserver"]:
                raise BirdPlanError(f"Having 'redistribute[default]' as True for a '{self.type}' makes no sense")
            # Proceed with exporting...
            self._addline("\t# Accept the default route as we're redistributing, but only if, its been accepted above")
            self._addline(f"\tif (net = DEFAULT_ROUTE_V{ipv} && accept_route > 0) then {{")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting default route ", net, " due to match on '
                ' accept_route>0 (redistribute default)";',
                debug=True,
            )
            self._addline("\t\taccept;")
        # Else explicitly reject it
        else:
            self._addline("\t# Reject the default route as we are not redistributing it")
            self._addline(f"\tif (net = DEFAULT_ROUTE_V{ipv}) then {{")
            self._addline(f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting default route ", net, " export";')
            self._addline("\t\treject;")
        self._addline("\t}")

        # Redistribute BGP routes
        if self.redistribute_bgp:
            self._addline("\t# Redistribute BGP routes (which is everything in our table)")
            self._addline("\tif (source = RTS_BGP) then {")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on RTS_BGP";', debug=True
            )
            self._add_redistribute_properties(self.redistribute_bgp)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")

        # Redistribute our own BGP routes
        if self.redistribute_bgp_own:
            self._addline("\t# Redistribute our own BGP routes")
            self._addline("\tif (BGP_LC_RELATION_OWN ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on BGP_LC_RELATION_OWN";',
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on BGP_LC_RELATION_OWN";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_bgp_own)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute customer BGP routes
        if self.redistribute_bgp_customer:
            self._addline("\t# Redistribute customer BGP routes")
            self._addline("\tif (BGP_LC_RELATION_CUSTOMER ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on '
                'BGP_LC_RELATION_CUSTOMER";',
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on '
                'BGP_LC_RELATION_CUSTOMER";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_bgp_customer)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute peering BGP routes
        if self.redistribute_bgp_peering:
            self._addline("\t# Redistribute peering BGP routes")
            self._addline("\tif (BGP_LC_RELATION_PEER ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on BGP_LC_RELATION_PEER";',
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on BGP_LC_RELATION_PEER";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_bgp_peering)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
            self._addline("\tif (BGP_LC_RELATION_ROUTESERVER ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on '
                'BGP_LC_RELATION_ROUTESERVER";',
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on '
                'BGP_LC_RELATION_ROUTESERVER";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_bgp_peering)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")
        # Redistribute transit BGP routes
        if self.redistribute_bgp_transit:
            self._addline("\t# Redistribute transit BGP routes")
            self._addline("\tif (BGP_LC_RELATION_TRANSIT ~ bgp_large_community) then {")
            self._addline(f"\t\tif !bgp_can_export_v{ipv}({self.asn}) then {{")
            self._addline(
                f'\t\t\tprint "[{self.filter_name_import_bgp((ipv))}] Cannot export ", net, " with match on '
                'BGP_LC_RELATION_TRANSIT";',
                debug=True,
            )
            self._addline("\t\t\treject;")
            self._addline("\t\t}")
            self._addline(
                f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " due to match on '
                'BGP_LC_RELATION_TRANSIT";',
                debug=True,
            )
            self._add_redistribute_properties(self.redistribute_bgp_transit)
            self._addline("\t\taccept_route = 1;")
            self._addline("\t}")

        # Check if we're accepting the route...
        self._addline("\tif (accept_route > 0) then {")
        # Do large community prepending if the peer is a customer, peer, routeserver or transit
        if self.type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we are adding a large community to outgoing routes
            for large_community in sorted(self.outgoing_large_communities):
                self._addline(
                    f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Adding LC {large_community} to ", net;', debug=True
                )
                self._addline(f"\t\tbgp_large_community.add({large_community});")
            # Check if we're doing prepending
            self._addline("\t\t# Do prepend if we have any LCs set")
            self._addline(f"\t\tbgp_export_prepend({self.asn});")
        # Finally accept
        self._addline("\t\t# Finally accept")
        self._addline(f'\t\tprint "[{self.filter_name_import_bgp((ipv))}] Accepting ", net, " to peer";', debug=True)
        self._addline("\t\taccept;")
        self._addline("\t}")

        # By default reject all routes
        self._addline("\t# Reject by default")
        self._addline(f'\tprint "[{self.filter_name_import_bgp((ipv))}] Rejecting ", net, " to peer (fallthrough)";', debug=True)
        self._addline("\treject;")
        self._addline("};")

    def _peer_export_filter(self, ipv):
        """Peer export filter setup from peer table to peer."""

        # Configure export filter to the BGP peer
        self._addline("# Export filter TO the BGP peer from the peer BGP table")
        self._addline(f"filter {self.filter_name_export(ipv)}")
        self._addline("{")
        # Check if we're quarantined, if we are reject routes to the peer
        if self.quarantined:
            self._addline("\t# Peer is quarantined so reject exporting of routes")
            self._addline(f'\tprint "[{self.filter_name_export(ipv)}] Rejecting ", net, " to peer (quarantined)";', debug=True)
            self._addline("\treject;")
        # If we're not quarantined, then export routes
        else:
            self._addline("\t# We accept all routes going to the peer that are in the peer BGP table")
            self._addline(f'\tif (proto != "{self.protocol_name(ipv)}") then accept;')
        self._addline("};")

    def _peer_import_filter(self, ipv):
        """Peer import filter setup from peer to peer table."""

        # Configure import filter from the BGP peer
        self._addline("# Import filter FROM the BGP peer TO the peer BGP table")
        self._addline(f"filter {self.filter_name_import(ipv)} {{")

        # If this is the route from our peer, we need to check what type it is
        type_lines = []

        # Clients
        if self.type == "customer":
            type_lines.append("\t\tbgp_lc_remove_internal();")
            type_lines.append(f"\t\tbgp_import_customer({self.asn}, {self.cost});")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'customer' makes no sense")
            type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append(f"\t\tbgp_filter_asn_invalid({self.asn});")
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Peers
        elif self.type == "peer":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append(f"\t\tbgp_import_peer({self.asn}, {self.cost});")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'peer' makes no sense")
            type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append(f"\t\tbgp_filter_asn_invalid({self.asn});")
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Routecollector
        elif self.type == "routecollector":
            type_lines.append("\t\tbgp_lc_remove_all();")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'routecollector' makes no sense")
            type_lines.append("\t\tbgp_filter_routecollector();")
        # Routeserver
        elif self.type == "routeserver":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append(f"\t\tbgp_import_routeserver({self.asn}, {self.cost});")
            if self.accept_default:
                raise BirdPlanError("Having 'accept[default]' as True for a 'routeserver' makes no sense")
            type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_bogons_v{ipv}();")
            type_lines.append(f"\t\tbgp_filter_size_v{ipv}();")
            type_lines.append("\t\tbgp_filter_asn_short();")
            type_lines.append("\t\tbgp_filter_asn_transit();")
        # Route reflector client
        elif self.type == "rrclient":
            if not self.accept_default:
                type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
        # Route reflector server
        elif self.type == "rrserver":
            if not self.accept_default:
                type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
        # Route reflector server to route reflector server
        elif self.type == "rrserver-rrserver":
            if not self.accept_default:
                type_lines.append(f"\t\tbgp_filter_default_v{ipv}();")
        # Transit providers
        elif self.type == "transit":
            type_lines.append("\t\tbgp_lc_remove_all();")
            type_lines.append(f"\t\tbgp_import_transit({self.asn}, {self.cost});")
            if self.accept_default:
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
            type_lines.append(f"\t\tbgp_filter_asn_invalid({self.asn});")
        else:
            raise BirdPlanError(f"The BGP peer type '{self.type}' is not supported")

        # Check if we're filtering allowed ASNs
        if self.filter_asns:
            type_lines.append("\t\t# Filter on the allowed ASNs")
            type_lines.append(f"\t\tbgp_filter_asns({self.asn_list_name});")

        # Check if we're filtering allowed prefixes
        if self.filter_prefixes:
            type_lines.append("\t\t# Filter on the allowed prefixes")
            type_lines.append(f"\t\tbgp_filter_prefixes_v{ipv}({self.prefix_list_name}{ipv});")

        # Quarantine mode...
        if self.quarantined:
            type_lines.append("\t\tbgp_filter_quarantine();")

        # Check if we are adding a large community to incoming routes
        for large_community in sorted(self.incoming_large_communities):
            if self.root.debug:
                type_lines.append(f'\t\tprint "[{self.filter_name_import(ipv)}] Adding LC {large_community} to ", net;')
            type_lines.append(f"\t\tbgp_large_community.add({large_community});")

        # If we have lines from the above add them
        if type_lines:
            self._addline("\t# Process routes from our peer")
            self._addline(f'\tif (proto = "{self.protocol_name(ipv)}") then {{')
            self._addlines(type_lines)
            self._addline("\t}")

        self._addline("\taccept;")
        self._addline("};")

    def _setup_peer_protocol(self, ipv):
        """Peer protocol setup for a single protocol."""

        # Get our source and neighbor addresses
        source_address = getattr(self, f"source_address{ipv}")
        neighbor = getattr(self, f"neighbor{ipv}")

        self._addline(f"protocol bgp {self.protocol_name(ipv)} {{")
        self._addline(f'\tdescription "AS{self.asn} {self.name} - {self.description}";')

        self._addline("\tlocal as BGP_ASN;")
        self._addline(f"\tsource address {source_address};")
        self._addline("\tstrict bind;")
        self._addline(f"\tneighbor {neighbor} as {self.asn};")
        # Check if this is a passive peer
        if self.passive:
            self._addline("\tpassive;")

        # Add various tunables
        if self.connect_delay_time:
            self._addline(f"\tconnect delay time {self.connect_delay_time};")
        if self.connect_retry_time:
            self._addline(f"\tconnect retry time {self.connect_retry_time};")
        if self.error_wait_time:
            self._addline(f"\terror wait time {self.error_wait_time};")
        if self.multihop:
            self._addline(f"\tmultihop {self.multihop};")
        if self.password:
            self._addline(f'\tpassword "{self.password}";')

        # Handle route reflector clients
        if self.type == "rrclient":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrclient
            if not self.parent.rr_cluster_id:
                raise BirdPlanError("BGP route reflectors require a 'cluster_id' set if they have 'rrclient' peers")
            # Set this peer as a route reflector client
            self._addline("\trr client;")
            self._addline(f"\trr cluster id {self.parent.rr_cluster_id};")

        # Handle route reflector server-to-server
        if self.type == "rrserver-rrserver":
            # First of all check if we have a route reflector cluster ID, we need one to have a rrserver-rrserver peer
            if not self.parent.rr_cluster_id:
                raise BirdPlanError("BGP route reflectors require a 'cluster_id' if they have 'rrserver-rrserver' peers")
            # Set this peer as a route reflector client
            self._addline("\trr client;")
            self._addline(f"\trr cluster id {self.parent.rr_cluster_id};")

        # Setup peer table
        self._addline(f"\tipv{ipv} {{")
        self._addline(f"\t\ttable {self.bgp_table_name(ipv)};")
        self._addline(f"\t\tigp table master{ipv};")
        # Setup import and export table so we can do soft reconfiguration
        self._addline("\t\timport table;")
        self._addline("\t\texport table;")
        # Setup prefix limit
        prefix_limit = getattr(self, f"prefix_limit{ipv}")
        if prefix_limit:
            self._addline(f"\t\timport limit {prefix_limit};")
        # Setup filters
        self._addline(f"\t\timport filter {self.filter_name_import(ipv)};")
        self._addline(f"\t\texport filter {self.filter_name_export(ipv)};")
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
    def asn(self) -> str:
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
    def prefix_list_name(self):
        """Return our prefix list name."""
        return self._prefix_list_name

    @property
    def asn_list_name(self):
        """Return our ASN list name."""
        return self._asn_list_name

    @property
    def cost(self) -> int:
        """Return our prefix cost."""
        return self._cost

    @property
    def incoming_large_communities(self):
        """Return our incoming large communities."""
        return self._incoming_large_communities

    @property
    def outgoing_large_communities(self):
        """Return our outgoing large communities."""
        return self._outgoing_large_communities

    @property
    def passive(self):
        """Return if we only accept connections, not make them."""
        return self._passive

    @property
    def redistribute_default(self) -> Union[bool, Dict]:
        """Return our redistribute["default"] value."""
        return self._redistribute["default"]

    @property
    def redistribute_connected(self) -> Union[bool, Dict]:
        """Return our redistribute["connected"] value."""
        return self._redistribute["connected"]

    @property
    def redistribute_kernel(self) -> Union[bool, Dict]:
        """Return our redistribute["kernel"] value."""
        return self._redistribute["kernel"]

    @property
    def redistribute_static(self) -> Union[bool, Dict]:
        """Return our redistribute["static"] value."""
        return self._redistribute["static"]

    @property
    def redistribute_originated(self) -> Union[bool, Dict]:
        """Return our redistribute["originated"] value."""
        return self._redistribute["originated"]

    @property
    def redistribute_bgp(self) -> Union[bool, Dict]:
        """Return our redistribute["bgp"] value."""
        return self._redistribute["bgp"]

    @property
    def redistribute_bgp_own(self) -> Union[bool, Dict]:
        """Return our redistribute["bgp_own"] value."""
        return self._redistribute["bgp_own"]

    @property
    def redistribute_bgp_customer(self) -> Union[bool, Dict]:
        """Return our redistribute["bgp_customer"] value."""
        return self._redistribute["bgp_customer"]

    @property
    def redistribute_bgp_peering(self) -> Union[bool, Dict]:
        """Return our redistribute["bgp_peering"] value."""
        return self._redistribute["bgp_peering"]

    @property
    def redistribute_bgp_transit(self) -> Union[bool, Dict]:
        """Return our redistribute["bgp_transit"] value."""
        return self._redistribute["bgp_transit"]

    @property
    def accept_default(self) -> bool:
        """Return if we're accepting the default route or not."""
        return self._accept["default"]

    @property
    def filter_asns(self) -> List[str]:
        """Return the asns we filter on."""
        return self._filter["asns"]

    @property
    def filter_prefixes(self):
        """Return the prefixes we filter on."""
        return self._filter["prefixes"]

    @property
    def filter_as_sets(self):
        """Return the AS-SETs we filter on."""
        return self._filter["as_sets"]

    @property
    def peeringdb(self):
        """Return our peeringdb entry, if there is one."""
        if self.asn > 64512 and self.asn < 65534:
            return {"info_prefixes4": None, "info_prefixes6": None}
        # If we don't having peerindb info, grab it
        if not self._peeringdb:
            self._peeringdb = requests.get("https://www.peeringdb.com/api/net?asn__in=%s" % self.asn).json()["data"][0]
        # Lastly return it
        return self._peeringdb

    @property
    def prefix_limit4(self) -> Optional[str]:
        """Return our IPv4 prefix limit."""
        return self._prefix_limit4

    @property
    def prefix_limit6(self) -> Optional[str]:
        """Return our IPv4 prefix limit."""
        return self._prefix_limit6

    #
    # Helper properties
    #

    @property
    def has_asn_filter(self):
        """Return if we filter on ASNs."""
        return self.filter_asns or self.filter_as_sets

    @property
    def has_ipv4(self):
        """Return if we have IPv4."""
        return self.neighbor4 is not None

    @property
    def has_ipv6(self):
        """Return if we have IPv6."""
        return self.neighbor6 is not None

    @property
    def has_prefix_filter(self):
        """Return if we filter on prefixes."""
        return self.filter_prefixes or self.filter_as_sets

    @property
    def quarantined(self) -> bool:
        """Return if we're quarantined."""
        return self._quarantined
