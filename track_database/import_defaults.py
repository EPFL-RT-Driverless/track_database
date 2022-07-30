import os

from .io import *


def import_default_skidpad():
    path = os.path.join(os.path.dirname(__file__), "data/default_skidpad.csv")
    return load_track(path)


def import_default_acceleration_track():
    path = os.path.join(
        os.path.dirname(__file__), "data/default_acceleration_track.csv"
    )
    return load_track(path)
