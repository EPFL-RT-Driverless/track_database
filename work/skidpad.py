# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import numpy as np
from time import perf_counter

from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
from track_database import *
import trajectory_planning_helpers as tph
from reference_path import ReferencePath

# import FS track from database =================================================
(
    original_center_points,
    original_widths,
    right_cones,
    left_cones,
) = load_default_skidpad()

# compute reference path =======================================================
start = perf_counter()
reference_path = ReferencePath(
    original_center_points,
    original_widths,
    closed=False,
    psi_s=np.pi / 2,
    psi_e=np.pi / 2,
    v_x_max=25.0,
    a_y_max=15.0,
    W=1.551,
    min_curv=False,
    compute_intermediate_vals=True,
)
print("computation time of the ReferencePath: {}s".format(perf_counter() - start))


def plot_colored_line(fig, ax, x, y, z, cmap="viridis"):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(z.min(), z.max())
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax)


center_points_plot = reference_path.intermediate_vals["center_points"]

reference_points = reference_path.reference_points
reference_velocity = reference_path.reference_velocity

plt.figure()
plt.plot(
    center_points_plot[:, 0],
    center_points_plot[:, 1],
    "k:",
)
plot_colored_line(
    plt.gcf(),
    plt.gca(),
    reference_points[:, 0],
    reference_points[:, 1],
    reference_velocity,
    cmap="viridis",
)
plt.scatter(right_cones[:, 0], right_cones[:, 1], color="yellow", zorder=10, marker="^")
plt.scatter(left_cones[:, 0], left_cones[:, 1], color="blue", zorder=10, marker="^")
plt.axis("equal")
plt.tight_layout()
plt.show()
