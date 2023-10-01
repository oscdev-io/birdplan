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

"""Basic test case for PeeringDB."""

from birdplan.peeringdb import PeeringDB


class Test:
    """Basic test case for PeeringDB."""

    def test_peeringdb_get_prefix_limits(self):
        """Basic test for PeeringDB ASN retrieval using a string."""

        peeringdb = PeeringDB()
        peeringdb_info = peeringdb.get_prefix_limits(174)

        assert peeringdb_info["info_prefixes4"] > 1, "Failed to get info_prefixes4 from PeeringDB using a string"
        assert peeringdb_info["info_prefixes6"] > 1, "Failed to get info_prefixes4 from PeeringDB using a string"

    def test_peeringdb_get_prefix_limits_cached(self):
        """Basic test for PeeringDB ASN retrieval using a string, we should get the cached value."""

        peeringdb = PeeringDB()
        peeringdb_info = peeringdb.get_prefix_limits(174)

        assert peeringdb_info["info_prefixes4"] > 1, "Failed to get info_prefixes4 from PeeringDB using a string"
        assert peeringdb_info["info_prefixes6"] > 1, "Failed to get info_prefixes4 from PeeringDB using a string"

    def test_private_asn_16bit_lower(self):
        """Basic test for PeeringDB ASN in the 16bit range."""

        peeringdb = PeeringDB()
        peeringdb_info = peeringdb.get_prefix_limits(64512)

        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"
        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"

    def test_private_asn_16bit_upper(self):
        """Basic test for PeeringDB ASN in the 16bit range."""

        peeringdb = PeeringDB()
        peeringdb_info = peeringdb.get_prefix_limits(65534)

        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"
        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"

    def test_private_asn_32bit_lower(self):
        """Basic test for PeeringDB ASN in the 32bit range."""

        peeringdb = PeeringDB()
        peeringdb_info = peeringdb.get_prefix_limits(4200000000)

        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"
        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"

    def test_private_asn_32bit_upper(self):
        """Basic test for PeeringDB ASN in the 32bit range."""

        peeringdb = PeeringDB()
        peeringdb_info = peeringdb.get_prefix_limits(4294967294)

        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"
        assert peeringdb_info["info_prefixes4"] is None, "A PeeringDB query on a private ASN should return None"
