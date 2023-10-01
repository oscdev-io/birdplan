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

"""Basic test case for BGPQ3."""

from birdplan.bgpq3 import BGPQ3


class Test:
    """Basic test case for BGPQ3."""

    def test_bgpq3_asns_str(self):
        """Basic test for BGPQ3 ASN retrieval using a string."""

        bgpq3 = BGPQ3()
        asn_list = bgpq3.get_asns("AS174:AS-COGENT")

        assert len(asn_list) > 1, "Failed to get ASN list from BGPQ3 using a string"

    def test_bgpq3_asns_list(self):
        """Basic test for BGPQ3 ASN retrieval using a string."""

        bgpq3 = BGPQ3()
        asn_list = bgpq3.get_asns(["AS174:AS-COGENT"])

        assert len(asn_list) > 1, "Failed to get ASN list from BGPQ3 using a list"

    def test_bgpq3_prefixes_str(self):
        """Basic test for BGPQ3 prefix retrieval using a string."""

        bgpq3 = BGPQ3()
        prefix_list = bgpq3.get_prefixes("AS174:AS-COGENT")

        assert "ipv4" in prefix_list, "No IPv4 prefixes returned"
        assert "ipv6" in prefix_list, "No IPv4 prefixes returned"

        assert len(prefix_list["ipv4"]) > 1, "Failed to get prefix list from BGPQ3 using a string"
        assert len(prefix_list["ipv6"]) > 1, "Failed to get prefix list from BGPQ3 using a string"

    def test_bgpq3_prefixes_list(self):
        """Basic test for BGPQ3 prefix retrieval using a list."""

        bgpq3 = BGPQ3()
        prefix_list = bgpq3.get_prefixes(["AS174:AS-COGENT"])

        assert "ipv4" in prefix_list, "No IPv4 prefixes returned"
        assert "ipv6" in prefix_list, "No IPv4 prefixes returned"

        assert len(prefix_list["ipv4"]) > 1, "Failed to get prefix list from BGPQ3 using a string"
        assert len(prefix_list["ipv6"]) > 1, "Failed to get prefix list from BGPQ3 using a string"
