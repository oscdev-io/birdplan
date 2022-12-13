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

"""BIRD functions configuration."""

import textwrap
from collections import OrderedDict
from typing import Any, Callable, Dict, List

from ...bird_config.globals import BirdConfigGlobals
from .base import SectionBase


class BirdVariable(str):
    """BIRD constant class."""


class bird_function:  # pylint: disable=invalid-name,too-few-public-methods
    r'''
    BIRD function decorator class.

    This decorator is used to decorate a BIRD function returned in Python.

    When the decorated function is used, a reference to the function is stored and when the configuration is
    generated the function is called and the output included in the configuration functions section.

    An example of a decorated function is below...
    ```
        @bird_function("bgp_some_function")
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

    def __init__(self, bird_func_name: str):
        """Initialize object."""
        # Lets keep track of our BIRD function name
        self.bird_func_name = bird_func_name

    def __call__(self, func: Callable[..., str]) -> Callable[..., str]:  # noqa: C901
        """Return the wrapper."""

        def wrapped_function(*args: Any, **kwargs: Any) -> str:
            """My decorator."""
            # Grab the parent object
            parent_object = args[0]
            # Make sure it has a bird_functions attribute
            if hasattr(parent_object, "bird_functions"):
                # Check if this function exists...
                if self.bird_func_name not in parent_object.bird_functions:
                    # If not add it to the function list
                    parent_object.bird_functions[self.bird_func_name] = func(*args)
            else:
                raise RuntimeError("Decorator 'bird_function' used on a class method without a 'bird_functions' attribute")

            bird_args: List[str] = []
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
                    if arg:
                        value = "true"
                    else:
                        value = "false"
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

    bird_functions: Dict[str, str]

    def __init__(self, birdconfig_globals: BirdConfigGlobals):
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        self._section = "Global Functions"

        self.bird_functions = OrderedDict()

    def configure(self) -> None:
        """Configure global constants."""
        super().configure()

        # Check if we're adding functions
        for _, content in self.bird_functions.items():
            self.conf.add(textwrap.dedent(content))
            self.conf.add("")

    @bird_function("prefix_is_longer")
    def prefix_is_longer(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD prefix_is_longer function."""

        return """\
            # Match a prefix longer than "size"
            function prefix_is_longer(string filter_name; int size) {
                if (net.len > size) then {
                    if DEBUG then print filter_name,
                        " [prefix_is_longer] Matched ", net, " from ", proto, " against size ", size;
                    return true;
                } else {
                    return false;
                }
            }"""

    @bird_function("prefix_is_shorter")
    def prefix_is_shorter(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD prefix_is_shorter function."""

        return """\
            # Match a prefix shorter than "size"
            function prefix_is_shorter(string filter_name; int size) {
                if (net.len < size) then {
                    if DEBUG then print filter_name,
                        " [prefix_is_shorter] Matched ", net, " from ", proto, " against size ", size;
                    return true;
                }
                return false;
            }"""

    @bird_function("accept_kernel")
    def accept_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD accept_kernel function."""

        return f"""\
            # Accept kernel route
            function accept_kernel(string filter_name) {{
                if (!{self.is_kernel()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_kernel] Accepting kernel route ", {self.route_info()};
                accept;
            }}"""

    @bird_function("accept_kernel_default")
    def accept_kernel_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD accept_kernel_default function."""

        return f"""\
            # Accept kernel route
            function accept_kernel_default(string filter_name) {{
                if (!{self.is_kernel()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_kernel_default] Accepting kernel default route ", {self.route_info()};
                accept;
            }}"""

    @bird_function("accept_static")
    def accept_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD accept_static function."""

        return f"""\
            # Accept static route
            function accept_static(string filter_name) {{
                if (!{self.is_static()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_static] Accepting static route ", {self.route_info()};
                accept;
            }}"""

    @bird_function("accept_static_default")
    def accept_static_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD accept_static_default function."""

        return f"""\
            # Accept static default route
            function accept_static_default(string filter_name) {{
                if (!{self.is_static()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [accept_static] Accepting static default route ", {self.route_info()};
                accept;
            }}"""

    @bird_function("is_bgp")
    def is_bgp(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD is_bgp function."""

        return """\
            # Match BGP routes
            function is_bgp(string filter_name) {
                if (source = RTS_BGP) then return true;
                return false;
            }"""

    @bird_function("is_bogon")
    def is_bogon(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD is_bogon function."""

        return f"""\
            # Match on IP bogons
            function is_bogon(string filter_name) {{
                if ((net.type = NET_IP4 && net ~ BOGONS_V4) || (net.type = NET_IP6 && net ~ BOGONS_V6)) then {{
                    if DEBUG then print filter_name,
                        " [is_bogon] Matched ", {self.route_info()};
                    return true;
                }}
                return false;
            }}"""

    @bird_function("is_connected")
    def is_connected(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD is_connected function."""

        return """\
            # Match connected route
            function is_connected(string filter_name) {
                if (proto = "direct4" || proto = "direct6") then return true;
                return false;
            }"""

    @bird_function("is_default")
    def is_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD is_default function."""

        return """\
            # Match default route
            function is_default(string filter_name) {
                if ((net.type = NET_IP4 && net = DEFAULT_ROUTE_V4) || (net.type = NET_IP6 && net = DEFAULT_ROUTE_V6)) then
                    return true;
                return false;
            }"""

    @bird_function("is_kernel")
    def is_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD is_kernel function."""

        return """\
            # Match kernel route
            function is_kernel(string filter_name) {
                if (source = RTS_INHERIT) then return true;
                return false;
            }"""

    @bird_function("is_static")
    def is_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD is_static function."""

        return """\
            # Match static route
            function is_static(string filter_name) {
                if (proto = "static4" || proto = "static6") then return true;
                return false;
            }"""

    @bird_function("redistribute_kernel")
    def redistribute_kernel(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD redistribute_kernel function."""

        return f"""\
            # Accept kernel route
            function redistribute_kernel(string filter_name) {{
                if (!{self.is_kernel()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_kernel] Accepting kernel route ", {self.route_info()};
                accept;
            }}"""

    @bird_function("redistribute_kernel_default")
    def redistribute_kernel_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD redistribute_kernel_default function."""

        return f"""\
            # Accept kernel route
            function redistribute_kernel_default(string filter_name) {{
                if (!{self.is_kernel()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_kernel_default] Accepting kernel default route ", {self.route_info()};
                accept;
            }}"""

    @bird_function("redistribute_static")
    def redistribute_static(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD redistribute_static function."""

        return f"""\
            # Accept static route
            function redistribute_static(string filter_name) {{
                if (!{self.is_static()} || {self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_static] Accepting static route ", {self.route_info()};
                accept;
            }}"""

    @bird_function("redistribute_static_default")
    def redistribute_static_default(self, *args: Any) -> str:  # pylint: disable=unused-argument
        """BIRD redistribute_static_default function."""

        return f"""\
            # Accept static default route
            function redistribute_static_default(string filter_name) {{
                if (!{self.is_static()} || !{self.is_default()}) then return false;
                if DEBUG then print filter_name,
                    " [redistribute_static] Accepting static default route ", {self.route_info()};
                accept;
            }}"""

    def route_info(self) -> str:  # pylint: disable=unused-argument
        """BIRD route_info function."""

        return """net, " from ", proto"""
