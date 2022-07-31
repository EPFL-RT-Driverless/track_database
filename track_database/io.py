import numpy as np
import pandas as pd

from .constants import *


def load_track(path: str):
    """
    Loads a track from a csv file at the given path and returns three np.ndarray's for
    the center line, left cones and right cones.
    """
    df = pd.read_csv(path)
    left_cones = df[left_labels].to_numpy().T
    right_cones = df[right_labels].to_numpy().T
    center_points = df[center_labels].to_numpy().T
    return center_points, left_cones, right_cones


def export_track(
    path: str,
    df: pd.DataFrame = None,
    center_points: np.ndarray = None,
    left_cones: np.ndarray = None,
    right_cones: np.ndarray = None,
):
    """
    Exports a track to a csv file at the given path. The track should include the
    coordinates of the left cones, right cones and cenetr line points, either specified
    by three np.ndarray's or by a pd.DataFrame
    """
    assert df is not None or (
        center_points is not None and left_cones is not None and right_cones is not None
    )
    if df is None:
        df_center = pd.DataFrame(center_points.T, columns=center_labels)
        df_left = pd.DataFrame(left_cones.T, columns=left_labels)
        df_right = pd.DataFrame(right_cones.T, columns=right_labels)
        df = pd.concat([df_center, df_left, df_right], axis=1)

    df.to_csv(path, index=False)
