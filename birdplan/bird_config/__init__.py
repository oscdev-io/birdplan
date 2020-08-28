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

"""Bird configuration package."""

from typing import Optional
from .base import BirdConfigBase
from .constants import BirdConfigConstants
from .logging import BirdConfigLogging
from .main import BirdConfigMain
from .master import BirdConfigMaster
from .protocol.device import BirdConfigProtocolDevice
from .protocol.kernel import BirdConfigProtocolKernel
from .protocol.static import BirdConfigProtocolStatic
from .protocol.rip import BirdConfigProtocolRIP
from .protocol.ospf import BirdConfigProtocolOSPF
from .protocol.bgp import BirdConfigProtocolBGP
from .router_id import BirdConfigRouterID


class BirdConfig(BirdConfigBase):  # pylint: disable=too-many-instance-attributes
    """BirdConfig is responsible for configuring Bird."""

    _router_id: str
    _log_file: Optional[str]
    _debug: bool

    _constants: BirdConfigConstants
    _master: BirdConfigMaster
    _static: BirdConfigProtocolStatic
    _rip: BirdConfigProtocolRIP
    _ospf: BirdConfigProtocolOSPF
    _bgp: BirdConfigProtocolBGP

    def __init__(self):
        """Initialize the object."""
        super().__init__(root=self)

        # Router ID
        self._router_id = "0.0.0.0"

        # Log file
        self._log_file = None

        # Debugging
        self._debug = False
        self._test_mode = False

        # Constants
        self._constants = BirdConfigConstants(parent=self)
        # Master tables
        self._master = BirdConfigMaster(parent=self)
        # Static protocol
        self._static = BirdConfigProtocolStatic(parent=self)
        # RIP protocol
        self._rip = BirdConfigProtocolRIP(parent=self)
        # OSPF protocol
        self._ospf = BirdConfigProtocolOSPF(parent=self)
        # BGP protocol
        self._bgp = BirdConfigProtocolBGP(parent=self)

    def static_add_route(self, route):
        """Add static route."""
        self.static.add_route(route)

    def get_config(self):
        """Return the Bird configuration."""

        main = BirdConfigMain(parent=self)
        main.configure()

        logging = BirdConfigLogging(parent=self)
        logging.configure()

        router_id = BirdConfigRouterID(parent=self)
        router_id.configure()

        self.constants.configure()

        protocol_device = BirdConfigProtocolDevice(parent=self)
        protocol_device.configure()

        protocol_kernel = BirdConfigProtocolKernel(parent=self)
        protocol_kernel.configure()

        self.master.configure()

        self.static.configure()

        if self.rip.interfaces:
            self.rip.configure()

        if self.ospf.areas:
            self.ospf.configure()

        if self.bgp.peers_config:
            self.bgp.configure()

        return self.config_lines

    @property
    def router_id(self) -> str:
        """Return our router_id."""
        return self._router_id

    @router_id.setter
    def router_id(self, router_id: str):
        """Set router_id."""
        self._router_id = router_id

    @property
    def log_file(self) -> Optional[str]:
        """Return the log file to use."""
        return self._log_file

    @log_file.setter
    def log_file(self, log_file: str):
        """Set the log file to use."""
        self._log_file = log_file

    @property
    def debug(self) -> bool:
        """Return debugging mode."""
        return self._debug

    @debug.setter
    def debug(self, debug: bool):
        """Set debugging mode."""
        self._debug = debug

    @property
    def test_mode(self) -> bool:
        """Return if we're running in test mode."""
        return self._test_mode

    @test_mode.setter
    def test_mode(self, test_mode: bool):
        """Set test mode."""
        self._test_mode = test_mode

    @property
    def constants(self) -> BirdConfigConstants:
        """Return our constants."""
        return self._constants

    @property
    def master(self) -> BirdConfigMaster:
        """Return our master config."""
        return self._master

    @property
    def static(self) -> BirdConfigProtocolStatic:
        """Return our static protocol config."""
        return self._static

    @property
    def rip(self) -> BirdConfigProtocolRIP:
        """Return our RIP protocol config."""
        return self._rip

    @property
    def ospf(self) -> BirdConfigProtocolOSPF:
        """Return our OSPF protocol config."""
        return self._ospf

    @property
    def bgp(self) -> BirdConfigProtocolBGP:
        """Return our BGP protocol config."""
        return self._bgp
