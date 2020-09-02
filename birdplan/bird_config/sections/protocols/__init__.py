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
from .kernel import ProtocolKernel
from .static import ProtocolStatic
from .rip import ProtocolRIP
from .ospf import ProtocolOSPF
from .bgp import ProtocolBGP
from ..base import SectionBase


class SectionProtocols(SectionBase):
    """BIRD protocols section."""

    _device: ProtocolDevice
    _kernel: ProtocolKernel
    _static: ProtocolStatic
    _rip: ProtocolRIP
    _ospf: ProtocolOSPF
    _bgp: ProtocolBGP

    def __init__(self, **kwargs):
        """Initialize object."""
        super().__init__(**kwargs)

        self._device = ProtocolDevice(**kwargs)
        self._kernel = ProtocolKernel(**kwargs)
        self._static = ProtocolStatic(**kwargs)
        self._rip = ProtocolRIP(**kwargs)
        self._ospf = ProtocolOSPF(**kwargs)
        self._bgp = ProtocolBGP(**kwargs)

    def configure(self):
        """Configure all protocols."""
        super().configure()

        self.conf.add(self.device)
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
