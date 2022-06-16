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
# pylint: disable=import-error,too-few-public-methods

"""BGP filtering test case."""

from ..template_replace_aspath_notallowed_aspath import Template
from ....config.peertype_customer.e1r1_highasn_no_filter import PeerTypeConfig


class Test(PeerTypeConfig, Template):
    """BGP filtering test case."""

    # We need to add an additional ASN to the filter list
    r1_peer_extra_config = """
      filter:
        origin_asns: [4200000000, 4200000002]
"""
