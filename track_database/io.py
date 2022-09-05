# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import os
from typing import Tuple

import numpy as np

__all__ = ["load_data", "save_data"]


def load_data(path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Loads data from a directory containing 4 CSV files:
    - center.csv: each row contains the x and y coordinates of a point on the center line
    - widths.csv: each row contains the right and left (in this order) width of the track at the
      corresponding point on the center line
    - right_cones.csv: each row contains the x and y coordinates of a cone on the right
      side of the track
    - left_cones.csv: each row contains the x and y coordinates of a cone on the left
      side of the track
    Raises an error if not all the files are found or the first two do not have the same
    number of rows.
    """
    # assert that the given path is a directory and contains the right files
    assert os.path.isdir(path)
    assert os.path.isfile(os.path.join(path, "center.csv"))
    assert os.path.isfile(os.path.join(path, "widths.csv"))
    assert os.path.isfile(os.path.join(path, "left_cones.csv"))
    assert os.path.isfile(os.path.join(path, "right_cones.csv"))
    # read the data from the files using np.loadtxt
    center = np.loadtxt(os.path.join(path, "center.csv"), delimiter=",", comments="#")
    widths = np.loadtxt(os.path.join(path, "widths.csv"), delimiter=",", comments="#")
    left_cones = np.loadtxt(
        os.path.join(path, "left_cones.csv"), delimiter=",", comments="#"
    )
    right_cones = np.loadtxt(
        os.path.join(path, "right_cones.csv"), delimiter=",", comments="#"
    )
    assert center.shape[0] == widths.shape[0]
    return center, widths, right_cones, left_cones


def save_data(
    path: str,
    center_points: np.ndarray,
    widths: np.ndarray,
    right_cones: np.ndarray,
    left_cones: np.ndarray,
):
    """
    Exports track data to a CSV file at the given path.
    """
    if os.path.exists(path) and not os.path.isdir(path):
        raise ValueError("Path already exists and is not a directory")
    if not os.path.exists(path):
        os.mkdir(path)
    elif os.path.isdir(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))

    assert center_points.shape[0] == widths.shape[0]

    np.savetxt(os.path.join(path, "center.csv"), center_points, delimiter=",")
    np.savetxt(os.path.join(path, "widths.csv"), widths, delimiter=",")
    np.savetxt(os.path.join(path, "left_cones.csv"), left_cones, delimiter=",")
    np.savetxt(os.path.join(path, "right_cones.csv"), right_cones, delimiter=",")
