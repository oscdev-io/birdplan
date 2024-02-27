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

# type: ignore
# pylint: disable=import-error,too-few-public-methods

"""BGP filtering test case."""

from ....config.peertype_transit.e1r1 import PeerTypeConfig
from ..template_global_blackhole_length_import_constraints import Template

__all__ = ["Test"]


class Test(PeerTypeConfig, Template):
    """BGP filtering test case."""

    routers_config_exception = {
        "r1": r"Having 'peertype_constraints:blackhole_import_minlen4' specified for peer type 'transit' makes no sense"
    }
