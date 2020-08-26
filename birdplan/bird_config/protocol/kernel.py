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

"""BIRD kernel protocol configuration."""

from ..base import BirdConfigBase


class BirdConfigProtocolKernel(BirdConfigBase):
    """BIRD kernel protocol configuration."""

    def configure(self):
        """Configure the kernel protocol."""
        self._addtitle("Kernel Protocol")

        # Setup kernel tables
        self._addline("ipv4 table t_kernel4;")
        self._addline("ipv6 table t_kernel6;")

        # Configure the kernel protocol
        self._configure_protocol_kernel(4)
        self._configure_protocol_kernel(6)

        self._addline("")

    def _configure_protocol_kernel(self, ipv):
        """Protocol configuration."""
        self._addline("")
        self._addline("protocol kernel kernel%s {" % ipv)
        self._addline('\tdescription "Kernel protocol for IPv%s";' % ipv)
        self._addline("")
        self._addline("\tmetric 600; # Set the BIRD metric to be used when creating kernel routes to fall in line with our OS")
        self._addline("\tlearn; # Learn routes from the kernel")
        self._addline("\tpersist; # Dont remove routes on BIRD shutdown")
        self._addline("\tmerge paths on; # Merge similar BGP paths into a multi-hop")
        self._addline("")
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_kernel%s;" % ipv)
        self._addline("")
        self._addline("\t\texport all;")
        self._addline("\t\timport all;")
        self._addline("\t};")
        self._addline("};")
