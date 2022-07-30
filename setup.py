from setuptools import setup

setup(
    name="track_database",
    version="1.0.0",
    packages=["track_database"],
    package_dir={"track_database": "track_database"},
    package_data={"track_database": ["data/*.csv"]},
    url="https://github.com/EPFL-RT-Driverless/track_database",
    author="tudoroancea",
    author_email="oancea.tudor@icloud.com",
    description="A package for loading and exporting track data.",
    install_requires=[
        "numpy",
        "pandas",
    ],
)
