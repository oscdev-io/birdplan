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

"""BIRD protocols section."""

from .device import ProtocolDevice
from .direct import ProtocolDirect
from .kernel import ProtocolKernel
from .pipe import ProtocolPipe
from .static import ProtocolStatic
from .rip import ProtocolRIP
from .ospf import ProtocolOSPF
from .bgp import ProtocolBGP
from ..base import SectionBase
from ..constants import SectionConstants
from ..functions import SectionFunctions
from ..tables import SectionTables
from ...globals import BirdConfigGlobals


class SectionProtocols(SectionBase):
    """BIRD protocols section."""

    _device: ProtocolDevice
    _direct: ProtocolDirect
    _kernel: ProtocolKernel
    _static: ProtocolStatic
    _rip: ProtocolRIP
    _ospf: ProtocolOSPF
    _bgp: ProtocolBGP

    def __init__(
        self, birdconfig_globals: BirdConfigGlobals, constants: SectionConstants, functions: SectionFunctions, tables: SectionTables
    ):
        """Initialize object."""
        super().__init__(birdconfig_globals)

        self._device = ProtocolDevice(birdconfig_globals, constants, functions, tables)
        self._direct = ProtocolDirect(birdconfig_globals, constants, functions, tables)
        self._kernel = ProtocolKernel(birdconfig_globals, constants, functions, tables)
        self._static = ProtocolStatic(birdconfig_globals, constants, functions, tables)
        self._rip = ProtocolRIP(birdconfig_globals, constants, functions, tables)
        self._ospf = ProtocolOSPF(birdconfig_globals, constants, functions, tables)
        self._bgp = ProtocolBGP(birdconfig_globals, constants, functions, tables)

    def configure(self) -> None:
        """Configure all protocols."""
        super().configure()

        # Add device protocol
        self.conf.add(self.device)

        # Add direct protocol
        self.conf.add(self.direct)
        # Add pipe between direct and master tables
        bgp_direct_pipe = ProtocolPipe(
            self.birdconfig_globals,
            table_from="master",
            table_to="direct",
            table_import="all",
        )
        self.conf.add(bgp_direct_pipe)

        # Add kernel protocol
        self.conf.add(self.kernel)

        # If we have static routes, pull in the static configuration
        if self.static.routes:
            self.conf.add(self.static)

        # If we have RIP interfaces, pull in the RIP configuration
        if self.rip.interfaces:
            self.conf.add(self.rip)

        # If we have OSPF interfaces, pull the OSPF configuration
        if self.ospf.interfaces:
            self.conf.add(self.ospf)

        # If we have BGP peers, pull in the BGP configuration
        if self.bgp.peers_config:
            self.conf.add(self.bgp)

    @property
    def device(self) -> ProtocolDevice:
        """Return the device protocol."""
        return self._device

    @property
    def direct(self) -> ProtocolDirect:
        """Return the direct protocol."""
        return self._direct

    @property
    def kernel(self) -> ProtocolKernel:
        """Return the kernel protocol."""
        return self._kernel

    @property
    def static(self) -> ProtocolStatic:
        """Return the static protocol."""
        return self._static

    @property
    def rip(self) -> ProtocolRIP:
        """Return the RIP protocol."""
        return self._rip

    @property
    def ospf(self) -> ProtocolOSPF:
        """Return the OSPF protocol."""
        return self._ospf

    @property
    def bgp(self) -> ProtocolBGP:
        """Return the BGP protocol."""
        return self._bgp
