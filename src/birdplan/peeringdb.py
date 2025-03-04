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

"""PeeringDB support class."""

import time
from typing import Any

import requests

from .exceptions import BirdPlanError

__all__ = ["PeeringDB"]


PeeringDBInfo = dict[str, Any]


# Keep a cache for results returned while loaded into memory
#
# Example:
#  > peeringdb_cache = {
#  >  'objects': {
#  >      'asn:174': {  # ASN
#  >          '_timestamp': 0000000000,
#  >          'value': xxxxxx,
#  >      }
#  >  }
#  > }
peeringdb_cache: dict[str, dict[str, Any]] = {}

# Keep track of the timestamp of our last request
peeringdb_last_request: float = 0


PEERINGDB_16BIT_LOWER = 64512
PEERINGDB_16BIT_UPPER = 65534
PEERINGDB_32BIT_LOWER = 4200000000
PEERINGDB_32BIT_UPPER = 4294967294


class PeeringDB:  # pylint: disable=too-few-public-methods
    """PeeringDB support class."""

    def __init__(self) -> None:
        """Initialize object."""

    def get_prefix_limits(self, asn: int) -> PeeringDBInfo:
        """Return our peeringdb info entry, if there is one."""
        global peeringdb_last_request  # noqa: PLW0603

        # We cannot do lookups on private ASN's
        if (PEERINGDB_16BIT_LOWER <= asn <= PEERINGDB_16BIT_UPPER) or (PEERINGDB_32BIT_LOWER <= asn <= PEERINGDB_32BIT_UPPER):
            return {"info_prefixes4": None, "info_prefixes6": None}

        # Try pull result from our cache
        result = self._cache(f"asn:{asn}")
        # If we can't, grab the result from PeeringDB live
        if not result:
            # Sleep if last request was made within the past 5s
            time_delta = time.time() - peeringdb_last_request + 5
            if time_delta < 0:
                time.sleep(abs(time_delta))
            # Update the last request
            peeringdb_last_request = time.time()
            # Request the PeeringDB info for this AS
            try:
                response = requests.get(f"https://www.peeringdb.com/api/net?asn__in={asn}", timeout=10)
            except requests.exceptions.Timeout as e:  # pragma: no cover
                raise BirdPlanError(f"PeeringDB request timed out: {e}") from None
            # Update the last request
            peeringdb_last_request = time.time()
            # Check the result is not empty
            if not response:  # pragma: no cover
                raise BirdPlanError("PeeringDB returned and empty result")
            # Decode response
            result = response.json()["data"][0]
            # Cache the result we got
            self._cache(f"asn:{asn}", result)

        # Total cluster .... just to get typing happy
        peeringdb_info = {"info_prefixes4": 1, "info_prefixes6": 1}
        if result and "info_prefixes4" in result:
            peeringdb_info["info_prefixes4"] = result["info_prefixes4"]
        if result and "info_prefixes6" in result:
            peeringdb_info["info_prefixes6"] = result["info_prefixes6"]

        # Lastly return it
        return peeringdb_info

    def _cache(self, obj: str, value: PeeringDBInfo | None = None) -> dict[str, Any] | None:
        """Retrieve or store value in cache."""

        if "objects" not in peeringdb_cache:
            peeringdb_cache["objects"] = {}

        if not value:
            # If the cached obj does not exist, return None
            if obj not in peeringdb_cache["objects"]:
                return None
            # Grab the cached object
            cached = peeringdb_cache["objects"][obj]
            # Make sure its timestamp is within 60s of being retrieved, if not, return None
            if cached["_timestamp"] + 60 < time.time():  # pragma: no cover
                return None
            # Else its valid, return the cached value
            return cached["value"]

        # Set the cached value
        peeringdb_cache["objects"][obj] = {
            "_timestamp": time.time(),
            "value": value,
        }

        return value
