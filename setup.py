"""BirdPlan configuration generator."""
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2019-2020, AllWorldIT.
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

import re
from setuptools import find_packages, setup

main_py = open("birdplan/__init__.py").read()
metadata = dict(re.findall('__([A-Z]+)__ = "([^"]+)"', main_py))

NAME = "birdplan"
VERSION = metadata["VERSION"]

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name=NAME,
    version=VERSION,
    author="Nigel Kukard",
    author_email="nkukard@lbsd.net",
    description="BirdPlan configuration file generator",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://oscdev.io/software/birdplan",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic:: System:: Networking",
    ],
    python_requires=">=3.8",
    install_requires=["birdclient", "nsnetsim", "pyyaml", "colorama"],
    packages=find_packages(),
    entry_points={"console_scripts": ["birdplan=birdplan.cmdline:run_birdplan"]},
)
