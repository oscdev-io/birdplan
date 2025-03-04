#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""BIRD BGP peer action support."""

from enum import Enum
from typing import Any

from ......exceptions import BirdPlanConfigError
from ..... import util
from ....functions import BirdVariable, SectionFunctions
from ..bgp_functions import BGPFunctions

__all__ = ["BGPPeerActions"]


class BGPPeerActionType(Enum):
    """BGP peer action type enum."""

    IMPORT = "import"
    EXPORT = "export"


class BGPPeerAction:
    """BGP peer action."""

    _global_functions: SectionFunctions
    _bgp_functions: BGPFunctions

    _asn: int
    _peer_name: str

    _action_id: int
    _action_type: BGPPeerActionType

    _match_origin_asn: list[str]
    _match_prefix: list[str]
    _match_community: list[str]
    _match_extended_community: list[str]
    _match_large_community: list[str]

    _action_reject: bool
    _action_add_community: list[str]
    _action_add_extended_community: list[str]
    _action_add_large_community: list[str]
    _action_remove_community: list[str]
    _action_remove_extended_community: list[str]
    _action_remove_large_community: list[str]
    _action_prepend: int

    def __init__(  # noqa: PLR0913
        self,
        global_functions: SectionFunctions,
        bgp_functions: BGPFunctions,
        asn: int,
        peer_name: str,
        action_id: int,
        action: dict[str, Any],
    ) -> None:
        """Initialize BGP peer action."""

        self._global_functions = global_functions
        self._bgp_functions = bgp_functions

        self._asn = asn
        self._peer_name = peer_name
        self._action_id = action_id

        # Grab action type
        self._action_type = BGPPeerActionType(action["type"])

        # Initialize matches and actions
        self._match_origin_asn = []
        self._match_prefix = []
        self._match_community = []
        self._match_extended_community = []
        self._match_large_community = []

        self._action_reject = False
        self._action_add_community = []
        self._action_add_extended_community = []
        self._action_add_large_community = []
        self._action_remove_community = []
        self._action_remove_extended_community = []
        self._action_remove_large_community = []
        self._action_prepend = 0

        # Parse action data
        if "matches" in action:
            self._parse_matches(action["matches"])
        self._parse_actions(action["action"])

    def _parse_matches(self, matches: dict[str, Any]) -> None:
        """Parse the matches."""

        # Check what matches we have
        for match_k, match_v in matches.items():
            # Make sure we only have lists or strings
            if not isinstance(match_v, list) and not isinstance(match_v, str):
                raise BirdPlanConfigError("Action value for 'match' is not valid")
            # If we have a string, convert it to a list
            match_v_list: list[str] = []
            if isinstance(match_v, str):
                match_v_list.append(match_v)
            else:
                match_v_list.extend(match_v)
            # Process each type of match
            if match_k in ("origin_asn", "prefix", "community", "extended_community", "large_community"):
                setattr(self, f"_match_{match_k}", match_v_list)
            else:
                raise BirdPlanConfigError(f"Action match type '{match_k}' is not valid")

    def _parse_actions(self, action: str | dict[str, Any]) -> None:  # noqa: C901,PLR0912
        """Parse the actions."""
        # Check if this is a simple string action
        if isinstance(action, str):
            # Check if its a reject action
            if action == "reject":
                self._action_reject = True
            # And if its not known, raise an error
            else:
                raise BirdPlanConfigError(f"Action value '{action}' is not valid")
            return
        # Check what actions we have
        for action_k, action_v in action.items():
            # Make sure we only have lists or strings
            if not isinstance(action_v, list) and not isinstance(action_v, str) and not isinstance(action_v, int):
                raise BirdPlanConfigError("Action value for 'action' is not valid")
            # If we have a string, convert it to a list
            action_v_list: list[str | int] = []
            if isinstance(action_v, list):
                action_v_list.extend(action_v)
            else:
                action_v_list.append(action_v)

            # Process each type of action
            if action_k in (
                "add_community",
                "add_extended_community",
                "add_large_community",
                "remove_community",
                "remove_extended_community",
                "remove_large_community",
            ):
                setattr(self, f"_action_{action_k}", action_v_list)
            elif action_k == "prepend":
                # Make sure prepend can only be a string
                if isinstance(action_v, str):
                    prepend = int(action_v)
                elif isinstance(action_v, int):
                    prepend = action_v
                else:
                    raise BirdPlanConfigError(f"Action prepend value '{action_v}' is not valid")
                # Make sure prepend value is valid
                if 10 > prepend < 1:  # noqa: PLR2004
                    raise BirdPlanConfigError(f"Action prepend value '{action_v}' is not valid")
                self._action_prepend = prepend
            else:
                raise BirdPlanConfigError(f"Action type '{action_k}' is not valid")

    def generate_constants(self) -> list[str]:  # noqa: C901
        """Generate the constants for the action."""
        constants = []
        # Loop with basic match types
        for match_type in (
            "origin_asn",
            "prefix",
        ):
            match_list_name = getattr(self, f"match_list_name_{match_type}")
            # Pull out straight matches
            match_list = [x for x in getattr(self, f"_match_{match_type}") if not x.startswith("!")]
            # Pull out negative NOT matches
            match_list_not = [x[1:] for x in getattr(self, f"_match_{match_type}") if x.startswith("!")]
            # Generate origin ASN match lists
            if match_type == "origin_asn":
                if match_list:
                    constants.append(f"define {match_list_name} = [")
                    constants.extend([f"  {line}" for line in ", ".join(match_list).split(" ")])
                    constants.append("];")
                if match_list_not:
                    constants.append(f"define {match_list_name}_not = [")
                    constants.extend([f"  {line}" for line in ", ".join(match_list_not).split(" ")])
                    constants.append("];")
            # Generate prefix match lists
            elif match_type == "prefix":
                # Pull out IPv4 and IPv6 prefixes lists
                match_list_v4, match_list_not_v4, match_list_v6, match_list_not_v6 = self._get_match_prefix_lists()
                # Generate IPv4 prefix match lists
                if match_list_v4:
                    constants.append(f"define {match_list_name}_v4 = [")
                    constants.extend([f"  {line}" for line in ", ".join([x.replace(" ", "") for x in match_list_v4]).split(" ")])
                    constants.append("];")
                if match_list_not_v4:
                    constants.append(f"define {match_list_name}_not_v4 = [")
                    constants.extend(
                        [f"  {line}" for line in ", ".join([x.replace(" ", "") for x in match_list_not_v4]).split(" ")]
                    )
                    constants.append("];")
                # Generate IPv6 prefix match lists
                if match_list_v6:
                    constants.append(f"define {match_list_name}_v6 = [")
                    constants.extend([f"  {line}" for line in ", ".join([x.replace(" ", "") for x in match_list_v6]).split(" ")])
                    constants.append("];")
                if match_list_not_v6:
                    constants.append(f"define {match_list_name}_not_v6 = [")
                    constants.extend(
                        [f"  {line}" for line in ", ".join([x.replace(" ", "") for x in match_list_not_v6]).split(" ")]
                    )
                    constants.append("];")

        # Loop with community match types
        for match_type in (
            "community",
            "extended_community",
            "large_community",
        ):
            match_list_name = getattr(self, f"match_list_name_{match_type}")
            match_list = getattr(self, f"_match_{match_type}")
            # Loop with match list and convert from xxx:yyy to (xxx,yyy) format
            match_list = util.sanitize_community_list(match_list)
            if match_list:
                constants.append(f"define {match_list_name} = [")
                constants.extend([f"  {line}" for line in ", ".join(match_list).split(" ")])
                constants.append("];")
        # Return list of constants for this peer
        return constants

    def generate_function(self) -> list[str]:  # noqa: C901,PLR0912,PLR0915
        """Generate the function for the action."""
        function = []
        # Generate function header
        function.append(f"function {self.function_name}() -> bool")
        function.append("string filter_name;")
        function.append("{")
        function.append(f'  filter_name = "{self.function_name}";')

        # Generate match statements
        # NK: We use the for loop because we have duplicate code between the various match types
        for match_type in (
            "origin_asn",
            "prefix",
            "community",
            "extended_community",
            "large_community",
        ):
            match_list_name = getattr(self, f"match_list_name_{match_type}")
            # Grab list of raw matches
            match_list_raw = getattr(self, f"_match_{match_type}")
            # Pull out straight matches
            match_list = [x for x in match_list_raw if not x.startswith("!")]
            # Pull out negative NOT matches
            match_list_not = [x[1:] for x in match_list_raw if x.startswith("!")]

            # Add commentfor this match type
            if match_list_raw:
                function.append(f"  # Match {match_type}")
            # Check origin ASN match
            if match_type == "origin_asn":
                if match_list:
                    function.append(f"  if (bgp_path.first !~ {match_list_name}) then return true;")
                if match_list_not:
                    function.append(f"  if (bgp_path.first !~ {match_list_name}_not) then return true;")
            # Check prefix match
            elif match_type == "prefix":
                # Pull out IPv4 and IPv6 prefixes lists
                match_list_v4, match_list_not_v4, match_list_v6, match_list_not_v6 = self._get_match_prefix_lists()
                # Check IPv4 prefix match
                if match_list_v4 or match_list_not_v4:
                    function.append("  if (net.type = NET_IP4) then {{")
                    if match_list_v4:
                        function.append(f"    if (net !~ {match_list_name}_v4) then return true;")
                    if match_list_not_v4:
                        function.append(f"    if (net ~ {match_list_name}_not_v4) then return true;")
                    function.append("  }}")
                # Check IPv6 prefix match
                if match_list_v6 or match_list_not_v6:
                    function.append("  if (net.type = NET_IP6) then {{")
                    if match_list_v6:
                        function.append(f"    if (net !~ {match_list_name}_v6) then return true;")
                    if match_list_not_v6:
                        function.append(f"    if (net ~ {match_list_name}_not_v6) then return true;")
                    function.append("  }}")
            # Check community match
            elif match_type == "community":
                if match_list:
                    function.append(f"  if (bgp_community !~ {match_list_name}) then return true;")
                if match_list_not:
                    function.append(f"  if (bgp_community ~ {match_list_name}_not) then return true;")
            # Check extended community match
            elif match_type == "extended_community":
                if match_list:
                    function.append(f"  if (bgp_ext_community !~ {match_list_name}) then return true;")
                if match_list_not:
                    function.append(f"  if (bgp_ext_community ~ {match_list_name}_not) then return true;")
            # Check large community match
            elif match_type == "large_community":
                if match_list:
                    function.append(f"  if (bgp_large_community !~ {match_list_name}) then return true;")
                if match_list_not:
                    function.append(f"  if (bgp_large_community ~ {match_list_name}_not) then return true;")

        #
        # Generate action statements
        #

        fallthrough_value = "true"

        # Handle reject action
        if self._action_reject:
            if self.action_type == BGPPeerActionType.IMPORT:
                function.append(
                    f"  if DEBUG then print\n"
                    f"""    "{self.function_name} [action:{self.action_id}] Filtering ","""
                    f" {self.global_functions.route_info()};"
                )
                function.append("  bgp_large_community.add(BGP_LC_FILTERED_ACTION);")
            elif self.action_type == BGPPeerActionType.EXPORT:
                function.append(
                    f"  if DEBUG then print\n"
                    f"""    "{self.function_name} [action:{self.action_id}] Rejecting ","""
                    f" {self.global_functions.route_info()};"
                )
            # Set fallthrough value to false as we're rejecting
            fallthrough_value = "false"

        # Handle add_community action
        if self._action_add_community:
            function.append(
                f"  if DEBUG then print\n"
                f"""    "{self.function_name} [action:{self.action_id}] Adding communities """
                f"""{", ".join(self._action_add_community)} to ","""
                f" {self.global_functions.route_info()};"
            )
            function.extend(
                [f"  bgp_community.add({community});" for community in util.sanitize_community_list(self._action_add_community)]
            )

        # Handle add_extended_community action
        if self._action_add_extended_community:
            function.append(
                f"  if DEBUG then print\n"
                f"""    "{self.function_name} [action:{self.action_id}] Adding extended communities """
                f"""{", ".join(self._action_add_extended_community)} to ","""
                f" {self.global_functions.route_info()};"
            )
            function.extend(
                [
                    f"  bgp_ext_community.add({community});"
                    for community in util.sanitize_community_list(self._action_add_extended_community)
                ]
            )

        # Handle add_large_community action
        if self._action_add_large_community:
            function.append(
                f"  if DEBUG then print\n"
                f"""    "{self.function_name} [action:{self.action_id}] Adding large communities """
                f"""{", ".join(self._action_add_large_community)} to ","""
                f" {self.global_functions.route_info()};"
            )
            function.extend(
                [
                    f"  bgp_large_community.add({community});"
                    for community in util.sanitize_community_list(self._action_add_large_community)
                ]
            )

        # Handle remove_community action
        if self._action_remove_community:
            function.append(
                f"  if DEBUG then print\n"
                f"""    "{self.function_name} [action:{self.action_id}] Removing communities """
                f"""{", ".join(self._action_remove_community)} from ","""
                f" {self.global_functions.route_info()};"
            )
            function.extend([f"  bgp_community.remove({community});" for community in self._action_remove_community])

        # Handle remove_extended_community action
        if self._action_remove_extended_community:
            function.append(
                f"  if DEBUG then print\n"
                f"""    "{self.function_name} [action:{self.action_id}] Removing extended communities """
                f"""{", ".join(self._action_remove_extended_community)} from ","""
                f" {self.global_functions.route_info()};"
            )
            function.extend(
                [f"  bgp_extended_community.remove({community});" for community in self._action_remove_extended_community]
            )

        # Handle remove_large_community action
        if self._action_remove_large_community:
            function.append(
                f"  if DEBUG then print\n"
                f"""    "{self.function_name} [action:{self.action_id}] Removing large communities """
                f"""{", ".join(self._action_remove_large_community)} from ","""
                f" {self.global_functions.route_info()};"
            )
            function.extend([f"  bgp_large_community.remove({community});" for community in self._action_remove_large_community])

        # Handle prepend action
        if self._action_prepend:
            function.append(f"  {self.bgp_functions.peer_prepend(BirdVariable('BGP_ASN'), self._action_prepend)};")
        # Generate function footer
        function.append(f"  return {fallthrough_value};")
        function.append("}")

        # Return list of function lines
        return function

    def _get_match_prefix_lists(self) -> tuple[list[str], list[str], list[str], list[str]]:
        """Get the match prefix lists for IPv4 an IPv6."""
        match_list_v4 = [x for x in self._match_prefix if ":" not in x]
        match_list_not_v4 = [x for x in self._match_prefix if ":" not in x]
        match_list_v6 = [x for x in self._match_prefix if ":" in x]
        match_list_not_v6 = [x for x in self._match_prefix if ":" in x]
        return match_list_v4, match_list_not_v4, match_list_v6, match_list_not_v6

    @property
    def global_functions(self) -> SectionFunctions:
        """Return the global functions."""
        return self._global_functions

    @property
    def bgp_functions(self) -> BGPFunctions:
        """Return the BGP functions."""
        return self._bgp_functions

    @property
    def function_name(self) -> str:
        """Return our origin ASN deny list name."""
        return f"bgp_AS{self.asn}_{self.peer_name}_action{self.action_id}_{self.action_type.value}"

    @property
    def match_list_name_origin_asn(self) -> str:
        """Return our origin ASN deny list name."""
        return f"bgp_AS{self.asn}_{self.peer_name}_action{self.action_id}_match_origin_asn"

    @property
    def match_list_name_prefix(self) -> str:
        """Return our origin ASN deny list name."""
        return f"bgp_AS{self.asn}_{self.peer_name}_action{self.action_id}_match_prefix"

    @property
    def match_list_name_community(self) -> str:
        """Return our origin ASN deny list name."""
        return f"bgp_AS{self.asn}_{self.peer_name}_action{self.action_id}_match_community"

    @property
    def match_list_name_extended_community(self) -> str:
        """Return our origin ASN deny list name."""
        return f"bgp_AS{self.asn}_{self.peer_name}_action{self.action_id}_match_extended_community"

    @property
    def match_list_name_large_community(self) -> str:
        """Return our origin ASN deny list name."""
        return f"bgp_AS{self.asn}_{self.peer_name}_action{self.action_id}_match_large_community"

    @property
    def asn(self) -> int:
        """Return the ASN."""
        return self._asn

    @property
    def peer_name(self) -> str:
        """Return the peer name."""
        return self._peer_name

    @property
    def action_id(self) -> int:
        """Return the action ID."""
        return self._action_id

    @property
    def action_type(self) -> BGPPeerActionType:
        """Return the action type."""
        return self._action_type


