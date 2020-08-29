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

"""Base test classes for our tests."""

# pylint: disable=too-few-public-methods,no-self-use

from typing import Any, Dict, List, Optional
import pytest
from simulation import Simulation
from birdplan import BirdPlan  # pylint: disable=import-error


#
# Test case base classes
#


@pytest.mark.incremental
class BirdPlanBaseTestCase:
    """Base test case for our tests."""

    test_dir: Optional[str] = None
    routers: List[str] = []
    sim: Simulation

    def _test_configure(self, sim: Simulation, tmpdir: str, extra_macros: Optional[Dict[str, str]] = None):
        """Create our configuration files."""
        # Generate config files
        for router in self.routers:
            bird_conffile = f"{tmpdir}/bird.conf.{router}"
            bird_logfile = f"{tmpdir}/bird.log.{router}"

            # Lets start configuring...
            birdplan = BirdPlan()

            # Set test mode
            birdplan.birdconf.test_mode = True

            # Work out the macro's we'll be using
            macros = {"@LOGFILE@": bird_logfile}
            if extra_macros:
                macros.update(extra_macros)

            # Load yaml config
            birdplan.load(f"{self.test_dir}/{router}.yaml", macros)

            # Generate BIRD config
            birdplan.generate(bird_conffile)
            sim.add_conffile(f"CONFFILE({router})", bird_conffile)
            sim.add_logfile(f"LOGFILE({router})", bird_logfile)

            # Add the birdplan configuration object to the simulation
            sim.add_config(router, birdplan)

    def _bird_route_table(self, sim: Simulation, name: str, route_table_name: str, **kwargs) -> Any:
        """Routing table retrieval helper."""
        # Grab the route table
        route_table = sim.node(name).birdc_show_route_table(route_table_name, **kwargs)
        # Add report
        sim.add_report_obj(f"BIRD({name})[{route_table_name}]", route_table)
        # Return route table
        return route_table

    def _bird_bgp_peer_table(self, sim: Simulation, name: str, peer_name: str, ipv: int) -> str:
        """Get a bird BGP peer table name."""
        # Grab BirdConfig object for this router name
        birdconf = sim.config(name).birdconf

        # Work-around for mypy error saying its undefined...
        if not birdconf:
            raise RuntimeError("It should not happen that birdconf.bgp is not set")

        # Grab BGP peer BGP table name
        return birdconf.bgp.peer(peer_name).bgp_table_name(ipv)
