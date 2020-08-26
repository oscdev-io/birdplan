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

# pylint: disable=import-error,too-few-public-methods

from typing import Any, List, Optional
import pytest
from nsnetsim.generic_node import GenericNode
from simulation import Simulation
from birdplan import BirdPlan


#
# Test case base classes
#


@pytest.mark.incremental
class BirdPlanBaseTestCase:
    """Base test case for our tests."""

    test_dir: Optional[str] = None
    routers: List[str] = []
    sim: Simulation

    def _test_configure(self, sim, tmpdir):
        """Create our configuration files."""
        # Lets start configuring...
        birdplan = BirdPlan()
        # Generate config files
        for router in self.routers:
            bird_conffile = f"{tmpdir}/bird.conf.{router}"
            bird_logfile = f"{tmpdir}/bird.log.{router}"
            # Load yaml config
            birdplan.load(f"{self.test_dir}/{router}.yaml", {"@LOGFILE@": bird_logfile})
            # Generate BIRD config
            birdplan.generate(bird_conffile)
            sim.add_conffile(f"CONFFILE({router})", bird_conffile)
            sim.add_logfile(f"LOGFILE({router})", bird_logfile)

    def _bird_route_table(self, sim: Simulation, node: GenericNode, route_table_name: str, **kwargs) -> Any:
        """Routing table retrieval helper."""
        # Grab the route table
        route_table = sim.node(node).birdc_show_route_table(route_table_name, **kwargs)
        # Add report
        sim.add_report_obj(f"BIRD({node})[{route_table_name}]", route_table)
        # Return route table
        return route_table
