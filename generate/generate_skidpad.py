# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
from os.path import join, dirname
from track_database import *

if __name__ == "__main__":
    save_data(
        join(dirname(__file__), "../track_database/data/default_skidpad"),
        *skidpad(factor=1.0, short=False),
    )
    save_data(
        join(dirname(__file__), "../track_database/data/default_short_skidpad"),
        *skidpad(factor=1.0, short=True),
    )
