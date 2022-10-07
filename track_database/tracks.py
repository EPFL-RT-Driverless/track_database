# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import os
from typing import Tuple

import numpy as np

from .primitives import *
from .io import *

__all__ = [
    "acceleration_track",
    "skidpad",
    "load_default_acceleration_track",
    "load_default_skidpad",
    "load_default_short_skidpad",
    "load_default_fs_track",
]


def acceleration_track(
    factor: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    assert 0.0 < factor <= 1.0
    center_line = factor * line(0.0, 0.0, 0.0, 150.3, number_points=30, endpoint=True)
    widths = 1.5 * factor * np.ones_like(center_line)
    left_cones = factor * line(-1.5, 0.3, -1.5, 150.3, number_points=30, endpoint=True)
    right_cones = factor * line(1.5, 0.3, 1.5, 150.3, number_points=30, endpoint=True)
    return center_line, widths, right_cones, left_cones


def skidpad(
    factor: float = 1.0, short: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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
        axis=0,
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
        axis=0,
    )
    center_line_parts = [
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
    ]
    if not short:
        center_line_parts.append(
            circle(
                x_center=9.125,
                y_center=15.0,
                radius=9.125,
                start_angle=np.pi,
                trigonometric_sense=False,
                number_points=30,
                endpoint=False,
            )
        )
        center_line_parts.append(
            circle(
                x_center=-9.125,
                y_center=15.0,
                radius=9.125,
                start_angle=0.0,
                trigonometric_sense=True,
                number_points=30,
                endpoint=False,
            )
        )
    center_line_parts.append(
        circle(
            x_center=-9.125,
            y_center=15.0,
            radius=9.125,
            start_angle=0.0,
            trigonometric_sense=True,
            number_points=30,
            endpoint=False,
        )
    )
    center_line_parts.append(
        line(0.0, 15.0, 0.0, 40.0, number_points=10, startpoint=False)
    )
    center_line = factor * np.concatenate(
        center_line_parts,
        axis=0,
    )
    widths = 1.5 * factor * np.ones_like(center_line)
    return center_line, widths, right_cones, left_cones


def load_default_skidpad() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Loads the default track for the skidpad event.
    Returns the center line, the widths, the right and the left cones, in this order.
    """
    path = os.path.join(os.path.dirname(__file__), "data/default_skidpad")
    return load_data(path)


def load_default_short_skidpad() -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray
]:
    """
    Loads the default track for the skidpad event.
    Returns the center line, the widths, the right and the left cones, in this order.
    """
    path = os.path.join(os.path.dirname(__file__), "data/default_short_skidpad")
    return load_data(path)


def load_default_acceleration_track() -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray
]:
    """
    Loads the default track for the acceleration event.
    Returns the center line, the widths, the right and the left cones, in this order.
    """
    path = os.path.join(os.path.dirname(__file__), "data/default_acceleration_track")
    return load_data(path)


def load_default_fs_track() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Loads the default track for the Formula Student event.
    Returns the center line, the widths, the right and the left cones, in this order.
    """
    path = os.path.join(os.path.dirname(__file__), "data/fs_track")
    return load_data(path)
