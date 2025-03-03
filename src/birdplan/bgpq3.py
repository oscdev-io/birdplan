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

"""BGPQ3/4 support class."""

import functools
import ipaddress
import json
import shutil
import subprocess  # nosec
import time
from typing import Any

from .exceptions import BirdPlanError

__all__ = ["BGPQ3"]


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
bgpq3_cache: dict[str, dict[str, Any]] = {}


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

    @functools.lru_cache(maxsize=1)  # noqa: B019
    def _exe(self) -> str:
        """Return the bgpq3 executable."""

        for exe in ("bgpq3", "bgpq4"):
            if shutil.which(exe):
                return exe

        raise BirdPlanError("bgpq3/bgpq4 executable not found in PATH")

    def get_asns(self, as_sets: str | list[str]) -> list[str]:  # pylint: disable=too-many-branches
        """Get prefixes."""

        # Build an object list depending on the type of "objects" above
        objects: list[str] = []
        if isinstance(as_sets, str):
            objects.append(as_sets)
        else:
            objects.extend(as_sets)

        # Grab ASNs
        is_birdplan_internal = False
        asns_bgpq3: dict[str, list[str]] = {}
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
                except BirdPlanError as err:
                    raise BirdPlanError(f"Failed to query IRR ASNs from object '{obj}':\n{err}") from None
                # Cache the result we got
                self._cache(f"asns:{obj}", result)
            # Check if this is a birdplan internal object
            if obj.startswith("_BIRDPLAN:"):
                is_birdplan_internal = True
            # Update return value with result
            asns_bgpq3.update(result)

        # If we don't have "asns" returned in the JSON structure, raise an exception
        if "asns" not in asns_bgpq3:  # pragma: no cover
            raise BirdPlanError(f"BGPQ3 output error, expecting 'asns': {asns_bgpq3}")

        filtered_asns = []
        for asn in asns_bgpq3["asns"]:
            # Convert to int for below
            asn_i = int(asn)
            # 0	Reserved by [RFC7607]	[RFC7607]
            # 112	Used by the AS112 project to sink misdirected DNS queries; see [RFC7534]	[RFC7534]
            # 23456	AS_TRANS; reserved by [RFC6793]	[RFC6793]
            # 65535	Reserved by [RFC7300]	[RFC7300]
            # 4294967295	Reserved by [RFC7300]	[RFC7300]
            if asn_i in [0, 112, 23456, 65535, 4294967295]:
                continue

            #
            # NK: So objects that start with _BIRDPLAN are used for the tests, so we need to treat them a little differently below
            #     if that's the case.
            #

            # 64496-64511	For documentation and sample code; reserved by [RFC5398]	[RFC5398]
            if (64496 <= asn_i <= 64511) and not is_birdplan_internal:
                continue
            # 64512-65534	For private use; reserved by [RFC6996]	[RFC6996]
            if (64512 <= asn_i <= 65534) and not is_birdplan_internal:
                continue
            # 65536-65551	For documentation and sample code; reserved by [RFC5398]	[RFC5398]
            if (65536 <= asn_i <= 65551) and not is_birdplan_internal:
                continue

            # 4200000000-4294967294	For private use; reserved by [RFC6996]	[RFC6996]
            if 4200000000 <= asn_i <= 4294967294:
                continue
            # We passed all the checks, lets add to the filtered list
            filtered_asns.append(asn)

        return filtered_asns

    def get_prefixes(self, as_sets: str | list[str]) -> dict[str, list[str]]:
        """Get prefixes."""

        # Build an object list depending on the type of "objects" above
        objects: list[str] = []
        if isinstance(as_sets, str):
            objects.append(as_sets)
        else:
            objects.extend(as_sets)

        # Grab IPv4 and IPv6 prefixes
        prefixes_bgpq3: dict[str, list[dict[str, Any]]] = {}
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
        prefixes: dict[str, list[str]] = {"ipv4": [], "ipv6": []}

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
                    # Add prefix, format is %s{%s,%s}
                    prefixes[family].append(f"{prefix['prefix']}{{{greater_equal},{prefix['less-equal']}}}")

        return prefixes

    def _bgpq3(self, args: list[str]) -> Any:
        """Run bgpq3."""

        # Run the IP tool with JSON output
        cmd_args = [self._exe(), "-h", self.server, "-j"]
        # Add our args
        cmd_args.extend(args)

        # Grab result from process execution
        result = subprocess.check_output(cmd_args, stderr=subprocess.STDOUT)  # nosec
        try:
            decoded = json.loads(result)
        except json.JSONDecodeError as err:
            raise BirdPlanError(f"Failed to decode JSON output from {self._exe()}: {err}") from None
        # Return the decoded json output
        return decoded

    def _cache(self, obj: str, value: Any | None = None) -> Any | None:
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
