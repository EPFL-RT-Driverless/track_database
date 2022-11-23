# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import matplotlib.pyplot as plt
from track_database import *

if __name__ == "__main__":
    # load default skidpad from file ===================================================
    # center_line.csv, widths, right_cones, left_cones = load_default_skidpad()
    (
        center_line,
        widths,
        right_cones,
        left_cones,
    ) = load_default_short_skidpad()
    # center_line.csv, widths, right_cones, left_cones = load_default_acceleration_track()
    # (center_line.csv, widths, right_cones, left_cones) = load_default_fs_track()

    plt.plot(center_line[:, 0], center_line[:, 1], color="red", marker="+")
    plt.scatter(left_cones[:, 0], left_cones[:, 1], color="blue", marker="^")
    plt.scatter(right_cones[:, 0], right_cones[:, 1], color="yellow", marker="^")
    plt.axis("equal")
    plt.show()
