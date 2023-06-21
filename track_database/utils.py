# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import numpy as np
from matplotlib import pyplot as plt

__all__ = [
    "load_cones",
    "save_cones",
    "load_center_line",
    "save_center_line",
    "plot_cones",
]


def load_cones(
    filename: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Loads the cones stored in CSV file specified by filename. This file must have the
    following format:
        cone_type,X,Y,Z,std_X,std_Y,std_Z,right,left
    The returned arrays correspond to (in this order) the blue cones, yellow cones, big
    orange cones, small orange cones (possibly empty), right cones and left cones (all
    colors .
    """
    arr = np.genfromtxt(filename, delimiter=",", dtype=str, skip_header=1)
    blue_cones = arr[arr[:, 0] == "blue"][:, 1:3].astype(float)
    yellow_cones = arr[arr[:, 0] == "yellow"][:, 1:3].astype(float)
    big_orange_cones = arr[arr[:, 0] == "big_orange"][:, 1:3].astype(float)
    small_orange_cones = arr[arr[:, 0] == "small_orange"][:, 1:3].astype(float)
    right_cones = arr[arr[:, 7] == "1"][:, 1:3].astype(float)
    left_cones = arr[arr[:, 8] == "1"][:, 1:3].astype(float)
    return (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        right_cones,
        left_cones,
    )


def save_cones(
    filename: str, blue_cones, yellow_cones, big_orange_cones, small_orange_cones
):
    """
    Save the cones in CSV file specified by filename. This file will have the following
    format:
        cone_type,X,Y,Z,std_X,std_Y,std_Z,right,left
    """
    with open(filename, "w") as f:
        f.write("cone_type,X,Y,Z,std_X,std_Y,std_Z,right,left\n")
        for cone in blue_cones:
            f.write("blue,{},{},0.0,0.0,0.0,0.0,0,1\n".format(cone[0], cone[1]))
        for cone in yellow_cones:
            f.write("yellow,{},{},0.0,0.0,0.0,0.0,1,0\n".format(cone[0], cone[1]))
        for cone in big_orange_cones:
            f.write(
                "big_orange,{},{},0.0,0.0,0.0,0.0,{},{}\n".format(
                    cone[0],
                    cone[1],
                    int(cone[0] > 0),
                    int(cone[0] < 0),
                )
            )
        for cone in small_orange_cones:
            f.write(
                "small_orange,{},{},0.0,0.0,0.0,0.0,{},{}\n".format(
                    cone[0],
                    cone[1],
                    int(cone[0] > 0),
                    int(cone[0] < 0),
                )
            )


def load_center_line(filename: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Loads the center line stored in CSV file specified by filename. This file must have
    the following format:
        X,Y,right_width,left_width
    Returns the center line as a numpy array of shape (N, 2) and the corresponding
    (right and left) track widths as a numpy array of shape (N,2).
    """
    arr = np.genfromtxt(filename, delimiter=",", dtype=float, skip_header=1)
    return arr[:, :2], arr[:, 2:]


def save_center_line(filename: str, center_line: np.ndarray, track_widths: np.ndarray):
    """
    Save the center line in CSV file specified by filename. This file will have the
    following format:
        X,Y,right_width,left_width
    """
    np.savetxt(
        filename,
        np.hstack((center_line, track_widths)),
        delimiter=",",
        header="x,y,right_width,left_width",
    )


def plot_cones(
    blue_cones,
    yellow_cones,
    big_orange_cones,
    small_orange_cones,
    origin=np.zeros(2),
    show=True,
):
    plt.scatter(blue_cones[:, 0], blue_cones[:, 1], s=14, c="b", marker="^")
    plt.scatter(yellow_cones[:, 0], yellow_cones[:, 1], s=14, c="y", marker="^")
    plt.scatter(
        big_orange_cones[:, 0], big_orange_cones[:, 1], s=28, c="orange", marker="^"
    )
    try:
        plt.scatter(
            small_orange_cones[:, 0],
            small_orange_cones[:, 1],
            s=7,
            c="orange",
            marker="^",
        )
    except IndexError:
        pass
    plt.scatter(origin[0], origin[1], c="g", marker="x")
    plt.axis("equal")
    plt.tight_layout()
    if show:
        plt.show()
