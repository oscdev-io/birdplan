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

"""BIRD BGP peer action support."""

from typing import Any, Dict, List, Tuple

from ......exceptions import BirdPlanConfigError
from ..... import util
from ....functions import BirdVariable
from ..bgp_functions import BGPFunctions

__all__ = ["BGPPeerActions"]


class BGPPeerAction:
    """BGP peer action."""

    _bgp_functions: BGPFunctions

    _asn: int
    _peer_name: str

    _action_id: int
    _direction: str

    _match_origin_asn: List[str]
    _match_prefix: List[str]
    _match_community: List[str]
    _match_extended_community: List[str]
    _match_large_community: List[str]

    _action_reject: bool
    _action_add_community: List[str]
    _action_add_extended_community: List[str]
    _action_add_large_community: List[str]
    _action_remove_community: List[str]
    _action_remove_extended_community: List[str]
    _action_remove_large_community: List[str]
    _action_prepend: int

    def __init__(self, bgp_functions: BGPFunctions, asn: int, peer_name: str, action_id: int, action: Dict[str, Any]) -> None:
        """Initialize BGP peer action."""

        self._bgp_functions = bgp_functions

        self._asn = asn
        self._peer_name = peer_name
        self._action_id = action_id

        # Grab direction
        self._direction = action["direction"]

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
        self._parse_matches(action["matches"])
        self._parse_actions(action["action"])

    def _parse_matches(self, matches: Dict[str, Any]) -> None:
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

    def _parse_actions(self, action: Dict[str, Any]) -> None:
        """Parse the actions."""
        # Check what actions we have
        for action_k, action_v in action.items():
            # Make sure we only have lists or strings
            if not isinstance(action_v, list) and not isinstance(action_v, str):
                raise BirdPlanConfigError("Action value for 'action' is not valid")
            # If we have a string, convert it to a list
            action_v_list: list[str] = []
            if isinstance(action_v, str):
                action_v_list.append(action_v)
            else:
                action_v_list.extend(action_v)
            # Process each type of action
            if action_k == "reject":
                self._action_reject = True
            elif action_k in (
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
                if not isinstance(action_v, str):
                    raise BirdPlanConfigError(f"Action prepend value '{action_v}' is not valid")
                # Convert to integer
                prepend = int(action_v)
                # Make sure prepend value is valid
                if 10 > prepend < 1:
                    raise BirdPlanConfigError(f"Action prepend value '{action_v}' is not valid")
                self._action_prepend = prepend
            else:
                raise BirdPlanConfigError(f"Action type '{action_k}' is not valid")

    def generate_constants(self) -> List[str]:  # pylint: disable=too-many-branches
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
                    for line in ", ".join(match_list).split(" "):
                        constants.append(f"  {line}")
                    constants.append("];")
                if match_list_not:
                    constants.append(f"define {match_list_name}_not = [")
                    for line in ", ".join(match_list_not).split(" "):
                        constants.append(f"  {line}")
                    constants.append("];")
            # Generate prefix match lists
            elif match_type == "prefix":
                # Pull out IPv4 and IPv6 prefixes lists
                match_list_v4, match_list_not_v4, match_list_v6, match_list_not_v6 = self._get_match_prefix_lists()
                # Generate IPv4 prefix match lists
                if match_list_v4:
                    constants.append(f"define {match_list_name}_v4 = [")
                    for line in ", ".join([x.replace(" ", "") for x in match_list_v4]).split(" "):
                        constants.append(f"  {line}")
                    constants.append("];")
                if match_list_not_v4:
                    constants.append(f"define {match_list_name}_not_v4 = [")
                    for line in ", ".join([x.replace(" ", "") for x in match_list_not_v4]).split(" "):
                        constants.append(f"  {line}")
                    constants.append("];")
                # Generate IPv6 prefix match lists
                if match_list_v6:
                    constants.append(f"define {match_list_name}_v6 = [")
                    for line in ", ".join([x.replace(" ", "") for x in match_list_v6]).split(" "):
                        constants.append(f"  {line}")
                    constants.append("];")
                if match_list_not_v6:
                    constants.append(f"define {match_list_name}_not_v6 = [")
                    for line in ", ".join([x.replace(" ", "") for x in match_list_not_v6]).split(" "):
                        constants.append(f"  {line}")
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
                for line in ", ".join(match_list).split(" "):
                    constants.append(f"  {line}")
                constants.append("];")
        # Return list of constants for this peer
        return constants

    def generate_function(self) -> List[str]:  # pylint: disable=too-many-branches,too-many-statements
        """Generate the function for the action."""
        function = []
        # Generate function header
        function.append(f"function {self.function_name}() {{")

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

        # Handle reject action
        if self._action_reject:
            function.append("  return false;")

        # Handle add_community action
        if self._action_add_community:
            for community in self._action_add_community:
                function.append(f"  bgp_community.add({community});")

        # Handle add_extended_community action
        if self._action_add_extended_community:
            for community in self._action_add_extended_community:
                function.append(f"  bgp_extended_community.add({community});")

        # Handle add_large_community action
        if self._action_add_large_community:
            for community in self._action_add_large_community:
                function.append(f"  bgp_large_community.add({community});")

        # Handle remove_community action
        if self._action_remove_community:
            for community in self._action_remove_community:
                function.append(f"  bgp_community.remove({community});")

        # Handle remove_extended_community action
        if self._action_remove_extended_community:
            for community in self._action_remove_extended_community:
                function.append(f"  bgp_extended_community.remove({community});")

        # Handle remove_large_community action
        if self._action_remove_large_community:
            for community in self._action_remove_large_community:
                function.append(f"  bgp_large_community.remove({community});")

        # Handle prepend action
        if self._action_prepend:
            function.append(f"  {self.bgp_functions.peer_prepend(BirdVariable(self._action_prepend))};")
        # Generate function footer
        function.append("  return true;")
        function.append("}")

        # Return list of function lines
        return function

    def _get_match_prefix_lists(self) -> Tuple[List[str], List[str], List[str], List[str]]:
        """Get the match prefix lists for IPv4 an IPv6."""
        match_list_v4 = [x for x in self._match_prefix if ":" not in x]
        match_list_not_v4 = [x for x in self._match_prefix if ":" not in x]
        match_list_v6 = [x for x in self._match_prefix if ":" in x]
        match_list_not_v6 = [x for x in self._match_prefix if ":" in x]
        return match_list_v4, match_list_not_v4, match_list_v6, match_list_not_v6

    @property
    def bgp_functions(self) -> BGPFunctions:
        """Return the BGP functions."""
        return self._bgp_functions

    @property
    def function_name(self) -> str:
        """Return our origin ASN deny list name."""
        return f"bgp_AS{self.asn}_{self.peer_name}_action{self.action_id}_{self.direction}"

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
    def direction(self) -> str:
        """Return the direction."""
        return self._direction


class BGPPeerActions:
    """BGP peer actions."""

    _bgp_functions: BGPFunctions

    _asn: int
    _peer_name: str
    _actions: List[BGPPeerAction]

    def __init__(self, bgp_functions: BGPFunctions, asn: int, peer_name: str) -> None:
        """Initialize BGP peer actions."""

        self._asn = asn
        self._peer_name = peer_name

        self._bgp_functions = bgp_functions

    def configure(self, actions: List[Dict[str, Any]]) -> None:
        """Configure BGP peer actions."""

        # Check type of data provided
        if not isinstance(actions, list):
            raise BirdPlanConfigError(
                f"Configuration item has invalid type '{type(actions)}' in bgp:peers:{self.peer_name}:actions"
            )
        # Loop with actions
        action_id = 1
        for action in actions:
            self.actions.append(BGPPeerAction(self.bgp_functions, self.asn, self.peer_name, action_id, action))
            action_id += 1

    def generate_constants(self) -> List[str]:
        """Generate the constants for the actions."""
        constants = []
        for action in self.actions:
            constants.extend(action.generate_constants())
        return constants

    def generate_functions(self) -> List[str]:
        """Generate the functions for the actions."""
        functions = []
        for action in self.actions:
            functions.extend(action.generate_function())
        return functions

    @property
    def asn(self) -> int:
        """Return the ASN."""
        return self._asn

    @property
    def peer_name(self) -> str:
        """Return the peer name."""
        return self._peer_name

    @property
    def actions(self) -> List[BGPPeerAction]:
        """Return the actions."""
        return self._actions

    @property
    def bgp_functions(self) -> BGPFunctions:
        """Return the BGP functions."""
        return self._bgp_functions
