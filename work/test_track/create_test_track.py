from track_database.primitives import line, circular_arc
from track_database.utils import (
    save_cones,
    save_center_line,
    plot_cones,
    load_center_line,
    load_cones,
)
import matplotlib.pyplot as plt
import numpy as np


def main(name, track_width, length, width, ncones_straight, ncones_arc):
    blue_line_1 = line(
        -track_width, 0.0, -track_width, length, ncones_straight, endpoint=False
    )
    yellow_line_1 = line(
        track_width, 0.0, track_width, length, ncones_straight, endpoint=False
    )
    blue_line_2 = line(
        -width + track_width,
        length,
        -width + track_width,
        0.0,
        ncones_straight,
        startpoint=False,
    )
    yellow_line_2 = line(
        -width - track_width,
        length,
        -width - track_width,
        0.0,
        ncones_straight,
        startpoint=False,
    )
    blue_arc_1 = circular_arc(
        -width / 2,
        length,
        width / 2 - track_width,
        0.0,
        np.pi,
        ncones_arc,
        endpoint=True,
    )
    yellow_arc_1 = circular_arc(
        -width / 2,
        length,
        width / 2 + track_width,
        0.0,
        np.pi,
        ncones_arc,
        endpoint=True,
    )
    yellow_cones = np.concatenate((yellow_line_1, yellow_arc_1, yellow_line_2))
    blue_cones = np.concatenate((blue_line_1, blue_arc_1, blue_line_2))
    big_orange_cones = np.array([[1.5, 4.75], [1.5, 5.25], [-1.5, 4.75], [-1.5, 5.25]])
    save_cones(f"{name}_cones.csv", blue_cones, yellow_cones, big_orange_cones, [])

    center_line = np.vstack(
        (
            line(0.0, 0.0, 0.0, length, number_points=ncones_straight, endpoint=False),
            circular_arc(
                -width / 2,
                length,
                width / 2,
                0.0,
                np.pi,
                number_points=ncones_arc,
                endpoint=False,
            ),
            line(
                -width,
                length,
                -width,
                0.0,
                endpoint=True,
                number_points=ncones_straight,
            ),
        )
    )
    save_center_line(
        f"{name}_center_line.csv", center_line, 1.5 * np.ones_like(center_line)
    )


def visualize(name):
    blue_cones, yellow_cones, _, _, _, _ = load_cones(f"{name}_cones.csv")
    plot_cones(blue_cones, yellow_cones, np.empty((0, 2)), np.empty((0, 2)), show=False)
    center_line, _ = load_center_line(f"{name}_center_line.csv")
    plt.plot(center_line[:, 0], center_line[:, 1], "k--")
    plt.scatter(center_line[:, 0], center_line[:, 1], c="k")
    plt.show()


if __name__ == "__main__":
    main(
        name="test_track",
        track_width=2.0,
        length=15.0,
        width=10.0,
        ncones_straight=5,
        ncones_arc=7,
    )
    visualize("test_track")
