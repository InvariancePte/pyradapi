#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="setup.py" company="Invariance Pte Limited">
#  Copyright (C) 2022 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
# </copyright>
# --------------------


import setuptools


setuptools.setup(
    name="pyradapi",
    version="0.151",
    packages=["pyradapi"],
    description="A python package to use radix api easily",
    license="Invariance Pte Limited",
    requires=[],
    package_dir={"": "src"},
)
