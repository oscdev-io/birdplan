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

"""BIRD direct protocol configuration."""

from ..base import BirdConfigBase


class BirdConfigProtocolDirect(BirdConfigBase):
    """BIRD direct protocol configuration."""

    def __init__(self, parent, name="", **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Add a suffix if we have a name
        if name:
            self._name_suffix = "_%s" % name
        else:
            self._name_suffix = ""

        # Grab the list of interfaces we need
        self._interfaces = kwargs.get("interfaces", [])

    def configure(self):
        """Configure the direct protocol."""
        # If we're not handling a specific direct protocol, add a title
        if not self.name_suffix:
            self._addtitle("Direct Protocol")

        # If we have a list of interfaces, create the config lines
        interface_lines = []
        if self.interfaces:
            # Create list of quoted interfaces
            interface_list = []
            for interface in self.interfaces:
                interface_list.append('"%s"' % interface)
            # Drop in a comma between them
            interface_str = ", ".join(interface_list)
            interface_lines.append("")
            interface_lines.append("\tinterface %s;" % interface_str)

        self._addline("ipv4 table t_direct4%s;" % self.name_suffix)
        self._addline("ipv6 table t_direct6%s;" % self.name_suffix)
        self._addline("")

        self._setup_protocol(4, interface_lines)
        self._setup_protocol(6, interface_lines)

    def _setup_protocol(self, ipv, lines):
        self._addline("protocol direct direct%s%s {" % (ipv, self.name_suffix))
        self._addline('\tdescription "Direct protocol for IPv%s";' % ipv)
        self._addline("")
        self._addline("\tipv%s {" % ipv)
        self._addline("\t\ttable t_direct%s%s;" % (ipv, self.name_suffix))
        self._addline("")
        self._addline("\t\texport none;")
        self._addline("\t\timport all;")
        self._addline("\t};")
        self._addlines(lines)
        self._addline("};")
        self._addline("")

    @property
    def name_suffix(self):
        """Return our name suffix."""
        return self._name_suffix

    @property
    def interfaces(self):
        """Return our interfaces."""
        return self._interfaces