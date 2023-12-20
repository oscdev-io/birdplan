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

"""BirdPlan YAML backend."""

__all__ = ["YAML", "YAMLError"]

import logging

try:
    from .ruamel import YAML, YAMLError, __with_libyaml__

    if __with_libyaml__:
        logging.debug("YAML: Using ruamel.yaml with libyaml")
    else:
        logging.debug("YAML: Using ruamel.yaml without libyaml")
except ImportError:
    from .pyaml import YAML, YAMLError  # type: ignore

    logging.debug("YAML: Using pyyaml")