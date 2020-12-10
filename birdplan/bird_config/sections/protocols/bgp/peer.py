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

from typing import Dict, List, Optional, Union

from .bgp_attributes import BGPAttributes
from .bgp_functions import BGPFunctions
from .peer_attributes import (
    BGPPeerAttributes,
    BGPPeerFilterPolicy,
    BGPPeerFilterItem,
    BGPPeerLargeCommunities,
    BGPPeerLocation,
    BGPPeerPeeringDB,
    BGPPeerPrefixLimit,
    BGPPeerPrepend,
    BGPPeerRoutePolicyAccept,
    BGPPeerRoutePolicyRedistribute,
)
from .typing import BGPPeerConfig
from ..pipe import ProtocolPipe, ProtocolPipeFilterType
from ..base import SectionProtocolBase
from ...constants import SectionConstants
from ...functions import BirdVariable, SectionFunctions
from ...tables import SectionTables
from .... import util
from ....globals import BirdConfigGlobals
from .....bgpq3 import BGPQ3
from .....exceptions import BirdPlanError


class ProtocolBGPPeer(SectionProtocolBase):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """BIRD BGP protocol peer configuration."""

    _bgp_attributes: BGPAttributes
    _bgp_functions: BGPFunctions
    _peer_attributes: BGPPeerAttributes

    def __init__(
        self,
        birdconfig_globals: BirdConfigGlobals,
        constants: SectionConstants,
        functions: SectionFunctions,
        tables: SectionTables,
        bgp_attributes: BGPAttributes,
        bgp_functions: BGPFunctions,
        peer_name: str,
        peer_config: BGPPeerConfig,
    ):  # pylint: disable=too-many-branches,too-many-statements,too-many-arguments
        """Initialize the object."""
        super().__init__(birdconfig_globals, constants, functions, tables)

        # Initialize our attributes
        self._bgp_attributes = bgp_attributes
        self._bgp_functions = bgp_functions
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
        # Make sure it is valid
        if self.peer_type not in (
            "customer",
            "internal",
            "peer",
            "routecollector",
            "routeserver",
            "rrclient",
            "rrserver",
            "rrserver-rrserver",
            "transit",
        ):
            raise BirdPlanError(f"The BGP peer type '{self.peer_type}' is not supported")

        # First of all check if we have a route reflector cluster ID, we need one to have a rrclient
        if self.peer_type in ("rrclient", "rrserver-rrserver") and not self.bgp_attributes.rr_cluster_id:
            raise BirdPlanError(f"The BGP peer type '{self.peer_type}' requires a BGP 'cluster_id' options to be specified")

        # Check if we have a peer asn
        if "asn" not in peer_config:
            raise BirdPlanError(f"BGP peer '{self.name}' need a 'asn' field")
        self.asn = peer_config["asn"]

        # Check if we're replacing the ASN in the AS-PATH
        if "replace_aspath" in peer_config:
            # Do a sanity check on replacing the ASN
            if self.peer_type not in ("customer", "internal"):
                raise BirdPlanError(
                    f"Having 'replace_aspath' set for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            # Make sure the ASN is private and not public
            if self.birdconfig_globals.test_mode:
                # In test mode the only private ASN range is 4294900001 to 4294967294
                if not (self.asn >= 4200000000 and self.asn <= 4294900000):
                    raise BirdPlanError(
                        f"Having 'replace_aspath' set for peer '{self.name}' with a non-private ASN {self.asn} makes no sense"
                    )
            # We're not in test mode...
            else:
                # Make sure we're within the full set of private ASN ranges
                if not ((self.asn >= 64512 and self.asn <= 65534) or (self.asn >= 4200000000 and self.asn <= 4294967294)):
                    raise BirdPlanError(
                        f"Having 'replace_aspath' set for peer '{self.name}' with a non-private ASN {self.asn} makes no sense"
                    )
            # Check if we're actually replacing it?
            if peer_config["replace_aspath"]:
                self.replace_aspath = True
                self.prefix_import_minlen4 = 16
                self.prefix_import_maxlen4 = 29
                self.prefix_export_minlen4 = 16
                self.prefix_export_maxlen4 = 29
                self.prefix_import_maxlen6 = 64
                self.prefix_import_minlen6 = 32
                self.prefix_export_maxlen6 = 64
                self.prefix_export_minlen6 = 32

        # If the peer type is of internal nature, but doesn't match our peer type, throw an exception
        if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.asn != self.bgp_attributes.asn and not (self.peer_type == "internal" and self.replace_aspath):
                raise BirdPlanError(
                    f"BGP peer '{self.name}' ({self.asn}) is of internal nature, "
                    f"but has a different ASN ({self.bgp_attributes.asn})"
                )

        # Setup the peer location
        if "location" in peer_config:
            # Make sure the peer type configuration is valid for the specification of the peer location
            if self.peer_type not in ("customer", "peer", "routeserver", "routecollector", "transit"):
                raise BirdPlanError(
                    f"BGP peer '{self.name}' has 'location' configuration but it makes no sense for peer type '{self.peer_type}'"
                )
            # Check for our ISO-3166 location
            if "iso3166" in peer_config["location"]:
                self.location.iso3166 = peer_config["location"]["iso3166"]
            # Check for our UN.M49 location
            if "unm49" in peer_config["location"]:
                self.location.unm49 = peer_config["location"]["unm49"]

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
            if self.peer_type not in ("customer", "peer", "routeserver", "transit"):
                raise BirdPlanError(f"Having 'cost' specified for peer '{self.name}' with type '{self.peer_type}' makes no sense")
            self.cost = peer_config["cost"]

        # Check if we're in graceful_shutdown mode
        if self.bgp_attributes.graceful_shutdown:
            self.graceful_shutdown = True
        if "graceful_shutdown" in peer_config:
            self.graceful_shutdown = peer_config["graceful_shutdown"]

        # Check if we are adding a large community to outgoing routes
        if "incoming_large_communities" in peer_config:
            # Raise an exception if incoming large communities makes no sense for this peer type
            if self.peer_type == "routecollector":
                raise BirdPlanError(
                    f"Having 'incoming_large_communities' set for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            # Add incoming large communities
            for large_community in sorted(peer_config["incoming_large_communities"]):
                self.large_communities.incoming.append(util.sanitize_community(large_community))
        # Check if we are adding large communities to outgoing routes
        if "outgoing_large_communities" in peer_config:
            # Add outgoing large community configuration
            if isinstance(peer_config["outgoing_large_communities"], dict):
                for large_community_type, large_community_config in peer_config["outgoing_large_communities"].items():
                    if large_community_type not in (
                        "default",
                        "connected",
                        "kernel",
                        "kernel_blackhole",
                        "static",
                        "static_blackhole",
                        "originated",
                        "bgp",
                        "bgp_own",
                        "bgp_customer",
                        "bgp_peering",
                        "bgp_transit",
                    ):
                        raise BirdPlanError(
                            f"BGP peer 'outgoing_large_community' configuration '{large_community_type}' for peer '{self.name}' "
                            f"with type '{self.peer_type}' is invalid"
                        )
                    # Check that we're not doing something stupid
                    if self.peer_type in ("peer", "routecollector", "routeserver", "transit") and large_community_type in (
                        "default",
                        "bgp_peering",
                        "bgp_transit",
                    ):
                        raise BirdPlanError(
                            f"Having 'outgoing_large_communities:{large_community_type}' specified for peer '{self.name}' "
                            f"with type '{self.peer_type}' makes no sense"
                        )
                    if self.peer_type not in (
                        "internal",
                        "routeserver",
                        "routecollector",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        if large_community_type in ("kernel_blackhole", "static_blackhole"):
                            raise BirdPlanError(
                                f"Having 'outgoing_large_communities:{large_community_type}' specified for peer '{self.name}' "
                                f"with type '{self.peer_type}' makes no sense"
                            )
                    # Grab the large community attribute
                    large_community_attr = getattr(self.large_communities.outgoing, large_community_type)
                    # Then append them...
                    for large_community in sorted(large_community_config):
                        large_community_attr.append(util.sanitize_community(large_community))
            # If its just a number set the count
            else:
                for large_community in sorted(peer_config["outgoing_large_communities"]):
                    self.large_communities.outgoing.bgp.append(util.sanitize_community(large_community))

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
                    "kernel",
                    "kernel_blackhole",
                    "static",
                    "static_blackhole",
                    "originated",
                    "bgp",
                    "bgp_own",
                    "bgp_customer",
                    "bgp_peering",
                    "bgp_transit",
                ):
                    raise BirdPlanError(f"The BGP redistribute type '{redistribute_type}' is not known")
                setattr(self.route_policy_redistribute, redistribute_type, redistribute_config)
        # Do a sanity check on our redistribution
        if self.peer_type in ("peer", "routecollector", "routeserver", "transit"):
            # Check things we are not supposed to be redistributing to external peers
            if self.route_policy_redistribute.default:
                raise BirdPlanError(
                    f"Having 'redistribute:default' set to True for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            if self.route_policy_redistribute.bgp:
                raise BirdPlanError(
                    f"Having 'redistribute:bgp' set to True for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            if self.route_policy_redistribute.bgp_peering:
                raise BirdPlanError(
                    f"Having 'redistribute:bgp_peering' set to True for peer '{self.name}' "
                    f"with type '{self.peer_type}' makes no sense"
                )
            if self.route_policy_redistribute.bgp_transit:
                raise BirdPlanError(
                    f"Having 'redistribute:bgp_transit' set to True for peer '{self.name}' "
                    f"with type '{self.peer_type}' makes no sense"
                )
        if self.peer_type not in (
            "internal",
            "routeserver",
            "routecollector",
            "rrclient",
            "rrserver",
            "rrserver-rrserver",
            "transit",
        ):
            if self.route_policy_redistribute.kernel_blackhole:
                raise BirdPlanError(
                    f"Having 'redistribute:kernel_blackhole' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "makes no sense"
                )
            if self.route_policy_redistribute.static_blackhole:
                raise BirdPlanError(
                    f"Having 'redistribute:static_blackhole' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "makes no sense"
                )
        # Check that we have static routes imported first
        if self.route_policy_redistribute.connected and not self.bgp_attributes.route_policy_import.connected:
            raise BirdPlanError(f"BGP needs connected routes to be imported before they can be redistributed to peer '{self.name}'")

        # Check that we have static routes imported first
        if self.route_policy_redistribute.kernel and not self.bgp_attributes.route_policy_import.kernel:
            raise BirdPlanError(f"BGP needs kernel routes to be imported before they can be redistributed to peer '{self.name}'")

        # Check that we have static routes imported first
        if self.route_policy_redistribute.static and not self.bgp_attributes.route_policy_import.static:
            raise BirdPlanError(f"BGP needs static routes to be imported before they can be redistributed to peer '{self.name}'")

        # If the peer is a customer or peer, check if we have a prefix limit, if not add it from peeringdb
        if self.peer_type in ("customer", "peer"):
            if self.has_ipv4 and ("prefix_limit4" not in peer_config):
                self.prefix_limit4 = "peeringdb"
            if self.has_ipv6 and ("prefix_limit6" not in peer_config):
                self.prefix_limit6 = "peeringdb"
        # Check for peer config, this should override the above
        if self.has_ipv4 and "prefix_limit4" in peer_config:
            # Having a prefix limit set for anything other than these peer types
            if self.peer_type not in ("customer", "peer"):
                raise BirdPlanError(
                    f"Having 'prefix_limit4' set for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            self.prefix_limit4 = peer_config["prefix_limit4"]
        if self.has_ipv6 and "prefix_limit6" in peer_config:
            # Having a prefix limit set for anything other than these peer types
            if self.peer_type not in ("customer", "peer"):
                raise BirdPlanError(
                    f"Having 'prefix_limit6' set for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            self.prefix_limit6 = peer_config["prefix_limit6"]
        # Work out the prefix limits...
        if self.has_ipv4 and self.prefix_limit4 and self.prefix_limit4 == "peeringdb":
            self.prefix_limit4 = self.peeringdb["info_prefixes4"]
        if self.has_ipv6 and self.prefix_limit6 and self.prefix_limit6 == "peeringdb":
            self.prefix_limit6 = self.peeringdb["info_prefixes6"]

        # Check for filters we need to setup
        if "filter" in peer_config:
            # Raise an exception if filters makes no sense for this peer type
            if self.peer_type == "routecollector":
                raise BirdPlanError(f"Having 'filter' specified for peer '{self.name}' with type '{self.peer_type}' makes no sense")
            # Add filters
            for filter_type, filter_config in peer_config["filter"].items():
                if filter_type not in ("prefixes", "origin_asns", "peer_asns", "as_sets"):
                    raise BirdPlanError(
                        f"BGP peer 'filter' configuration '{filter_type}' for peer '{self.name}' with type '{self.peer_type}' "
                        "is invalid"
                    )
                # Set filter policy
                setattr(self.filter_policy, filter_type, filter_config)

        # Check if we should be enabling blackholing by default
        if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver") or (
            self.peer_type == "customer" and self.filter_policy.prefixes
        ):
            self.route_policy_accept.blackhole = True

        # If this is a rrserver to rrserver peer, we need to by default redistribute the default route (if we have one)
        if self.peer_type == "rrserver-rrserver":
            self.route_policy_accept.default = True
        # Work out what we're going to be accepting
        if "accept" in peer_config:
            for accept_type, accept_config in peer_config["accept"].items():
                if accept_type not in ("default", "blackhole"):
                    raise BirdPlanError(
                        f"BGP peer 'accept' configuration '{accept_type}' for peer '{self.name}' with type '{self.peer_type}' "
                        " is invalid"
                    )
                # Set route policy accept
                setattr(self.route_policy_accept, accept_type, accept_config)

        # Check accept default is valid
        if self.peer_type not in (
            "internal",
            "rrclient",
            "rrserver",
            "rrserver-rrserver",
            "transit",
        ):
            if self.route_policy_accept.default:
                raise BirdPlanError(
                    f"Having 'accept:default' set to True for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )

        # Check if blackholing can be enabled for this peer type
        if self.peer_type not in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.route_policy_accept.blackhole:
                raise BirdPlanError(
                    f"Having 'accept:blackhole' set to True for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )

        # Check if this is a customer with blackholing and without a prefix filter set
        if self.peer_type == "customer":
            if self.route_policy_accept.blackhole and not self.filter_policy.prefixes:
                raise BirdPlanError(
                    f"Having 'accept:blackhole' set to True for peer '{self.name}' with type '{self.peer_type}' and without "
                    "'filter:prefixes' set makes no sense"
                )

        # Check for prepending we need to setup
        if "prepend" in peer_config:
            # Add prepending configuration
            if isinstance(peer_config["prepend"], dict):
                for prepend_type, prepend_config in peer_config["prepend"].items():
                    if prepend_type not in (
                        "default",
                        "connected",
                        "kernel",
                        "kernel_blackhole",
                        "static",
                        "static_blackhole",
                        "originated",
                        "bgp",
                        "bgp_own",
                        "bgp_customer",
                        "bgp_peering",
                        "bgp_transit",
                    ):
                        raise BirdPlanError(
                            f"BGP peer 'prepend' configuration '{prepend_type}' for peer '{self.name}' with type "
                            f"'{self.peer_type}' is invalid"
                        )
                    # Check that we're not doing something stupid
                    if self.peer_type in ("peer", "routecollector", "routeserver", "transit"):
                        if prepend_type in ("default", "bgp_peering", "bgp_transit"):
                            raise BirdPlanError(
                                f"Having 'prepend:{prepend_type}' specified for peer '{self.name}' with type '{self.peer_type}' "
                                "makes no sense"
                            )
                    if self.peer_type not in (
                        "internal",
                        "routeserver",
                        "routecollector",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        if prepend_type in ("kernel_blackhole", "static_blackhole"):
                            raise BirdPlanError(
                                f"Having 'prepend:{prepend_type}' specified for peer '{self.name}' with type '{self.peer_type}' "
                                "makes no sense"
                            )
                    # Grab the prepend attribute
                    prepend_attr = getattr(self.prepend, prepend_type)
                    # Set prepend count
                    setattr(prepend_attr, "own_asn", prepend_config)
            # If its just a number set the count
            else:
                self.prepend.bgp.own_asn = peer_config["prepend"]

        # Check if we're quarantined
        if "quarantine" in peer_config and peer_config["quarantine"]:
            self.quarantined = True

        # Check if we have a blackhole community
        if "blackhole_community" in peer_config:
            if self.peer_type not in ("routeserver", "routecollector", "transit"):
                raise BirdPlanError(
                    f"Having 'blackhole_community' specified for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            # List of communities to add...
            communities = []
            # Check if this is a plain string community
            if isinstance(peer_config["blackhole_community"], str):
                communities.append(peer_config["blackhole_community"])
            # Check if this is a list of communities
            elif isinstance(peer_config["blackhole_community"], list):
                communities.extend(peer_config["blackhole_community"])
            # Finally if this is not a boolean, then its unsupported
            elif isinstance(peer_config["blackhole_community"], bool):
                self.blackhole_community = peer_config["blackhole_community"]
            else:
                raise BirdPlanError(
                    f"Option 'blackhole_community' specified for peer '{self.name}' with type '{self.peer_type}' "
                    f"has an invalid type"
                )
            # If we have communities, this can be a list or a single item in the list
            if communities:
                # Initialize our configuration list
                self.blackhole_community = []
                # Loop with each community
                for community in communities:
                    # Check how many :'s we have
                    component_count = community.count(":")
                    if component_count < 1 or component_count > 2:
                        raise BirdPlanError(
                            f"Option 'blackhole_community' specified for peer '{self.name}' with type '{self.peer_type}' "
                            f"has an invalid value '{community}'"
                        )
                    # Add to our configuration
                    self.blackhole_community.append(util.sanitize_community(community))

        # Setup our limits
        for attr_name in (
            "blackhole_import_maxlen4",
            "blackhole_import_minlen4",
            "blackhole_export_maxlen4",
            "blackhole_export_minlen4",
            "blackhole_import_maxlen6",
            "blackhole_import_minlen6",
            "blackhole_export_maxlen6",
            "blackhole_export_minlen6",
            "prefix_import_maxlen4",
            "prefix_import_minlen4",
            "prefix_export_maxlen4",
            "prefix_export_minlen4",
            "prefix_import_maxlen6",
            "prefix_import_minlen6",
            "prefix_export_maxlen6",
            "prefix_export_minlen6",
            "aspath_import_maxlen",
            "aspath_import_minlen",
            "community_import_maxlen",
            "extended_community_import_maxlen",
            "large_community_import_maxlen",
        ):
            # Check if we have peer configuration for this attribute, if we do set it
            if attr_name in peer_config:
                setattr(self, attr_name, peer_config[attr_name])

    def configure(self) -> None:
        """Configure BGP peer."""
        super().configure()

        self.conf.add("")
        self.conf.add(f"# Peer type: {self.peer_type}")
        self.conf.add("")

        # Setup routing tables
        self._setup_peer_tables()

        # Setup ASN lists
        self._setup_origin_asns()
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
            export_filter_type=ProtocolPipeFilterType.UNVERSIONED,
            import_filter_type=ProtocolPipeFilterType.UNVERSIONED,
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

    @property
    def filter_name_export(self) -> str:
        """Return the IP versioned peer export filter name."""
        return f"f_bgp_AS{self.asn}_{self.name}_peer_export"

    @property
    def filter_name_import(self) -> str:
        """Return the IP versioned peer import filter name."""
        return f"f_bgp_AS{self.asn}_{self.name}_peer_import"

    @property
    def filter_name_export_bgp(self) -> str:
        """Return the IP versioned BGP export filter name."""
        return f"f_bgp_AS{self.asn}_{self.name}_peer_bgp_export"

    @property
    def filter_name_import_bgp(self) -> str:
        """Return the IP versioned BGP import filter name."""
        return f"f_bgp_AS{self.asn}_{self.name}_peer_bgp_import"

    def import_prefix_list_name(self, ipv: str) -> str:
        """Return our prefix list name."""
        return f"bgp{ipv}_AS{self.asn}_{self.name}_prefixes_import"

    def _setup_peer_tables(self) -> None:
        """Peering routing table setup."""
        self.tables.conf.append(f"# BGP Peer Tables: {self.asn} - {self.name}")
        if self.has_ipv4:
            self.tables.conf.append(f"ipv4 table {self.bgp_table_name('4')};")
        if self.has_ipv6:
            self.tables.conf.append(f"ipv6 table {self.bgp_table_name('6')};")
        self.tables.conf.append("")

    def _setup_origin_asns(self) -> None:
        """Origin ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_origin_asn_filter:
            return

        # Grab IRR prefixes
        irr_asns = []
        if self.filter_policy.as_sets:
            bgpq3 = BGPQ3()
            irr_asns = bgpq3.get_asns(self.filter_policy.as_sets)

        self.conf.add(f"define {self.origin_asn_list_name} = [")
        asns = []
        # Add ASN list with comments
        if self.filter_policy.origin_asns:
            asns.append(f"# {len(self.filter_policy.origin_asns)} statically defined")
            for asn in self.filter_policy.origin_asns:
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

    def _setup_peer_asns(self) -> None:
        """Peer ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_peer_asn_filter:
            return

        self.conf.add(f"define {self.peer_asn_list_name} = [")
        asns = []
        # Add ASN list with comments
        if self.filter_policy.peer_asns:
            asns.append(f"# {len(self.filter_policy.peer_asns)} statically defined")
            for asn in self.filter_policy.peer_asns:
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

            self.conf.add(f"define {self.import_prefix_list_name(ipv)} = [")
            # Loop with each line
            for line in prefixes_str.splitlines():
                # Remove comma from the comments
                if "#" in line:
                    line = line[:-1]
                # Add line to our output
                self.conf.add(f"  {line}")
            self.conf.add("];")
            self.conf.add("")

    def _peer_to_bgp_export_filter(self) -> None:
        """Export filters into our main BGP routing table from the BGP peer table."""

        # Set our filter name
        filter_name = self.filter_name_export_bgp

        # Configure export filter to our main BGP table
        self.conf.add("# Export filter TO the main BGP table from the BGP peer table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        # If this is a filtered route, reject it
        self.conf.add(f"  {self.bgp_functions.reject_filtered()};")
        # Enable blackholing for customers and internal peers
        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.conf.add(f"  {self.bgp_functions.accept_blackhole()};")
        # Enable blackhole large community origination for internal peers
        if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.conf.add(f"  {self.bgp_functions.accept_blackhole_originated()};")
        # Finally accept the route
        self.conf.add(f"  {self.bgp_functions.accept()};")
        self.conf.add("};")
        self.conf.add("")

    def _peer_to_bgp_import_filter(self) -> None:  # pylint: disable=too-many-branches,too-many-statements
        """Import filter FROM the main BGP table to the BGP peer table."""

        # Set our filter name
        filter_name = self.filter_name_import_bgp

        # Configure import filter from our main BGP table
        self.conf.add("# Import filter FROM the main BGP table to the BGP peer table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("bool accept_route;")
        self.conf.add("bool bypass_bgp_redistribution_checks;")
        self.conf.add("bool is_blackhole;")
        self.conf.add("bool exportable;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        self.conf.add("  accept_route = false;")
        self.conf.add("  bypass_bgp_redistribution_checks = false;")
        self.conf.add("  is_blackhole = false;")
        self.conf.add("")

        # Reject NOADVERTISE
        self.conf.add(f"  {self.bgp_functions.reject_noadvertise()};")

        # Do not export blackhole routes to customers or peers
        if self.peer_type in ("customer", "peer"):
            self.conf.add(f"  {self.bgp_functions.reject_blackholes()};")

        # Blackhole support for routeservers
        if self.peer_type in ("routeserver", "routecollector"):
            # If the peer accepts blackhole communites, check if we're going to be exporting this blackhole
            if self.blackhole_community:
                self.conf.add("  # Peer is blackhole community capable")
                # Create function call
                func = self.bgp_functions.allow_blackholes(
                    True,
                    self.route_policy_redistribute.kernel_blackhole,
                    self.route_policy_redistribute.static_blackhole,
                    self.asn,
                    65413,
                )
                self.conf.add(f"  if {func} then")
                self.conf.add("    is_blackhole = true;")
            else:
                self.conf.add("  # Peer is not blackhole community capable")
                self.conf.add(f"  {self.bgp_functions.allow_blackholes(False, False, False, self.asn, 65413)};")
        # Blackhole support for transit
        elif self.peer_type == "transit":
            # If the peer accepts blackhole communites, check if we're going to be exporting this blackhole
            if self.blackhole_community:
                # Create function call
                func = self.bgp_functions.allow_blackholes(
                    True,
                    self.route_policy_redistribute.kernel_blackhole,
                    self.route_policy_redistribute.static_blackhole,
                    self.asn,
                    65412,
                )
                self.conf.add("  # Peer is blackhole community capable")
                self.conf.add(f"  if {func} then")
                self.conf.add("    is_blackhole = true;")
            else:
                self.conf.add("  # Peer is not blackhole community capable")
                self.conf.add(f"  {self.bgp_functions.allow_blackholes(False, False, False, self.asn, 65412)};")

        # Reject NOEXPORT
        if self.peer_type in ("customer", "peer", "routecollector", "routeserver", "transit"):
            self.conf.add(f"  {self.bgp_functions.reject_noexport()};")

        # Check for peer types we're not exporting to
        if self.peer_type == "customer":
            self.conf.add(f"  {self.bgp_functions.reject_noexport_customer()};")
        if self.peer_type in ("peer", "routecollector", "routeserver"):
            self.conf.add(f"  {self.bgp_functions.reject_noexport_peer()};")
        if self.peer_type == "transit":
            self.conf.add(f"  {self.bgp_functions.reject_noexport_transit()};")

        # Rejections based on location-based large communities
        if self.peer_type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we have a ISO-3166 country code
            if self.location.iso3166:
                self.conf.add("  # Check if we're not exporting this route based on the ISO-3166 location")
                self.conf.add(f"  {self.bgp_functions.reject_noexport_location(self.location.iso3166)};")

        # Check for connected route redistribution
        if self.route_policy_redistribute.connected:
            self.conf.add(f"  if {self.bgp_functions.redistribute_connected(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.redistribute_connected(False)};")
        # Check for kernel route redistribution
        if self.route_policy_redistribute.kernel:
            self.conf.add(f"  if {self.bgp_functions.redistribute_kernel(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.redistribute_kernel(False)};")
        # Check for kernel blackhole route redistribution
        if self.route_policy_redistribute.kernel_blackhole:
            self.conf.add(f"  if {self.bgp_functions.redistribute_kernel_blackhole(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.redistribute_kernel_blackhole(False)};")
        # Check for static route redistribution
        if self.route_policy_redistribute.static:
            self.conf.add(f"  if {self.bgp_functions.redistribute_static(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.redistribute_static(False)};")
        # Check for static blackhole route redistribution
        if self.route_policy_redistribute.static_blackhole:
            self.conf.add(f"  if {self.bgp_functions.redistribute_static_blackhole(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.redistribute_static_blackhole(False)};")
        # Check for originated route redistribution
        if self.route_policy_redistribute.originated:
            self.conf.add(f"  if {self.bgp_functions.redistribute_originated(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.redistribute_originated(False)};")

        # Do not redistribute the default route, no matter where we get it from
        if self.route_policy_redistribute.default:
            self.conf.add(
                f"  if {self.bgp_functions.redistribute_default(True, BirdVariable('accept_route'))}"
                " then bypass_bgp_redistribution_checks = true;"
            )
        else:
            self.conf.add(f"  {self.bgp_functions.redistribute_default(False, BirdVariable('accept_route'))};")

        # Start of BGP type checks ...
        self.conf.add("  # BGP route type tests...")
        self.conf.add("  if (!bypass_bgp_redistribution_checks) then {")
        self.conf.add("    # Check if the route is exportable, we need this in the redistribution checks below")
        self.conf.add("     if !is_blackhole then {")
        self.conf.add(f"       exportable = {self._bgp_export_ok()};")
        self.conf.add("     } else {")
        self.conf.add(f"       exportable = {self._bgp_export_blackhole_ok()};")
        self.conf.add("     }")

        # Check redistribution for internal BGP route types
        if self.route_policy_redistribute.bgp:
            self.conf.add(f"    if {self.bgp_functions.redistribute_bgp()} then accept_route = true;")
        if self.route_policy_redistribute.bgp_own:
            self.conf.add(f"    if {self.bgp_functions.redistribute_bgp_own(BirdVariable('exportable'))} then accept_route = true;")
        if self.route_policy_redistribute.bgp_customer:
            self.conf.add(
                f"    if {self.bgp_functions.redistribute_bgp_customer(BirdVariable('exportable'))} then accept_route = true;"
            )
        if self.route_policy_redistribute.bgp_peering:
            self.conf.add(
                f"    if {self.bgp_functions.redistribute_bgp_peering(BirdVariable('exportable'))} then accept_route = true;"
            )
        if self.route_policy_redistribute.bgp_transit:
            self.conf.add(
                f"    if {self.bgp_functions.redistribute_bgp_transit(BirdVariable('exportable'))} then accept_route = true;"
            )

        # End of BGP type tests
        self.conf.add("  }")

        # Check if we're accepting the route...
        self.conf.add("  if (accept_route) then {")
        # Check if we are adding a large community to outgoing routes
        if self.large_communities.outgoing.default:
            for large_community in self.large_communities.outgoing.default:
                self.conf.add(f"    {self.bgp_functions.lc_add_default(BirdVariable(large_community))};")
        if self.large_communities.outgoing.connected:
            for large_community in self.large_communities.outgoing.connected:
                self.conf.add(f"    {self.bgp_functions.lc_add_connected(BirdVariable(large_community))};")
        if self.large_communities.outgoing.kernel:
            for large_community in self.large_communities.outgoing.kernel:
                self.conf.add(f"    {self.bgp_functions.lc_add_kernel(BirdVariable(large_community))};")
        if self.large_communities.outgoing.kernel_blackhole:
            for large_community in self.large_communities.outgoing.kernel_blackhole:
                self.conf.add(f"    {self.bgp_functions.lc_add_kernel_blackhole(BirdVariable(large_community))};")
        if self.large_communities.outgoing.originated:
            for large_community in self.large_communities.outgoing.originated:
                self.conf.add(f"    {self.bgp_functions.lc_add_originated(BirdVariable(large_community))};")
        if self.large_communities.outgoing.static:
            for large_community in self.large_communities.outgoing.static:
                self.conf.add(f"    {self.bgp_functions.lc_add_static(BirdVariable(large_community))};")
        if self.large_communities.outgoing.static_blackhole:
            for large_community in self.large_communities.outgoing.static_blackhole:
                self.conf.add(f"    {self.bgp_functions.lc_add_static_blackhole(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp:
            for large_community in self.large_communities.outgoing.bgp:
                self.conf.add(f"    {self.bgp_functions.lc_add_bgp(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_own:
            for large_community in self.large_communities.outgoing.bgp_own:
                self.conf.add(f"    {self.bgp_functions.lc_add_bgp_own(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_customer:
            for large_community in self.large_communities.outgoing.bgp_customer:
                self.conf.add(f"    {self.bgp_functions.lc_add_bgp_customer(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_peering:
            for large_community in self.large_communities.outgoing.bgp_peering:
                self.conf.add(f"    {self.bgp_functions.lc_add_bgp_peering(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_transit:
            for large_community in self.large_communities.outgoing.bgp_transit:
                self.conf.add(f"    {self.bgp_functions.lc_add_bgp_transit(BirdVariable(large_community))};")

        # For eBGP peer types, make sure we replace AS-PATHs with the LC action set
        if self.peer_type in ("customer", "peer", "routecollector", "routeserver", "transit"):
            self.conf.add(f"    {self.bgp_functions.replace_aspath()};")
            self.conf.add(f"    {self.bgp_functions.remove_lc_private()};")

        # Check if we're doing AS-PATH prepending...
        if self.prepend.default.own_asn:
            self.conf.add(f"    {self.bgp_functions.prepend_default(BirdVariable('BGP_ASN'), self.prepend.default.own_asn)};")
        if self.prepend.connected.own_asn:
            self.conf.add(f"    {self.bgp_functions.prepend_connected(BirdVariable('BGP_ASN'), self.prepend.connected.own_asn)};")
        if self.prepend.kernel.own_asn:
            self.conf.add(f"    {self.bgp_functions.prepend_kernel(BirdVariable('BGP_ASN'), self.prepend.kernel.own_asn)};")
        if self.prepend.kernel_blackhole.own_asn:
            func = self.bgp_functions.prepend_kernel_blackhole(BirdVariable("BGP_ASN"), self.prepend.kernel_blackhole.own_asn)
            self.conf.add(f"    {func};")
        if self.prepend.originated.own_asn:
            self.conf.add(f"    {self.bgp_functions.prepend_originated(BirdVariable('BGP_ASN'), self.prepend.originated.own_asn)};")
        if self.prepend.static.own_asn:
            self.conf.add(f"    {self.bgp_functions.prepend_static(BirdVariable('BGP_ASN'), self.prepend.static.own_asn)};")
        if self.prepend.static_blackhole.own_asn:
            func = self.bgp_functions.prepend_static_blackhole(BirdVariable("BGP_ASN"), self.prepend.static_blackhole.own_asn)
            self.conf.add(f"    {func};")
        if self.prepend.bgp.own_asn:
            self.conf.add(f"    {self.bgp_functions.prepend_bgp(BirdVariable('BGP_ASN'), self.prepend.bgp.own_asn)};")
        if self.prepend.bgp_own.own_asn:
            self.conf.add(f"    {self.bgp_functions.prepend_bgp_own(BirdVariable('BGP_ASN'), self.prepend.bgp_own.own_asn)};")
        if self.prepend.bgp_customer.own_asn:
            self.conf.add(
                f"    {self.bgp_functions.prepend_bgp_customer(BirdVariable('BGP_ASN'), self.prepend.bgp_customer.own_asn)};"
            )
        if self.prepend.bgp_peering.own_asn:
            self.conf.add(
                f"    {self.bgp_functions.prepend_bgp_peering(BirdVariable('BGP_ASN'), self.prepend.bgp_peering.own_asn)};"
            )
        if self.prepend.bgp_transit.own_asn:
            self.conf.add(
                f"    {self.bgp_functions.prepend_bgp_transit(BirdVariable('BGP_ASN'), self.prepend.bgp_transit.own_asn)};"
            )

        # Do large community prepending if the peer is a customer, peer, routeserver or transit
        if self.peer_type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we're doing prepending
            self.conf.add("    # Do large community based prepending")
            self.conf.add(f"    {self.bgp_functions.prepend_lc(self.asn)};")
            # Check if we have a ISO-3166 country code
            if self.location.iso3166:
                self.conf.add("    # Do prepending based on ISO-3166 location;")
                self.conf.add(f"    {self.bgp_functions.prepend_lc_location(self.location.iso3166)};")
        # If we have graceful_shutdown set, add the community
        if self.graceful_shutdown:
            self.conf.add(f"    {self.bgp_functions.graceful_shutdown()};")
        # Check if we need to do any blackhole manipulation
        if self.blackhole_community and isinstance(self.blackhole_community, list):
            self.conf.add("    # If this is a blackhole route, then add the communities")
            self.conf.add("    if is_blackhole then {")
            self.conf.add("      bgp_community.delete([BGP_COMMUNITY_BLACKHOLE]);")
            # Loop with the communities we have to add
            for community in self.blackhole_community:
                # Get community component count so we can see if its a normal or large community
                component_count = community.count(",")
                if component_count == 1:
                    self.conf.add(f"      {self.bgp_functions.community_add_blackhole(BirdVariable(community))};")
                elif component_count == 2:
                    self.conf.add(f"      {self.bgp_functions.lc_add_blackhole(BirdVariable(community))};")
            self.conf.add("    }")

        # Finally accept
        self.conf.add("    # Finally accept")
        self.conf.add('    if DEBUG then')
        self.conf.add(f'     print "[{filter_name}] Accepting ", net, " from t_bgp to t_bgp_peer (fallthrough)";')
        self.conf.add("    accept;")
        self.conf.add("  }")

        # By default reject all routes
        self.conf.add("  # Reject by default")
        self.conf.add('  if DEBUG then')
        self.conf.add(f'   print "[{filter_name}] Rejecting ", net, " from t_bgp to t_bgp_peer (fallthrough)";')
        self.conf.add("  reject;")
        self.conf.add("};")
        self.conf.add("")

    def _peer_export_filter(self) -> None:
        """Peer export filter setup from peer table to peer."""

        filter_name = self.filter_name_export

        # Configure export filter to the BGP peer
        self.conf.add("# Export filter TO the BGP peer from the peer BGP table")
        self.conf.add(f"filter {filter_name} {{")
        # Check if we're quarantined, if we are reject routes to the peer
        if self.quarantined:
            self.conf.add("  # Peer is quarantined so reject exporting of routes")
            self.conf.add('  if DEBUG then')
            self.conf.add(f'   print "[{filter_name}] Rejecting ", net, " from t_bgp_peer to peer (qurantined)";')
            self.conf.add("  reject;")
        # If we're not quarantined, then export routes
        else:
            self.conf.add("  # We accept all routes going to the peer that are in the peer BGP table")
            self.conf.add(f'  if (proto != "{self.protocol_name("4")}" && proto != "{self.protocol_name("6")}") then accept;')
        self.conf.add("};")
        self.conf.add("")

    def _peer_import_filter(self) -> None:  # pylint: disable=too-many-branches,too-many-statements
        """Peer import filter setup from peer to peer table."""

        # Set our filter name
        filter_name = self.filter_name_import

        # Configure import filter from the BGP peer
        self.conf.add("# Import filter FROM the BGP peer TO the peer BGP table")
        self.conf.add(f"filter {filter_name}")
        self.conf.add("string filter_name;")
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        self.conf.add("  # Only process routes from our peer, accept everything else")
        self.conf.add(f'  if (proto != "{self.protocol_name("4")}" && proto != "{self.protocol_name("6")}") then accept;')

        # Clients
        if self.peer_type == "customer":
            self.conf.add(f"  {self.bgp_functions.communities_strip_internal()};")
            self.conf.add(f"  {self.bgp_functions.import_customer(self.asn, self.cost)};")
            self.conf.add(f"  {self.bgp_functions.filter_default()};")
            self.conf.add(f"  {self.bgp_functions.filter_bogons()};")
            # The bgp_filter_prefix size test will exclude blackholes from checks
            self.conf.add(f"  {self._bgp_filter_prefix_size()};")
            # Check if we're going to accept a blackhole route
            if self.route_policy_accept.blackhole:
                self.conf.add(f"  {self._bgp_filter_blackhole_size()};")
            else:
                self.conf.add(f"  {self.bgp_functions.filter_blackhole()};")
            # If we're replacing the ASN we only allow private ASN's in the AS-PATH
            if self.replace_aspath:
                self.conf.add(f"  {self.bgp_functions.filter_asn_private(BirdVariable(f'[{self.asn}]'))};")
            # Else, filter bogon ASN's
            else:
                self.conf.add(f"  {self.bgp_functions.filter_asn_bogons()};")
            self.conf.add(f"  {self.bgp_functions.filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_invalid(self.asn)};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_transit()};")
            self.conf.add(f"  {self.bgp_functions.filter_nexthop_not_peerip()};")
            self.conf.add(f"  {self._bgp_filter_community_lengths()};")
        # Peers
        elif self.peer_type == "peer":
            self.conf.add(f"  {self.bgp_functions.communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.import_peer(self.asn, self.cost)};")
            self.conf.add(f"  {self.bgp_functions.filter_default()};")
            self.conf.add(f"  {self.bgp_functions.filter_bogons()};")
            self.conf.add(f"  {self._bgp_filter_prefix_size()};")
            self.conf.add(f"  {self.bgp_functions.filter_blackhole()};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_bogons()};")
            self.conf.add(f"  {self.bgp_functions.filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};")
            self.conf.add(f"  {self.bgp_functions.filter_nexthop_not_peerip()};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_invalid(self.asn)};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_transit()};")
            self.conf.add(f"  {self._bgp_filter_community_lengths()};")
        # Routecollector
        elif self.peer_type == "routecollector":
            self.conf.add(f"  {self.bgp_functions.communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.import_routecollector()};")
        # Routeserver
        elif self.peer_type == "routeserver":
            self.conf.add(f"  {self.bgp_functions.communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.import_routeserver(self.asn, self.cost)};")
            self.conf.add(f"  {self.bgp_functions.filter_default()};")
            self.conf.add(f"  {self.bgp_functions.filter_bogons()};")
            self.conf.add(f"  {self._bgp_filter_prefix_size()};")
            self.conf.add(f"  {self.bgp_functions.filter_blackhole()};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_bogons()};")
            self.conf.add(f"  {self.bgp_functions.filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_transit()};")
            self.conf.add(f"  {self._bgp_filter_community_lengths()};")
        # Internal router peer types
        elif self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.conf.add(f"  {self.bgp_functions.filter_lc_no_relation()};")
            if not self.route_policy_accept.default:
                self.conf.add(f"  {self.bgp_functions.filter_default()};")
            if self.peer_type == "internal" and self.replace_aspath:
                self.conf.add(f"  {self.bgp_functions.filter_asn_private(BirdVariable('PRIVATE_ASNS'))};")
            # Check if we're going to accept a blackhole route
            if self.route_policy_accept.blackhole:
                self.conf.add(f"  {self._bgp_filter_blackhole_size()};")
            else:
                self.conf.add(f"  {self.bgp_functions.filter_blackhole()};")
        # Transit providers
        elif self.peer_type == "transit":
            self.conf.add(f"  {self.bgp_functions.communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.import_transit(self.asn, self.cost)};")
            if self.route_policy_accept.default:
                self.conf.add("  # Bypass bogon and size filters for the default route")
                self.conf.add(f"  if !{self.functions.is_default()} then {{")
                self.conf.add(f"    {self.bgp_functions.filter_bogons()};")
                self.conf.add(f"    {self._bgp_filter_prefix_size()};")
                self.conf.add("  }")
            else:
                self.conf.add(f"  {self.bgp_functions.filter_default()};")
                self.conf.add(f"  {self.bgp_functions.filter_bogons()};")
                self.conf.add(f"  {self._bgp_filter_prefix_size()};")
            self.conf.add(f"  {self.bgp_functions.filter_blackhole()};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_bogons()};")
            self.conf.add(f"  {self.bgp_functions.filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};")
            self.conf.add(f"  {self.bgp_functions.filter_asn_invalid(self.asn)};")
            self.conf.add(f"  {self.bgp_functions.filter_nexthop_not_peerip()};")
            self.conf.add(f"  {self._bgp_filter_community_lengths()};")

        # Flip around the meaning of filters depending on peer type
        # For customer and peer, it is an ALLOW list
        if self.peer_type in ("customer", "peer"):
            # Check if we're filtering allowed origin ASNs
            if self.filter_policy.origin_asns:
                self.conf.add("  # Filter on the allowed origin ASNs")
                self.conf.add(f"  {self.bgp_functions.filter_origin_asns_allow(BirdVariable(self.origin_asn_list_name))};")
            # Check if we're filtering allowed peer ASNs
            if self.filter_policy.peer_asns:
                self.conf.add("  # Filter on the allowed peer ASNs")
                self.conf.add(f"  {self.bgp_functions.filter_peer_asns_allow(BirdVariable(self.peer_asn_list_name))};")
            # Check if we're filtering allowed prefixes
            if self.filter_policy.prefixes:
                self.conf.add("  # Filter on the allowed prefixes")
                # Check if we have IPv4 support and output the filter
                if self.has_ipv4:
                    self.conf.add("  if (net.type = NET_IP4) then")
                    self.conf.add(
                        f"    {self.bgp_functions.filter_prefixes_allow(BirdVariable(self.import_prefix_list_name('4')))};"
                    )
                # Check if we have IPv6 support and output the filter
                if self.has_ipv6:
                    self.conf.add("  if (net.type = NET_IP6) then")
                    self.conf.add(
                        f"    {self.bgp_functions.filter_prefixes_allow(BirdVariable(self.import_prefix_list_name('6')))};"
                    )
        # For everything else it is a DENY list
        elif self.peer_type != "routecollector":
            # Check if we're filtering denied origin ASNs
            if self.filter_policy.origin_asns:
                self.conf.add("  # Filter on the denied origin ASNs")
                self.conf.add(f"  {self.bgp_functions.filter_origin_asns_deny(BirdVariable(self.origin_asn_list_name))};")
            # Check if we're filtering denied peer ASNs
            if self.filter_policy.peer_asns:
                self.conf.add("  # Filter on the denied peer ASNs")
                self.conf.add(f"  {self.bgp_functions.filter_peer_asns_deny(BirdVariable(self.peer_asn_list_name))};")
            # Check if we're filtering denied prefixes
            if self.filter_policy.prefixes:
                self.conf.add("  # Filter on the denied prefixes")
                # Check if we have IPv4 support and output the filter
                if self.has_ipv4:
                    self.conf.add("  if (net.type = NET_IP4) then")
                    self.conf.add(
                        f"    {self.bgp_functions.filter_prefixes_deny(BirdVariable(self.import_prefix_list_name('4')))};"
                    )
                # Check if we have IPv6 support and output the filter
                if self.has_ipv6:
                    self.conf.add("  if (net.type = NET_IP6) then")
                    self.conf.add(
                        f"    {self.bgp_functions.filter_prefixes_deny(BirdVariable(self.import_prefix_list_name('6')))};"
                    )

        # Quarantine mode...
        # NK: We don't quarantine route collectors as they are automagically filtered
        if self.quarantined and self.peer_type != "routecollector":
            # Quarantine prefixes
            self.conf.add("  # Quarantine all prefixes received")
            self.conf.add(f"  {self.bgp_functions.quarantine_peer()};")

        # Add location-based large communities
        if self.peer_type in ("customer", "peer", "routeserver", "transit"):
            # Check if we have a ISO-3166 country code
            if self.location.iso3166:
                self.conf.add(f"  {self.bgp_functions.import_location_iso3166(self.location.iso3166)};")
            # Check if we have a UN.M49 country code
            if self.location.unm49:
                self.conf.add(f"  {self.bgp_functions.import_location_unm49(self.location.unm49)};")

        # If this is a customer or internal peer type, check if we're doing replacement of the AS-PATH and add the action community
        if self.peer_type in ("customer", "internal"):
            if self.replace_aspath:
                # Lastly add the large community to replace the ASN
                self.conf.add(f'  print "[{filter_name}] Adding LC action BGP_LC_ACTION_REPLACE_ASPATH to ", net;')
                self.conf.add("  bgp_large_community.add(BGP_LC_ACTION_REPLACE_ASPATH);")

        # Check if we are adding a large community to incoming routes
        if self.large_communities.incoming:
            # Loop with large communities and add to the prefix
            for large_community in sorted(self.large_communities.incoming):
                if self.birdconfig_globals.debug:
                    self.conf.add(f'  print "[{filter_name}] Adding LC {large_community} to ", net;')
                self.conf.add(f"  bgp_large_community.add({large_community});")

        # Support for changing incoming local_pref
        if self.peer_type == "customer":
            self.conf.add(f"  {self.bgp_functions.import_localpref()};")

        # Enable graceful_shutdown for this prefix
        if self.graceful_shutdown:
            self.conf.add(f"  {self.bgp_functions.graceful_shutdown()};")
        # Set local_pref to 0 (GRACEFUL_SHUTDOWN) for the peer in graceful_shutdown
        self.conf.add(f"  {self.bgp_functions.import_graceful_shutdown()};")

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
        if self.peer_type in ("rrclient", "rrserver-rrserver"):
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
        self.conf.add(f"    import filter {self.filter_name_import};")
        self.conf.add(f"    export filter {self.filter_name_export};")
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
        self._peer_to_bgp_export_filter()
        self._peer_to_bgp_import_filter()

    def _setup_peer_filters(self) -> None:
        """Peer filter setup."""
        self._peer_export_filter()
        self._peer_import_filter()

    def _bgp_export_ok(self) -> str:
        """Generate the BGP can export function with relevant arguments to see if we can export a prefix."""
        return self.bgp_functions.export_ok(
            self.asn, self.prefix_export_maxlen4, self.prefix_export_minlen4, self.prefix_export_maxlen6, self.prefix_export_minlen6
        )

    def _bgp_export_blackhole_ok(self) -> str:
        """Generate the BGP can export function with relevant arguments to see if we can export a blackhole prefix."""
        return self.bgp_functions.export_blackhole_ok(
            self.asn,
            self.blackhole_export_maxlen4,
            self.blackhole_export_minlen4,
            self.blackhole_export_maxlen6,
            self.blackhole_export_minlen6,
        )

    def _bgp_filter_prefix_size(self) -> str:
        """Return a BGP prefix size filter for a specific IP version."""
        return self.bgp_functions.filter_prefix_size(
            self.prefix_import_maxlen4, self.prefix_import_minlen4, self.prefix_import_maxlen6, self.prefix_import_minlen6
        )

    def _bgp_filter_blackhole_size(self) -> str:
        """Return a BGP blackhole size filter for a specific IP version."""
        return self.bgp_functions.filter_blackhole_size(
            self.blackhole_import_maxlen4,
            self.blackhole_import_minlen4,
            self.blackhole_import_maxlen6,
            self.blackhole_import_minlen6,
        )

    def _bgp_filter_community_lengths(self) -> str:
        """Generate the BGP filter function for the community lengths."""
        maxlen = self.community_import_maxlen
        maxlen_extended = self.extended_community_import_maxlen
        maxlen_large = self.large_community_import_maxlen
        return self.bgp_functions.filter_community_lengths(maxlen, maxlen_extended, maxlen_large)

    @property
    def bgp_attributes(self) -> BGPAttributes:
        """Return the BGP protocol attributes."""
        return self._bgp_attributes

    @property
    def bgp_functions(self) -> BGPFunctions:
        """Return the BGP functions."""
        return self._bgp_functions

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
    def location(self) -> BGPPeerLocation:
        """Return our location."""
        return self.peer_attributes.location

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
    def prepend(self) -> BGPPeerPrepend:
        """Return our prepending."""
        return self.peer_attributes.prepend

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
    def replace_aspath(self) -> bool:
        """Return the ASN which replaces the AS-PATH."""
        return self.peer_attributes.replace_aspath

    @replace_aspath.setter
    def replace_aspath(self, replace_aspath: bool) -> None:
        """Set the ASN which will replace the AS-PATH."""
        self.peer_attributes.replace_aspath = replace_aspath

    @property
    def peeringdb(self) -> BGPPeerPeeringDB:
        """Return our peeringdb entry."""
        return self.peer_attributes.peeringdb

    @property
    def blackhole_community(self) -> Optional[Union[bool, List[str]]]:
        """Return the current value of blackhole_community."""
        return self.peer_attributes.blackhole_community

    @blackhole_community.setter
    def blackhole_community(self, blackhole_community: Union[List[str], bool]) -> None:
        """Set the blackhole community."""
        self.peer_attributes.blackhole_community = blackhole_community

    # IPV4 BLACKHOLE IMPORT PREFIX LENGTHS

    @property
    def blackhole_import_maxlen4(self) -> int:
        """Return the current value of blackhole_import_maxlen4."""
        return self.peer_attributes.blackhole_import_maxlen4 or self.bgp_attributes.blackhole_import_maxlen4

    @blackhole_import_maxlen4.setter
    def blackhole_import_maxlen4(self, blackhole_import_maxlen4: int) -> None:
        """Setter for blackhole_import_maxlen4."""
        self.peer_attributes.blackhole_import_maxlen4 = blackhole_import_maxlen4

    @property
    def blackhole_import_minlen4(self) -> int:
        """Return the current value of blackhole_import_minlen4."""
        return self.peer_attributes.blackhole_import_minlen4 or self.bgp_attributes.blackhole_import_minlen4

    @blackhole_import_minlen4.setter
    def blackhole_import_minlen4(self, blackhole_import_minlen4: int) -> None:
        """Setter for blackhole_import_minlen4."""
        self.peer_attributes.blackhole_import_minlen4 = blackhole_import_minlen4

    # IPV4 BLACKHOLE EXPORT PREFIX LENGTHS

    @property
    def blackhole_export_maxlen4(self) -> int:
        """Return the current value of blackhole_export_maxlen4."""
        return self.peer_attributes.blackhole_export_maxlen4 or self.bgp_attributes.blackhole_export_maxlen4

    @blackhole_export_maxlen4.setter
    def blackhole_export_maxlen4(self, blackhole_export_maxlen4: int) -> None:
        """Setter for blackhole_export_maxlen4."""
        self.peer_attributes.blackhole_export_maxlen4 = blackhole_export_maxlen4

    @property
    def blackhole_export_minlen4(self) -> int:
        """Return the current value of blackhole_export_minlen4."""
        return self.peer_attributes.blackhole_export_minlen4 or self.bgp_attributes.blackhole_export_minlen4

    @blackhole_export_minlen4.setter
    def blackhole_export_minlen4(self, blackhole_export_minlen4: int) -> None:
        """Setter for blackhole_export_minlen4."""
        self.peer_attributes.blackhole_export_minlen4 = blackhole_export_minlen4

    # IPV6 BLACKHOLE IMPORT PREFIX LENGTHS

    @property
    def blackhole_import_maxlen6(self) -> int:
        """Return the current value of blackhole_import_maxlen6."""
        return self.peer_attributes.blackhole_import_maxlen6 or self.bgp_attributes.blackhole_import_maxlen6

    @blackhole_import_maxlen6.setter
    def blackhole_import_maxlen6(self, blackhole_import_maxlen6: int) -> None:
        """Setter for blackhole_import_maxlen6."""
        self.peer_attributes.blackhole_import_maxlen6 = blackhole_import_maxlen6

    @property
    def blackhole_import_minlen6(self) -> int:
        """Return the current value of blackhole_import_minlen6."""
        return self.peer_attributes.blackhole_import_minlen6 or self.bgp_attributes.blackhole_import_minlen6

    @blackhole_import_minlen6.setter
    def blackhole_import_minlen6(self, blackhole_import_minlen6: int) -> None:
        """Setter for blackhole_import_minlen6."""
        self.peer_attributes.blackhole_import_minlen6 = blackhole_import_minlen6

    # IPV6 BLACKHOLE EXPORT PREFIX LENGTHS

    @property
    def blackhole_export_maxlen6(self) -> int:
        """Return the current value of blackhole_export_maxlen6."""
        return self.peer_attributes.blackhole_export_maxlen6 or self.bgp_attributes.blackhole_export_maxlen6

    @blackhole_export_maxlen6.setter
    def blackhole_export_maxlen6(self, blackhole_export_maxlen6: int) -> None:
        """Setter for blackhole_export_maxlen6."""
        self.peer_attributes.blackhole_export_maxlen6 = blackhole_export_maxlen6

    @property
    def blackhole_export_minlen6(self) -> int:
        """Return the current value of blackhole_export_minlen6."""
        return self.peer_attributes.blackhole_export_minlen6 or self.bgp_attributes.blackhole_export_minlen6

    @blackhole_export_minlen6.setter
    def blackhole_export_minlen6(self, blackhole_export_minlen6: int) -> None:
        """Setter for blackhole_export_minlen6."""
        self.peer_attributes.blackhole_export_minlen6 = blackhole_export_minlen6

    # IPV4 IMPORT PREFIX LENGTHS

    @property
    def prefix_import_maxlen4(self) -> int:
        """Return the current value of prefix_import_maxlen4."""
        return self.peer_attributes.prefix_import_maxlen4 or self.bgp_attributes.prefix_import_maxlen4

    @prefix_import_maxlen4.setter
    def prefix_import_maxlen4(self, prefix_import_maxlen4: int) -> None:
        """Setter for prefix_import_maxlen4."""
        self.peer_attributes.prefix_import_maxlen4 = prefix_import_maxlen4

    @property
    def prefix_import_minlen4(self) -> int:
        """Return the current value of prefix_import_minlen4."""
        return self.peer_attributes.prefix_import_minlen4 or self.bgp_attributes.prefix_import_minlen4

    @prefix_import_minlen4.setter
    def prefix_import_minlen4(self, prefix_import_minlen4: int) -> None:
        """Setter for prefix_import_minlen4."""
        self.peer_attributes.prefix_import_minlen4 = prefix_import_minlen4

    # IPV4 EXPORT PREFIX LENGHTS

    @property
    def prefix_export_maxlen4(self) -> int:
        """Return the current value of prefix_export_maxlen4."""
        return self.peer_attributes.prefix_export_maxlen4 or self.bgp_attributes.prefix_export_maxlen4

    @prefix_export_maxlen4.setter
    def prefix_export_maxlen4(self, prefix_export_maxlen4: int) -> None:
        """Setter for prefix_export_maxlen4."""
        self.peer_attributes.prefix_export_maxlen4 = prefix_export_maxlen4

    @property
    def prefix_export_minlen4(self) -> int:
        """Return the current value of prefix_export_minlen4."""
        return self.peer_attributes.prefix_export_minlen4 or self.bgp_attributes.prefix_export_minlen4

    @prefix_export_minlen4.setter
    def prefix_export_minlen4(self, prefix_export_minlen4: int) -> None:
        """Setter for prefix_export_minlen4."""
        self.peer_attributes.prefix_export_minlen4 = prefix_export_minlen4

    # IPV6 IMPORT LENGTHS

    @property
    def prefix_import_maxlen6(self) -> int:
        """Return the current value of prefix_import_maxlen6."""
        return self.peer_attributes.prefix_import_maxlen6 or self.bgp_attributes.prefix_import_maxlen6

    @prefix_import_maxlen6.setter
    def prefix_import_maxlen6(self, prefix_import_maxlen6: int) -> None:
        """Setter for prefix_import_maxlen6."""
        self.peer_attributes.prefix_import_maxlen6 = prefix_import_maxlen6

    @property
    def prefix_import_minlen6(self) -> int:
        """Return the current value of prefix_import_minlen6."""
        return self.peer_attributes.prefix_import_minlen6 or self.bgp_attributes.prefix_import_minlen6

    @prefix_import_minlen6.setter
    def prefix_import_minlen6(self, prefix_import_minlen6: int) -> None:
        """Setter for prefix_import_minlen6."""
        self.peer_attributes.prefix_import_minlen6 = prefix_import_minlen6

    # IPV6 EXPORT LENGTHS

    @property
    def prefix_export_minlen6(self) -> int:
        """Return the current value of prefix_export_minlen6."""
        return self.peer_attributes.prefix_export_minlen6 or self.bgp_attributes.prefix_export_minlen6

    @prefix_export_minlen6.setter
    def prefix_export_minlen6(self, prefix_export_minlen6: int) -> None:
        """Setter for prefix_export_minlen6."""
        self.peer_attributes.prefix_export_minlen6 = prefix_export_minlen6

    @property
    def prefix_export_maxlen6(self) -> int:
        """Return the current value of prefix_export_maxlen6."""
        return self.peer_attributes.prefix_export_maxlen6 or self.bgp_attributes.prefix_export_maxlen6

    @prefix_export_maxlen6.setter
    def prefix_export_maxlen6(self, prefix_export_maxlen6: int) -> None:
        """Setter for prefix_export_maxlen6."""
        self.peer_attributes.prefix_export_maxlen6 = prefix_export_maxlen6

    # AS PATH LENGTHS

    @property
    def aspath_import_minlen(self) -> int:
        """Return the current value of aspath_import_minlen."""
        return self.peer_attributes.aspath_import_minlen or self.bgp_attributes.aspath_import_minlen

    @aspath_import_minlen.setter
    def aspath_import_minlen(self, aspath_import_minlen: int) -> None:
        """Set the AS path minlen."""
        self.peer_attributes.aspath_import_minlen = aspath_import_minlen

    @property
    def aspath_import_maxlen(self) -> int:
        """Return the current value of aspath_import_maxlen."""
        return self.peer_attributes.aspath_import_maxlen or self.bgp_attributes.aspath_import_maxlen

    @aspath_import_maxlen.setter
    def aspath_import_maxlen(self, aspath_import_maxlen: int) -> None:
        """Set the AS path maxlen."""
        self.peer_attributes.aspath_import_maxlen = aspath_import_maxlen

    # COMMUNITY LENGTHS

    @property
    def community_import_maxlen(self) -> int:
        """Return the current value of community_import_maxlen."""
        return self.peer_attributes.community_import_maxlen or self.bgp_attributes.community_import_maxlen

    @community_import_maxlen.setter
    def community_import_maxlen(self, community_import_maxlen: int) -> None:
        """Set the value of community_import_maxlen."""
        self.peer_attributes.community_import_maxlen = community_import_maxlen

    @property
    def extended_community_import_maxlen(self) -> int:
        """Return the current value of extended_community_import_maxlen."""
        return self.peer_attributes.extended_community_import_maxlen or self.bgp_attributes.extended_community_import_maxlen

    @extended_community_import_maxlen.setter
    def extended_community_import_maxlen(self, extended_community_import_maxlen: int) -> None:
        """Set the value of extended_community_import_maxlen."""
        self.peer_attributes.extended_community_import_maxlen = extended_community_import_maxlen

    @property
    def large_community_import_maxlen(self) -> int:
        """Return the current value of large_community_import_maxlen."""
        return self.peer_attributes.large_community_import_maxlen or self.bgp_attributes.large_community_import_maxlen

    @large_community_import_maxlen.setter
    def large_community_import_maxlen(self, large_community_import_maxlen: int) -> None:
        """Set the value of large_community_import_maxlen."""
        self.peer_attributes.large_community_import_maxlen = large_community_import_maxlen

    #
    # Helper properties
    #

    @property
    def origin_asn_list_name(self) -> str:
        """Return our origin ASN list name."""
        return f"bgp_AS{self.asn}_{self.name}_origin_asns"

    @property
    def peer_asn_list_name(self) -> str:
        """Return our peer ASN list name."""
        return f"bgp_AS{self.asn}_{self.name}_peer_asns"

    @property
    def has_origin_asn_filter(self) -> BGPPeerFilterItem:
        """Return if we filter on origin ASNs."""
        return self.filter_policy.origin_asns or self.filter_policy.as_sets

    @property
    def has_peer_asn_filter(self) -> BGPPeerFilterItem:
        """Return if we filter on peer ASNs."""
        return self.filter_policy.peer_asns

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
