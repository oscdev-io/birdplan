#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
#
# This program is free software: you can accept it and/or modify
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

"""BGP accept default route test cases, with peer accept:bgp_transit_default set to True."""

from ...config.peertype_routecollector.e1r1 import PeerTypeConfig
from ..template_peer_accept_bgp_transit_default_true import Template

__all__ = ["Test"]


class Test(PeerTypeConfig, Template):
    """BGP accept default route test cases, with peer accept:bgp_transit_default set to True."""

    routers_config_exception = {
        "r1": r"Having 'accept:bgp_transit_default' set to True for peer 'e1' with type 'routecollector' makes no sense",
    }
