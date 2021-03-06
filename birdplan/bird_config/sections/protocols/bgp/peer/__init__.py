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
import re

from .peer_attributes import (
    BGPPeerAttributes,
    BGPPeerFilterPolicy,
    BGPPeerFilterItem,
    BGPPeerLargeCommunities,
    BGPPeerLocation,
    BGPPeerPrefixLimit,
    BGPPeerPrepend,
    BGPPeerRoutePolicyAccept,
    BGPPeerRoutePolicyRedistribute,
    BGPPeerConstraints,
)

from ..bgp_attributes import BGPAttributes, BGPPeertypeConstraints
from ..bgp_functions import BGPFunctions
from ..typing import BGPPeerConfig
from ...pipe import ProtocolPipe, ProtocolPipeFilterType
from ...base import SectionProtocolBase
from ....constants import SectionConstants
from ....functions import BirdVariable, SectionFunctions
from ....tables import SectionTables
from ..... import util
from .....globals import BirdConfigGlobals
from ......bgpq3 import BGPQ3
from ......exceptions import BirdPlanError
from ......peeringdb import PeeringDB


class ProtocolBGPPeer(SectionProtocolBase):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """BIRD BGP protocol peer configuration."""

    _bgp_attributes: BGPAttributes
    _bgp_functions: BGPFunctions
    _peer_attributes: BGPPeerAttributes
    _state: Dict[str, Any]

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
        self._state = {}

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

        #
        # bgp:peers:$PEER:outgoing_large_communities
        #

        # Check for outgoing_large_communities we need to setup
        if "outgoing_large_communities" in peer_config:
            # Add outgoing_large_communities configuration
            if isinstance(peer_config["outgoing_large_communities"], dict):
                # Check if we're adding large communities to blackhole routes
                if "blackhole" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["blackhole"])
                    self.large_communities.outgoing.kernel_blackhole = lc_option
                    self.large_communities.outgoing.static_blackhole = lc_option
                    self.large_communities.outgoing.bgp_customer_blackhole = lc_option
                    self.large_communities.outgoing.bgp_own_blackhole = lc_option
                # Check if we're adding large communities to default routes
                if "default" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["default"])
                    self.large_communities.outgoing.kernel_default = lc_option
                    self.large_communities.outgoing.originated_default = lc_option
                    self.large_communities.outgoing.static_default = lc_option
                    self.large_communities.outgoing.bgp_own_default = lc_option
                    self.large_communities.outgoing.bgp_transit_default = lc_option
                # Check if we're adding outgoing large communitiesing to all BGP routes
                if "bgp" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["bgp"])
                    self.large_communities.outgoing.bgp_customer = lc_option
                    self.large_communities.outgoing.bgp_customer_blackhole = lc_option
                    self.large_communities.outgoing.bgp_own = lc_option
                    self.large_communities.outgoing.bgp_own_blackhole = lc_option
                    self.large_communities.outgoing.bgp_own_default = lc_option
                    self.large_communities.outgoing.bgp_peering = lc_option
                    self.large_communities.outgoing.bgp_transit = lc_option
                    self.large_communities.outgoing.bgp_transit_default = lc_option
                # Check if we're adding outgoing large communities to all BGP blackhole routes
                if "bgp_blackhole" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["bgp_blackhole"])
                    self.large_communities.outgoing.bgp_customer_blackhole = lc_option
                    self.large_communities.outgoing.bgp_own_blackhole = lc_option
                # Check if we're adding outgoing large communities to all BGP default routes
                if "bgp_default" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["bgp_default"])
                    self.large_communities.outgoing.bgp_own_default = lc_option
                    self.large_communities.outgoing.bgp_transit_default = lc_option
                # Check if we're adding outgoing large communities to all customer BGP routes
                if "bgp_customer" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["bgp_customer"])
                    self.large_communities.outgoing.bgp_customer_blackhole = lc_option
                # Check if we're adding outgoing large communities to all our own BGP routes
                if "bgp_own" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["bgp_own"])
                    self.large_communities.outgoing.bgp_own_blackhole = lc_option
                    self.large_communities.outgoing.bgp_own_default = lc_option
                # Check if we're adding outgoing large communities to all transit BGP routes
                if "bgp_transit" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["bgp_transit"])
                    self.large_communities.outgoing.bgp_transit_default = lc_option
                # Check if we're adding outgoing large communities to all kernel routes
                if "kernel" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["kernel"])
                    self.large_communities.outgoing.kernel_blackhole = lc_option
                    self.large_communities.outgoing.kernel_default = lc_option
                # Check if we're adding outgoing large communities to all originated routes
                if "originated" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["originated"])
                    self.large_communities.outgoing.originated_default = lc_option
                # Check if we're adding outgoing large communities to all static routes
                if "static" in peer_config["outgoing_large_communities"]:
                    lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"]["static"])
                    self.large_communities.outgoing.static_blackhole = lc_option
                    self.large_communities.outgoing.static_default = lc_option

                for lc_type, lc_config in peer_config["outgoing_large_communities"].items():
                    if lc_type not in (
                        "bgp",
                        "bgp_blackhole",
                        "bgp_customer_blackhole",
                        "bgp_customer",
                        "bgp_default",
                        "bgp_own_blackhole",
                        "bgp_own_default",
                        "bgp_own",
                        "bgp_peering",
                        "bgp_transit_default",
                        "bgp_transit",
                        "blackhole",
                        "connected",
                        "default",
                        "kernel",
                        "kernel_blackhole",
                        "kernel_default",
                        "originated",
                        "originated_default",
                        "static",
                        "static_blackhole",
                        "static_default",
                    ):
                        raise BirdPlanError(
                            f"BGP peer 'outgoing_large_communities' configuration '{lc_type}' for peer '{self.name}' with type "
                            f"'{self.peer_type}' is invalid"
                        )
                    # Check that we're not doing something stupid
                    if self.peer_type in ("peer", "routecollector", "routeserver", "transit"):
                        if lc_type in (
                            "bgp_default",
                            "bgp_own_default",
                            "bgp_peering",
                            "bgp_transit",
                            "bgp_transit_default",
                            "default",
                            "kernel_default",
                            "originated_default",
                            "static_default",
                        ):
                            raise BirdPlanError(
                                f"Having 'outgoing_large_communities:{lc_type}' specified for peer '{self.name}' "
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
                        if lc_type in (
                            "bgp_blackhole",
                            "bgp_customer_blackhole",
                            "bgp_own_blackhole",
                            "blackhole",
                            "kernel_blackhole",
                            "static_blackhole",
                        ):
                            raise BirdPlanError(
                                f"Having 'outgoing_large_communities:{lc_type}' specified for peer '{self.name}' "
                                f"with type '{self.peer_type}' makes no sense"
                            )
                    # Exclude virtual options "bgp" and "default" from being set
                    if lc_type not in ("bgp", "bgp_blackhole", "bgp_default", "blackhole", "default"):
                        # Set the community list
                        setattr(self.large_communities.outgoing, lc_type, util.sanitize_community_list(lc_config))
            # If its just a number set the count
            else:
                lc_option = util.sanitize_community_list(peer_config["outgoing_large_communities"])
                self.large_communities.outgoing.connected = lc_option
                self.large_communities.outgoing.kernel = lc_option
                self.large_communities.outgoing.kernel_default = lc_option
                self.large_communities.outgoing.kernel_blackhole = lc_option
                self.large_communities.outgoing.originated = lc_option
                self.large_communities.outgoing.originated_default = lc_option
                self.large_communities.outgoing.static = lc_option
                self.large_communities.outgoing.static_blackhole = lc_option
                self.large_communities.outgoing.static_default = lc_option
                self.large_communities.outgoing.bgp_customer = lc_option
                self.large_communities.outgoing.bgp_customer_blackhole = lc_option
                self.large_communities.outgoing.bgp_own = lc_option
                self.large_communities.outgoing.bgp_own_blackhole = lc_option
                self.large_communities.outgoing.bgp_own_default = lc_option
                self.large_communities.outgoing.bgp_peering = lc_option
                self.large_communities.outgoing.bgp_transit = lc_option
                self.large_communities.outgoing.bgp_transit_default = lc_option

        # Turn on passive mode for route reflectors and customers
        if self.peer_type in ("customer", "rrclient"):
            self.passive = True
        # But allow it to be set manually
        if "passive" in peer_config:
            self.passive = peer_config["passive"]

        # Default redistribution settings based on peer type
        if self.peer_type in (
            "customer",
            "internal",
            "routecollector",
            "routeserver",
            "rrclient",
            "rrserver",
            "rrserver-rrserver",
            "peer",
            "transit",
        ):
            self.route_policy_redistribute.bgp_own = True
            self.route_policy_redistribute.bgp_customer = True
        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.route_policy_redistribute.bgp_peering = True
            self.route_policy_redistribute.bgp_transit = True
        # Default redistribution settings based on route type
        if self.peer_type in ("internal", "routecollector", "routeserver", "rrclient", "rrserver", "rrserver-rrserver", "transit"):
            self.route_policy_redistribute.bgp_customer_blackhole = True
            self.route_policy_redistribute.bgp_own_blackhole = True
        if self.peer_type == "rrserver-rrserver":
            self.route_policy_redistribute.bgp_own_default = True
            self.route_policy_redistribute.bgp_transit_default = True

        # Work out what we're going to be redistributing
        if "redistribute" in peer_config:
            # Check if we're disabling BGP redistribution
            if "bgp" in peer_config["redistribute"] and not peer_config["redistribute"]["bgp"]:
                self.route_policy_redistribute.bgp_customer = False
                self.route_policy_redistribute.bgp_own = False
                self.route_policy_redistribute.bgp_peering = False
                self.route_policy_redistribute.bgp_transit = False
                self.route_policy_redistribute.bgp_customer_blackhole = False
                self.route_policy_redistribute.bgp_own_blackhole = False
                self.route_policy_redistribute.bgp_own_default = False
                self.route_policy_redistribute.bgp_transit_default = False
            # Disable customer blackhole routes by default if we're not redistributing customer BGP routes
            if "bgp_customer" in peer_config["redistribute"] and not peer_config["redistribute"]["bgp_customer"]:
                self.route_policy_redistribute.bgp_customer_blackhole = False
            # Disable own blackhole and default routes by default if we're not redistributing our own BGP routes
            if "bgp_own" in peer_config["redistribute"] and not peer_config["redistribute"]["bgp_own"]:
                self.route_policy_redistribute.bgp_own_blackhole = False
                self.route_policy_redistribute.bgp_own_default = False
            # Disable transit default routes by default if we're not redistributing transit BGP routes
            if "bgp_transit" in peer_config["redistribute"] and not peer_config["redistribute"]["bgp_transit"]:
                self.route_policy_redistribute.bgp_transit_default = False

            # Process each option individually now...
            for redistribute_type, redistribute_config in peer_config["redistribute"].items():
                if redistribute_type not in (
                    "bgp",
                    "bgp_customer",
                    "bgp_customer_blackhole",
                    "bgp_own",
                    "bgp_own_blackhole",
                    "bgp_own_default",
                    "bgp_peering",
                    "bgp_transit",
                    "bgp_transit_default",
                    "connected",
                    "kernel",
                    "kernel_blackhole",
                    "kernel_default",
                    "originated",
                    "originated_default",
                    "static",
                    "static_blackhole",
                    "static_default",
                ):
                    raise BirdPlanError(f"The BGP redistribute type '{redistribute_type}' is not known")
                # "bgp" is set above as defaults
                if redistribute_type != "bgp":
                    setattr(self.route_policy_redistribute, redistribute_type, redistribute_config)
        # Do a sanity check on our redistribution
        if self.peer_type not in (
            "internal",
            "routeserver",
            "routecollector",
            "rrclient",
            "rrserver",
            "rrserver-rrserver",
            "transit",
        ):
            # We should not redistribute blackhole routes to peers types customer and peer
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
            if self.route_policy_redistribute.bgp_customer_blackhole:
                raise BirdPlanError(
                    f"Having 'redistribute:bgp_customer_blackhole' set to True for peer '{self.name}' "
                    f"with type '{self.peer_type}' makes no sense"
                )
            if self.route_policy_redistribute.bgp_own_blackhole:
                raise BirdPlanError(
                    f"Having 'redistribute:bgp_own_blackhole' set to True for peer '{self.name}' "
                    f"with type '{self.peer_type}' makes no sense"
                )
        if self.peer_type in ("peer", "routecollector", "routeserver", "transit"):
            # We should not be distributing default routes to non-customer eBGP peers
            if self.route_policy_redistribute.kernel_default:
                raise BirdPlanError(
                    f"Having 'redistribute:kernel_default' set to True for peer '{self.name}' with type '{self.peer_type}' makes "
                    "no sense"
                )
            if self.route_policy_redistribute.originated_default:
                raise BirdPlanError(
                    f"Having 'redistribute:originated_default' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "makes no sense"
                )
            if self.route_policy_redistribute.static_default:
                raise BirdPlanError(
                    f"Having 'redistribute:static_default' set to True for peer '{self.name}' with type '{self.peer_type}' makes "
                    "no sense"
                )
            # We should not be redistributing peering routes or transit routes to non-customer eBGP peers
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
            # We should not redistribute default routes to non customer eBGP peer types
            if self.route_policy_redistribute.bgp_own_default:
                raise BirdPlanError(
                    f"Having 'redistribute:bgp_own_default' set to True for peer '{self.name}' "
                    f"with type '{self.peer_type}' makes no sense"
                )
            if self.route_policy_redistribute.bgp_transit_default:
                raise BirdPlanError(
                    f"Having 'redistribute:bgp_transit_default' set to True for peer '{self.name}' "
                    f"with type '{self.peer_type}' makes no sense"
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
            if self.has_ipv4:
                if "prefix_limit4" not in peer_config:
                    self.prefix_limit4 = "peeringdb"
                else:
                    self.prefix_limit4 = peer_config["prefix_limit4"]
            if self.has_ipv6:
                if "prefix_limit6" not in peer_config:
                    self.prefix_limit6 = "peeringdb"
                else:
                    self.prefix_limit6 = peer_config["prefix_limit6"]
        # Having a prefix limit set for anything other than the above peer types makes no sense
        else:
            if "prefix_limit4" in peer_config:
                raise BirdPlanError(
                    f"Having 'prefix_limit4' set for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )
            if "prefix_limit6" in peer_config:
                raise BirdPlanError(
                    f"Having 'prefix_limit6' set for peer '{self.name}' with type '{self.peer_type}' makes no sense"
                )

        # Check for filters we need to setup
        if "filter" in peer_config:
            # Raise an exception if filters makes no sense for this peer type
            if self.peer_type == "routecollector":
                raise BirdPlanError(f"Having 'filter' specified for peer '{self.name}' with type '{self.peer_type}' makes no sense")
            # Add filters
            for filter_type, filter_config in peer_config["filter"].items():
                if filter_type not in ("as_sets", "aspath_asns", "origin_asns", "peer_asns", "prefixes"):
                    raise BirdPlanError(
                        f"BGP peer 'filter' configuration '{filter_type}' for peer '{self.name}' with type '{self.peer_type}' "
                        "is invalid"
                    )
                # Set filter policy
                setattr(self.filter_policy, filter_type, filter_config)

        #
        # bgp:peers:$PPER:accept
        #

        # Check if we should accept our own blackhole routes
        if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.route_policy_accept.bgp_own_blackhole = True
            self.route_policy_accept.bgp_customer_blackhole = True
        # Check if we should be accepting customer blackhole routes
        if self.peer_type == "customer" and self.has_prefix_filter:
            self.route_policy_accept.bgp_customer_blackhole = True

        # If this is a rrserver to rrserver peer, we need to by default redistribute the default route (if we have one)
        if self.peer_type == "rrserver-rrserver":
            self.route_policy_accept.bgp_own_default = True
            self.route_policy_accept.bgp_transit_default = True

        # Get peer configuration and set our attributes
        if "accept" in peer_config:
            for accept_type, accept_config in peer_config["accept"].items():
                if accept_type not in ("bgp_customer_blackhole", "bgp_own_blackhole", "bgp_own_default", "bgp_transit_default"):
                    raise BirdPlanError(
                        f"BGP peer 'accept' configuration '{accept_type}' for peer '{self.name}' with type '{self.peer_type}'"
                        " is invalid"
                    )
                # Set route policy accept
                setattr(self.route_policy_accept, accept_type, accept_config)

        # Check bgp:accept:bgp_customer_blackhole
        if self.peer_type not in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.route_policy_accept.bgp_customer_blackhole:
                raise BirdPlanError(
                    f"Having 'accept:bgp_customer_blackhole' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "makes no sense"
                )
        # Internal peer type checks
        if self.peer_type not in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            # Check bgp:accept:bgp_own_blackhole
            if self.route_policy_accept.bgp_own_blackhole:
                raise BirdPlanError(
                    f"Having 'accept:bgp_own_blackhole' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "makes no sense"
                )
            # Check bgp:accept:bgp_own_blackhole
            if self.route_policy_accept.bgp_own_default:
                raise BirdPlanError(
                    f"Having 'accept:bgp_own_default' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "makes no sense"
                )
        # Check bgp:accept:bgp_transit_default
        if self.peer_type not in ("internal", "rrclient", "rrserver", "rrserver-rrserver", "transit"):
            if self.route_policy_accept.bgp_transit_default:
                raise BirdPlanError(
                    f"Having 'accept:bgp_transit_default' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "makes no sense"
                )
        # Check if this is a customer with blackholing and without a prefix filter set
        if self.peer_type == "customer":
            if self.route_policy_accept.bgp_customer_blackhole and not self.has_prefix_filter:
                raise BirdPlanError(
                    f"Having 'accept:bgp_customer_blackhole' set to True for peer '{self.name}' with type '{self.peer_type}' "
                    "and without 'filter:prefixes' or 'filter:as_sets' set makes no sense"
                )

        #
        # bgp:peers:$PEER:prepend
        #

        # Check for prepending we need to setup
        if "prepend" in peer_config:
            # Add prepending configuration
            if isinstance(peer_config["prepend"], dict):
                # Check if we're prepending blackhole routes
                if "blackhole" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["blackhole"]
                    self.prepend.kernel_blackhole.own_asn = prepend_option
                    self.prepend.static_blackhole.own_asn = prepend_option
                    self.prepend.bgp_customer_blackhole.own_asn = prepend_option
                    self.prepend.bgp_own_blackhole.own_asn = prepend_option
                # Check if we're prepending default routes
                if "default" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["default"]
                    self.prepend.kernel_default.own_asn = prepend_option
                    self.prepend.originated_default.own_asn = prepend_option
                    self.prepend.static_default.own_asn = prepend_option
                    self.prepend.bgp_own_default.own_asn = prepend_option
                    self.prepend.bgp_transit_default.own_asn = prepend_option
                # Check if we're prepending all BGP routes
                if "bgp" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["bgp"]
                    self.prepend.bgp_customer.own_asn = prepend_option
                    self.prepend.bgp_customer_blackhole.own_asn = prepend_option
                    self.prepend.bgp_own.own_asn = prepend_option
                    self.prepend.bgp_own_blackhole.own_asn = prepend_option
                    self.prepend.bgp_own_default.own_asn = prepend_option
                    self.prepend.bgp_peering.own_asn = prepend_option
                    self.prepend.bgp_transit.own_asn = prepend_option
                    self.prepend.bgp_transit_default.own_asn = prepend_option
                # Check if we're prepending all BGP blackhole routes
                if "bgp_blackhole" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["bgp_blackhole"]
                    self.prepend.bgp_customer_blackhole.own_asn = prepend_option
                    self.prepend.bgp_own_blackhole.own_asn = prepend_option
                # Check if we're prepending all BGP default routes
                if "bgp_default" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["bgp_default"]
                    self.prepend.bgp_transit_default.own_asn = prepend_option
                    self.prepend.bgp_own_default.own_asn = prepend_option
                # Check if we're prepending all customer BGP routes
                if "bgp_customer" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["bgp_customer"]
                    self.prepend.bgp_customer_blackhole.own_asn = prepend_option
                # Check if we're prepending all our own BGP routes
                if "bgp_own" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["bgp_own"]
                    self.prepend.bgp_own_blackhole.own_asn = prepend_option
                    self.prepend.bgp_own_default.own_asn = prepend_option
                # Check if we're prepending all transit BGP routes
                if "bgp_transit" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["bgp_transit"]
                    self.prepend.bgp_transit_default.own_asn = prepend_option
                # Check if we're prepending all kernel routes
                if "kernel" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["kernel"]
                    self.prepend.kernel_blackhole.own_asn = prepend_option
                    self.prepend.kernel_default.own_asn = prepend_option
                # Check if we're prepending all originated routes
                if "originated" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["originated"]
                    self.prepend.originated_default.own_asn = prepend_option
                # Check if we're prepending all static routes
                if "static" in peer_config["prepend"]:
                    prepend_option = peer_config["prepend"]["static"]
                    self.prepend.static_blackhole.own_asn = prepend_option
                    self.prepend.static_default.own_asn = prepend_option

                for prepend_type, prepend_config in peer_config["prepend"].items():
                    if prepend_type not in (
                        "bgp",
                        "bgp_blackhole",
                        "bgp_customer",
                        "bgp_customer_blackhole",
                        "bgp_default",
                        "bgp_own",
                        "bgp_own_blackhole",
                        "bgp_own_default",
                        "bgp_peering",
                        "bgp_transit",
                        "bgp_transit_default",
                        "blackhole",
                        "connected",
                        "default",
                        "kernel",
                        "kernel_blackhole",
                        "kernel_default",
                        "originated",
                        "originated_default",
                        "static",
                        "static_blackhole",
                        "static_default",
                    ):
                        raise BirdPlanError(
                            f"BGP peer 'prepend' configuration '{prepend_type}' for peer '{self.name}' with type "
                            f"'{self.peer_type}' is invalid"
                        )
                    # Check that we're not doing something stupid
                    if self.peer_type in ("peer", "routecollector", "routeserver", "transit"):
                        if prepend_type in (
                            "bgp_default",
                            "default",
                            "kernel_default",
                            "static_default",
                            "originated_default",
                            "bgp_own_default",
                            "bgp_peering",
                            "bgp_transit",
                            "bgp_transit_default",
                        ):
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
                        if prepend_type in (
                            "bgp_blackhole",
                            "blackhole",
                            "kernel_blackhole",
                            "static_blackhole",
                            "bgp_customer_blackhole",
                            "bgp_own_blackhole",
                        ):
                            raise BirdPlanError(
                                f"Having 'prepend:{prepend_type}' specified for peer '{self.name}' with type '{self.peer_type}' "
                                "makes no sense"
                            )
                    # Exclude virtual options "bgp" and "default" from being set
                    if prepend_type not in ("bgp", "bgp_blackhole", "bgp_default", "blackhole", "default"):
                        # Grab the prepend attribute
                        prepend_attr = getattr(self.prepend, prepend_type)
                        # Set prepend count
                        setattr(prepend_attr, "own_asn", prepend_config)
            # If its just a number set the count
            else:
                prepend_option = peer_config["prepend"]
                self.prepend.bgp_customer.own_asn = prepend_option
                self.prepend.bgp_customer_blackhole.own_asn = prepend_option
                self.prepend.bgp_own.own_asn = prepend_option
                self.prepend.bgp_own_blackhole.own_asn = prepend_option
                self.prepend.bgp_own_default.own_asn = prepend_option
                self.prepend.bgp_peering.own_asn = prepend_option
                self.prepend.bgp_transit.own_asn = prepend_option
                self.prepend.bgp_transit_default.own_asn = prepend_option
                self.prepend.connected.own_asn = prepend_option
                self.prepend.kernel.own_asn = prepend_option
                self.prepend.kernel_blackhole.own_asn = prepend_option
                self.prepend.kernel_default.own_asn = prepend_option
                self.prepend.originated.own_asn = prepend_option
                self.prepend.originated_default.own_asn = prepend_option
                self.prepend.static.own_asn = prepend_option
                self.prepend.static_blackhole.own_asn = prepend_option
                self.prepend.static_default.own_asn = prepend_option

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

        # Setup our constraint overrides
        if "constraints" in peer_config:
            for constraint_name, constraint_value in peer_config["constraints"].items():
                if constraint_name not in (
                    "blackhole_import_maxlen4",
                    "blackhole_import_minlen4",
                    "blackhole_export_maxlen4",
                    "blackhole_export_minlen4",
                    "blackhole_import_maxlen6",
                    "blackhole_import_minlen6",
                    "blackhole_export_maxlen6",
                    "blackhole_export_minlen6",
                    "import_maxlen4",
                    "import_minlen4",
                    "export_maxlen4",
                    "export_minlen4",
                    "import_maxlen6",
                    "import_minlen6",
                    "export_maxlen6",
                    "export_minlen6",
                    "aspath_import_maxlen",
                    "aspath_import_minlen",
                    "community_import_maxlen",
                    "extended_community_import_maxlen",
                    "large_community_import_maxlen",
                ):
                    raise BirdPlanError(
                        f"BGP peer 'constraints' configuration '{constraint_name}' for peer '{self.name}' with type "
                        f"'{self.peer_type}' is invalid"
                    )
                # Make sure this peer supports blackhole imports
                if constraint_name.startswith("blackhole_import_"):
                    if self.peer_type not in (
                        "customer",
                        "internal",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                    ):
                        raise BirdPlanError(
                            f"Having '{constraint_name}' specified for peer '{self.name}' with type '{self.peer_type}' "
                            "makes no sense"
                        )
                # Make sure this peer accepts blackhole exports
                if constraint_name.startswith("blackhole_export_"):
                    if self.peer_type not in (
                        "internal",
                        "routeserver",
                        "routecollector",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        raise BirdPlanError(
                            f"Having '{constraint_name}' specified for peer '{self.name}' with type '{self.peer_type}' "
                            "makes no sense"
                        )
                # Make sure this peer supports imports
                if "import" in constraint_name:
                    if self.peer_type not in (
                        "customer",
                        "internal",
                        "peer",
                        "routeserver",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        raise BirdPlanError(
                            f"Having '{constraint_name}' specified for peer '{self.name}' with type '{self.peer_type}' "
                            "makes no sense"
                        )
                # Set constraint
                setattr(self.constraints, constraint_name, constraint_value)

        #
        # NETWORK RELATED QUERIES
        #
        prev_state = {}
        if (
            "bgp" in self.birdconfig_globals.state
            and "peers" in self.birdconfig_globals.state["bgp"]
            and self.name in self.birdconfig_globals.state["bgp"]["peers"]
        ):
            prev_state = self.birdconfig_globals.state["bgp"]["peers"][self.name]

        # Work out the prefix limits...
        if self.prefix_limit4 == "peeringdb" or self.prefix_limit6 == "peeringdb":
            # Grab PeeringDB entries
            peeringdb = PeeringDB()
            peeringdb_info = peeringdb.get_prefix_limits(self.asn)

            # Check if we're setting our IPv4 prefix limit from peeringdb
            if self.prefix_limit4 == "peeringdb":
                # Sanity checks
                if (
                    "prefix_limit" in prev_state
                    and "peeringdb" in prev_state["prefix_limit"]
                    and "ipv4" in prev_state["prefix_limit"]["peeringdb"]
                ):
                    # Check if there was a substantial reduction in number of prefixes allowed
                    if peeringdb_info["info_prefixes4"] * 2 < prev_state["prefix_limit"]["peeringdb"]["ipv4"]:
                        raise BirdPlanError(
                            f"PeeringDB IPv4 prefix limit for peer '{self.name}' decreased substantially from previous run: "
                            "last=%s, now=%s" % (prev_state["prefix_limit"]["peeringdb"]["ipv4"], peeringdb_info["info_prefixes4"])
                        )
                    # Check if there was a substantial increase in number of prefixes allowed
                    if peeringdb_info["info_prefixes4"] / 2 > prev_state["prefix_limit"]["peeringdb"]["ipv4"]:
                        raise BirdPlanError(
                            f"PeeringDB IPv4 prefix limit for peer '{self.name}' increased substantially from previous run: "
                            "last=%s, now=%s" % (prev_state["prefix_limit"]["peeringdb"]["ipv4"], peeringdb_info["info_prefixes4"])
                        )
                # Set the limits
                self.prefix_limit4 = None
                self.prefix_limit4_peeringdb = peeringdb_info["info_prefixes4"]

            # Check if we're setting our IPv6 prefix limit from peeringdb
            if self.prefix_limit6 == "peeringdb":
                # Sanity checks
                if (
                    "prefix_limit" in prev_state
                    and "peeringdb" in prev_state["prefix_limit"]
                    and "ipv6" in prev_state["prefix_limit"]["peeringdb"]
                ):
                    # Check if there was a substantial reduction in number of prefixes allowed
                    if peeringdb_info["info_prefixes6"] * 2 < prev_state["prefix_limit"]["peeringdb"]["ipv6"]:
                        raise BirdPlanError(
                            f"PeeringDB IPv6 prefix limit for peer '{self.name}' decreased substantially from previous run: "
                            "last=%s, now=%s" % (prev_state["prefix_limit"]["peeringdb"]["ipv6"], peeringdb_info["info_prefixes6"])
                        )
                    # Check if there was a substantial increase in number of prefixes allowed
                    if peeringdb_info["info_prefixes6"] / 2 > prev_state["prefix_limit"]["peeringdb"]["ipv6"]:
                        raise BirdPlanError(
                            f"PeeringDB IPv6 prefix limit for peer '{self.name}' increased substantially from previous run: "
                            "last=%s, now=%s" % (prev_state["prefix_limit"]["peeringdb"]["ipv6"], peeringdb_info["info_prefixes6"])
                        )
                # Set the limits
                self.prefix_limit6 = None
                self.prefix_limit6_peeringdb = peeringdb_info["info_prefixes6"]

        # Check if we're going to be pulling in AS-SET information
        if self.filter_policy.as_sets:
            # Grab BGPQ3 object to use below
            bgpq3 = BGPQ3()

            # Grab ASNs from IRR
            irr_asns = bgpq3.get_asns(self.filter_policy.as_sets)
            # If we have results populate our IRR origin ASN list
            if irr_asns:
                self.filter_policy.origin_asns_irr.extend(irr_asns)

            # Grab IRR prefixes
            irr_prefixes = bgpq3.get_prefixes(self.filter_policy.as_sets)
            # Lets work out what to do with the IPv4 prefixes
            if irr_prefixes["ipv4"]:
                # Sanity checks for IPv4 network count
                if (
                    "filter" in prev_state
                    and "prefixes" in prev_state["filter"]
                    and "irr" in prev_state["filter"]["prefixes"]
                    and "ipv4" in prev_state["filter"]["prefixes"]["irr"]
                ):
                    # Check if there was a substantial reduction in number of prefixes allowed
                    new_network_count = util.network_count(irr_prefixes["ipv4"])
                    old_network_count = util.network_count(prev_state["filter"]["prefixes"]["irr"]["ipv4"])
                    if new_network_count * 2 < old_network_count:
                        raise BirdPlanError(
                            f"IRR IPv4 network count for peer '{self.name}' decreased substantially from previous run: "
                            "last=%s, now=%s" % (old_network_count, new_network_count)
                        )
                    # Check if there was a substantial increase in number of prefixes allowed
                    if new_network_count / 2 > old_network_count:
                        raise BirdPlanError(
                            f"IRR IPv4 network count for peer '{self.name}' increased substantially from previous run: "
                            "last=%s, now=%s" % (old_network_count, new_network_count)
                        )
                # All looks good, add them
                self.filter_policy.prefixes_irr.extend(irr_prefixes["ipv4"])
            # Lets work out what to do with the IPv6 prefixes
            if irr_prefixes["ipv6"]:
                # Sanity checks for IPv6 network count
                if (
                    "filter" in prev_state
                    and "prefixes" in prev_state["filter"]
                    and "irr" in prev_state["filter"]["prefixes"]
                    and "ipv6" in prev_state["filter"]["prefixes"]["irr"]
                ):
                    # Check if there was a substantial reduction in number of prefixes allowed
                    new_network_count = util.network_count(irr_prefixes["ipv6"])
                    old_network_count = util.network_count(prev_state["filter"]["prefixes"]["irr"]["ipv6"])
                    if new_network_count * 2 < old_network_count:
                        raise BirdPlanError(
                            f"IRR IPv6 network count for peer '{self.name}' decreased substantially from previous run: "
                            "last=%s, now=%s" % (old_network_count, new_network_count)
                        )
                    # Check if there was a substantial increase in number of prefixes allowed
                    if new_network_count / 2 > old_network_count:
                        raise BirdPlanError(
                            f"IRR IPv6 network count for peer '{self.name}' increased substantially from previous run: "
                            "last=%s, now=%s" % (old_network_count, new_network_count)
                        )
                # All looks good, add them
                self.filter_policy.prefixes_irr.extend(irr_prefixes["ipv6"])

    def configure(self) -> None:
        """Configure BGP peer."""
        super().configure()

        # Save basic peer information
        self.state["asn"] = self.asn
        self.state["description"] = self.description

        # Check for some config options we also need to save
        if self.prefix_limit4:
            if "prefix_limit" not in self.state:
                self.state["prefix_limit"] = {}
            if self.prefix_limit4_peeringdb:
                # Make sure we have a peeringdb attribute
                if "peeringdb" not in self.state["prefix_limit"]:
                    self.state["prefix_limit"]["peeringdb"] = {}
                # Add our peeringdb IPv4 limit
                self.state["prefix_limit"]["peeringdb"]["ipv4"] = self.prefix_limit4_peeringdb
            else:
                # Make sure we have a static attribute
                if "static" not in self.state["prefix_limit"]:
                    self.state["prefix_limit"]["static"] = {}
                # Add our static IPv4 limit
                self.state["prefix_limit"]["static"]["ipv4"] = self.prefix_limit4
        if self.prefix_limit6:
            if "prefix_limit" not in self.state:
                self.state["prefix_limit"] = {}
            if self.prefix_limit6_peeringdb:
                # Make sure we have a peeringdb attribute
                if "peeringdb" not in self.state["prefix_limit"]:
                    self.state["prefix_limit"]["peeringdb"] = {}
                # Add our peeringdb IPv6 limit
                self.state["prefix_limit"]["peeringdb"]["ipv6"] = self.prefix_limit6_peeringdb
            else:
                # Make sure we have a static attribute
                if "static" not in self.state["prefix_limit"]:
                    self.state["prefix_limit"]["static"] = {}
                # Add our static IPv6 limit
                self.state["prefix_limit"]["static"]["ipv6"] = self.prefix_limit6

        self.conf.add("")
        self.conf.add(f"# Peer type: {self.peer_type}")
        self.conf.add("")

        # Setup routing tables
        self._setup_peer_tables()

        # Setup ASN lists
        self._setup_aspath_asns()
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

        # Make sure our state exists
        if "bgp" not in self.birdconfig_globals.state:
            self.birdconfig_globals.state["bgp"] = {}
        if "peers" not in self.birdconfig_globals.state["bgp"]:
            self.birdconfig_globals.state["bgp"]["peers"] = {}

        # Save our configuration
        self.birdconfig_globals.state["bgp"]["peers"][self.name] = self.state

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

    def import_blackhole_prefix_list_name(self, ipv: str) -> str:
        """Return our blackhole prefix list name."""
        return f"bgp{ipv}_AS{self.asn}_{self.name}_blackhole_prefixes_import"

    def _setup_peer_tables(self) -> None:
        """Peering routing table setup."""

        # Start with no tables as we can have IPv4 and/or IPv6 tables below
        state_tables = {}

        self.tables.conf.append(f"# BGP Peer Tables: {self.asn} - {self.name}")

        # Only create an IPv4 table if we have IPv4 configuration
        if self.has_ipv4:
            self.tables.conf.append(f"ipv4 table {self.bgp_table_name('4')};")
            state_tables["ipv4"] = self.bgp_table_name("4")

        # Only create an IPv6 table if we have IPv6 configuration
        if self.has_ipv6:
            self.tables.conf.append(f"ipv6 table {self.bgp_table_name('6')};")
            state_tables["ipv6"] = self.bgp_table_name("6")

        self.tables.conf.append("")

        # Store our BGP table names
        self.state["tables"] = state_tables

    def _setup_aspath_asns(self) -> None:
        """AS-PATH ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_aspath_asn_filter:
            return

        state = {}

        aspath_asns = []
        calculated_aspath_asns = []

        # If we're a "customer" or "peer", make sure the aspath_asns list has our own ASN
        if self.peer_type in ("customer", "peer"):
            aspath_asns.append("# Peer ASN automatically added")
            aspath_asns.append(f"{self.asn}")

        # Populate AS-PATH ASN list
        if self.filter_policy.aspath_asns:
            # Store static filter info in our state
            state["static"] = self.filter_policy.aspath_asns
            # Loop with ASNs specified in configuration
            for asn in self.filter_policy.aspath_asns:
                if asn not in aspath_asns:
                    aspath_asns.append(f"{asn}")
                if asn not in calculated_aspath_asns:
                    calculated_aspath_asns.append(asn)
            aspath_asns.insert(0, f"# Explicitly defined {len(aspath_asns)} items")

        # If we're a "customer" or "peer", pull in the origin_asns and irr_asns lists
        if self.peer_type in ("customer", "peer"):
            # Check if we can add our ORIGIN ASNs
            if self.filter_policy.origin_asns:
                extra_aspath_asns = []
                # Loop with ASNs specified in configuration
                for asn in self.filter_policy.origin_asns:
                    # Make sure we don't add duplicates
                    if asn not in aspath_asns and asn not in extra_aspath_asns:
                        extra_aspath_asns.append(f"{asn}")
                    if asn not in calculated_aspath_asns:
                        calculated_aspath_asns.append(asn)
                # If we're a "customer" or "peer", pull in the origin_asns into our aspath_asns list
                aspath_asns.append(f"# Explicitly defined {len(extra_aspath_asns)} items")
                aspath_asns.extend(extra_aspath_asns)

            # Check if we got results, if so add the IRR ASNs to the aspath_asns list
            if self.filter_policy.origin_asns_irr:
                extra_aspath_asns = []
                # Loop with ASNs retrieved from IRR records
                for asn in self.filter_policy.origin_asns_irr:
                    if asn not in aspath_asns and asn not in extra_aspath_asns:
                        extra_aspath_asns.append(f"{asn}")
                    if asn not in calculated_aspath_asns:
                        calculated_aspath_asns.append(asn)
                    aspath_asns.append(
                        f"# Retrieved {len(extra_aspath_asns)} items from IRR with object '{self.filter_policy.as_sets}'"
                    )
                    aspath_asns.extend(extra_aspath_asns)

        self.conf.add(f"define {self.aspath_asn_list_name} = [")
        # Loop with each line and add commas where needed
        for count, asn in enumerate(aspath_asns):
            asn_str = f"  {asn}"
            if not asn.startswith("#") and count < len(aspath_asns) - 1:
                asn_str += ","
            self.conf.add(asn_str)
        self.conf.add("];")
        self.conf.add("")

        # Store calculated aspath filter info in our state
        state["calculated"] = calculated_aspath_asns

        # Save state
        if "filter" not in self.state:
            self.state["filter"] = {}
        self.state["filter"]["aspath_asns"] = state

    def _setup_origin_asns(self) -> None:
        """Origin ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_origin_asn_filter:
            return

        state = {}

        origin_asns = []

        # Populate our origin ASN list from configuration
        if self.filter_policy.origin_asns:
            # Store filter info in our state
            state["static"] = self.filter_policy.origin_asns
            # Loop with ASNs specified in configuration
            extra_origin_asns = []
            for asn in self.filter_policy.origin_asns:
                # Make sure we don't add duplicates
                if asn not in origin_asns and asn not in extra_origin_asns:
                    extra_origin_asns.append(f"{asn}")
            origin_asns.append(f"# Explicitly defined {len(extra_origin_asns)} items")
            origin_asns.extend(extra_origin_asns)

        # Grab IRR ASNs
        if self.filter_policy.origin_asns_irr:
            # Store filter info in our state
            state["irr"] = self.filter_policy.origin_asns_irr
            # Loop with ASNs retrieved from IRR records
            extra_origin_asns = []
            for asn in self.filter_policy.origin_asns_irr:
                if asn not in origin_asns and asn not in extra_origin_asns:
                    extra_origin_asns.append(f"{asn}")
            origin_asns.append(f"# Retrieved {len(extra_origin_asns)} items from IRR with object '{self.filter_policy.as_sets}'")
            origin_asns.extend(extra_origin_asns)

        self.conf.add(f"define {self.origin_asn_list_name} = [")
        # Loop with each line and add commas where needed
        for count, asn in enumerate(origin_asns):
            asn_str = f"  {asn}"
            if not asn.startswith("#") and count < len(origin_asns) - 1:
                asn_str += ","
            self.conf.add(asn_str)
        self.conf.add("];")
        self.conf.add("")

        # Save state
        if "filter" not in self.state:
            self.state["filter"] = {}
        self.state["filter"]["origin_asns"] = state

    def _setup_peer_asns(self) -> None:
        """Peer ASN list setup."""

        # Short circuit and exit if we have none
        if not self.has_peer_asn_filter:
            return

        state = {}

        peer_asns = []

        # Add ASN list with comments
        if self.filter_policy.peer_asns:
            # Save our peer ASN list in our state
            state["static"] = self.filter_policy.peer_asns
            peer_asns.append(f"# Explicitly defined {len(self.filter_policy.peer_asns)} items")
            for asn in self.filter_policy.peer_asns:
                peer_asns.append(f"{asn}")

        self.conf.add(f"define {self.peer_asn_list_name} = [")
        # Loop with each line and add commas where needed
        for count, asn in enumerate(peer_asns):
            asn_str = f"  {asn}"
            if not asn.startswith("#") and count < len(peer_asns) - 1:
                asn_str += ","
            self.conf.add(asn_str)
        self.conf.add("];")
        self.conf.add("")

        # Save state
        if "filter" not in self.state:
            self.state["filter"] = {}
        self.state["filter"]["peer_asns"] = state

    def _setup_peer_prefixes(self) -> None:
        """Prefix list setup."""

        # Short circuit and exit if we have none
        if not self.has_prefix_filter:
            return

        state: Dict[str, Dict[str, Any]] = {}

        # Work out prefixes
        prefix_lists: Dict[str, List[str]] = {"4": [], "6": []}
        for prefix in sorted(self.filter_policy.prefixes):
            if ":" in prefix:
                prefix_lists["6"].append(prefix)
            else:
                prefix_lists["4"].append(prefix)
        prefix_lists_irr: Dict[str, List[str]] = {"4": [], "6": []}
        for prefix in sorted(self.filter_policy.prefixes_irr):
            if ":" in prefix:
                prefix_lists_irr["6"].append(prefix)
            else:
                prefix_lists_irr["4"].append(prefix)

        # Output prefix definitions
        for ipv in ["4", "6"]:
            prefix_list = prefix_lists[ipv]
            prefix_list_irr = prefix_lists_irr[ipv]

            prefixes = []
            blackholes = []

            # Add statically defined prefix list
            if prefix_list:
                # Save prefix list in our state
                if "static" not in state:
                    state["static"] = {}
                state["static"][f"ipv{ipv}"] = prefix_list

                for prefix in prefix_list:
                    prefixes.append(prefix)
                    # Add blackhole
                    blackhole = "%s+" % re.split(r"[{+]", prefix, 1)[0]
                    blackholes.append(blackhole)
            # Sort and unique our results
            prefixes = sorted(set(prefixes))
            blackholes = sorted(set(blackholes))
            # Add title for this section
            prefixes.insert(0, f"# {len(prefix_list)} explicitly defined")
            blackholes.insert(0, f"# {len(prefix_list)} explicitly defined")

            # Add prefix list from IRR
            if prefix_list_irr:
                # Save prefix list in our state
                if "irr" not in state:
                    state["irr"] = {}
                state["irr"][f"ipv{ipv}"] = prefix_list_irr

                prefixes_irr = []
                blackholes_irr = []

                # Loop with each prefix we got from IRR
                for prefix in prefix_list_irr:
                    # Make sure we're not making duplicates
                    if prefix not in prefixes:
                        prefixes_irr.append(prefix)
                    # Add blackhole, and make sure we're not duplicating here either
                    blackhole = "%s+" % prefix.split("{", 1)[0]
                    if blackhole not in blackholes:
                        blackholes_irr.append(blackhole)

                # Add title to top of prefixes retrieved via IRR
                prefixes.append(f"# Retrieved {len(prefixes_irr)} items from IRR with object '{self.filter_policy.as_sets}'")
                blackholes.append(f"# Retrieved {len(blackholes_irr)} items from IRR with object '{self.filter_policy.as_sets}'")
                # Extend our lists
                prefixes.extend(prefixes_irr)
                blackholes.extend(blackholes_irr)

            self.conf.add(f"define {self.import_prefix_list_name(ipv)} = [")
            # Loop with each line and add commas where needed
            for count, prefix in enumerate(prefixes):
                prefix_str = f"  {prefix}"
                if not prefix.startswith("#") and count < len(prefixes) - 1:
                    prefix_str += ","
                self.conf.add(prefix_str)
            self.conf.add("];")
            self.conf.add("")

            # We only need to output the blackhole list if the peer is a peertype that we support receiving blackhole prefixes from
            if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
                self.conf.add(f"define {self.import_blackhole_prefix_list_name(ipv)} = [")
                # Loop with each line and add commas where needed
                for count, blackhole in enumerate(blackholes):
                    blackhole_str = f"  {blackhole}"
                    if not blackhole.startswith("#") and count < len(blackholes) - 1:
                        blackhole_str += ","
                    self.conf.add(blackhole_str)
                self.conf.add("];")
                self.conf.add("")

        # Save state
        if "filter" not in self.state:
            self.state["filter"] = {}
        self.state["filter"]["prefixes"] = state

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
        self.conf.add(f"  {self.bgp_functions.peer_reject_filtered()};")
        # Enable blackholing for customers and internal peers
        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.conf.add(f"  {self.bgp_functions.peer_accept_blackhole()};")
        # Enable blackhole large community origination for internal peers
        if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.conf.add(f"  {self.bgp_functions.peer_accept_blackhole_originated()};")
        # Finally accept the route
        self.conf.add(f"  {self.bgp_functions.peer_accept()};")
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
        self.conf.add("{")
        self.conf.add(f'  filter_name = "{filter_name}";')
        self.conf.add("  accept_route = false;")
        self.conf.add("")

        # Reject NOADVERTISE
        self.conf.add(f"  {self.bgp_functions.peer_reject_noadvertise()};")

        # Do not export blackhole routes to customers or peers
        if self.peer_type in ("customer", "peer"):
            self.conf.add(f"  {self.bgp_functions.peer_reject_blackholes()};")
        # Check if we allow blackholes
        blackhole_function_arg = None
        if self.peer_type in ("routeserver", "routecollector"):
            blackhole_function_arg = 65413
        elif self.peer_type == "transit":
            blackhole_function_arg = 65412
        # For eBGP peers we need to verify that the blackhole is targetted
        if blackhole_function_arg:
            # If the peer accepts blackhole communites, check if we're going to be exporting this blackhole
            if self.blackhole_community:
                self.conf.add("  # Peer is blackhole community capable")
                # Grab BIRD function to reject non targetted blackhole routes
                peer_reject_non_targetted_blackhole = self.bgp_functions.peer_reject_non_targetted_blackhole(
                    True,
                    self.route_policy_redistribute.kernel_blackhole,
                    self.route_policy_redistribute.static_blackhole,
                    self.asn,
                    blackhole_function_arg,
                )
                self.conf.add(f"  {peer_reject_non_targetted_blackhole};")
            else:
                self.conf.add("  # Peer is not blackhole community capable")
                # Grab BIRD function to reject non targetted blackhole routes
                peer_reject_non_targetted_blackhole = self.bgp_functions.peer_reject_non_targetted_blackhole(
                    False, False, False, self.asn, blackhole_function_arg
                )
                self.conf.add(f"  {peer_reject_non_targetted_blackhole};")

        # IMPORTANT: This must be after peer_reject_non_targetted_blackhole as peer_reject_non_targetted_blackhole removes
        #            the NOEXPORT community
        # Reject NOEXPORT and NOEXPORT ASN
        if self.peer_type not in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.conf.add(f"  {self.bgp_functions.peer_reject_noexport()};")
            self.conf.add(f"  {self.bgp_functions.peer_reject_noexport_asn(self.asn)};")

        # Check for peer types we're not exporting to
        if self.peer_type == "customer":
            self.conf.add(f"  {self.bgp_functions.peer_reject_noexport_customer()};")
        if self.peer_type in ("peer", "routecollector", "routeserver"):
            self.conf.add(f"  {self.bgp_functions.peer_reject_noexport_peer()};")
        if self.peer_type == "transit":
            self.conf.add(f"  {self.bgp_functions.peer_reject_noexport_transit()};")

        # Rejections based on location-based large communities
        if self.peer_type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we have a ISO-3166 country code
            if self.location.iso3166:
                self.conf.add("  # Check if we're not exporting this route based on the ISO-3166 location")
                self.conf.add(f"  {self.bgp_functions.peer_reject_noexport_location(self.location.iso3166)};")

        # Check for connected route redistribution
        if self.route_policy_redistribute.connected:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_connected(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_connected(False)};")
        # Check for kernel route redistribution
        if self.route_policy_redistribute.kernel:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_kernel(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_kernel(False)};")
        # Check for kernel blackhole route redistribution
        if self.route_policy_redistribute.kernel_blackhole:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_kernel_blackhole(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_kernel_blackhole(False)};")
        # Check for kernel default route redistribution
        if self.route_policy_redistribute.kernel_default:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_kernel_default(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_kernel_default(False)};")
        # Check for static route redistribution
        if self.route_policy_redistribute.static:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_static(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_static(False)};")
        # Check for static blackhole route redistribution
        if self.route_policy_redistribute.static_blackhole:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_static_blackhole(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_static_blackhole(False)};")
        # Check for static default route redistribution
        if self.route_policy_redistribute.static_default:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_static_default(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_static_default(False)};")
        # Check for originated route redistribution
        if self.route_policy_redistribute.originated:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_originated(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_originated(False)};")
        # Check for originated default route redistribution
        if self.route_policy_redistribute.originated_default:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_originated_default(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_originated_default(False)};")

        # Check redistribution BGP routes originating from the different peer types
        # BGP routes originating from customers
        if self.route_policy_redistribute.bgp_customer:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_customer(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_customer(False)};")

        if self.route_policy_redistribute.bgp_customer_blackhole:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_customer_blackhole(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_customer_blackhole(False)};")

        # BGP routes originating from within our federation
        if self.route_policy_redistribute.bgp_own:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_own(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_own(False)};")

        if self.route_policy_redistribute.bgp_own_blackhole:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_own_blackhole(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_own_blackhole(False)};")

        if self.route_policy_redistribute.bgp_own_default:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_own_default(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_own_default(False)};")

        # BGP routes originating from peering
        if self.route_policy_redistribute.bgp_peering:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_peering(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_peering(False)};")

        # BGP routes originating from transit
        if self.route_policy_redistribute.bgp_transit:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_transit(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_transit(False)};")

        if self.route_policy_redistribute.bgp_transit_default:
            self.conf.add(f"  if {self.bgp_functions.peer_redistribute_bgp_transit_default(True)} then accept_route = true;")
        else:
            self.conf.add(f"  {self.bgp_functions.peer_redistribute_bgp_transit_default(False)};")

        # Check if the route is exportable
        self.conf.add("  # BGP exportable checks")
        self.conf.add(f"  if !{self.functions.is_default()} then {{")
        # Reject bogons for eBGP peer types
        if self.peer_type not in ("internal", "rrclient", "rrserver", "rrserver-server"):
            self.conf.add(f"     {self.bgp_functions.peer_reject_bogons()};")
        self.conf.add(f"     if {self.bgp_functions.is_blackhole()} then {{")
        self.conf.add(f"       {self._peer_reject_non_exportable_blackhole()};")
        self.conf.add("     } else {")
        self.conf.add(f"       {self._peer_reject_non_exportable()};")
        self.conf.add("     }")

        # End of BGP type tests
        self.conf.add("  }")

        # Check if we're accepting the route...
        self.conf.add("  if (accept_route) then {")
        # Check if we are adding a large community to outgoing routes
        if self.large_communities.outgoing.connected:
            for large_community in self.large_communities.outgoing.connected:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_connected(BirdVariable(large_community))};")
        if self.large_communities.outgoing.kernel:
            for large_community in self.large_communities.outgoing.kernel:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_kernel(BirdVariable(large_community))};")
        if self.large_communities.outgoing.kernel_blackhole:
            for large_community in self.large_communities.outgoing.kernel_blackhole:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_kernel_blackhole(BirdVariable(large_community))};")
        if self.large_communities.outgoing.kernel_default:
            for large_community in self.large_communities.outgoing.kernel_default:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_kernel_default(BirdVariable(large_community))};")
        if self.large_communities.outgoing.originated:
            for large_community in self.large_communities.outgoing.originated:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_originated(BirdVariable(large_community))};")
        if self.large_communities.outgoing.originated_default:
            for large_community in self.large_communities.outgoing.originated_default:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_originated_default(BirdVariable(large_community))};")
        if self.large_communities.outgoing.static:
            for large_community in self.large_communities.outgoing.static:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_static(BirdVariable(large_community))};")
        if self.large_communities.outgoing.static_blackhole:
            for large_community in self.large_communities.outgoing.static_blackhole:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_static_blackhole(BirdVariable(large_community))};")
        if self.large_communities.outgoing.static_default:
            for large_community in self.large_communities.outgoing.static_default:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_static_default(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_own:
            for large_community in self.large_communities.outgoing.bgp_own:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_own(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_own_blackhole:
            for large_community in self.large_communities.outgoing.bgp_own_blackhole:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_own_blackhole(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_own_default:
            for large_community in self.large_communities.outgoing.bgp_own_default:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_own_default(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_customer:
            for large_community in self.large_communities.outgoing.bgp_customer:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_customer(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_customer_blackhole:
            for large_community in self.large_communities.outgoing.bgp_customer_blackhole:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_customer_blackhole(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_peering:
            for large_community in self.large_communities.outgoing.bgp_peering:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_peering(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_transit:
            for large_community in self.large_communities.outgoing.bgp_transit:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_transit(BirdVariable(large_community))};")
        if self.large_communities.outgoing.bgp_transit_default:
            for large_community in self.large_communities.outgoing.bgp_transit_default:
                self.conf.add(f"    {self.bgp_functions.peer_lc_add_bgp_transit_default(BirdVariable(large_community))};")

        # For eBGP peer types, make sure we replace AS-PATHs with the LC action set
        if self.peer_type in ("customer", "peer", "routecollector", "routeserver", "transit"):
            self.conf.add(f"    {self.bgp_functions.peer_replace_aspath()};")
            self.conf.add(f"    {self.bgp_functions.peer_remove_lc_private()};")

        # Check if we're doing AS-PATH prepending...
        if self.prepend.connected.own_asn:
            self.conf.add(
                f"    {self.bgp_functions.peer_prepend_connected(BirdVariable('BGP_ASN'), self.prepend.connected.own_asn)};"
            )

        if self.prepend.kernel.own_asn:
            self.conf.add(f"    {self.bgp_functions.peer_prepend_kernel(BirdVariable('BGP_ASN'), self.prepend.kernel.own_asn)};")

        if self.peer_type in ("internal", "routecollector", "routeserver", "rrclient", "rrserver", "rrserver-rrserver", "transit"):
            if self.prepend.kernel_blackhole.own_asn:
                peer_prepend_kernel_blackhole = self.bgp_functions.peer_prepend_kernel_blackhole(
                    BirdVariable("BGP_ASN"), self.prepend.kernel_blackhole.own_asn
                )
                self.conf.add(f"    {peer_prepend_kernel_blackhole};")

        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.prepend.kernel_default.own_asn:
                peer_prepend_kernel_default = self.bgp_functions.peer_prepend_kernel_default(
                    BirdVariable("BGP_ASN"), self.prepend.kernel_default.own_asn
                )
                self.conf.add(f"    {peer_prepend_kernel_default};")

        if self.prepend.originated.own_asn:
            self.conf.add(
                f"    {self.bgp_functions.peer_prepend_originated(BirdVariable('BGP_ASN'), self.prepend.originated.own_asn)};"
            )

        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.prepend.originated_default.own_asn:
                peer_prepend_originated_default = self.bgp_functions.peer_prepend_originated_default(
                    BirdVariable("BGP_ASN"), self.prepend.originated_default.own_asn
                )
                self.conf.add(f"    {peer_prepend_originated_default};")

        if self.prepend.static.own_asn:
            self.conf.add(f"    {self.bgp_functions.peer_prepend_static(BirdVariable('BGP_ASN'), self.prepend.static.own_asn)};")

        if self.peer_type in ("internal", "routecollector", "routeserver", "rrclient", "rrserver", "rrserver-rrserver", "transit"):
            if self.prepend.static_blackhole.own_asn:
                peer_prepend_static_blackhole = self.bgp_functions.peer_prepend_static_blackhole(
                    BirdVariable("BGP_ASN"), self.prepend.static_blackhole.own_asn
                )
                self.conf.add(f"    {peer_prepend_static_blackhole};")

        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.prepend.static_default.own_asn:
                peer_prepend_static_default = self.bgp_functions.peer_prepend_static_default(
                    BirdVariable("BGP_ASN"), self.prepend.static_default.own_asn
                )
                self.conf.add(f"    {peer_prepend_static_default};")

        if self.prepend.bgp_own.own_asn:
            self.conf.add(f"    {self.bgp_functions.peer_prepend_bgp_own(BirdVariable('BGP_ASN'), self.prepend.bgp_own.own_asn)};")

        if self.peer_type in ("internal", "routecollector", "routeserver", "rrclient", "rrserver", "rrserver-rrserver", "transit"):
            if self.prepend.bgp_own_blackhole.own_asn:
                peer_prepend_bgp_own_blackhole = self.bgp_functions.peer_prepend_bgp_own_blackhole(
                    BirdVariable("BGP_ASN"), self.prepend.bgp_own_blackhole.own_asn
                )
                self.conf.add(f"    {peer_prepend_bgp_own_blackhole};")

        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.prepend.bgp_own_default.own_asn:
                peer_prepend_bgp_own_default = self.bgp_functions.peer_prepend_bgp_own_default(
                    BirdVariable("BGP_ASN"), self.prepend.bgp_own_default.own_asn
                )
                self.conf.add(f"    {peer_prepend_bgp_own_default};")

        if self.prepend.bgp_customer.own_asn:
            self.conf.add(
                f"    {self.bgp_functions.peer_prepend_bgp_customer(BirdVariable('BGP_ASN'), self.prepend.bgp_customer.own_asn)};"
            )

        if self.peer_type in ("internal", "routecollector", "routeserver", "rrclient", "rrserver", "rrserver-rrserver", "transit"):
            if self.prepend.bgp_customer_blackhole.own_asn:
                peer_prepend_bgp_customer_blackhole = self.bgp_functions.peer_prepend_bgp_customer_blackhole(
                    BirdVariable("BGP_ASN"), self.prepend.bgp_customer_blackhole.own_asn
                )
                self.conf.add(f"    {peer_prepend_bgp_customer_blackhole};")

        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.prepend.bgp_peering.own_asn:
                self.conf.add(
                    f"    {self.bgp_functions.peer_prepend_bgp_peering(BirdVariable('BGP_ASN'), self.prepend.bgp_peering.own_asn)};"
                )

        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.prepend.bgp_transit.own_asn:
                self.conf.add(
                    f"    {self.bgp_functions.peer_prepend_bgp_transit(BirdVariable('BGP_ASN'), self.prepend.bgp_transit.own_asn)};"
                )

        if self.peer_type in ("customer", "internal", "rrclient", "rrserver", "rrserver-rrserver"):
            if self.prepend.bgp_transit_default.own_asn:
                peer_prepend_bgp_transit_default = self.bgp_functions.peer_prepend_bgp_transit_default(
                    BirdVariable("BGP_ASN"), self.prepend.bgp_transit_default.own_asn
                )
                self.conf.add(f"    {peer_prepend_bgp_transit_default};")

        # Do large community prepending if the peer is a customer, peer, routeserver or transit
        if self.peer_type in ("customer", "peer", "routeserver", "routecollector", "transit"):
            # Check if we're doing prepending
            self.conf.add("    # Do large community based prepending")
            self.conf.add(f"    {self.bgp_functions.peer_prepend_lc(self.asn)};")
            # Check if we have a ISO-3166 country code
            if self.location.iso3166:
                self.conf.add("    # Do prepending based on ISO-3166 location;")
                self.conf.add(f"    {self.bgp_functions.peer_prepend_lc_location(self.location.iso3166)};")
        # If we have graceful_shutdown set, add the community
        if self.graceful_shutdown:
            self.conf.add(f"    {self.bgp_functions.peer_graceful_shutdown()};")
        # Check if we need to do any blackhole manipulation
        if self.blackhole_community and isinstance(self.blackhole_community, list):
            self.conf.add("    # If this is a blackhole route, then add the communities")
            self.conf.add(f"    if {self.bgp_functions.is_blackhole()} then {{")
            self.conf.add("      bgp_community.delete([BGP_COMMUNITY_BLACKHOLE]);")
            # Loop with the communities we have to add
            for community in self.blackhole_community:
                # Get community component count so we can see if its a normal or large community
                component_count = community.count(",")
                if component_count == 1:
                    self.conf.add(f"      {self.bgp_functions.peer_community_add_blackhole(BirdVariable(community))};")
                elif component_count == 2:
                    self.conf.add(f"      {self.bgp_functions.peer_lc_add_blackhole(BirdVariable(community))};")
            self.conf.add("    }")

        # Finally accept
        self.conf.add("    # Finally accept")
        self.conf.add("    if DEBUG then")
        self.conf.add(
            f'      print "[{filter_name}] Accepting ", {self.functions.route_info()}, " from t_bgp to t_bgp_peer (fallthrough)";'
        )
        self.conf.add("    accept;")
        self.conf.add("  }")

        # By default reject all routes
        self.conf.add("  # Reject by default")
        self.conf.add("  if DEBUG then")
        self.conf.add(
            f'    print "[{filter_name}] Rejecting ", {self.functions.route_info()}, " from t_bgp to t_bgp_peer (fallthrough)";'
        )
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
            self.conf.add("  if DEBUG then")
            self.conf.add(
                f'   print "[{filter_name}] Rejecting ", {self.functions.route_info()}, " from t_bgp_peer to peer (qurantined)";'
            )
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
            self.conf.add(f"  {self.bgp_functions.peer_communities_strip_internal()};")
            self.conf.add(f"  {self.bgp_functions.peer_import_customer(self.asn, self.cost)};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_default()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_bogons()};")
            # The bgp_filter_prefix size test will exclude blackholes from checks
            self.conf.add(f"  {self._bgp_filter_prefix_size()};")
            # Check if we're going to accept a blackhole route
            if self.route_policy_accept.bgp_customer_blackhole:
                self.conf.add(f"  {self._bgp_filter_blackhole_size()};")
            else:
                self.conf.add(f"  {self.bgp_functions.peer_filter_blackhole()};")
            # If we're replacing the ASN we only allow private ASN's in the AS-PATH
            if self.replace_aspath:
                self.conf.add(f"  {self.bgp_functions.peer_filter_asn_private(BirdVariable(f'[{self.asn}]'))};")
            # Else, filter bogon ASN's
            else:
                self.conf.add(f"  {self.bgp_functions.peer_filter_asn_bogons()};")
            self.conf.add(
                f"  {self.bgp_functions.peer_filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};"
            )
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_invalid(self.asn)};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_transit()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_nexthop_not_peerip()};")

        # Peers
        elif self.peer_type == "peer":
            self.conf.add(f"  {self.bgp_functions.peer_communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.peer_import_peer(self.asn, self.cost)};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_default()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_blackhole()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_bogons()};")
            self.conf.add(f"  {self._bgp_filter_prefix_size()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_bogons()};")
            self.conf.add(
                f"  {self.bgp_functions.peer_filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};"
            )
            self.conf.add(f"  {self.bgp_functions.peer_filter_nexthop_not_peerip()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_invalid(self.asn)};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_transit()};")

        # Routecollector
        elif self.peer_type == "routecollector":
            self.conf.add(f"  {self.bgp_functions.peer_communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_routecollector_all()};")
        # Routeserver
        elif self.peer_type == "routeserver":
            self.conf.add(f"  {self.bgp_functions.peer_communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.peer_import_routeserver(self.asn, self.cost)};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_default()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_blackhole()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_bogons()};")
            self.conf.add(f"  {self._bgp_filter_prefix_size()};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_bogons()};")
            self.conf.add(
                f"  {self.bgp_functions.peer_filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};"
            )
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_transit()};")

        # Internal router peer types
        elif self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
            self.conf.add(f"  {self.bgp_functions.peer_filter_lc_no_relation()};")

            # If we are not accepting any default routes, just filter them all out
            if not self.route_policy_accept.bgp_own_default and not self.route_policy_accept.bgp_transit_default:
                self.conf.add(f"  {self.bgp_functions.peer_filter_default()};")
            else:
                # Filter own default routes if we're not accepting them
                if not self.route_policy_accept.bgp_own_default:
                    self.conf.add(f"  {self.bgp_functions.peer_filter_own_default()};")
                # Filter transit default routes if we're not accepting them
                if not self.route_policy_accept.bgp_transit_default:
                    self.conf.add(f"  {self.bgp_functions.peer_filter_transit_default()};")
                # Filter any non-own and non-transit default routes (invalid default routes)
                self.conf.add(f"  {self.bgp_functions.peer_filter_invalid_default()};")

            # If we're not accepting any blackhole routes, just filter them all out
            if not self.route_policy_accept.bgp_customer_blackhole and not self.route_policy_accept.bgp_own_blackhole:
                self.conf.add(f"  {self.bgp_functions.peer_filter_blackhole()};")
            else:
                # Filter customer blackhole routes if we're not accepting them
                if not self.route_policy_accept.bgp_customer_blackhole:
                    self.conf.add(f"  {self.bgp_functions.peer_filter_customer_blackhole()};")
                # Filter own blackhole routes if we're not accepting them
                if not self.route_policy_accept.bgp_own_blackhole:
                    self.conf.add(f"  {self.bgp_functions.peer_filter_own_blackhole()};")
                # Filter any non-own and non-transit blackhole routes (invalid blackhole routes)
                self.conf.add(f"  {self.bgp_functions.peer_filter_invalid_blackhole()};")
                self.conf.add(f"  {self._bgp_filter_blackhole_size()};")

            self.conf.add("  # Bypass prefix size filters for the default route")
            self.conf.add(f"  if !{self.functions.is_default()} then {self._bgp_filter_prefix_size()};")

            # Check if we're replacing the AS-PATH
            if self.peer_type == "internal" and self.replace_aspath:
                self.conf.add(f"  {self.bgp_functions.peer_filter_asn_private(BirdVariable('PRIVATE_ASNS'))};")

            # NK: Should we be filtering AS-PATH lengths for internal systems?
            # - probably safer to do so?
            self.conf.add(
                f"  {self.bgp_functions.peer_filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};"
            )

        # Transit providers
        elif self.peer_type == "transit":
            self.conf.add(f"  {self.bgp_functions.peer_communities_strip_all()};")
            self.conf.add(f"  {self.bgp_functions.peer_import_transit(self.asn, self.cost)};")
            # Check if we need to filter out the default route
            if not self.route_policy_accept.bgp_transit_default:
                self.conf.add(f"  {self.bgp_functions.peer_filter_default()};")

            self.conf.add(f"  {self.bgp_functions.peer_filter_blackhole()};")
            self.conf.add("  # Bypass bogon filters for the default route")
            self.conf.add(f"  if !{self.functions.is_default()} then {self.bgp_functions.peer_filter_bogons()};")
            self.conf.add("  # Bypass prefix size filters for the default route")
            self.conf.add(f"  if !{self.functions.is_default()} then {self._bgp_filter_prefix_size()};")

            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_bogons()};")
            self.conf.add(
                f"  {self.bgp_functions.peer_filter_aspath_length(self.aspath_import_maxlen, self.aspath_import_minlen)};"
            )
            self.conf.add(f"  {self.bgp_functions.peer_filter_asn_invalid(self.asn)};")
            self.conf.add(f"  {self.bgp_functions.peer_filter_nexthop_not_peerip()};")

        # With exception of routecollector (which is not supposed to be sending us routes), check the community lengths
        if self.peer_type != "routecollector":
            self.conf.add(f"  {self._bgp_filter_community_lengths()};")

        # Flip around the meaning of filters depending on peer type
        # For customer and peer, it is an ALLOW list
        if self.peer_type in ("customer", "peer"):
            # Check if we're filtering allowed origin ASNs
            if self.has_origin_asn_filter:
                self.conf.add(f"  {self.bgp_functions.peer_filter_origin_asns_allow(BirdVariable(self.origin_asn_list_name))};")
            # Check if we're filtering allowed peer ASNs
            if self.has_peer_asn_filter:
                self.conf.add(f"  {self.bgp_functions.peer_filter_asns_allow(BirdVariable(self.peer_asn_list_name))};")
            # Check if we're filtering allowed AS-PATH ASNs
            if self.has_aspath_asn_filter:
                self.conf.add(f"  {self.bgp_functions.peer_filter_aspath_allow(BirdVariable(self.aspath_asn_list_name))};")
            # Check if we're filtering allowed prefixes
            if self.has_prefix_filter:
                self.conf.add("  # Filter on the allowed prefixes")
                # Check if we have IPv4 support and output the filter
                peer_filter_prefixes_allow = self.bgp_functions.peer_filter_prefixes_allow(
                    BirdVariable(self.import_prefix_list_name("4")), BirdVariable(self.import_prefix_list_name("6"))
                )
                self.conf.add(f"  {peer_filter_prefixes_allow};")

                # For peer types that support blackholes, add the blackhole filter
                if self.peer_type == "customer":
                    peer_filter_blackholes_allow = self.bgp_functions.peer_filter_prefixes_blackhole_allow(
                        BirdVariable(self.import_blackhole_prefix_list_name("4")),
                        BirdVariable(self.import_blackhole_prefix_list_name("6")),
                    )
                    self.conf.add(f"  {peer_filter_blackholes_allow};")

        # For everything else it is a DENY list
        elif self.peer_type != "routecollector":
            # Check if we're filtering denied origin ASNs
            if self.has_origin_asn_filter:
                self.conf.add(f"  {self.bgp_functions.peer_filter_origin_asns_deny(BirdVariable(self.origin_asn_list_name))};")
            # Check if we're filtering denied peer ASNs
            if self.has_peer_asn_filter:
                self.conf.add(f"  {self.bgp_functions.peer_filter_asns_deny(BirdVariable(self.peer_asn_list_name))};")
            # Check if we're filtering allowed AS-PATH ASNs
            if self.has_aspath_asn_filter:
                self.conf.add(f"  {self.bgp_functions.peer_filter_aspath_deny(BirdVariable(self.aspath_asn_list_name))};")
            # Check if we're filtering denied prefixes
            if self.has_prefix_filter:
                peer_filter_prefixes_deny = self.bgp_functions.peer_filter_prefixes_deny(
                    BirdVariable(self.import_prefix_list_name("4")), BirdVariable(self.import_prefix_list_name("6"))
                )
                self.conf.add(f"  {peer_filter_prefixes_deny};")

                # For peer types that support blackholes, add the blackhole filter
                if self.peer_type in ("internal", "rrclient", "rrserver", "rrserver-rrserver"):
                    peer_filter_blackholes_deny = self.bgp_functions.peer_filter_prefixes_blackhole_deny(
                        BirdVariable(self.import_blackhole_prefix_list_name("4")),
                        BirdVariable(self.import_blackhole_prefix_list_name("6")),
                    )
                    self.conf.add(f"  {peer_filter_blackholes_deny};")

        # Quarantine mode...
        # NK: We don't quarantine route collectors as they are automagically filtered
        if self.quarantined and self.peer_type != "routecollector":
            # Quarantine prefixes
            self.conf.add("  # Quarantine all prefixes received")
            self.conf.add(f"  {self.bgp_functions.peer_quarantine()};")

        # Add location-based large communities
        if self.peer_type in ("customer", "peer", "routeserver", "transit"):
            # Check if we have a ISO-3166 country code
            if self.location.iso3166:
                self.conf.add(f"  {self.bgp_functions.peer_import_location_iso3166(self.location.iso3166)};")
            # Check if we have a UN.M49 country code
            if self.location.unm49:
                self.conf.add(f"  {self.bgp_functions.peer_import_location_unm49(self.location.unm49)};")

        # If this is a customer or internal peer type, check if we're doing replacement of the AS-PATH and add the action community
        if self.peer_type in ("customer", "internal"):
            if self.replace_aspath:
                # Lastly add the large community to replace the ASN
                self.conf.add(
                    f'  print "[{filter_name}] Adding LC action BGP_LC_ACTION_REPLACE_ASPATH to ", {self.functions.route_info()};'
                )
                self.conf.add("  bgp_large_community.add(BGP_LC_ACTION_REPLACE_ASPATH);")

        # Check if we are adding a large community to incoming routes
        if self.large_communities.incoming:
            # Loop with large communities and add to the prefix
            for large_community in sorted(self.large_communities.incoming):
                if self.birdconfig_globals.debug:
                    self.conf.add(f'  print "[{filter_name}] Adding LC {large_community} to ", {self.functions.route_info()};')
                self.conf.add(f"  bgp_large_community.add({large_community});")

        # Support for changing incoming local_pref
        if self.peer_type == "customer":
            self.conf.add(f"  {self.bgp_functions.peer_import_localpref()};")

        # Enable graceful_shutdown for this prefix
        if self.graceful_shutdown:
            self.conf.add(f"  {self.bgp_functions.peer_graceful_shutdown()};")
        # Set local_pref to 0 (GRACEFUL_SHUTDOWN) for the peer in graceful_shutdown
        self.conf.add(f"  {self.bgp_functions.peer_import_graceful_shutdown()};")

        self.conf.add("  accept;")
        self.conf.add("};")
        self.conf.add("")

    def _setup_peer_protocol(self, ipv: str) -> None:
        """Peer protocol setup for a single protocol."""

        protocol_state = {}

        # Save the current protocol name
        protocol_state["name"] = self.protocol_name(ipv)

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
            protocol_state["mode"] = "passive"
            self.conf.add("  passive;")
        else:
            protocol_state["mode"] = "active"

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

        # Make sure we have protocols in our state
        if "protocols" not in self.state:
            self.state["protocols"] = {}

        # Save protocol state
        self.state["protocols"][f"ipv{ipv}"] = protocol_state

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

    def _peer_reject_non_exportable(self) -> str:
        """Generate the function call to peer_reject_non_exportable."""
        return self.bgp_functions.peer_reject_non_exportable(
            self.export_maxlen4, self.export_minlen4, self.export_maxlen6, self.export_minlen6
        )

    def _peer_reject_non_exportable_blackhole(self) -> str:
        """Generate the function call to peer_reject_non_exportable_blackhole."""
        return self.bgp_functions.peer_reject_non_exportable_blackhole(
            self.blackhole_export_maxlen4,
            self.blackhole_export_minlen4,
            self.blackhole_export_maxlen6,
            self.blackhole_export_minlen6,
        )

    def _bgp_filter_prefix_size(self) -> str:
        """Return a BGP prefix size filter for a specific IP version."""
        return self.bgp_functions.peer_filter_prefix_size(
            self.import_maxlen4, self.import_minlen4, self.import_maxlen6, self.import_minlen6
        )

    def _bgp_filter_blackhole_size(self) -> str:
        """Return a BGP blackhole size filter for a specific IP version."""
        return self.bgp_functions.peer_filter_blackhole_size(
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
        return self.bgp_functions.peer_filter_community_lengths(maxlen, maxlen_extended, maxlen_large)

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
    def state(self) -> Dict[str, Any]:
        """Return our state info."""
        return self._state

    @state.setter
    def state(self, state: Dict[str, Any]) -> None:
        """Set our state."""
        self.state = state

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
        return self.peer_attributes.prefix_limit4 or self.peer_attributes.prefix_limit4_peeringdb

    @prefix_limit4.setter
    def prefix_limit4(self, prefix_limit4: Optional[str]) -> None:
        """Set our IPv4 prefix limit."""
        self.peer_attributes.prefix_limit4 = prefix_limit4

    @property
    def prefix_limit6(self) -> BGPPeerPrefixLimit:
        """Return our IPv4 prefix limit."""
        return self.peer_attributes.prefix_limit6 or self.peer_attributes.prefix_limit6_peeringdb

    @prefix_limit6.setter
    def prefix_limit6(self, prefix_limit6: Optional[str]) -> None:
        """Set our IPv6 prefix limit."""
        self.peer_attributes.prefix_limit6 = prefix_limit6

    @property
    def prefix_limit4_peeringdb(self) -> BGPPeerPrefixLimit:
        """Return our IPv4 prefix limit from PeeringDB."""
        return self.peer_attributes.prefix_limit4_peeringdb

    @prefix_limit4_peeringdb.setter
    def prefix_limit4_peeringdb(self, prefix_limit4: Optional[str]) -> None:
        """Set our IPv4 prefix limit from PeeringDB."""
        self.peer_attributes.prefix_limit4_peeringdb = prefix_limit4

    @property
    def prefix_limit6_peeringdb(self) -> BGPPeerPrefixLimit:
        """Return our IPv6 prefix limit from PeeringDB."""
        return self.peer_attributes.prefix_limit6_peeringdb

    @prefix_limit6_peeringdb.setter
    def prefix_limit6_peeringdb(self, prefix_limit6: Optional[str]) -> None:
        """Set our IPv6 prefix limit from PeeringDB."""
        self.peer_attributes.prefix_limit6_peeringdb = prefix_limit6

    @property
    def replace_aspath(self) -> bool:
        """Return the ASN which replaces the AS-PATH."""
        return self.peer_attributes.replace_aspath

    @replace_aspath.setter
    def replace_aspath(self, replace_aspath: bool) -> None:
        """Set the ASN which will replace the AS-PATH."""
        self.peer_attributes.replace_aspath = replace_aspath

    @property
    def blackhole_community(self) -> Optional[Union[bool, List[str]]]:
        """Return the current value of blackhole_community."""
        return self.peer_attributes.blackhole_community

    @blackhole_community.setter
    def blackhole_community(self, blackhole_community: Union[List[str], bool]) -> None:
        """Set the blackhole community."""
        self.peer_attributes.blackhole_community = blackhole_community

    @property
    def constraints(self) -> BGPPeerConstraints:
        """Return our own BGP constraint overrides."""
        return self.peer_attributes.constraints

    @property
    def global_constraints(self) -> BGPPeertypeConstraints:
        """Return the global constraints for our peer type."""
        # Work out the peer type we're going to use for the global constraints
        peer_type = self.peer_type
        if peer_type == "customer" and self.replace_aspath:
            peer_type = "customer.private"

        return self.bgp_attributes.peertype_constraints[peer_type]

    # IPV4 BLACKHOLE IMPORT PREFIX LENGTHS

    @property
    def blackhole_import_maxlen4(self) -> int:
        """Return the current value of blackhole_import_maxlen4."""
        return self.constraints.blackhole_import_maxlen4 or self.global_constraints.blackhole_import_maxlen4

    @blackhole_import_maxlen4.setter
    def blackhole_import_maxlen4(self, blackhole_import_maxlen4: int) -> None:
        """Setter for blackhole_import_maxlen4."""
        self.constraints.blackhole_import_maxlen4 = blackhole_import_maxlen4

    @property
    def blackhole_import_minlen4(self) -> int:
        """Return the current value of blackhole_import_minlen4."""
        return self.constraints.blackhole_import_minlen4 or self.global_constraints.blackhole_import_minlen4

    @blackhole_import_minlen4.setter
    def blackhole_import_minlen4(self, blackhole_import_minlen4: int) -> None:
        """Setter for blackhole_import_minlen4."""
        self.constraints.blackhole_import_minlen4 = blackhole_import_minlen4

    # IPV4 BLACKHOLE EXPORT PREFIX LENGTHS

    @property
    def blackhole_export_maxlen4(self) -> int:
        """Return the current value of blackhole_export_maxlen4."""
        return self.constraints.blackhole_export_maxlen4 or self.global_constraints.blackhole_export_maxlen4

    @blackhole_export_maxlen4.setter
    def blackhole_export_maxlen4(self, blackhole_export_maxlen4: int) -> None:
        """Setter for blackhole_export_maxlen4."""
        self.constraints.blackhole_export_maxlen4 = blackhole_export_maxlen4

    @property
    def blackhole_export_minlen4(self) -> int:
        """Return the current value of blackhole_export_minlen4."""
        return self.constraints.blackhole_export_minlen4 or self.global_constraints.blackhole_export_minlen4

    @blackhole_export_minlen4.setter
    def blackhole_export_minlen4(self, blackhole_export_minlen4: int) -> None:
        """Setter for blackhole_export_minlen4."""
        self.constraints.blackhole_export_minlen4 = blackhole_export_minlen4

    # IPV6 BLACKHOLE IMPORT PREFIX LENGTHS

    @property
    def blackhole_import_maxlen6(self) -> int:
        """Return the current value of blackhole_import_maxlen6."""
        return self.constraints.blackhole_import_maxlen6 or self.global_constraints.blackhole_import_maxlen6

    @blackhole_import_maxlen6.setter
    def blackhole_import_maxlen6(self, blackhole_import_maxlen6: int) -> None:
        """Setter for blackhole_import_maxlen6."""
        self.constraints.blackhole_import_maxlen6 = blackhole_import_maxlen6

    @property
    def blackhole_import_minlen6(self) -> int:
        """Return the current value of blackhole_import_minlen6."""
        return self.constraints.blackhole_import_minlen6 or self.global_constraints.blackhole_import_minlen6

    @blackhole_import_minlen6.setter
    def blackhole_import_minlen6(self, blackhole_import_minlen6: int) -> None:
        """Setter for blackhole_import_minlen6."""
        self.constraints.blackhole_import_minlen6 = blackhole_import_minlen6

    # IPV6 BLACKHOLE EXPORT PREFIX LENGTHS

    @property
    def blackhole_export_maxlen6(self) -> int:
        """Return the current value of blackhole_export_maxlen6."""
        return self.constraints.blackhole_export_maxlen6 or self.global_constraints.blackhole_export_maxlen6

    @blackhole_export_maxlen6.setter
    def blackhole_export_maxlen6(self, blackhole_export_maxlen6: int) -> None:
        """Setter for blackhole_export_maxlen6."""
        self.constraints.blackhole_export_maxlen6 = blackhole_export_maxlen6

    @property
    def blackhole_export_minlen6(self) -> int:
        """Return the current value of blackhole_export_minlen6."""
        return self.constraints.blackhole_export_minlen6 or self.global_constraints.blackhole_export_minlen6

    @blackhole_export_minlen6.setter
    def blackhole_export_minlen6(self, blackhole_export_minlen6: int) -> None:
        """Setter for blackhole_export_minlen6."""
        self.constraints.blackhole_export_minlen6 = blackhole_export_minlen6

    # IPV4 IMPORT PREFIX LENGTHS

    @property
    def import_maxlen4(self) -> int:
        """Return the current value of import_maxlen4."""
        return self.constraints.import_maxlen4 or self.global_constraints.import_maxlen4

    @import_maxlen4.setter
    def import_maxlen4(self, import_maxlen4: int) -> None:
        """Setter for import_maxlen4."""
        self.constraints.import_maxlen4 = import_maxlen4

    @property
    def import_minlen4(self) -> int:
        """Return the current value of import_minlen4."""
        return self.constraints.import_minlen4 or self.global_constraints.import_minlen4

    @import_minlen4.setter
    def import_minlen4(self, import_minlen4: int) -> None:
        """Setter for import_minlen4."""
        self.constraints.import_minlen4 = import_minlen4

    # IPV4 EXPORT PREFIX LENGHTS

    @property
    def export_maxlen4(self) -> int:
        """Return the current value of export_maxlen4."""
        return self.constraints.export_maxlen4 or self.global_constraints.export_maxlen4

    @export_maxlen4.setter
    def export_maxlen4(self, export_maxlen4: int) -> None:
        """Setter for export_maxlen4."""
        self.constraints.export_maxlen4 = export_maxlen4

    @property
    def export_minlen4(self) -> int:
        """Return the current value of export_minlen4."""
        return self.constraints.export_minlen4 or self.global_constraints.export_minlen4

    @export_minlen4.setter
    def export_minlen4(self, export_minlen4: int) -> None:
        """Setter for export_minlen4."""
        self.constraints.export_minlen4 = export_minlen4

    # IPV6 IMPORT LENGTHS

    @property
    def import_maxlen6(self) -> int:
        """Return the current value of import_maxlen6."""
        return self.constraints.import_maxlen6 or self.global_constraints.import_maxlen6

    @import_maxlen6.setter
    def import_maxlen6(self, import_maxlen6: int) -> None:
        """Setter for import_maxlen6."""
        self.constraints.import_maxlen6 = import_maxlen6

    @property
    def import_minlen6(self) -> int:
        """Return the current value of import_minlen6."""
        return self.constraints.import_minlen6 or self.global_constraints.import_minlen6

    @import_minlen6.setter
    def import_minlen6(self, import_minlen6: int) -> None:
        """Setter for import_minlen6."""
        self.constraints.import_minlen6 = import_minlen6

    # IPV6 EXPORT LENGTHS

    @property
    def export_minlen6(self) -> int:
        """Return the current value of export_minlen6."""
        return self.constraints.export_minlen6 or self.global_constraints.export_minlen6

    @export_minlen6.setter
    def export_minlen6(self, export_minlen6: int) -> None:
        """Setter for export_minlen6."""
        self.constraints.export_minlen6 = export_minlen6

    @property
    def export_maxlen6(self) -> int:
        """Return the current value of export_maxlen6."""
        return self.constraints.export_maxlen6 or self.global_constraints.export_maxlen6

    @export_maxlen6.setter
    def export_maxlen6(self, export_maxlen6: int) -> None:
        """Setter for export_maxlen6."""
        self.constraints.export_maxlen6 = export_maxlen6

    # AS PATH LENGTHS

    @property
    def aspath_import_minlen(self) -> int:
        """Return the current value of aspath_import_minlen."""
        return self.constraints.aspath_import_minlen or self.global_constraints.aspath_import_minlen

    @aspath_import_minlen.setter
    def aspath_import_minlen(self, aspath_import_minlen: int) -> None:
        """Set the AS path minlen."""
        self.constraints.aspath_import_minlen = aspath_import_minlen

    @property
    def aspath_import_maxlen(self) -> int:
        """Return the current value of aspath_import_maxlen."""
        return self.constraints.aspath_import_maxlen or self.global_constraints.aspath_import_maxlen

    @aspath_import_maxlen.setter
    def aspath_import_maxlen(self, aspath_import_maxlen: int) -> None:
        """Set the AS path maxlen."""
        self.constraints.aspath_import_maxlen = aspath_import_maxlen

    # COMMUNITY LENGTHS

    @property
    def community_import_maxlen(self) -> int:
        """Return the current value of community_import_maxlen."""
        return self.constraints.community_import_maxlen or self.global_constraints.community_import_maxlen

    @community_import_maxlen.setter
    def community_import_maxlen(self, community_import_maxlen: int) -> None:
        """Set the value of community_import_maxlen."""
        self.constraints.community_import_maxlen = community_import_maxlen

    @property
    def extended_community_import_maxlen(self) -> int:
        """Return the current value of extended_community_import_maxlen."""
        return self.constraints.extended_community_import_maxlen or self.global_constraints.extended_community_import_maxlen

    @extended_community_import_maxlen.setter
    def extended_community_import_maxlen(self, extended_community_import_maxlen: int) -> None:
        """Set the value of extended_community_import_maxlen."""
        self.constraints.extended_community_import_maxlen = extended_community_import_maxlen

    @property
    def large_community_import_maxlen(self) -> int:
        """Return the current value of large_community_import_maxlen."""
        return self.constraints.large_community_import_maxlen or self.global_constraints.large_community_import_maxlen

    @large_community_import_maxlen.setter
    def large_community_import_maxlen(self, large_community_import_maxlen: int) -> None:
        """Set the value of large_community_import_maxlen."""
        self.constraints.large_community_import_maxlen = large_community_import_maxlen

    #
    # Helper properties
    #

    @property
    def aspath_asn_list_name(self) -> str:
        """Return our AS-PATH ASN list name."""
        return f"bgp_AS{self.asn}_{self.name}_aspath_asns"

    @property
    def origin_asn_list_name(self) -> str:
        """Return our origin ASN list name."""
        return f"bgp_AS{self.asn}_{self.name}_origin_asns"

    @property
    def peer_asn_list_name(self) -> str:
        """Return our peer ASN list name."""
        return f"bgp_AS{self.asn}_{self.name}_peer_asns"

    @property
    def has_aspath_asn_filter(self) -> BGPPeerFilterItem:
        """Return if we filter on ASNs in the AS-PATH."""

        # We pull in "origin_asns" here to populate the aspath_asns for better filtering
        if self.peer_type in ("customer", "peer"):
            return self.filter_policy.aspath_asns or self.filter_policy.origin_asns or self.filter_policy.as_sets

        return self.filter_policy.aspath_asns

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
