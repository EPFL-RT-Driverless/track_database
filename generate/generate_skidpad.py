from os.path import join, dirname
from track_database import *

center_points, left_cones, right_cones = skidpad()
export_track(
    path=join(dirname(__file__), "../track_database/data/default_skidpad.csv"),
    center_points=center_points,
    left_cones=left_cones,
    right_cones=right_cones,
)
