#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2023, AllWorldIT
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
# pylint: disable=import-error,too-few-public-methods

"""BGP peer AS-SET changes test case template."""

import time
from typing import Any, List

from birdplan import bgpq3

from ....basetests import BirdPlanBaseTestCase
from ....simulation import Simulation


class Template(BirdPlanBaseTestCase):
    """BGP peer AS-SET changes test case template."""

    routers = ["r1"]
    exabgps = ["e1"]

    r1_template_peer_config = """
      filter:
        as_sets: "_BIRDPLAN:AS-SET"
"""

    def _birdplan_run(  # pylint: disable=too-many-arguments,too-many-locals
        self, sim: Simulation, tmpdir: str, router: str, args: List[str]
    ) -> Any:
        """Run BirdPlan for a given router."""

        # Pre-populate cache
        bgpq3.bgpq3_cache = {
            "whois.radb.net:43": {
                "objects": {
                    "asns:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {"asns": [65001, 65003]},
                    },
                    "prefixes:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {
                            "ipv4": [
                                {"prefix": "100.64.0.0/22", "exact": True},
                                {"prefix": "100.64.128.0/19", "exact": False, "greater-equal": 24, "less-equal": 24},
                            ],
                            "ipv6": [
                                {"prefix": "fc00::/46", "exact": True},
                                {"prefix": "fc00:10::/43", "exact": False, "greater-equal": 48, "less-equal": 48},
                            ],
                        },
                    },
                }
            }
        }

        # Grab return result
        res = super()._birdplan_run(sim, tmpdir, router, args)

        return res

    def test_setup(self, sim, testpath, tmpdir):
        """Set up our test."""
        self._test_setup(sim, testpath, tmpdir)

    def test_bird_status(self, sim):
        """Test BIRD status."""
        self._test_bird_status(sim)

    def test_as_sets_reload(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Rewrite configuration file
        super()._birdplan_run(sim, tmpdir, "r1", ["configure"])

    def test_as_sets_ipv4_increase(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Pre-populate cache
        bgpq3.bgpq3_cache = {
            "whois.radb.net:43": {
                "objects": {
                    "asns:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {"asns": [65001, 65003]},
                    },
                    "prefixes:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {
                            "ipv4": [
                                {"prefix": "100.64.0.0/22", "exact": True},
                                {"prefix": "100.64.128.0/17", "exact": False, "greater-equal": 24, "less-equal": 24},
                            ],
                            "ipv6": [
                                {"prefix": "fc00::/46", "exact": True},
                                {"prefix": "fc00:10::/43", "exact": False, "greater-equal": 48, "less-equal": 48},
                            ],
                        },
                    },
                }
            }
        }

        # Check if we get an exception now during reconfiguration
        if getattr(self, "r1_peer_type", None) in ("customer", "peer"):
            super()._birdplan_run(sim, tmpdir, "r1", ["configure", "--ignore-irr-changes"])

    def test_as_sets_ipv6_increase(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Pre-populate cache
        bgpq3.bgpq3_cache = {
            "whois.radb.net:43": {
                "objects": {
                    "asns:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {"asns": [65001, 65003]},
                    },
                    "prefixes:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {
                            "ipv4": [
                                {"prefix": "100.64.0.0/22", "exact": True},
                                {"prefix": "100.64.128.0/19", "exact": False, "greater-equal": 24, "less-equal": 24},
                            ],
                            "ipv6": [
                                {"prefix": "fc00::/46", "exact": True},
                                {"prefix": "fc00:10::/41", "exact": False, "greater-equal": 48, "less-equal": 48},
                            ],
                        },
                    },
                }
            }
        }

        # Check if we get an exception now during reconfiguration
        if getattr(self, "r1_peer_type", None) in ("customer", "peer"):
            super()._birdplan_run(sim, tmpdir, "r1", ["configure", "--ignore-irr-changes"])

    def test_as_sets_ipv4_decrease(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Pre-populate cache
        bgpq3.bgpq3_cache = {
            "whois.radb.net:43": {
                "objects": {
                    "asns:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {"asns": [65001, 65003]},
                    },
                    "prefixes:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {
                            "ipv4": [
                                {"prefix": "100.64.0.0/22", "exact": True},
                                {"prefix": "100.64.128.0/21", "exact": False, "greater-equal": 24, "less-equal": 24},
                            ],
                            "ipv6": [
                                {"prefix": "fc00::/46", "exact": True},
                                {"prefix": "fc00:10::/43", "exact": False, "greater-equal": 48, "less-equal": 48},
                            ],
                        },
                    },
                }
            }
        }

        # Check if we get an exception now during reconfiguration
        if getattr(self, "r1_peer_type", None) in ("customer", "peer"):
            super()._birdplan_run(sim, tmpdir, "r1", ["configure", "--ignore-irr-changes"])

    def test_as_sets_ipv6_decrease(self, sim, tmpdir):
        """Graceful shutdown test to customize template."""

        # Pre-populate cache
        bgpq3.bgpq3_cache = {
            "whois.radb.net:43": {
                "objects": {
                    "asns:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {"asns": [65001, 65003]},
                    },
                    "prefixes:_BIRDPLAN:AS-SET": {
                        "_timestamp": time.time() + 3600,
                        "value": {
                            "ipv4": [
                                {"prefix": "100.64.0.0/22", "exact": True},
                                {"prefix": "100.64.128.0/19", "exact": False, "greater-equal": 24, "less-equal": 24},
                            ],
                            "ipv6": [
                                {"prefix": "fc00::/46", "exact": True},
                                {"prefix": "fc00:10::/45", "exact": False, "greater-equal": 48, "less-equal": 48},
                            ],
                        },
                    },
                }
            }
        }

        # Check if we get an exception now during reconfiguration
        if getattr(self, "r1_peer_type", None) in ("customer", "peer"):
            super()._birdplan_run(sim, tmpdir, "r1", ["configure", "--ignore-irr-changes"])

    def test_bird_cmdline_bgp_peer_summary(self, sim, tmpdir):
        """Test showing BGP peer summary."""
        self._test_bird_cmdline_bgp_peer_summary(sim, tmpdir)

    def test_bird_cmdline_bgp_peer_show(self, sim, tmpdir):
        """Test showing BGP peer."""
        self._test_bird_cmdline_bgp_peer_show(sim, tmpdir)
