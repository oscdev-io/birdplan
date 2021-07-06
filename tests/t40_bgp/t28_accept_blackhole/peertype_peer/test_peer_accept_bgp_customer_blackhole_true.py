#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2020, AllWorldIT
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
# pylint: disable=import-error,too-few-public-methods,no-self-use

"""BGP accept blackhole route test cases, with peer accept:bgp_customer_blackhole set to True."""

from ..template_peer_accept_bgp_customer_blackhole_true import Template
from ...config.peertype_peer.e1r1 import PeerTypeConfig


class Test(PeerTypeConfig, Template):
    """BGP accept blackhole route test cases, with peer accept:bgp_customer_blackhole set to True."""

    routers_config_exception = {
        "r1": r"Having 'accept:bgp_customer_blackhole' set to True for peer 'e1' with type 'peer' makes no sense",
    }