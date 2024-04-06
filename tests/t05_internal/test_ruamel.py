#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (c) 2019-2024, AllWorldIT
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

"""YAML library tests for PyYAML."""

# pylint: disable=redefined-outer-name

import io
import pathlib
from typing import Any, List, Tuple

import pytest

from birdplan.yaml.ruamel import YAML

__all__: List[str] = []


@pytest.fixture
def yaml() -> YAML:
    """YAML object."""
    return YAML()


@pytest.fixture
def test_data() -> dict[str, Tuple[int, int, int]]:
    """Test data."""
    return {"key": (1, 2, 3)}


def test_load_from_string(yaml: YAML, test_data: Any) -> None:
    """Test loading from string."""
    yaml_string = "key: !!python/tuple [1, 2, 3]\n"
    result = yaml.load(yaml_string)
    assert result == test_data


def test_load_from_path(yaml: YAML, test_data: Any, tmp_path: pathlib.Path) -> None:
    """Test loading from path."""
    path = tmp_path / "test.yaml"
    path.write_text("key: !!python/tuple [1, 2, 3]\n")
    result = yaml.load(path)
    assert result == test_data


def test_load_from_file(yaml: YAML, test_data: Any) -> None:
    """Test loading from file."""
    yaml_file = io.StringIO("key: !!python/tuple [1, 2, 3]\n")
    result = yaml.load(yaml_file)
    assert result == test_data


def test_dump_to_path(yaml: YAML, test_data: Any, tmp_path: pathlib.Path) -> None:
    """Test dumping to path."""
    path = tmp_path / "test_dump.yaml"
    yaml.dump(test_data, path)
    result = path.read_text()
    assert result == "key: !!python/tuple [1, 2, 3]\n"


def test_dump_to_file(yaml: YAML, test_data: Any) -> None:
    """Test dumping to file."""
    yaml_file = io.StringIO()
    yaml.dump(test_data, yaml_file)
    yaml_file.seek(0)
    result = yaml_file.read()
    assert result == "key: !!python/tuple [1, 2, 3]\n"
