#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""BGP prepending test case."""

from ....config.peertype_peer.r1r2 import PeerTypeConfig
from ..template_prepend_blackhole import Template

__all__ = ["Test"]


class Test(PeerTypeConfig, Template):
    """BGP prepending test case."""

    routers_config_exception = {"r1": r"Having 'prepend:blackhole' specified for peer 'r2' with type 'peer' makes no sense"}
