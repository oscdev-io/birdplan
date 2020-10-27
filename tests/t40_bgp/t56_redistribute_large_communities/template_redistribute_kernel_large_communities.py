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

# type: ignore
# pylint: disable=import-error,too-few-public-methods,no-self-use

"""BGP redistribute large community test case template."""

from .template_base import TemplateBase


class Template(TemplateBase):
    """BGP redistribute large community test case template."""

    r1_template_global_config = """
  import:
    kernel: True
"""

    def r1_template_peer_config(self):
        """Return custom peer config."""

        return f"""
      redistribute:
        kernel:
          large_communities:
            - {self.r1_asn}:5000:1
"""

    def _test_announce_routes(self, sim):
        """Add kernel routes to BIRD instances."""

        # Add gateway'd kernel routes
        sim.node("r1").run_ip(["route", "add", "100.101.0.0/24", "via", "192.168.1.2"])
        sim.node("r1").run_ip(["route", "add", "fc00:101::/48", "via", "fc01::2"])
