# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import numpy as np
from time import perf_counter

from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
from track_database import *
from reference_path import ReferencePath

# import FS track from database =================================================
(
    original_center_points,
    original_widths,
    right_cones,
    left_cones,
) = load_default_fs_track()
rot_matrix = np.array(
    [
        [np.cos(-np.pi / 2), -np.sin(-np.pi / 2)],
        [np.sin(-np.pi / 2), np.cos(-np.pi / 2)],
    ]
)
original_center_points = np.matmul(original_center_points, rot_matrix.T)
right_cones = np.matmul(right_cones, rot_matrix.T)
left_cones = np.matmul(left_cones, rot_matrix.T)
widths = 0.5 * original_widths

# compute reference path =======================================================
start = perf_counter()
reference_path = ReferencePath(
    original_center_points,
    widths,
    closed=True,
    v_x_max=25.0,
    a_y_max=15.0,
    W=1.551,
    min_curv=True,
    compute_intermediate_vals=True,
)
print("computation time of the ReferencePath: {}s".format(perf_counter() - start))

new_center_points = reference_path.intermediate_vals["center_points"]
right_bound = reference_path.intermediate_vals["right_bound"]
left_bound = reference_path.intermediate_vals["left_bound"]
reference_points = reference_path.reference_points
reference_velocity = reference_path.reference_velocity


reference_points = np.vstack((reference_points, reference_points[0, :]))
reference_velocity = np.hstack((reference_velocity, reference_velocity[0]))
new_center_points = np.vstack((new_center_points, new_center_points[0, :]))
right_bound = np.vstack((right_bound, right_bound[0, :]))
left_bound = np.vstack((left_bound, left_bound[0, :]))


def plot_colored_line(fig, ax, x, y, z, cmap="viridis"):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(z.min(), z.max())
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax)


plt.figure()
plt.plot(new_center_points[:, 0], new_center_points[:, 1], "k:")
plot_colored_line(
    plt.gcf(),
    plt.gca(),
    reference_points[:, 0],
    reference_points[:, 1],
    reference_velocity,
    cmap="inferno",
)
plt.plot(right_bound[:, 0], right_bound[:, 1], color="yellow", zorder=1)
plt.scatter(right_cones[:, 0], right_cones[:, 1], color="yellow", zorder=10, marker="^")
plt.plot(left_bound[:, 0], left_bound[:, 1], color="blue", zorder=1)
plt.scatter(left_cones[:, 0], left_cones[:, 1], color="blue", zorder=10, marker="^")
plt.axis("equal")
plt.tight_layout()
plt.show()
