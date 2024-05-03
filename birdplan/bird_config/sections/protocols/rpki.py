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

"""BIRD RPKI protocol configuration."""

import urllib.parse
from typing import List, Optional, Union

from ...globals import BirdConfigGlobals
from ..base import SectionBase
from ..bird_attributes import SectionBirdAttributes
from ..tables import SectionTables

__all__ = ["ProtocolRPKI"]


BIRDPLAN_RPKI_PRIVATE_KEY = "/etc/birdplan/rpki_id_rsa"
BIRDPLAN_RPKI_PUBLIC_KEY = "/etc/birdplan/rpki_known_hosts"
BIRDPLAN_RPKI_USERNAME = "rpki"


class RPKISource:
    """RPKI server configuration."""

    # List-based sources
    _rpki_data: Optional[List[str]]
    # String-based sources, aka a URI
    _protocol: Optional[str]
    _hostname: Optional[str]
    _port: Optional[int]

    _private_key: Optional[str]
    _public_key: Optional[str]
    _username: Optional[str]

    _local_address: Optional[str]
    _refresh: Optional[int]
    _retry: Optional[int]

    def __init__(self, rpki_source: Union[str, List[str]]) -> None:  # pylint: disable=too-many-branches
        """Initialize object."""

        self._rpki_data = None
        self._protocol = None
        self._hostname = None

        self._port = None
        self._private_key = None
        self._public_key = None
        self._username = None

        self._local_address = None
        self._refresh = None
        self._retry = None

        # Check if we have a list of RPKI data
        if isinstance(rpki_source, list):
            self._rpki_data = rpki_source

        else:
            # Parse RPKI server URI to get protocol, hostname, port and parameters
            parsed_uri = urllib.parse.urlparse(rpki_source)

            # Grab the protocol
            self._protocol = parsed_uri.scheme
            if self._protocol not in ["ssh", "tcp"]:
                raise ValueError(f"Invalid protocol '{self._protocol}' for RPKI server '{rpki_source}'")

            # Check if we have a hostname we can use
            hostname = parsed_uri.hostname
            if not hostname:
                raise ValueError(f"Invalid hostname '{hostname}' for RPKI server '{rpki_source}'")
            self._hostname = hostname

            # Work out which port we're using
            if parsed_uri.port:
                self._port = parsed_uri.port
            else:
                if self._protocol == "ssh":
                    self._port = 22
                elif self._protocol == "tcp":
                    self._port = 323

            # Grab parameters
            parameters = urllib.parse.parse_qs(parsed_uri.query)

            # If we're dealing with SSH, check for private and public keys in the query parameters
            if self._protocol == "ssh":
                # Private key
                if "private_key" in parameters:
                    self._private_key = parameters["private_key"][-1]
                else:
                    self._private_key = BIRDPLAN_RPKI_PRIVATE_KEY
                # Public key
                if "public_key" in parameters:
                    self._public_key = parameters["public_key"][-1]
                # Username
                if "username" in parameters:
                    self._username = parameters["username"][-1]
                else:
                    self._username = BIRDPLAN_RPKI_USERNAME

            # Check for additional options
            if "local_address" in parameters:
                self._local_address = parameters["local_address"][-1]
            if "refresh" in parameters:
                self._refresh = int(parameters["refresh"][-1])
            if "retry" in parameters:
                self._retry = int(parameters["retry"][-1])

    @property
    def protocol(self) -> Optional[str]:
        """Return the protocol."""
        return self._protocol

    @property
    def hostname(self) -> Optional[str]:
        """Return the hostname."""
        return self._hostname

    @property
    def port(self) -> Optional[int]:
        """Return the port."""
        return self._port

    @property
    def private_key(self) -> Optional[str]:
        """Return the private key."""
        return self._private_key

    @property
    def public_key(self) -> Optional[str]:
        """Return the public key."""
        return self._public_key

    @property
    def username(self) -> Optional[str]:
        """Return the username."""
        return self._username

    @property
    def rpki_data(self) -> Optional[List[str]]:
        """Return the RPKI data."""
        return self._rpki_data

    @property
    def local_address(self) -> Optional[str]:
        """Return the local address."""
        return self._local_address

    @property
    def refresh(self) -> Optional[int]:
        """Return the refresh interval."""
        return self._refresh

    @property
    def retry(self) -> Optional[int]:
        """Return the retry interval."""
        return self._retry

    @property
    def is_uri(self) -> bool:
        """Return True if the source is a URI."""
        return self._protocol is not None


