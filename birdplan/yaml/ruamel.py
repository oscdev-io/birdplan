#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2023, AllWorldIT.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""BirdPlan YAML handling."""

import io
import pathlib
from typing import Any, Optional, Union

import ruamel.yaml as ryaml
from ruamel.yaml import __with_libyaml__
from ruamel.yaml.error import YAMLError

from .base import YAMLBase

__all__ = ["YAML", "YAMLError", "__with_libyaml__"]


class YAML(YAMLBase):
    """YAML class."""

    _ryaml: ryaml.YAML

    def __init__(self) -> None:
        """Initialize our parser YAML."""

        # Create a YAML object
        self._yaml = ryaml.YAML(typ="safe")

        # Don't use flow style as its harder to diff
        self._yaml.default_flow_style = False

        # Register the custom ctag 'tag:yaml.org,2002:python/tuple' to handle tuples
        self._yaml.constructor.add_constructor(
            "tag:yaml.org,2002:python/tuple", lambda loader, node: tuple(loader.construct_sequence(node))
        )
        self._yaml.representer.add_representer(
            tuple, lambda dumper, data: dumper.represent_sequence("tag:yaml.org,2002:python/tuple", data, flow_style=True)
        )

    def load(self, yaml: Union[str, pathlib.Path, io.IOBase]) -> Any:
        """Load YAML string."""
        return self._yaml.load(yaml)

    def dump(self, data: Any, stream: Optional[Union[pathlib.Path, io.IOBase]] = None) -> Any:
        """Dump to YAML."""
        if stream:
            return self._yaml.dump(
                data,
                stream,
            )

        # Create a string IO object and dump the YAML data to it
        dumpstr = io.StringIO()  # pragma: no cover
        with dumpstr:  # pragma: no cover
            self._yaml.dump(data, dumpstr)
            return dumpstr.getvalue()