class BGPPeerActions:
    """BGP peer actions."""

    _global_functions: SectionFunctions
    _bgp_functions: BGPFunctions

    _asn: int
    _peer_name: str
    _actions: list[BGPPeerAction]

    def __init__(self, global_functions: SectionFunctions, bgp_functions: BGPFunctions, asn: int, peer_name: str) -> None:
        """Initialize BGP peer actions."""

        self._global_functions = global_functions
        self._bgp_functions = bgp_functions

        self._asn = asn
        self._peer_name = peer_name

        self._actions = []

    def configure(self, actions: list[dict[str, Any]]) -> None:
        """Configure BGP peer actions."""
        # Check type of data provided
        if not isinstance(actions, list):
            raise BirdPlanConfigError(
                f"Configuration item has invalid type '{type(actions)}' in bgp:peers:{self.peer_name}:actions"
            )
        # Loop with actions
        action_id = 1
        for action in actions:
            self.actions.append(
                BGPPeerAction(self.global_functions, self.bgp_functions, self.asn, self.peer_name, action_id, action)
            )
            action_id += 1

    def generate_constants(self) -> list[str]:
        """Generate the constants for the actions."""
        constants = []
        for action in self.actions:
            constants.extend(action.generate_constants())
        return constants

    def generate_functions(self) -> list[str]:
        """Generate the functions for the actions."""
        functions = []
        for action in self.actions:
            functions.extend(action.generate_function())
        return functions

    @property
    def global_functions(self) -> SectionFunctions:
        """Return the global functions."""
        return self._global_functions

    @property
    def bgp_functions(self) -> BGPFunctions:
        """Return the BGP functions."""
        return self._bgp_functions

    @property
    def asn(self) -> int:
        """Return the ASN."""
        return self._asn

    @property
    def peer_name(self) -> str:
        """Return the peer name."""
        return self._peer_name

    @property
    def actions(self) -> list[BGPPeerAction]:
        """Return the actions."""
        return self._actions
