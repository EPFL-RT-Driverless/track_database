import numpy as np
import pandas as pd

left_labels = ["X_left", "Y_left"]
right_labels = ["X_right", "Y_right"]
center_labels = ["X_center", "Y_center"]


def load_track(path: str):
    """
    Loads a track from a csv file.
    """
    df = pd.read_csv(path, header=1)
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
    Exports a track to a csv file.
    """
    assert df is not None or (
        center_points is not None and left_cones is not None and right_cones is not None
    )
    if df is None:
        df = pd.DataFrame(columns=center_labels + left_labels + right_labels)
        df[center_labels] = center_points.T
        df[left_labels] = left_cones.T
        df[right_labels] = right_cones.T

    df.to_csv(path, index=False)
