# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import os.path
from os import listdir

import numpy as np

try:
    from .utils import *
except ImportError:
    from utils import *

__all__ = ["available_tracks", "load_track", "Track"]

available_tracks = [
    "acceleration",
    "skidpad",
    "short_skidpad",
    "fsds_competition_1",
    "fsds_competition_2",
    "fsds_competition_3",
    "fsds_default",
    "21_05_2023",
    "VSV",
    "VSV_XS",
    "VSV_XL",
    "autoX_Vaudoise_Sponso",
    "bike_test_0"
]


class Track:
    """
    Plain Old Data Structure (PODS) that represents a track. The track is defined by a
    set of cones and a center line. The cones are stored in the following arrays:
        blue_cones: array of blue cones
        yellow_cones: array of yellow cones
        big_orange_cones: array of big orange cones
        small_orange_cones: array of small orange cones
        right_cones: array of right cones
        left_cones: array of left cones
    The center line is stored in the following array:
        center_line: array of points on the center line
        track_widths: array of track widths at each point on the center line
    """

    name: str
    blue_cones: np.ndarray
    yellow_cones: np.ndarray
    big_orange_cones: np.ndarray
    small_orange_cones: np.ndarray
    right_cones: np.ndarray
    left_cones: np.ndarray
    center_line: np.ndarray
    track_widths: np.ndarray

    def __init__(self, name: str):
        self.name = name
        if name not in available_tracks:
            try:
                cone_file = os.path.join(
                    name,
                    list(
                        filter(
                            lambda file: file.endswith("_cones.csv"), os.listdir(name)
                        )
                    )[0],
                )
                print("Cone file : ", cone_file)
                center_line = os.path.join(
                    name,
                    list(
                        filter(
                            lambda file: file.endswith("_center_line.csv"),
                            os.listdir(name),
                        )
                    )[0],
                )
                print("center line file : ", center_line)
                (
                    self.blue_cones,
                    self.yellow_cones,
                    self.big_orange_cones,
                    self.small_orange_cones,
                    self.right_cones,
                    self.left_cones,
                ) = load_cones(cone_file)
                self.center_line, self.track_widths = load_center_line(center_line)
            except IndexError:
                raise ValueError(
                    f"Track {name} not available, or could not find the required csv files. Available tracks are: {available_tracks}"
                )
        else:
            path_to_file = (
                os.path.dirname(__file__) + "/data/" + name + "/" + name + "_cones.csv"
            )
            path_to_center_line = (
                os.path.dirname(__file__)
                + "/data/"
                + name
                + "/"
                + name
                + "_center_line.csv"
            )
            (
                self.blue_cones,
                self.yellow_cones,
                self.big_orange_cones,
                self.small_orange_cones,
                self.right_cones,
                self.left_cones,
            ) = load_cones(path_to_file)

            self.center_line, self.track_widths = load_center_line(path_to_center_line)


def load_track(name: str) -> Track:
    return Track(name)
