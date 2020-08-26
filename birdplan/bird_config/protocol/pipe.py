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

"""BIRD pipe protocol configuration."""

from ..base import BirdConfigBase


class BirdConfigProtocolPipe(BirdConfigBase):  # pylint: disable=too-many-instance-attributes
    """BIRD pipe protocol configuration."""

    def __init__(self, parent, name="", **kwargs):
        """Initialize the object."""
        super().__init__(parent, **kwargs)

        # Add a suffix if we have a name
        if name:
            self._name_suffix = "_%s" % name
        else:
            self._name_suffix = ""

        # Grab table information
        self._table_from = kwargs.get("table_from")
        self._table_to = kwargs.get("table_to")
        self._table_export = kwargs.get("table_export", None)
        self._table_import = kwargs.get("table_import", None)
        self._table_export_filtered = kwargs.get("table_export_filtered", False)
        self._table_import_filtered = kwargs.get("table_import_filtered", False)

        # Are we excluding anything?
        self._has_ipv4 = kwargs.get("has_ipv4", True)
        self._has_ipv6 = kwargs.get("has_ipv6", True)

    def configure(self):
        """Create a pipe protocol."""

        if self.has_ipv4:
            self._addline("protocol pipe p_%s4_to_%s4%s {" % (self.table_from, self.table_to, self.name_suffix))
            self._addline('\tdescription "Pipe from %s4 to %s4%s";' % (self.t_table_from, self.t_table_to, self.name_suffix))
            self._addline("")
            self._addline("\ttable %s4;" % self.t_table_from)
            self._addline("\tpeer table %s4%s;" % (self.t_table_to, self.name_suffix))
            self._addline("")
            # Check if we're doing export filtering
            if self.table_export_filtered:
                self._addline("\texport filter f_%s_%s4_export;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\texport %s;" % self.table_export)
            # Check if we're doing import filtering
            if self.table_import_filtered:
                self._addline("\timport filter f_%s_%s4_import;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\timport %s;" % self.table_import)
            self._addline("};")
            self._addline("")

        if self.has_ipv6:
            self._addline("protocol pipe p_%s6_to_%s6%s {" % (self.table_from, self.table_to, self.name_suffix))
            self._addline('\tdescription "Pipe from %s6 to %s6%s";' % (self.t_table_from, self.t_table_to, self.name_suffix))
            self._addline("")
            self._addline("\ttable %s6;" % self.t_table_from)
            self._addline("\tpeer table %s6%s;" % (self.t_table_to, self.name_suffix))
            self._addline("")
            # Check if we're doing export filtering
            if self.table_export_filtered:
                self._addline("\texport filter f_%s_%s6_export;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\texport %s;" % self.table_export)
            # Check if we're doing import filtering
            if self.table_import_filtered:
                self._addline("\timport filter f_%s_%s6_import;" % (self.table_from, self.table_to))
            # If not add per normal
            else:
                self._addline("\timport %s;" % self.table_import)
            self._addline("};")
            self._addline("")

    @property
    def has_ipv4(self):
        """Return if we have IPv4."""
        return self._has_ipv4

    @property
    def has_ipv6(self):
        """Return if we have IPv6."""
        return self._has_ipv6

    @property
    def name_suffix(self):
        """Return our name suffix."""
        return self._name_suffix

    @property
    def t_table_from(self):
        """Return table_from, some tables don't have t_ prefixes."""
        if self._table_from == "master":
            return self._table_from
        return "t_%s" % self._table_from

    @property
    def t_table_to(self):
        """Return table_to, some tables don't have t_ prefixes."""
        if self._table_to == "master":
            return self._table_to
        return "t_%s" % self._table_to

    @property
    def table_from(self):
        """Return table_from, raw."""
        return self._table_from

    @property
    def table_to(self):
        """Return table_to, raw."""
        return self._table_to

    @property
    def table_export(self):
        """Return that state of us exporting the table."""
        return self._table_export

    @property
    def table_import(self):
        """Return that state of us importing the table."""
        return self._table_import

    @property
    def table_export_filtered(self):
        """Return that state of us exporting the table filtered."""
        return self._table_export_filtered

    @property
    def table_import_filtered(self):
        """Return that state of us importing the table filtered."""
        return self._table_import_filtered
