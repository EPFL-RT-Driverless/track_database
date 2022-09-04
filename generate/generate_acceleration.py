# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
from os.path import join, dirname
from track_database import acceleration_track, save_data

save_data(
    join(dirname(__file__), "../track_database/data/default_acceleration_track"),
    *acceleration_track(factor=1.0),
)
