import numpy as np

from .primitives import *


def acceleration_track(factor: float = 1.0):
    assert 0.0 < factor <= 1.0
    left_cones = factor * line(-1.5, 0.3, -1.5, 150.3, number_points=30, endpoint=True)
    right_cones = factor * line(1.5, 0.3, 1.5, 150.3, number_points=30, endpoint=True)
    center_line = factor * np.concatenate(
        (
            line(0.0, 0.3, 0.0, 150.3, number_points=30, endpoint=True),
            np.array([[0.0], [0.0]]),
        ),
        axis=1,
    )
    return center_line, left_cones, right_cones


def skidpad(factor: float = 1.0):
    assert 0.0 < factor <= 1.0
    # start of 15m, end of 25m
    bruh = np.sqrt(9.125**2 - (9.125 - 1.5) ** 2)
    left_cones = factor * np.concatenate(
        (
            line(-1.5, 0.0, -1.5, 15.0 - bruh, number_points=2, endpoint=False),
            circular_arc(
                x_center=9.125,
                y_center=15.0,
                radius=10.625,
                start_angle=6.0 / 16.0 * 2.0 * np.pi,
                end_angle=-6.0 / 16.0 * 2.0 * np.pi,
                number_points=13,
                endpoint=True,
            ),
            circle(
                x_center=-9.125,
                y_center=15.0,
                radius=7.625,
                start_angle=0.0,
                trigonometric_sense=True,
                number_points=16,
                endpoint=False,
            ),
            line(-1.5, 15.0 + bruh, -1.5, 40.0, number_points=3, startpoint=False),
        ),
        axis=1,
    )
    right_cones = factor * np.concatenate(
        (
            line(1.5, 0.0, 1.5, 15.0 - bruh, number_points=2, endpoint=False),
            circle(
                x_center=9.125,
                y_center=15.0,
                radius=7.625,
                start_angle=np.pi,
                trigonometric_sense=False,
                number_points=16,
                endpoint=False,
            ),
            circular_arc(
                x_center=-9.125,
                y_center=15.0,
                radius=10.625,
                start_angle=2.0 / 16.0 * 2.0 * np.pi,
                end_angle=14.0 / 16.0 * 2.0 * np.pi,
                number_points=13,
                endpoint=True,
            ),
            line(1.5, 15.0 + bruh, 1.5, 40.0, number_points=3, startpoint=False),
        ),
        axis=1,
    )
    center_line = factor * np.concatenate(
        (
            line(0.0, 0.0, 0.0, 15.0, number_points=10, endpoint=False),
            circle(
                x_center=9.125,
                y_center=15.0,
                radius=9.125,
                start_angle=np.pi,
                trigonometric_sense=False,
                number_points=30,
                endpoint=False,
            ),
            circle(
                x_center=-9.125,
                y_center=15.0,
                radius=9.125,
                start_angle=0.0,
                trigonometric_sense=True,
                number_points=30,
                endpoint=False,
            ),
            line(0.0, 15.0, 0.0, 40.0, number_points=10, startpoint=False),
        ),
        axis=1,
    )
    return center_line, left_cones, right_cones
