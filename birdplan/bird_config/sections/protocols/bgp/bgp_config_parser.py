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

"""BIRD BGP configuration parser."""

import logging
import re
from typing import Any

from .....console.colors import colored
from .....exceptions import BirdPlanConfigError
from .... import BirdConfig
from ....config_parser import ConfigParser
from ..rpki import RPKISource

__all__ = ["BGPConfigParser"]


class BGPConfigParser(ConfigParser):
    """BGP configuration parser."""

    _birdconf: BirdConfig

    def parse(self, config: dict[str, Any]) -> None:
        """Configure BGP protocol."""

        self._config_bgp(config)

    def _config_bgp(self, config: dict[str, Any]) -> None:
        """Configure bgp section."""

        # If we have no rip section, just return
        if "bgp" not in config:
            return

        # Check configuration options are supported
        for config_item in config["bgp"]:
            if config_item not in (
                # Globals
                "accept",
                "asn",
                "graceful_shutdown",
                "import",
                "originate",  # Origination
                "peers",
                "peertype_constraints",
                "quarantine",
                "rpki_source",
                "rr_cluster_id",
            ):
                raise BirdPlanConfigError(f"The 'bgp' config item '{config_item}' is not supported")

        # Set our ASN
        if "asn" not in config["bgp"]:
            raise BirdPlanConfigError('BGP configuration must have an "asn" item defined')
        self.birdconf.protocols.bgp.asn = config["bgp"]["asn"]

        # Setup RPKI server
        if "rpki_source" in config["bgp"]:
            try:
                self.birdconf.protocols.bgp.rpki_source = RPKISource(config["bgp"]["rpki_source"])
            except ValueError as e:
                raise BirdPlanConfigError(f"Invalid 'bgp' config item 'rpki_source': {e}") from None

        self._config_bgp_accept(config)
        self._config_bgp_globals(config)
        self._config_bgp_peertype_constraints(config)
        self._config_bgp_originate(config)

        self._config_bgp_import(config)
        self._config_bgp_peers(config)

    def _config_bgp_accept(self, config: dict[str, Any]) -> None:
        """Configure bgp:accept section."""

        # If we don't have an accept section, just return
        if "accept" not in config["bgp"]:
            return

        # Loop with accept items
        for accept, accept_config in config["bgp"]["accept"].items():
            # Check if we need to accept some kinds of routes
            if accept in (
                "bgp_customer_blackhole",
                "bgp_own_blackhole",
                "bgp_own_default",
                "bgp_transit_default",
                "originated",
                "originated_default",
            ):
                setattr(self.birdconf.protocols.bgp.route_policy_accept, accept, accept_config)
            # If we don't understand this 'accept' entry, throw an error
            else:
                raise BirdPlanConfigError(f"Configuration item '{accept}' not understood in bgp:accept")

    def _config_bgp_globals(self, config: dict[str, Any]) -> None:
        """Configure bgp globals."""

        # Setup graceful shutdown if specified
        if "graceful_shutdown" in config["bgp"]:
            self.birdconf.protocols.bgp.graceful_shutdown = config["bgp"]["graceful_shutdown"]

        # Setup graceful shutdown if specified
        if "quarantine" in config["bgp"]:
            self.birdconf.protocols.bgp.quarantine = config["bgp"]["quarantine"]

        # Set our route reflector cluster id
        if "rr_cluster_id" in config["bgp"]:
            self.birdconf.protocols.bgp.rr_cluster_id = config["bgp"]["rr_cluster_id"]

    def _config_bgp_peertype_constraints(self, config: dict[str, Any]) -> None:
        """Configure bgp:peertype_constraints section."""

        # If we don't have a peertype_constraints section, just return
        if "peertype_constraints" not in config["bgp"]:
            return

        for peer_type in config["bgp"]["peertype_constraints"]:
            # Make sure we have a valid peer type
            if peer_type not in (
                "customer",
                "customer.private",
                "internal",
                "peer",
                "routecollector",
                "routeserver",
                "rrclient",
                "rrserver",
                "rrserver-rrserver",
                "transit",
            ):
                raise BirdPlanConfigError(f"The 'bgp:peertype_constraints' config item '{peer_type}' is not supported")
            # Loop with constraint items
            for constraint_name in config["bgp"]["peertype_constraints"][peer_type]:
                # Make sure we have a valid constraint to set
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
                    "export_maxlen4",
                    "import_minlen4",
                    "export_minlen4",
                    "import_maxlen6",
                    "export_maxlen6",
                    "import_minlen6",
                    "export_minlen6",
                    "aspath_import_maxlen",
                    "aspath_import_minlen",
                    "community_import_maxlen",
                    "extended_community_import_maxlen",
                    "large_community_import_maxlen",
                ):
                    raise BirdPlanConfigError(
                        f"The 'bgp:peertype_constraints:{peer_type}' config item '{constraint_name}' is not supported"
                    )
                # Make sure this peer supports blackhole imports
                if constraint_name.startswith("blackhole_import_"):  # noqa: SIM102
                    if peer_type not in (
                        "customer",
                        "internal",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                    ):
                        raise BirdPlanConfigError(
                            f"Having 'peertype_constraints:{constraint_name}' specified for peer type '{peer_type}' "
                            "makes no sense"
                        )
                # Make sure this peer accepts blackhole exports
                if constraint_name.startswith("blackhole_export_"):  # noqa: SIM102
                    if peer_type not in (
                        "internal",
                        "routeserver",
                        "routecollector",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        raise BirdPlanConfigError(
                            f"Having 'peertype_constraints:{constraint_name}' specified for peer type '{peer_type}' "
                            "makes no sense"
                        )
                # Make sure this peer supports imports
                if "import" in constraint_name:  # noqa: SIM102
                    if peer_type not in (
                        "customer",
                        "customer.private",
                        "internal",
                        "peer",
                        "routeserver",
                        "rrclient",
                        "rrserver",
                        "rrserver-rrserver",
                        "transit",
                    ):
                        raise BirdPlanConfigError(
                            f"Having 'peertype_constraints:{constraint_name}' specified for peer type '{peer_type}' "
                            "makes no sense"
                        )
                # Finally set the constraint item
                setattr(
                    self.birdconf.protocols.bgp.constraints(peer_type),
                    constraint_name,
                    config["bgp"]["peertype_constraints"][peer_type][constraint_name],
                )

    def _config_bgp_originate(self, config: dict[str, Any]) -> None:
        """Configure bgp:originate section."""

        # If we don't have an accept section, just return
        if "originate" not in config["bgp"]:
            return

        # Add origination routes
        for route in config["bgp"]["originate"]:
            self.birdconf.protocols.bgp.add_originated_route(route)

    def _config_bgp_import(self, config: dict[str, Any]) -> None:  # pylint: disable=too-many-branches
        """Configure bgp:import section."""

        # If we don't have the option then just return
        if "import" not in config["bgp"]:
            return

        # Loop with redistribution items
        for import_type, import_config in config["bgp"]["import"].items():
            # Import connected routes into the main BGP table
            if import_type == "connected":
                # Set type
                import_connected: bool | list[str]
                # Check what kind of config we go...
                if isinstance(import_config, bool):
                    import_connected = import_config
                # Else if its a dict, we need to treat it a bit differently
                elif isinstance(import_config, dict):
                    # Check it has an "interfaces" key
                    if "interfaces" not in import_config:
                        raise BirdPlanConfigError(f"Configurion item '{import_type}' has no 'interfaces' option in bgp:import")
                    # If it does, check that it is a list
                    if not isinstance(import_config["interfaces"], list):
                        raise BirdPlanConfigError(f"Configurion item '{import_type}:interfaces' has an invalid type in bgp:import")
                    # Set import_connected as the interface list
                    import_connected = import_config["interfaces"]
                else:
                    raise BirdPlanConfigError(f"Configurion item '{import_type}' has an unsupported value")
                # Add configuration
                self.birdconf.protocols.bgp.route_policy_import.connected = import_connected

            # Import kernel routes into the main BGP table
            elif import_type == "kernel":
                self.birdconf.protocols.bgp.route_policy_import.kernel = import_config
            # Import kernel blackhole routes into the main BGP table
            elif import_type == "kernel_blackhole":
                self.birdconf.protocols.bgp.route_policy_import.kernel_blackhole = import_config
            # Import kernel default routes into the main BGP table
            elif import_type == "kernel_default":
                self.birdconf.protocols.bgp.route_policy_import.kernel_default = import_config

            # Import static routes into the main BGP table
            elif import_type == "static":
                self.birdconf.protocols.bgp.route_policy_import.static = import_config
            # Import static blackhole routes into the main BGP table
            elif import_type == "static_blackhole":
                self.birdconf.protocols.bgp.route_policy_import.static_blackhole = import_config
            # Import static default routes into the main BGP table
            elif import_type == "static_default":
                self.birdconf.protocols.bgp.route_policy_import.static_default = import_config

            # If we don't understand this 'redistribute' entry, throw an error
            else:
                raise BirdPlanConfigError(f"Configuration item '{import_type}' not understood in bgp:import")

    def _config_bgp_peers(self, config: dict[str, Any]) -> None:
        """Configure bgp:peers section."""

        if "peers" not in config["bgp"]:
            return

        # Loop with peer ASN and config
        peer_count = len(config["bgp"]["peers"])
        peer_cur: int = 1
        for peer_name, peer_config in config["bgp"]["peers"].items():
            # Make sure peer name is valid
            if not re.match(r"^[a-z0-9]+$", peer_name):
                raise BirdPlanConfigError(f"The peer name '{peer_name}' specified in 'bgp:peers' is not valid, use [a-z0-9]")

            # Log completion
            if not self.birdconf.birdconfig_globals.suppress_info:
                percentage_complete = (peer_cur / peer_count) * 100
                logging.info(
                    colored("Processing BGP peer %s/%s (%.2f%%): %s", "blue"), peer_cur, peer_count, percentage_complete, peer_name
                )

            # Configure peer
            self._config_bgp_peers_peer(config, peer_name, peer_config)

            # Bump current peer
            peer_cur += 1

    def _config_bgp_peers_peer(  # pylint: disable=too-many-branches,too-many-locals,too-many-statements
        self, config: dict[str, Any], peer_name: str, peer_config: dict[str, Any]
    ) -> None:
        """Configure bgp:peers single peer."""

        # Start with no peer config
        peer: dict[str, Any] = {}

        # Loop with each config item in the peer
        for config_item, config_value in peer_config.items():
            if config_item in (
                "asn",
                "blackhole_community",
                "connect_delay_time",
                "connect_retry_time",
                "cost",
                "description",
                "error_wait_time",
                "graceful_shutdown",
                "incoming_large_communities",
                "multihop",
                "neighbor4",
                "neighbor6",
                "passive",
                "password",
                "prefix_limit_action",
                "prefix_limit4",
                "prefix_limit6",
                "quarantine",
                "replace_aspath",
                "source_address4",
                "source_address6",
                "ttl_security",
                "type",
                "use_rpki",
            ):
                peer[config_item] = config_value

            # Peer add_paths configuration
            elif config_item == "add_paths":
                peer["add_paths"] = None
                if isinstance(config_value, bool):
                    if config_value:
                        peer["add_paths"] = "on"
                elif isinstance(config_value, str):
                    if config_value not in ("tx", "rx", "on"):
                        raise BirdPlanConfigError(
                            f"Configuration value '{config_value}' not understood in bgp:peers:{peer_name}:add_paths, valid values"
                            "are 'tx', 'rx', 'on'"
                        )
                    peer["add_paths"] = config_value
                else:
                    raise BirdPlanConfigError(
                        f"Configuration item has invalid type '{type(config_value)}' in bgp:peers:{peer_name}:add_paths"
                    )
            # Configure actions
            elif config_item == "actions":
                peer["actions"] = []
                # Check type of data provided
                if not isinstance(config_value, list):
                    raise BirdPlanConfigError(
                        f"Configuration item has invalid type '{type(config_value)}' in bgp:peers:{peer_name}:actions"
                    )
                # Loop with actions
                for action in config_value:
                    # Make sure each action has a direction, match and action
                    if "action" not in action or "direction" not in action or "matches" not in action:
                        raise BirdPlanConfigError(
                            f"Configuration item '{action}' not understood in bgp:peers:{peer_name}:actions"
                        )
                    # Check action options are valid
                    for action_k, action_v in action.items():
                        # Check the action specification
                        if action_k == "action":
                            # Check for string actions
                            if isinstance(action_v, str):
                                # The only string action we support is 'reject'
                                if action_v != "reject":
                                    raise BirdPlanConfigError(
                                        f"Configuration item '{action_v}' not understood in bgp:peers:{peer_name}:actions"
                                    )
                            # Make sure that all the actions are supported
                            elif isinstance(action_v, dict):
                                for action_vk, action_vv in action_v.items():
                                    # Check the action values that should be lists or strings
                                    if action_vk in [
                                        "add_community",
                                        "add_extended_community",
                                        "add_large_community",
                                        "remove_community",
                                        "remove_extended_community",
                                        "remove_large_community",
                                    ]:
                                        # Check that the action value is either a list or string
                                        if not isinstance(action_vv, list) and not isinstance(action_vv, str):
                                            raise BirdPlanConfigError(
                                                f"Configuration item '{action_vv}' not understood in bgp:peers:{peer_name}:actions"
                                            )
                                    # Make sure prepend is a string
                                    elif action_vk == "prepend":
                                        if not isinstance(action_vv, str):
                                            raise BirdPlanConfigError(
                                                f"Configuration item '{action_vv}' not understood in bgp:peers:{peer_name}:actions"
                                            )
                                    # And throw an error if the action is not understood
                                    else:
                                        raise BirdPlanConfigError(
                                            f"Configuration item '{action_vk}' not understood in bgp:peers:{peer_name}:actions"
                                        )

                            # The type of the action value is not one that we support
                            else:
                                raise BirdPlanConfigError(
                                    f"Configuration item '{action_v}' not understood in bgp:peers:{peer_name}:actions"
                                )
                        # Check the direction of the action
                        elif action_k == "direction":
                            if action_v not in ("in", "out"):
                                raise BirdPlanConfigError(
                                    f"Configuration item '{action_v}' not understood in bgp:peers:{peer_name}:actions"
                                )
                        # Check matchces
                        elif action_k == "matches":
                            if not isinstance(action_v, dict):
                                raise BirdPlanConfigError(
                                    f"Configuration item '{action_v}' not understood in bgp:peers:{peer_name}:actions"
                                )
                            # Loop with matches
                            for match_k, match_v in action_v.items():
                                # Check the match items are supported
                                if match_k not in ("origin_asn", "prefix", "community", "extended_community", "large_community"):
                                    raise BirdPlanConfigError(
                                        f"Configuration item '{match_k}' not understood in bgp:peers:{peer_name}:actions"
                                    )
                                # Check the match values
                                if not isinstance(match_v, list) and not isinstance(match_v, str):
                                    raise BirdPlanConfigError(
                                        f"Configuration item '{match_v}' not understood in bgp:peers:{peer_name}:actions"
                                    )
                        # Add action
                        peer["actions"].append({action_k: action_v})

            # Peer location configuration
            elif config_item == "location":
                peer["location"] = {}
                # Loop with location configuration items
                for location_type, location_config in config_value.items():
                    if location_type not in ("iso3166", "unm49"):
                        raise BirdPlanConfigError(
                            f"Configuration item '{location_type}' not understood in bgp:peers:{peer_name}:location"
                        )
                    peer["location"][location_type] = location_config
            # Work out redistribution
            elif config_item == "redistribute":
                peer["redistribute"] = {}
                # Loop with redistribution items
                for redistribute_type, redistribute_config in config_value.items():
                    if redistribute_type not in (
                        "connected",
                        "kernel",
                        "kernel_blackhole",
                        "kernel_default",
                        "static",
                        "static_blackhole",
                        "static_default",
                        "originated",
                        "originated_default",
                        "bgp",
                        "bgp_customer",
                        "bgp_customer_blackhole",
                        "bgp_own",
                        "bgp_own_blackhole",
                        "bgp_own_default",
                        "bgp_peering",
                        "bgp_transit",
                        "bgp_transit_default",
                    ):
                        raise BirdPlanConfigError(
                            f"Configuration item '{redistribute_type}' not understood in bgp:peers:{peer_name} redistribute"
                        )
                    peer["redistribute"][redistribute_type] = redistribute_config

            # Work out acceptance of routes
            elif config_item == "accept":
                peer["accept"] = {}
                # Loop with acceptance items
                for accept, accept_config in config_value.items():
                    if accept not in (
                        "bgp_customer_blackhole",
                        "bgp_own_blackhole",
                        "bgp_own_default",
                        "bgp_transit_default",
                    ):
                        raise BirdPlanConfigError(f"Configuration item '{accept}' not understood in bgp:peers:{peer_name}:accept")
                    peer["accept"][accept] = accept_config
            # Add import filters
            elif config_item in ("import_filter", "filter"):
                peer["import_filter"] = {}
                # Loop with filter configuration items
                for filter_type, filter_config in config_value.items():
                    if filter_type not in ("as_sets", "aspath_asns", "origin_asns", "peer_asns", "prefixes"):
                        raise BirdPlanConfigError(
                            f"Configuration item '{filter_type}' not understood in bgp:peers:{peer_name}:import_filter"
                        )
                    peer["import_filter"][filter_type] = filter_config
            # Add import filters
            elif config_item == "import_filter_deny":
                peer["import_filter_deny"] = {}
                # Loop with filter configuration items
                for filter_type, filter_config in config_value.items():
                    if filter_type not in ("aspath_asns", "origin_asns", "prefixes"):
                        raise BirdPlanConfigError(
                            f"Configuration item '{filter_type}' not understood in bgp:peers:{peer_name}:import_filter_deny"
                        )
                    peer["import_filter_deny"][filter_type] = filter_config
            # Add import filters
            elif config_item == "export_filter":
                peer["export_filter"] = {}
                # Loop with filter configuration items
                for filter_type, filter_config in config_value.items():
                    if filter_type not in ("origin_asns", "prefixes"):
                        raise BirdPlanConfigError(
                            f"Configuration item '{filter_type}' not understood in bgp:peers:{peer_name}:export_filter"
                        )
                    peer["export_filter"][filter_type] = filter_config

            # Work out outgoing community options
            elif config_item == "outgoing_communities":
                if isinstance(config_value, dict):
                    # Loop with outgoing community configuration items
                    for lc_type, lc_config in config_value.items():
                        if lc_type not in (
                            "blackhole",
                            "default",
                            "connected",
                            "kernel",
                            "kernel_blackhole",
                            "kernel_default",
                            "static",
                            "static_blackhole",
                            "static_default",
                            "originated",
                            "originated_default",
                            "bgp",
                            "bgp_own",
                            "bgp_own_blackhole",
                            "bgp_own_default",
                            "bgp_customer",
                            "bgp_customer_blackhole",
                            "bgp_peering",
                            "bgp_transit",
                            "bgp_transit_default",
                            "bgp_blackhole",
                            "bgp_default",
                        ):
                            raise BirdPlanConfigError(
                                f"Configuration item '{lc_type}' not understood in bgp:peers:{peer_name}:outgoing_communities"
                            )
                        # Make sure we have a prepend key
                        if "outgoing_communities" not in peer:
                            peer["outgoing_communities"] = {}
                        # Then add the config...
                        peer["outgoing_communities"][lc_type] = lc_config

                # Check in the case it is a list
                elif isinstance(config_value, list):
                    peer["outgoing_communities"] = config_value

                # Else if we don't know what it is, then throw an exception
                else:
                    raise BirdPlanConfigError(f"Configuration item bgp:peers:{peer_name}:outgoing_communities has incorrect type")

            # Work out outgoing large community options
            elif config_item == "outgoing_large_communities":
                if isinstance(config_value, dict):
                    # Loop with outgoing large community configuration items
                    for lc_type, lc_config in config_value.items():
                        if lc_type not in (
                            "blackhole",
                            "default",
                            "connected",
                            "kernel",
                            "kernel_blackhole",
                            "kernel_default",
                            "static",
                            "static_blackhole",
                            "static_default",
                            "originated",
                            "originated_default",
                            "bgp",
                            "bgp_own",
                            "bgp_own_blackhole",
                            "bgp_own_default",
                            "bgp_customer",
                            "bgp_customer_blackhole",
                            "bgp_peering",
                            "bgp_transit",
                            "bgp_transit_default",
                            "bgp_blackhole",
                            "bgp_default",
                        ):
                            raise BirdPlanConfigError(
                                f"Configuration item '{lc_type}' not understood in bgp:peers:{peer_name}:outgoing_large_communities"
                            )
                        # Make sure we have a prepend key
                        if "outgoing_large_communities" not in peer:
                            peer["outgoing_large_communities"] = {}
                        # Then add the config...
                        peer["outgoing_large_communities"][lc_type] = lc_config

                # Check in the case it is a list
                elif isinstance(config_value, list):
                    peer["outgoing_large_communities"] = config_value

                # Else if we don't know what it is, then throw an exception
                else:
                    raise BirdPlanConfigError(
                        f"Configuration item bgp:peers:{peer_name}:outgoing_large_communities has incorrect type"
                    )

            # Work out prepending options
            elif config_item == "prepend":
                if isinstance(config_value, dict):
                    # Loop with prepend configuration items
                    for prepend_type, prepend_config in config_value.items():
                        if prepend_type not in (
                            "blackhole",
                            "default",
                            "connected",
                            "kernel",
                            "kernel_blackhole",
                            "kernel_default",
                            "static",
                            "static_blackhole",
                            "static_default",
                            "originated",
                            "originated_default",
                            "bgp",
                            "bgp_own",
                            "bgp_own_blackhole",
                            "bgp_own_default",
                            "bgp_customer",
                            "bgp_customer_blackhole",
                            "bgp_peering",
                            "bgp_transit",
                            "bgp_transit_default",
                            "bgp_blackhole",
                            "bgp_default",
                        ):
                            raise BirdPlanConfigError(
                                f"Configuration item '{prepend_type}' not understood in bgp:peers:{peer_name}:prepend"
                            )
                        # Make sure we have a prepend key
                        if "prepend" not in peer:
                            peer["prepend"] = {}
                        # Then add the config...
                        peer["prepend"][prepend_type] = prepend_config
                else:
                    peer["prepend"] = config_value

            # Work out our constraints
            elif config_item == "constraints":
                # Loop with constraint configuration items
                for constraint_name, constraint_value in config_value.items():
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
                        "export_maxlen4",
                        "import_minlen4",
                        "export_minlen4",
                        "import_maxlen6",
                        "export_maxlen6",
                        "import_minlen6",
                        "export_minlen6",
                        "aspath_import_maxlen",
                        "aspath_import_minlen",
                        "community_import_maxlen",
                        "extended_community_import_maxlen",
                        "large_community_import_maxlen",
                    ):
                        raise BirdPlanConfigError(
                            f"Configuration item '{constraint_name}' not understood in bgp:peers:{peer_name}:prepend"
                        )
                    # Make sure we have a prepend key
                    if "constraints" not in peer:
                        peer["constraints"] = {}
                    # Then add the config...
                    peer["constraints"][constraint_name] = constraint_value

            else:
                raise BirdPlanConfigError(f"Configuration item '{config_item}' not understood in bgp:peers:{peer_name}")

        # Check items we need
        for required_item in ["asn", "description", "type"]:
            if required_item not in peer:
                raise BirdPlanConfigError(f"Configuration item '{required_item}' missing in bgp:peers:{peer_name}")

        # Check the peer type is valid
        if peer["type"] not in (
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
            raise BirdPlanConfigError(f"Configuration item 'type' for BGP peer '{peer_name}' has invalid value '%s'" % peer["type"])

        # Check that if we have a peer type of rrclient, that we have rr_cluster_id too...
        if (peer["type"] == "rrclient") and ("rr_cluster_id" not in config["bgp"]):
            raise BirdPlanConfigError(
                f"Configuration for BGP peer '{peer_name}' is missing 'rr_cluster_id' when having 'rrclient' peers"
            )
        # If we are a customer type, we must have filters defined
        if (peer["type"] == "customer") and ("import_filter" not in peer) and ("filter" not in peer):
            raise BirdPlanConfigError(
                f"Configuration for BGP peer '{peer_name}' is missing 'import_filter' when type is 'customer'"
            )
        # We must have a neighbor4 or neighbor6
        if ("neighbor4" not in peer) and ("neighbor6" not in peer):
            raise BirdPlanConfigError(f"Configuration for BGP peer '{peer_name}' is missing 'neighbor4' or 'neighbor6' config")
        # We must have a source_address4 for neighbor4
        if ("neighbor4" in peer) and ("source_address4" not in peer):
            raise BirdPlanConfigError(f"Configuration for BGP peer '{peer_name}' must have a 'source_address4'")
        # We must have a source_address6 for neighbor6
        if ("neighbor6" in peer) and ("source_address6" not in peer):
            raise BirdPlanConfigError(f"Configuration for BGP peer '{peer_name}' must have a 'source_address6'")

        # Check if we're using RPKI, if it's a supported peer type, and if we have no explicit setting specified
        # If all of this is true, we can enable it by default
        if (
            self.birdconf.protocols.bgp.rpki_source
            and peer["type"] in ("customer", "peer", "routerserver", "transit")
            and "use_rpki" not in peer
        ):
            peer["use_rpki"] = True

        # Make sure we have items we need
        self.birdconf.protocols.bgp.add_peer(peer_name, peer)
