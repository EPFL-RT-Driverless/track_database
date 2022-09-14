#  Copyright (c) 2022. Tudor Oancea EPFL Racing Team Driverless
from typing import Tuple, Union, Optional

import numpy as np
from numpy import ndarray
from scipy.interpolate import InterpolatedUnivariateSpline

import trajectory_planning_helpers as tph

__all__ = ["ReferencePath"]


class ReferencePath:
    # general options
    original_center_points: np.ndarray
    reference_points: np.ndarray
    reference_heading: np.ndarray
    reference_curvature: np.ndarray
    reference_velocity: np.ndarray

    closed: bool

    arc_lengths: np.ndarray
    total_length: float  # total length of the reference path
    total_time: float  # total race time of the reference path

    X_ref_vs_arc_length: InterpolatedUnivariateSpline
    Y_ref_vs_arc_length: InterpolatedUnivariateSpline
    heading_vs_arc_length: InterpolatedUnivariateSpline
    v_x_vs_arc_length: InterpolatedUnivariateSpline
    time_vs_arc_length: InterpolatedUnivariateSpline
    X_ref_vs_time: InterpolatedUnivariateSpline
    Y_ref_vs_time: InterpolatedUnivariateSpline

    intermediate_vals: Optional[dict[str, np.ndarray]]
    # has to contain the following keys: "center_points", "right_bound", "left_bound"

    def __init__(
        self,
        center_points: ndarray,
        widths: ndarray,
        closed: bool,
        v_x_max: float,
        a_y_max: float,
        W: Optional[float] = None,
        min_curv: bool = True,
        psi_s: Optional[float] = None,
        psi_e: Optional[float] = None,
        compute_intermediate_vals: bool = False,
    ):
        """
        Description:
        ------------
        Encapsulates the motion planning task by creating a reference path/trajectory
        and planning appropriate velocities along it.
        Supported procedures: minimal curvature optimization for the path generation and
        usage of the max lateral acceleration and curvature at any point to plan the
        velocity profile.

        Args:
        ------
        :param center_points: Nx2 array of center points, should be ordered in the sense
         of the track, not too far apart so that the center line can be accurately
         interpolated by cubic splines, and in all cases unclosed (i.e. the first and
         last points should not be the same).
        :param widths: Nx2 array of track widths (right and left) at each center point.
         Should be unclosed.
        :param closed: whether the track should be considered closed or not. If closed,
         the first and last points of the center line will be connected, if not, psi_s
         and psi_e will be used to compute the heading at the start and end of the track.
        :param v_x_max: maximum longitudinal velocity of the car
        :param a_y_max: maximum lateral acceleration of the car
        :param W: width of the car. Must be specified if min_curv is True.
        :param min_curv: whether the reference path should be computed with by curvature
         minimization or not. If not, the reference path will be the center line.
        :param psi_s: heading at the start of the track. Must be specified if closed is
         False.
        :param psi_e: heading at the end of the track. Must be specified if closed is
         False.
        """
        # input verification ======================================================
        if not closed:
            assert (
                psi_s is not None and psi_e is not None
            ), "psi_s and psi_e must be defined for unclosed tracks"

        assert center_points.shape[1] == 2
        assert widths.shape == center_points.shape
        if min_curv:
            assert W is not None, "W must be defined for min_curv=True"

        self.original_center_points = center_points
        self.closed = closed

        # fit cubic splines to fit the given center points =========================
        (
            original_center_coeffs_x,
            original_center_coeffs_y,
            _,
            original_center_normvectors,
        ) = tph.calc_splines(
            path=center_points,
            closed=closed,
            psi_s=psi_s,  # psi_s is ignored if closed is True
            psi_e=psi_e,  # psi_e is ignored if closed is True
        )

        if not closed:
            original_center_normvectors = np.vstack(
                (
                    original_center_normvectors,
                    tph.calc_normal_vectors(np.array(psi_e)),
                )
            )

        spline_lengths = tph.calc_spline_lengths(
            coeffs_x=original_center_coeffs_x,
            coeffs_y=original_center_coeffs_y,
            no_interp_points=100,
        )

        # compute the reference points =============================================
        if min_curv:
            # compute intermediate points more tightly spaced but not too much to avoid
            # long computation times in curvature minimization ========================
            (
                new_center_points,
                new_center_original_spline_idx,
                new_center_original_t_values,
                _,
            ) = tph.interp_splines(
                coeffs_x=original_center_coeffs_x,
                coeffs_y=original_center_coeffs_y,
                spline_lengths=spline_lengths,
                closed=closed,
                stepsize_approx=1.0,
            )

            # minimum curvature optimization =======================================
            (_, _, new_center_M, new_center_normvectors) = tph.calc_splines(
                path=new_center_points,
                closed=closed,
                psi_s=psi_s,
                psi_e=psi_e,
            )

            if not closed:
                new_center_normvectors = np.vstack(
                    (
                        new_center_normvectors,
                        tph.calc_normal_vectors(np.array(psi_e)),
                    )
                )

            new_widths = tph.interp_track_widths(
                1.5 * np.ones_like(widths),
                new_center_original_spline_idx,
                new_center_original_t_values,
            )
            if compute_intermediate_vals:
                self.intermediate_vals = {
                    "center_points": new_center_points,
                    "right_bound": new_center_points
                    + new_widths * new_center_normvectors,
                    "left_bound": new_center_points
                    - new_widths * new_center_normvectors,
                }
            else:
                self.intermediate_vals = None

            alpha_min_curv, _ = tph.opt_min_curv(
                reftrack=np.hstack((new_center_points, new_widths)),
                normvectors=new_center_normvectors,
                A=new_center_M,
                kappa_bound=0.4,
                w_veh=W,
                closed=closed,
                psi_s=psi_s,
                psi_e=psi_e,
                print_debug=True,
                method="quadprog",
            )

            # compute the new raceline =========================================================
            (
                reference_points,
                _,
                reference_coeffs_x,
                reference_coeffs_y,
                _,
                reference_new_center_spline_idx,
                reference_new_center_t_values,
                reference_new_center_s_values,
                reference_spline_lengths,
                reference_el_lengths,
            ) = tph.create_raceline(
                refline=new_center_points,
                normvectors=new_center_normvectors,
                alpha=alpha_min_curv,
                stepsize_interp=0.1,
                closed=closed,
                psi_s=psi_s,
                psi_e=psi_e,
            )

            # reuse interp_splines here to compute points on the center line but with 0.1mdistance
            self.intermediate_vals = {
                "center_points": new_center_points,
                "right_bound": new_center_points
                + np.expand_dims(new_widths[:, 0], 1) * new_center_normvectors,
                "left_bound": new_center_points
                - np.expand_dims(new_widths[:, 1], 1) * new_center_normvectors,
            }

        else:
            # compute the new raceline =========================================================
            (
                reference_points,
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
                refline=center_points,
                normvectors=original_center_normvectors,
                alpha=np.zeros(center_points.shape[0]),
                stepsize_interp=0.1,
                closed=closed,
                psi_s=psi_s,
                psi_e=psi_e,
            )
            headings, _ = tph.calc_head_curv_an(
                coeffs_x=reference_coeffs_x,
                coeffs_y=reference_coeffs_y,
                ind_spls=reference_new_center_spline_idx,
                t_spls=reference_new_center_t_values,
                calc_curv=False,
            )
            norm_vectors = tph.calc_normal_vectors(headings)

            new_widths = tph.interp_track_widths(
                widths,
                reference_new_center_spline_idx,
                reference_new_center_t_values,
            )
            if compute_intermediate_vals:
                self.intermediate_vals = {
                    "center_points": reference_points,
                    "right_bound": reference_points
                    + np.expand_dims(new_widths[:, 0], 1) * norm_vectors,
                    "left_bound": reference_points
                    - np.expand_dims(new_widths[:, 1], 1) * norm_vectors,
                }
            else:
                self.intermediate_vals = None

        self.reference_points = reference_points
        self.arc_lengths = reference_new_center_s_values

        if closed:
            self.total_length = (
                reference_new_center_s_values[-1] + reference_el_lengths[-1]
            )
        else:
            self.total_length = reference_new_center_s_values[-1]

        # compute reference heading and curvature =====================================
        self.reference_heading, self.reference_curvature = tph.calc_head_curv_an(
            coeffs_x=reference_coeffs_x,
            coeffs_y=reference_coeffs_y,
            ind_spls=reference_new_center_spline_idx,
            t_spls=reference_new_center_t_values,
        )

        # compute reference velocities =====================================================
        np.seterr(divide="ignore")
        self.reference_velocity = np.minimum(
            np.sqrt(a_y_max / np.abs(self.reference_curvature)),
            v_x_max * np.ones_like(self.reference_curvature),
        )
        np.seterr(divide="warn")
        # TODO: use calc_t_profile
        if closed:
            self.passage_time = np.insert(
                np.cumsum(
                    reference_el_lengths
                    / movmean(
                        np.append(self.reference_velocity, self.reference_velocity[0]),
                        2,
                    )
                ),
                0,
                0.0,
            )
        else:
            self.passage_time = np.insert(
                np.cumsum(reference_el_lengths / movmean(self.reference_velocity, 2)),
                0,
                0.0,
            )

        self.total_time = self.passage_time[-1]

        # create final interpolation objects =========================================
        self.X_ref_vs_arc_length = InterpolatedUnivariateSpline(
            np.append(reference_new_center_s_values, self.total_length)
            if closed
            else reference_new_center_s_values,
            np.append(reference_points[:, 0], reference_points[0, 0])
            if closed
            else reference_points[:, 0],
            k=1,
            ext="const",
        )
        self.Y_ref_vs_arc_length = InterpolatedUnivariateSpline(
            np.append(reference_new_center_s_values, self.total_length)
            if closed
            else reference_new_center_s_values,
            np.append(reference_points[:, 1], reference_points[0, 1])
            if closed
            else reference_points[:, 1],
            k=1,
            ext="const",
        )
        self.heading_vs_arc_length = InterpolatedUnivariateSpline(
            np.append(reference_new_center_s_values, self.total_length)
            if closed
            else reference_new_center_s_values,
            np.append(self.reference_heading, self.reference_heading[0])
            if closed
            else self.reference_heading,
            k=1,
            ext="const",
        )
        self.v_x_vs_arc_length = InterpolatedUnivariateSpline(
            np.append(reference_new_center_s_values, self.total_length)
            if closed
            else reference_new_center_s_values,
            np.append(self.reference_velocity, self.reference_velocity[0])
            if closed
            else self.reference_velocity,
            k=1,
            ext="const",
        )
        self.time_vs_arc_length = InterpolatedUnivariateSpline(
            np.append(reference_new_center_s_values, self.total_length)
            if closed
            else reference_new_center_s_values,
            self.passage_time,
            k=1,
            ext="const",
        )
        self.X_ref_vs_time = InterpolatedUnivariateSpline(
            self.passage_time,
            np.append(reference_points[:, 0], reference_points[0, 0])
            if closed
            else reference_points[:, 0],
            k=1,
            ext="const",
        )
        self.Y_ref_vs_time = InterpolatedUnivariateSpline(
            self.passage_time,
            np.append(reference_points[:, 1], reference_points[0, 1])
            if closed
            else reference_points[:, 1],
            k=1,
            ext="const",
        )

    def localize_point(
        self,
        pos: np.ndarray,
        guess: float,
        tolerance: Optional[float] = 20.0,
    ) -> Tuple[float, np.ndarray]:
        # TODO: implement a better localization method
        if self.closed:
            return tph.path_matching_global(
                path_cl=np.hstack(
                    (
                        np.vstack((self.reference_points, self.reference_points[0, :])),
                        np.reshape(
                            np.append(self.arc_lengths, self.total_length), (-1, 1)
                        ),
                    )
                ),
                ego_position=pos,
                s_expected=guess,
                s_range=tolerance,
            )
        else:
            # get relevant part of the reference path
            s_min = max(0.0, guess - tolerance)
            s_max = min(self.total_length, guess + tolerance)

            # get indices of according points
            idx_start = (
                np.searchsorted(self.arc_lengths, s_min, side="right") - 1
            )  # - 1 to include trajectory point before s_min
            idx_stop = (
                np.searchsorted(self.arc_lengths, s_max, side="left") + 1
            )  # + 1 to include trajectory point after s_max when slicing
            return tph.path_matching_local(
                path=np.hstack(
                    (
                        self.arc_lengths[idx_start:idx_stop].reshape(),
                        self.reference_points[idx_start:idx_stop],
                    )
                ),
                ego_position=pos,
                consider_as_closed=False,
            )

    def extract_horizon(
        self,
        horizon_size: int,
        sampling_time: float,
        pos: np.ndarray,
        guess: Optional[float] = None,
        tolerance: Optional[Union[float, list, tuple, np.ndarray]] = None,
    ) -> tuple[ndarray, float]:
        # localize on the reference path
        arc_length_localization, pos_localization = self.localize_point(
            pos, guess=guess, tolerance=tolerance
        )
        # get map passage time corresponding to the localization
        time_reference = self.time_vs_arc_length(arc_length_localization)
        # passage times vector for prediction horizon
        time_horizon = np.linspace(
            time_reference, time_reference + horizon_size * sampling_time, horizon_size
        )
        time_horizon = np.mod(time_horizon, self.total_time)
        # interpolate map to get reference points
        X_horizon = self.Y_ref_vs_time(time_horizon)
        Y_horizon = self.Y_ref_vs_time(time_horizon)
        return np.array([X_horizon, Y_horizon]), arc_length_localization


def movmean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def wrap_to_pi(x):
    return np.mod(x + np.pi, 2 * np.pi) - np.pi
