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

"""BIRD BGP protocol attributes."""

from typing import Dict, Optional


class BGPRoutePolicyAccept:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for acceptance of routes from the main BGP table into the master table.

    Attributes
    ----------
    default : bool
        Accept default route. Defaults to `False`.

    """

    default: bool

    def __init__(self):
        """Initialize object."""
        self.default = False


class BGPRoutePolicyImport:  # pylint: disable=too-few-public-methods
    """
    BGP route policy for importing of routes internally.

    Attributes
    ----------
    connected : Dict[str, bool]
        Import connected routes into the main BGP table. This attribute is indexed by interface name with a boolean option.
        The interface name can be an exact interface match, or a wildcard with a *.
    kernel : bool
        Import kernel routes into the main BGP table. Defaults to `False`.
    static : bool
        Import static routes into the main BGP table. Defaults to `False`.

    """

    connected: Dict[str, bool]
    kernel: bool
    static: bool

    def __init__(self):
        """Initialize object."""
        self.connected = {}
        self.kernel = False
        self.static = False


class BGPAttributes:  # pylint: disable=too-few-public-methods
    """
    BGP attributes.

    Attributes
    ----------
    asn : int
        BGP ASN.
    rr_cluster_id : Optional[str]
        Route relfector cluster ID in the case of us being a route reflector.
    route_policy_accept : BGPRoutePolicyAccept
        Route policy for acceptance of routes from the main BGP table into the master table.
    route_policy_import : BGPRoutePolicyImport
        Route policy for importing of routes from internal tables into our main BGP table.

    """

    asn: Optional[int]
    rr_cluster_id: Optional[str]
    route_policy_accept: BGPRoutePolicyAccept
    route_policy_import: BGPRoutePolicyImport

    prefix_import_maxlen4: int = 24
    prefix_import_minlen4: int = 8

    prefix_export_maxlen4: int = 24
    prefix_export_minlen4: int = 8

    prefix_import_maxlen6: int = 48
    prefix_import_minlen6: int = 16

    prefix_export_maxlen6: int = 48
    prefix_export_minlen6: int = 16

    aspath_maxlen: int = 100
    aspath_minlen: int = 1

    def __init__(self):
        """Initialize object."""

        self.asn = None

        self.rr_cluster_id = None

        self.route_policy_accept = BGPRoutePolicyAccept()
        self.route_policy_import = BGPRoutePolicyImport()
