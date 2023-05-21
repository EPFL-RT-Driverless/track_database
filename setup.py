# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    # delete lines starting with # and empty lines
    requirements = [
        r
        for r in requirements
        if not (r.startswith("#") or r.startswith("-e git+") or r.startswith("git+"))
    ]

setup(
    name="track_database",
    version="3.1.0",
    packages=["track_database"],
    package_dir={"track_database": "track_database"},
    package_data={"track_database": ["data/*.csv"]},
    url="https://github.com/EPFL-RT-Driverless/track_database",
    author="tudoroancea",
    description="A Python package to gather some default Formula Student tracks as well as some utility functions to import/export them in CSV format and to create new custom tracks.",
    long_description=readme,
    install_requires=requirements,
)
