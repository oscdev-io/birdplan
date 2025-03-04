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

"""BIRD functions configuration."""

import textwrap
from collections import OrderedDict
from collections.abc import Callable
from typing import Any

from ...bird_config.globals import BirdConfigGlobals
from .base import SectionBase

__all__ = ["BirdFunction", "BirdFunctionArg", "BirdVariable", "SectionFunctions"]


class BirdVariable(str):
    """BIRD constant class."""

    __slots__ = ()


# Bird function argument type
BirdFunctionArg = BirdVariable | str | int | bool


class BirdFunction:  # pylint: disable=invalid-name,too-few-public-methods
    r'''
    BIRD function decorator class.

    This decorator is used to decorate a BIRD function returned in Python.

    When the decorated function is used, a reference to the function is stored and when the configuration is
    generated the function is called and the output included in the configuration functions section.

    An example of a decorated function is below...
    ```
        @BirdFunction("bgp_some_function")
        def bgp_func(self) -> str:
            """Test function."""

            return """\
                # Some BIRD function
                function bgp_some_function(string filter_name; bool capable; int peer_asn; int type_asn) {
                    ...
                }
            }"""
    ```

    This would be used in BIRD configuration like this...
    ```
        conf.append(f"if {obj.bgpfunc('hello world')} then print 'hello there';")
    ```

    Parameters
    ----------
    bird_func_name : str
        BIRD function name.

    '''

    bird_func_name: str

    def __init__(self, bird_func_name: str) -> None:
        """Initialize object."""
        # Lets keep track of our BIRD function name
        self.bird_func_name = bird_func_name

    def __call__(self, func: Callable[..., str]) -> Callable[..., str]:
        """Return the wrapper."""

        def wrapped_function(*args: BirdFunctionArg, **kwargs: Any) -> str:  # noqa: ANN401
            """My decorator."""
            # Grab the parent object
            parent_object = args[0]
            # Make sure it has a bird_functions attribute
            if hasattr(parent_object, "bird_functions"):
                # Check if this function exists...
                bird_function_list = getattr(parent_object, "bird_functions")  # noqa: B009
                if self.bird_func_name not in bird_function_list:
                    # If not add it to the function list
                    bird_function_list[self.bird_func_name] = func(*args)
            else:
                raise RuntimeError("Decorator 'bird_function' used on a class method without a 'bird_functions' attribute")

            bird_args: list[str] = []
            # Check if we're not outputting the filter_name
            needs_filter_name = not kwargs.get("no_filter_name", False)
            if needs_filter_name:
                bird_args.append(BirdVariable("filter_name"))
            # Loop with python arguments and translate into BIRD arguments
            for arg in args[1:]:
                value = ""
                # Check for unquaoted BIRD variables
                if isinstance(arg, BirdVariable):
                    value = arg
                # Check for a boolean
                elif isinstance(arg, bool):
                    value = "true" if arg else "false"
                # Check for a number
                elif isinstance(arg, int):
                    value = f"{arg}"
                # Check if this is a string
                elif isinstance(arg, str):
                    value = f'"{arg}"'
                # Everything else is not implemented atm
                else:
                    raise NotImplementedError(f"Unknown type for '{self.bird_func_name}' value '{arg}'")
                # Add BIRD argument
                bird_args.append(value)

            # Build the list of BIRD arguments in a string
            bird_args_str = ", ".join(bird_args)
            # Return the BIRD function call
            return f"{self.bird_func_name}({bird_args_str})"

        # Finally return the wrapped function
        return wrapped_function


