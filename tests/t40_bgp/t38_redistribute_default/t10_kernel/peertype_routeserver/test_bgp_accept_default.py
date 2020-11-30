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

"""BGP test case for redistribution of kernel default routes, with default settings for accept:default."""

from ..template_bgp_accept_default import Template
from ....config.peertype_routeserver.r1r2 import PeerTypeConfig


class Test(PeerTypeConfig, Template):
    """BGP test case for redistribution of kernel default routes, with default settings for accept:default."""

    routers_config_exception = {
        "r1": r"Having 'redistribute:default' set for peer 'r2' with type 'routeserver' makes no sense",
        "r2": r"Having 'accept:default' set to True for peer 'r1' with type 'routeserver' makes no sense",
    }

    def _test_setup_specific(self, sim, tmpdir):
        """Set up our test - specific additions."""
        # We cannot add a route to r1 due to invalid configuration