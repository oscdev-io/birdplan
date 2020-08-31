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

from .base import SectionProtocolBase


class ProtocolKernel(SectionProtocolBase):
    """BIRD kernel protocol configuration."""

    _section = "Kernel Protocol"

    def configure(self):
        """Configure the kernel protocol."""
        super().configure()

        # Configure the kernel protocol
        self._configure_protocol_kernel(4)
        self._configure_protocol_kernel(6)

    def _configure_protocol_kernel(self, ipv: int):
        """Protocol configuration."""
        self.conf.add(f"protocol kernel kernel{ipv} {{")
        self.conf.add(f'  description "Kernel protocol for IPv{ipv}";')
        self.conf.add("")
        self.conf.add("  metric 600; # Set the BIRD metric to be used when creating kernel routes to fall in line with our OS")
        self.conf.add("  learn; # Learn routes from the kernel")
        self.conf.add("  persist; # Dont remove routes on BIRD shutdown")
        self.conf.add("  merge paths on; # Merge similar BGP paths into a multi-hop")
        self.conf.add("")
        self.conf.add(f"  ipv{ipv} {{")
        self.conf.add(f"    table t_kernel{ipv};")
        self.conf.add("")
        self.conf.add("    export all;")
        self.conf.add("    import all;")
        self.conf.add("  };")
        self.conf.add("};")
        self.conf.add("")
