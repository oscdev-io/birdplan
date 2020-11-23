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

from typing import Any, Callable, List

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
        def bgp_func(self) -> str:  # pylint: disable=no-self-use
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

    def __call__(self, func: Callable[..., str]) -> Callable[..., str]:
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

    _section: str = "Global Functions"

    _need_functions: bool

    def __init__(self, birdconfig_globals: BirdConfigGlobals):
        """Initialize the object."""
        super().__init__(birdconfig_globals)

        # Add functions to output
        self._need_functions = False

    def configure(self) -> None:
        """Configure global constants."""
        super().configure()

        # Check if we're adding functions
        if self.need_functions:
            self._configure_functions()

    def _configure_functions(self) -> None:
        """Configure functions."""
        self.conf.add('# Match a prefix longer than "size".')
        self.conf.add("function prefix_is_longer(int size) {")
        self.conf.add("  if (net.len > size) then {")
        self.conf.add('    print "[prefix_is_longer] Matched ", net, " against size ", size;', debug=True)
        self.conf.add("    return true;")
        self.conf.add("  } else {")
        self.conf.add("    return false;")
        self.conf.add("  }")
        self.conf.add("}")
        self.conf.add("")
        self.conf.add('# Match a prefix shorter than "size".')
        self.conf.add("function prefix_is_shorter(int size) {")
        self.conf.add("  if (net.len < size) then {")
        self.conf.add('    print "[prefix_is_shorter] Matched ", net, " against size ", size;', debug=True)
        self.conf.add("    return true;")
        self.conf.add("  } else {")
        self.conf.add("    return false;")
        self.conf.add("  }")
        self.conf.add("}")
        self.conf.add("")
        self.conf.add("# Match on IP bogons")
        self.conf.add("function is_bogon() {")
        self.conf.add("  if ((net.type = NET_IP4 && net ~ BOGONS_V4) || (net.type = NET_IP6 && net ~ BOGONS_V6)) then {")
        self.conf.add('    print "[is_bogon] Matched ", net;', debug=True)
        self.conf.add("    return true;")
        self.conf.add("  } else {")
        self.conf.add("    return false;")
        self.conf.add("  }")
        self.conf.add("}")
        self.conf.add("# Match a default route")
        self.conf.add("function is_default() {")
        self.conf.add("  if (net.type = NET_IP4 && net = DEFAULT_ROUTE_V4) then return true;")
        self.conf.add("  if (net.type = NET_IP6 && net = DEFAULT_ROUTE_V6) then return true;")
        self.conf.add("  return false;")
        self.conf.add("}")
        self.conf.add("")

    @property
    def need_functions(self) -> bool:
        """Return if functions should be added to our output constants block."""
        return self._need_functions

    @need_functions.setter
    def need_functions(self, need_functions: bool) -> None:
        """Set if functions should be added to our output constants block."""
        self._need_functions = need_functions
