#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
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

# type: ignore
# pylint: disable=import-error,too-few-public-methods

"""BGP outgoing large communities test case."""

from ....config.peertype_routeserver.peer.r1r2 import PeerTypeConfig
from ..template_outgoing_large_communities_bgp_peering import Template

__all__ = ["Test"]


class Test(PeerTypeConfig, Template):
    """BGP outgoing large communities test case."""

    routers_config_exception = {
        "r1": r"Having 'outgoing_large_communities:bgp_peering' specified for peer 'r2' with type 'routeserver' makes no sense"
    }
