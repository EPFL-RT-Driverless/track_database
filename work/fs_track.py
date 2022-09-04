# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import numpy as np
from time import perf_counter
from scipy.interpolate import PPoly, CubicSpline, InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
from track_database import *
import trajectory_planning_helpers as tph


# import FS track from database =================================================
start = perf_counter()
center_points, widths, right_cones, left_cones = load_default_fs_track()
N = center_points.shape[0] - 1  # index of the last point, N = 54

# plot track with cones ===========================================================
# plt.figure()
# plt.scatter(center_points[:, 0], center_points[:, 1], label="center", color="black")
# plt.scatter(left_cones[:, 0], left_cones[:, 1], label="left", color="blue")
# plt.scatter(right_cones[:, 0], right_cones[:, 1], label="right", color="yellow")
# plt.axis("equal")
# plt.title("original reference points and cones")
# plt.show()

# interpolate track with cubic splines ============================================
coeffs_x, coeffs_y, M, normvec_normalized = tph.calc_splines(
    np.vstack((center_points, center_points[0, :]))
)  # coeffs_x and coeffs_y have shape (55,4) and (55,4) cause there are N+1=55 splines
spline_lengths = tph.calc_spline_lengths(
    coeffs_x, coeffs_y, no_interp_points=100
)  # spline_lengths has shape (55,) cause again there are 55 splines
# x_spline = PPoly(
#     np.transpose(coeffs_x[:, ::-1]),
#     np.arange(N + 2, dtype=np.float64),
#     extrapolate="periodic",
# )
# y_spline = PPoly(
#     np.transpose(coeffs_y[:, ::-1]),
#     np.arange(N + 2, dtype=np.float64),
#     extrapolate="periodic",
# )
# t = np.linspace(0, N + 1, 100, dtype=np.float64, endpoint=False)
# plt.figure()
# plt.scatter(x_spline(t), y_spline(t))
# plt.axis("equal")
# plt.title("PPoly's at work")
# plt.show()

# create a new set of reference points more finely distributed ======================
(
    center_points_interp,
    spline_idx_center_points_interp,
    t_values_center_points_interp,
    s_center_points_interp,
) = tph.interp_splines(
    spline_lengths=spline_lengths,
    coeffs_x=coeffs_x,
    coeffs_y=coeffs_y,
    incl_last_point=False,
    stepsize_approx=1.0,
)
x_vs_arc_length = InterpolatedUnivariateSpline(
    s_center_points_interp, center_points_interp[:, 0], k=1
)
y_vs_arc_length = InterpolatedUnivariateSpline(
    s_center_points_interp, center_points_interp[:, 1], k=1
)
# plt.figure()
# plt.plot(raceline_interp[:, 0], raceline_interp[:, 1], label="raceline", color="black")
# plt.scatter(left_cones[:, 0], left_cones[:, 1], label="left", color="blue")
# plt.scatter(right_cones[:, 0], right_cones[:, 1], label="right", color="yellow")
# plt.axis("equal")
# plt.title("new finely distributed reference points with cones")
# plt.show()

# track widths =====================================================================
w_track = widths
w_track = np.ones((N + 1, 2)) * 1.5

w_track_interp = tph.interp_track_widths(
    w_track,
    spline_idx_center_points_interp,
    t_values_center_points_interp,
)

# minimum curvature optimization ===================================================
_, _, A, normvectors_interp = tph.calc_splines(
    path=np.vstack((center_points_interp, center_points_interp[0, :])),
)

alpha_min_curv, _ = tph.opt_min_curv(
    reftrack=np.hstack((center_points_interp, w_track_interp)),
    normvectors=normvectors_interp,
    A=A,
    kappa_bound=0.4,
    w_veh=2.0,
    closed=True,
    print_debug=True,
    method="quadprog",
)
(
    reference_points,
    A_reference_points,
    coeffs_x_reference_points,
    coeffs_y_reference_points,
    _,
    _,
    _,
    _,
    _,
) = tph.create_raceline(
    refline=center_points_interp,
    normvectors=normvectors_interp,
    alpha=alpha_min_curv,
    stepsize_interp=0.3,
)

bound1 = center_points_interp[:, 0:2] - normvectors_interp * np.expand_dims(
    w_track_interp[:, 0], axis=1
)
bound2 = center_points_interp[:, 0:2] + normvectors_interp * np.expand_dims(
    w_track_interp[:, 1], axis=1
)
print("time: ", perf_counter() - start)
plt.figure()
plt.plot(center_points_interp[:, 0], center_points_interp[:, 1], "k:")
plt.plot(reference_points[:, 0], reference_points[:, 1], color="orange")
plt.plot(bound2[:, 0], bound2[:, 1], color="blue", zorder=1)
plt.scatter(left_cones[:, 0], left_cones[:, 1], color="blue", zorder=10)
plt.plot(bound1[:, 0], bound1[:, 1], color="yellow", zorder=1)
plt.scatter(right_cones[:, 0], right_cones[:, 1], color="yellow", zorder=10)
plt.axis("equal")
plt.tight_layout()
plt.show()

# determine the heading angles and curvatures of each one of the new points =========
# (heading_angles_raceline_interp, curvatures_raceline_interp,) = tph.calc_head_curv_an(
#     coeffs_x=coeffs_x,
#     coeffs_y=coeffs_y,
#     ind_spls=spline_inds_raceline_interp,
#     t_spls=t_values_raceline_interp,
#     calc_curv=True,
# )
#
# interpolate linearly the heading angle and the curvature vs the arc length s ======
# heading_vs_arc_length = InterpolatedUnivariateSpline(
#     s_raceline_interp, heading_angles_raceline_interp, k=1
# )
# curvature_vs_arc_length = InterpolatedUnivariateSpline(
#     s_raceline_interp, curvatures_raceline_interp, k=1
# )

# determine velocity profile ======================================================