class ProtocolRPKI(SectionBase):
    """BIRD RPKI protocol configuration."""

    _server: RPKISource
    _birdattributes: SectionBirdAttributes
    _tables: SectionTables

    def __init__(
        self,
        birdconfig_globals: BirdConfigGlobals,
        birdattributes: SectionBirdAttributes,
        tables: SectionTables,
        rpki_source: RPKISource,
    ) -> None:
        """Initialize the object."""
        super().__init__(birdconfig_globals)
        self._server = rpki_source
        self._birdattributes = birdattributes
        self._tables = tables

    def configure(self) -> None:
        """Configure the RPKI protocol."""
        super().configure()

        # Set section header
        self._section = "RPKI Protocol"

        # Configure the RPKI protocol
        self._configure_tables_rpki()

        if self.server.is_uri:
            self._configure_protocol_rpki_uri()
        else:
            self._configure_protocol_rpki_static()

    def _configure_tables_rpki(self) -> None:
        """Tables configuration."""
        self.tables.conf.append("# RPKI ROA Tables")
        self.tables.conf.append("roa4 table t_roa4;")
        self.tables.conf.append("roa6 table t_roa6;")
        self.tables.conf.append("")

    def _configure_protocol_rpki_static(self) -> None:
        """Static protocol configuration."""
        # Build the IPv4 static table
        self.conf.add("protocol static rpki4 {")
        self.conf.add("")
        self.conf.add("  roa4 { table t_roa4; };")
        self.conf.add("")
        if self.server.rpki_data:
            for route in self.server.rpki_data:
                if "." not in route:
                    continue
                self.conf.add(f"  route {route};")
        self.conf.add("};")
        # Build the IPv6 static table
        self.conf.add("protocol static rpki6 {")
        self.conf.add("")
        self.conf.add("  roa6 { table t_roa6; };")
        self.conf.add("")
        if self.server.rpki_data:
            for route in self.server.rpki_data:
                if ":" not in route:
                    continue
                self.conf.add(f"  route {route};")
        self.conf.add("};")

    def _configure_protocol_rpki_uri(self) -> None:
        """Protocol configuration."""
        self.conf.add("protocol rpki rpki {")
        self.conf.add("")
        self.conf.add("  roa4 { table t_roa4; };")
        self.conf.add("  roa6 { table t_roa6; };")

        # SSH support
        if self.server.protocol == "ssh":
            self.conf.add(f"  remote {self.server.hostname} port {self.server.port};")
            self.conf.add("  transport ssh {")
            self.conf.add(f'    bird private key "{self.server.private_key}";')
            if self.server.public_key:
                self.conf.add(f'    remote public key "{self.server.public_key}";')
            self.conf.add(f'    user "{self.server.username}";')
            self.conf.add("  };")

        # TCP support
        elif self.server.protocol == "tcp":
            self.conf.add(f"  remote {self.server.hostname} port {self.server.port};")

        # Check if we have additional options
        if self.server.local_address:
            self.conf.add(f"  local address {self.server.local_address};")
        if self.server.refresh:
            self.conf.add(f"  refresh {self.server.refresh};")
        if self.server.retry:
            self.conf.add(f"  retry {self.server.retry};")

        self.conf.add("")
        self.conf.add("};")
        self.conf.add("")

    @property
    def server(self) -> RPKISource:
        """Return the RPKI server string."""
        return self._server

    @property
    def birdattributes(self) -> SectionBirdAttributes:
        """Return the attributes section."""
        return self._birdattributes

    @property
    def tables(self) -> SectionTables:
        """Return the tables section."""
        return self._tables
