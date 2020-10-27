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

"""BGP large community functions (outbound) test case."""

from ..template_large_community_prepend_location_1x_to_customer import Template


class Test(Template):
    """BGP large community functions (outbound) test case."""

    e1_extra_communities = "65000:3:1"

    r1_peer_asn = 65000
    r1_peer_type = "rrclient"
    r1_global_config = """
  rr_cluster_id: 0.0.0.1
"""

    e1_asn = 65000
