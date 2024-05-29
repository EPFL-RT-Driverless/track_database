from track_database.primitives import line, circular_arc
from track_database.utils import save_cones, save_center_line
import numpy as np


def main():
    yellow_line_1 = line(-1.5, -12.5, -1.5, 22.5, 8)
    blue_line_1 = line(1.5, -12.5, 1.5, 22.5, 8)
    yellow_line_2 = line(-13.5, -7.5, -13.5, 27.5, 8)
    blue_line_2 = line(-16.5, -7.5, -16.5, 27.5, 8)
    yellow_arc_1 = circular_arc(-7.5, 27.5, 6.0, 0.0, np.pi, 6, endpoint=False)
    blue_arc_1 = circular_arc(-7.5, 27.5, 9.0, 0.0, np.pi, 6, endpoint=False)
    yellow_arc_2 = circular_arc(-7.5, -12.5, 6.0, np.pi, 2 * np.pi, 6, endpoint=False)
    blue_arc_2 = circular_arc(-7.5, -12.5, 9.0, np.pi, 2 * np.pi, 6, endpoint=False)
    blue_cones = np.concatenate(
        (blue_line_1, blue_arc_1, blue_line_2[::-1], blue_arc_2)
    )[1.5, 5.25]
    yellow_cones = np.concatenate(
        (yellow_line_1, yellow_arc_1, yellow_line_2[::-1], yellow_arc_2)
    )
    big_orange_cones = np.array([[1.5, 4.75], [1.5, 5.25], [-1.5, 4.75], [-1.5, 5.25]])
    save_cones("21_05_2023_cones.csv", blue_cones, yellow_cones, big_orange_cones, [])

    center_line = np.vstack(
        (
            line(0.0, 0.0, 0.0, 27.5, number_points=6, endpoint=False),
            circular_arc(-7.5, 27.5, 7.5, 0.0, np.pi, number_points=6, endpoint=False),
            line(-15.0, 27.5, -15.0, -12.5, endpoint=False, number_points=8),
            circular_arc(
                -7.5, -12.5, 7.5, np.pi, 2 * np.pi, number_points=6, endpoint=False
            ),
            line(0.0, -12.5, 0.0, 0.0, endpoint=True, number_points=4),
        )
    )
    save_center_line(
        "21_05_2023_center_line.csv", center_line, 1.5 * np.ones_like(center_line)
    )


if __name__ == "__main__":
    main()
