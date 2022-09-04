# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
from os.path import join, dirname
from track_database import *

save_data(
    join(dirname(__file__), "../track_database/data/default_skidpad"),
    *skidpad(factor=1.0),
)
