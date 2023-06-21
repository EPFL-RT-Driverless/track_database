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



def main(name, right_width, left_width):
    yellow_line_1 = line(-left_width, 0.0, -left_width, 30.0, 8, endpoint=False)
    blue_line_1 = line(right_width, 0.0, right_width, 30.0, 8, endpoint=False)
    yellow_line_2 = line(-15.0 + left_width, 30.0, -15.0 + left_width, 0.0, 8, startpoint=False)
    blue_line_2 = line(-15.0 - right_width, 30.0, -15.0 - right_width, 0.0, 8, startpoint=False)
    yellow_arc_1 = circular_arc(
        -7.5, 30.0, 7.5 - left_width, 0.0, np.pi, 7, endpoint=True
    )
    blue_arc_1 = circular_arc(
        -7.5, 30.0, 7.5 + right_width, 0.0, np.pi, 7, endpoint=True
    )
    blue_cones = np.concatenate((blue_line_1, blue_arc_1, blue_line_2))
    yellow_cones = np.concatenate((yellow_line_1, yellow_arc_1, yellow_line_2))
    big_orange_cones = np.array([[1.5, 4.75], [1.5, 5.25], [-1.5, 4.75], [-1.5, 5.25]])
    save_cones(f"{name}_cones.csv", blue_cones, yellow_cones, big_orange_cones, [])

    center_line = np.vstack(
        (
            line(0.0, 0.0, 0.0, 30.0, number_points=6, endpoint=False),
            circular_arc(-7.5, 30.0, 7.5, 0.0, np.pi, number_points=6, endpoint=False),
            line(-15.0, 30.0, -15.0, 0.0, endpoint=True, number_points=8),
        )
    )
    save_center_line(
        f"{name}_center_line.csv", center_line, 1.5 * np.ones_like(center_line)
    )


def visualize(name):
    blue_cones, yellow_cones, _, _, _, _ = load_cones(
        f"{name}_cones.csv"
    )
    plot_cones(blue_cones, yellow_cones, np.empty((0, 2)), np.empty((0, 2)), show=False)
    center_line, _ = load_center_line(f"{name}_center_line.csv")
    plt.plot(center_line[:, 0], center_line[:, 1], "k--")
    plt.scatter(center_line[:, 0], center_line[:, 1], c="k")
    plt.show()


if __name__ == "__main__":
    # name, right_width, left_width = "VSV", 1.5, 1.5
    name, right_width, left_width = "VSV_XL", 2.5, 2.5
    main(name, right_width, left_width)
    visualize(name)
