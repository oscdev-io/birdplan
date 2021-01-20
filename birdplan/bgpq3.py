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

"""BGPQ3 support class."""

from typing import Any, Dict, List, Optional, Union
import ipaddress
import json
import subprocess  # nosec
import time

from .exceptions import BirdPlanError


# Keep a cache for results returned while loaded into memory
#
# Example:
# bgpq3_cache = {
#     'whois.radb.net:43': {
#         'objects': {
#             'AS174': {
#               '_timestamp': 0000000000,
#               'value': xxxxxx,
#             }
#         }
#     }
# }
bgpq3_cache: Dict[str, Dict[str, Any]] = {}


class BGPQ3:
    """BGPQ3 support class."""

    _host: str
    _port: int
    _sources: str

    def __init__(self, host: str = "whois.radb.net", port: int = 43, sources: str = "RADB"):
        """Initialize object."""

        # Grab items we can set and associated defaults
        self._host = host
        self._port = port
        self._sources = sources

    def get_asns(self, as_sets: Union[str, List[str]]) -> List[str]:
        """Get prefixes."""

        # Build an object list depending on the type of "objects" above
        objects: List[str] = []
        if isinstance(as_sets, str):
            objects.append(as_sets)
        else:
            objects.extend(as_sets)

        # Grab ASNs
        asns_bgpq3: Dict[str, List[str]] = {}
        for obj in objects:
            # Try pull result from our cache
            result: Any = self._cache(f"asns:{obj}")
            # If we can't, grab the result from BGPQ3 live
            if not result:
                # Try query object
                try:
                    result = self._bgpq3(["-l", "asns", "-t", "-3", obj])
                except subprocess.CalledProcessError as err:
                    raise BirdPlanError(f"Failed to query IRR ASNs from object '{obj}':\n%s" % err.output.decode("UTF-8")) from None
                # Cache the result we got
                self._cache(f"asns:{obj}", result)
            # Update return value with result
            asns_bgpq3.update(result)

        # If we don't have "asns" returned in the JSON structure, raise an exception
        if "asns" not in asns_bgpq3:  # pragma: no cover
            raise BirdPlanError(f"BGPQ3 output error, expecting 'asns': {asns_bgpq3}")

        return asns_bgpq3["asns"]

    def get_prefixes(self, as_sets: Union[str, List[str]]) -> Dict[str, List[str]]:
        """Get prefixes."""

        # Build an object list depending on the type of "objects" above
        objects: List[str] = []
        if isinstance(as_sets, str):
            objects.append(as_sets)
        else:
            objects.extend(as_sets)

        # Grab IPv4 and IPv6 prefixes
        prefixes_bgpq3: Dict[str, List[Dict[str, Any]]] = {}
        for obj in objects:
            # Try pull result from our cache
            result: Any = self._cache(f"prefixes:{obj}")
            # If we can't, grab the result from BGPQ3 live
            if not result:
                result = {}
                # Lets see if we get results back from our IRR queries
                try:
                    result.update(self._bgpq3(["-l", "ipv4", "-m", "24", "-4", "-A", obj]))
                except subprocess.CalledProcessError as err:
                    raise BirdPlanError(
                        f"Failed to query IRR IPv4 prefixes from object '{obj}':\n%s" % err.output.decode("UTF-8")
                    ) from None
                try:
                    result.update(self._bgpq3(["-l", "ipv6", "-m", "48", "-6", "-A", obj]))
                except subprocess.CalledProcessError as err:
                    raise BirdPlanError(
                        f"Failed to query IRR IPv6 prefixes from object '{obj}':\n%s" % err.output.decode("UTF-8")
                    ) from None
                # Cache the result we got
                self._cache(f"prefixes:{obj}", result)
            # Update return value with result
            prefixes_bgpq3.update(result)

        # Start out with no prefixes
        prefixes: Dict[str, List[str]] = {"ipv4": [], "ipv6": []}

        for family in ("ipv4", "ipv6"):
            for prefix in prefixes_bgpq3[family]:
                # If it is exact, its easy to add
                if prefix["exact"]:
                    prefixes[family].append(prefix["prefix"])
                else:
                    # Work out greater_equal component
                    if "greater-equal" in prefix:
                        greater_equal = prefix["greater-equal"]
                    else:
                        greater_equal = ipaddress.ip_network(prefix["prefix"]).prefixlen
                    # Add prefix
                    prefixes[family].append("%s{%s,%s}" % (prefix["prefix"], greater_equal, prefix["less-equal"]))

        return prefixes

    def _bgpq3(self, args: List[str]) -> Any:
        """Run bgpq3."""

        # Run the IP tool with JSON output
        cmd_args = ["/usr/bin/bgpq3", "-h", self.server, "-j"]
        # Add our args
        cmd_args.extend(args)

        # Grab result from process execution
        result = subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)  # nosec

        # Return the decoded json output
        return json.loads(result)

    def _cache(self, obj: str, value: Optional[Any] = None) -> Optional[Any]:
        """Retrieve or store value in cache."""

        if self.server not in bgpq3_cache:
            bgpq3_cache[self.server] = {"objects": {}}

        if not value:
            # If the cached obj does not exist, return None
            if obj not in bgpq3_cache[self.server]["objects"]:
                return None
            # Grab the cached object
            cached = bgpq3_cache[self.server]["objects"][obj]
            # Make sure its timestamp is within 60s of being retrieved, if not, return None
            if cached["_timestamp"] + 60 < time.time():  # pragma: no cover
                return None
            # Else its valid, return the cached value
            return cached["value"]

        # Set the cached value
        bgpq3_cache[self.server]["objects"][obj] = {
            "_timestamp": time.time(),
            "value": value,
        }

        return value

    @property
    def server(self) -> str:
        """Return the server we're using."""
        return f"{self.host}:{self.port}"

    @property
    def host(self) -> str:
        """Return the host we're using."""
        return self._host

    @property
    def port(self) -> int:
        """Return the port we're using."""
        return self._port