class SectionFunctions(SectionBase):
    """BIRD functions configuration."""

    bird_functions: dict[str, str]

    def __init__(self, birdconfig_globals: BirdConfigGlobals) -> None:
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        self._section = "Global Functions"

        self.bird_functions = OrderedDict()

    def configure(self) -> None:
        """Configure global constants."""
        super().configure()

        # Check if we're adding functions
        for content in self.bird_functions.values():
            self.conf.add(textwrap.dedent(content))
            self.conf.add("")

    @BirdFunction("prefix_is_longer")
    def prefix_is_longer(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD prefix_is_longer function."""

        return """\
            # Match a prefix longer than "size"
            function prefix_is_longer(string filter_name; int prefix_len) -> bool {
                if (net.len > prefix_len) then {
                    if DEBUG then print filter_name,
                        " [prefix_is_longer] Matched ", net, " from ", proto, " against length ", prefix_len;
                    return true;
                } else {
                    return false;
                }
            }"""

    @BirdFunction("prefix_is_shorter")
    def prefix_is_shorter(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD prefix_is_shorter function."""

        return """\
            # Match a prefix shorter than "size"
            function prefix_is_shorter(string filter_name; int prefix_len) -> bool {
                if (net.len < prefix_len) then {
                    if DEBUG then print filter_name,
                        " [prefix_is_shorter] Matched ", net, " from ", proto, " against length ", prefix_len;
                    return true;
                }
                return false;
            }"""

    @BirdFunction("accept_kernel")
    def accept_kernel(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD accept_kernel function."""

        return f"""\
            # Accept kernel route
            function accept_kernel(string filter_name) -> bool {{
                if (!{self.is_kernel()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_kernel] Accepting kernel route ", {self.route_info()};
                accept;
            }}"""

    @BirdFunction("accept_kernel_default")
    def accept_kernel_default(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD accept_kernel_default function."""

        return f"""\
            # Accept kernel route
            function accept_kernel_default(string filter_name) -> bool {{
                if (!{self.is_kernel()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_kernel_default] Accepting kernel default route ", {self.route_info()};
                accept;
            }}"""

    @BirdFunction("accept_static")
    def accept_static(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD accept_static function."""

        return f"""\
            # Accept static route
            function accept_static(string filter_name) -> bool {{
                if (!{self.is_static()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_static] Accepting static route ", {self.route_info()};
                accept;
            }}"""

    @BirdFunction("accept_static_default")
    def accept_static_default(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD accept_static_default function."""

        return f"""\
            # Accept static default route
            function accept_static_default(string filter_name) -> bool {{
                if (!{self.is_static()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_static] Accepting static default route ", {self.route_info()};
                accept;
            }}"""

    @BirdFunction("is_bgp")
    def is_bgp(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD is_bgp function."""

        return """\
            # Match BGP routes
            function is_bgp(string filter_name) -> bool {
                if (source = RTS_BGP) then return true;
                return false;
            }"""

    @BirdFunction("is_bogon")
    def is_bogon(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD is_bogon function."""

        return f"""\
            # Match on IP bogons
            function is_bogon(string filter_name) -> bool {{
                if ((net.type = NET_IP4 && net ~ BOGONS_V4) || (net.type = NET_IP6 && net ~ BOGONS_V6)) then {{
                    if DEBUG then print filter_name,
                        " [is_bogon] Matched ", {self.route_info()};
                    return true;
                }}
                return false;
            }}"""

    @BirdFunction("is_connected")
    def is_connected(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD is_connected function."""

        return """\
            # Match connected route
            function is_connected(string filter_name) -> bool {
                if (proto = "direct4" || proto = "direct6") then return true;
                return false;
            }"""

    @BirdFunction("is_default")
    def is_default(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD is_default function."""

        return """\
            # Match default route
            function is_default(string filter_name) -> bool {
                if ((net.type = NET_IP4 && net = DEFAULT_ROUTE_V4) || (net.type = NET_IP6 && net = DEFAULT_ROUTE_V6)) then
                    return true;
                return false;
            }"""

    @BirdFunction("is_kernel")
    def is_kernel(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD is_kernel function."""

        # NK: Below we explicitly exclude krt_source = 186 as we seem to import IPv6 routes into Bird for some reason
        return """\
            # Match kernel route
            function is_kernel(string filter_name) -> bool {
                if (source = RTS_INHERIT && krt_source != 186) then return true;
                return false;
            }"""

    @BirdFunction("is_static")
    def is_static(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD is_static function."""

        return """\
            # Match static route
            function is_static(string filter_name) -> bool {
                if (proto = "static4" || proto = "static6") then return true;
                return false;
            }"""

    @BirdFunction("redistribute_kernel")
    def redistribute_kernel(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD redistribute_kernel function."""

        return f"""\
            # Accept kernel route
            function redistribute_kernel(string filter_name) -> bool {{
                if (!{self.is_kernel()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_kernel] Accepting kernel route ", {self.route_info()};
                accept;
            }}"""

    @BirdFunction("redistribute_kernel_default")
    def redistribute_kernel_default(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD redistribute_kernel_default function."""

        return f"""\
            # Accept kernel route
            function redistribute_kernel_default(string filter_name) -> bool {{
                if (!{self.is_kernel()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_kernel_default] Accepting kernel default route ", {self.route_info()};
                accept;
            }}"""

    @BirdFunction("redistribute_static")
    def redistribute_static(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD redistribute_static function."""

        return f"""\
            # Accept static route
            function redistribute_static(string filter_name) -> bool {{
                if (!{self.is_static()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_static] Accepting static route ", {self.route_info()};
                accept;
            }}"""

    @BirdFunction("redistribute_static_default")
    def redistribute_static_default(self, *args: BirdFunctionArg) -> str:  # noqa: ARG002
        """BIRD redistribute_static_default function."""

        return f"""\
            # Accept static default route
            function redistribute_static_default(string filter_name) -> bool {{
                if (!{self.is_static()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_static] Accepting static default route ", {self.route_info()};
                accept;
            }}"""

    def route_info(self) -> str:  # pylint: disable=unused-argument
        """BIRD route_info function."""

        return """net, " from ", proto"""
