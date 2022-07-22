import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

if __name__ == "__main__":
    data = np.loadtxt("fs_track.csv", delimiter=",", skiprows=1)

    left_cones = data[:, :2].T
    right_cones = data[:, 2:4].T
    center_line_points = data[:, 4:6].T

    theta_vals = np.linspace(0.0, 1.0, center_line_points.shape[1])
    x_cl = CubicSpline(
        theta_vals,
        center_line_points[0, :],
        bc_type="periodic",
    )
    y_cl = CubicSpline(
        theta_vals,
        center_line_points[1, :],
        bc_type="periodic",
    )
    # plot track ===============
    plt.figure(figsize=(10, 5))
    plt.plot(left_cones[0, :], left_cones[1, :], "b+")
    plt.plot(right_cones[0, :], right_cones[1, :], "y+")
    plt.plot(
        x_cl(np.linspace(0.0, 1.0, 4 * center_line_points.shape[1])),
        y_cl(np.linspace(0.0, 1.0, 4 * center_line_points.shape[1])),
        "g-",
    )
    plt.axis("equal")
    plt.show(block=False)
