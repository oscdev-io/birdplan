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

# type: ignore
# pylint: disable=import-error,too-few-public-methods,no-self-use

"""BGP large community functions test case."""

from ..template_large_community_replace_aspath import Template
from ....config.peertype_transit.r1_to_r10_highasn import PeerTypeConfig


class Test(PeerTypeConfig, Template):
    """BGP large community functions test case."""

    routers_config_exception = {"r1": r"Having 'replace_aspath' set for peer 'e1' with type 'transit' makes no sense"}