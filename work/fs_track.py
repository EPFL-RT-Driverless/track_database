# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import numpy as np
from time import perf_counter

from matplotlib.collections import LineCollection
from scipy.interpolate import PPoly, CubicSpline, InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
from track_database import *
import trajectory_planning_helpers as tph


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

start = perf_counter()
# interpolate given points with cubic splines ============================================
(
    original_center_coeffs_x,
    original_center_coeffs_y,
    original_center_M,
    original_center_normvectors,
) = tph.calc_splines(np.vstack((original_center_points, original_center_points[0, :])))
original_center_spline_lengths = tph.calc_spline_lengths(
    original_center_coeffs_x, original_center_coeffs_y, no_interp_points=100
)

# create a new set of center points more finely distributed ======================
(
    new_center_points,
    new_center_original_spline_idx,
    new_center_original_t_values,
    new_center_original_s_values,
) = tph.interp_splines(
    coeffs_x=original_center_coeffs_x,
    coeffs_y=original_center_coeffs_y,
    spline_lengths=original_center_spline_lengths,
    incl_last_point=False,
    stepsize_approx=1.0,
)

# minimum curvature optimization ===================================================
(
    new_center_coeffs_x,
    new_center_coeffs_y,
    new_center_M,
    new_center_normvectors,
) = tph.calc_splines(
    path=np.vstack((new_center_points, new_center_points[0, :])),
)
new_widths = tph.interp_track_widths(
    1.5 * np.ones_like(original_widths),
    new_center_original_spline_idx,
    new_center_original_t_values,
)
alpha_min_curv, _ = tph.opt_min_curv(
    reftrack=np.hstack((new_center_points, new_widths)),
    normvectors=new_center_normvectors,
    A=new_center_M,
    kappa_bound=0.4,
    w_veh=2.0,
    closed=True,
    print_debug=True,
    method="quadprog",
)
# compute the new raceline =========================================================
(
    reference_points,
    reference_coeffs_M,
    reference_coeffs_x,
    reference_coeffs_y,
    reference_new_center_spline_idx,
    reference_new_center_t_values,
    reference_new_center_s_values,
    reference_spline_lengths,
    sth_sth,
) = tph.create_raceline(
    refline=new_center_points,
    normvectors=new_center_normvectors,
    alpha=alpha_min_curv,
    stepsize_interp=0.3,
)

# compute reference velocities =====================================================
reference_heading, reference_curvature = tph.calc_head_curv_an(
    coeffs_x=reference_coeffs_x,
    coeffs_y=reference_coeffs_y,
    ind_spls=reference_new_center_spline_idx,
    t_spls=reference_new_center_t_values,
)
reference_velocities = np.minimum(
    np.sqrt(15.0 / np.abs(reference_curvature)),
    32.0 * np.ones_like(reference_curvature),
)
print("v_x_min: ", np.min(reference_velocities))
print("v_x_max: ", np.max(reference_velocities))

left_bound = new_center_points[:, 0:2] - new_center_normvectors * np.expand_dims(
    new_widths[:, 0], axis=1
)
right_bound = new_center_points[:, 0:2] + new_center_normvectors * np.expand_dims(
    new_widths[:, 1], axis=1
)
print("computation time: {}s".format(perf_counter() - start))


def plot_colored_line(fig, ax, x, y, z, cmap="viridis"):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(z.min(), z.max())
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(z)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax)


left_bound = np.vstack((left_bound, left_bound[0, :]))
right_bound = np.vstack((right_bound, right_bound[0, :]))
new_center_points = np.vstack((new_center_points, new_center_points[0, :]))
reference_points = np.vstack((reference_points, reference_points[0, :]))
reference_velocities = np.hstack((reference_velocities, reference_velocities[0]))

plt.figure()
plt.plot(new_center_points[:, 0], new_center_points[:, 1], "k:")
# plt.plot(reference_points[:, 0], reference_points[:, 1], color="orange")
plot_colored_line(
    plt.gcf(),
    plt.gca(),
    reference_points[:, 0],
    reference_points[:, 1],
    reference_velocities,
    cmap="viridis",
)
plt.plot(right_bound[:, 0], right_bound[:, 1], color="yellow", zorder=1)
plt.scatter(right_cones[:, 0], right_cones[:, 1], color="yellow", zorder=10, marker="^")
plt.plot(left_bound[:, 0], left_bound[:, 1], color="blue", zorder=1)
plt.scatter(left_cones[:, 0], left_cones[:, 1], color="blue", zorder=10, marker="^")
plt.axis("equal")
plt.tight_layout()
plt.show()
