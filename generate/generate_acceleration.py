# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
from os.path import join, dirname
from track_database import acceleration_track, export_track

center_points, left_cones, right_cones = acceleration_track()
export_track(
    path=join(
        dirname(__file__), "../track_database/data/default_acceleration_track.csv"
    ),
    center_points=center_points,
    left_cones=left_cones,
    right_cones=right_cones,
)
