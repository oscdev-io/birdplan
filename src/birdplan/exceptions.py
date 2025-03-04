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

"""BirdPlan exceptions."""

import argparse

__all__ = ["BirdPlanConfigError", "BirdPlanError", "BirdPlanUsageError"]


class BirdPlanError(RuntimeError):
    """BirdPlan runtime error."""


class BirdPlanUsageError(BirdPlanError):
    """BirdPlan runtime error, raised when used incorrectly."""

    message: str
    parser: argparse.ArgumentParser

    def __init__(self, message: str, parser: argparse.ArgumentParser) -> None:
        """Initialize object."""

        super().__init__(message, parser)

        self.message = message
        self.parser = parser

    def __str__(self) -> str:
        """Return string representation of the exception."""

        return f"{self.message}\n\n{self.parser.format_help()}"


class BirdPlanConfigError(BirdPlanError):
    """BirdPlan runtime error, raised when configuration is incorrect."""
