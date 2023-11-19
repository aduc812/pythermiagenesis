#!/usr/bin/env python
from setuptools import setup


setup(
    name="pythermiagenesis",
    version="0.1.8",
    author="Johan Isaksson, extended by Sergey Omelkov",
    author_email="johan@generatorhallen.se, omelkovs@gmail.com",
    description="Python wrapper for getting data from Thermia Mega and Inverter heat pumps \
        via Modbus TCP or Modbus RTU.",
    include_package_data=True,
    url="https://github.com/aduc812/pythermiagenesis",
    license="MIT",
    packages=["pythermiagenesis"],
    python_requires=">=3.6",
    # install_requires=["pymodbustcp==0.1.10"],
    extras_require={
        'TCP':[ "pymodbustcp==0.1.10" ],
        'RTU':[ "pymodbus>=3.0.0" ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    setup_requires=("pytest-runner"),
    tests_require=(
        "asynctest",
        "pytest-cov",
        "pytest-asyncio",
        "pytest-trio",
        "pytest-tornasync",
    ),
)
