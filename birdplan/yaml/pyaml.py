#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2024, AllWorldIT.
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
from typing import Any, Optional, Tuple, Union

import yaml as pyaml
from yaml import YAMLError

from .base import YAMLBase

__all__ = ["YAML", "YAMLError"]


class BirdPlanSafeLoader(pyaml.SafeLoader):  # pylint: disable=too-many-ancestors
    """Safe YAML loader wtih some specific datatypes."""

    def construct_python_tuple(self, node: Any) -> Tuple[Any, ...]:
        """Tuple constructor."""
        return tuple(self.construct_sequence(node))


class BirdPlanSafeDumper(pyaml.SafeDumper):
    """Safe YAML dumper with some specific datatypes."""

    def represent_tuple(self, data: Tuple[Any, ...]) -> pyaml.nodes.SequenceNode:
        """Tuple representer."""
        return self.represent_sequence("tag:yaml.org,2002:python/tuple", data, flow_style=True)


BirdPlanSafeLoader.add_constructor("tag:yaml.org,2002:python/tuple", BirdPlanSafeLoader.construct_python_tuple)
BirdPlanSafeDumper.add_representer(tuple, BirdPlanSafeDumper.represent_tuple)


class YAML(YAMLBase):
    """YAML class."""

    def __init__(self) -> None:
        """Initialize our parser YAML."""

    def load(self, yaml: Union[str, pathlib.Path, io.IOBase]) -> Any:
        """Load YAML string."""

        yaml_data: str = ""
        # Handle strings
        if isinstance(yaml, str):
            yaml_data = yaml
        # Handle path objects
        elif isinstance(yaml, pathlib.Path):
            with open(yaml, "r", encoding="UTF-8") as yaml_file:
                yaml_data = yaml_file.read()
        # Whats left over is file objects
        elif isinstance(yaml, io.IOBase):
            yaml_data = yaml.read()

        return pyaml.load(yaml_data, BirdPlanSafeLoader)  # nosec

    def dump(self, data: Any, stream: Optional[Union[pathlib.Path, io.IOBase]] = None) -> Any:
        """Dump to YAML."""

        if stream:
            # Handle path objects
            if isinstance(stream, pathlib.Path):
                with open(stream, "w", encoding="UTF-8") as dump_file:
                    return pyaml.dump(data, stream=dump_file, encoding="UTF-8", Dumper=BirdPlanSafeDumper)
            # Whats left over is file objects
            return pyaml.dump(
                data,
                stream=stream,
                encoding="UTF-8",
                Dumper=BirdPlanSafeDumper,
            )

        # Create a string IO object and dump the YAML data to it
        dumpstr = io.StringIO()  # pragma: no cover
        with dumpstr:  # pragma: no cover
            pyaml.dump(data, dumpstr, encoding="UTF-8", Dumper=BirdPlanSafeDumper)
            return dumpstr.getvalue()
