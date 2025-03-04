#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2025, AllWorldIT
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

"""BirdPlan monitor interface."""

import contextlib
import sys
import time

from .cmdline import BirdPlanCommandLine
from .exceptions import BirdPlanError

__all__: list[str] = []


def _run_monitor() -> None:
    """Run the birdplan monitor."""
    birdplan_cmdline = BirdPlanCommandLine(is_console=False)

    with contextlib.suppress(BirdPlanError):
        birdplan_cmdline.run(["monitor"])


# Main entry point from the birdplan monitor
def main() -> None:
    """Entry point function for the birdplan monitor."""

    while True:
        try:
            _run_monitor()
        except KeyboardInterrupt:
            sys.exit(0)
        except BirdPlanError:
            pass
        # Sleep 2 minutes before trying again
        time.sleep(120)


if __name__ == "__main__":
    main()
    sys.exit(0)
