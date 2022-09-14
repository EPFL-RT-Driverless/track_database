import numpy as np
import matplotlib.pyplot as plt
from track_database.primitives import circular_arc
from track_database import load_default_skidpad
import trajectory_planning_helpers as tph


def bruh(points, psi_s, psi_e):
    coeffs_x, coeffs_y, _, normvectors = tph.calc_splines(
        path=points,
        closed=False,
        psi_s=psi_s,
        psi_e=psi_e,
    )
    normvectors = np.vstack((normvectors, tph.calc_normal_vectors_ahead(psi_e)))
    spline_lengths = tph.calc_spline_lengths(coeffs_x, coeffs_y)
    # points, _, _, _ = tph.interp_splines(
    #     coeffs_x,
    #     coeffs_y,
    #     closed=False,
    #     spline_lengths=spline_lengths,
    #     stepsize_approx=0.1,
    # )
    (
        points,
        _,
        reference_coeffs_x,
        reference_coeffs_y,
        reference_normvectors,
        reference_new_center_spline_idx,
        reference_new_center_t_values,
        reference_new_center_s_values,
        reference_spline_lengths,
        reference_el_lengths,
    ) = tph.create_raceline(
        points,
        alpha=np.zeros(len(points)),
        normvectors=normvectors,
        psi_s=psi_s,
        psi_e=psi_e,
        closed=False,
        stepsize_interp=0.1,
    )
    plt.plot(points[:, 0], points[:, 1])
    plt.axis("equal")


bruh(
    circular_arc(
        x_center=0,
        y_center=0,
        radius=10,
        start_angle=0,
        end_angle=1.5 * np.pi,
        number_points=100,
    ),
    psi_s=np.pi / 2,
    psi_e=0.0,
)
bruh(load_default_skidpad()[0], psi_s=np.pi / 2, psi_e=np.pi / 2)
plt.show()
