from track_database.primitives import line, circular_arc
from track_database.utils import save_cones, save_center_line
import numpy as np


def main():
    yellow_line_1 = line(1.5, -1.5, 1.5, 7.5, 4, True, True)
    blue_line_1 = line(-1.5, -1.5, -1.5, 10.5, 5, True, True)
    big_orange_cones = np.array([[1.5, 7], [-1.5, 7], [1.5, 8], [-1.5, 8]])
    yellow_rad_1 = circular_arc(
        3, 7.5, 1.5, np.pi, np.pi / 2, number_points=2, endpoint=True
    )
    yellow_rad_2 = circular_arc(
        3, 10.5, 1.5, np.pi * 3 / 2, 2 * np.pi, number_points=2, endpoint=True
    )
    blue_rad_1 = circular_arc(
        0, 10.5, 1.5, np.pi, np.pi / 2, number_points=2, endpoint=True
    )
    blue_rad_2 = circular_arc(
        0, 13.5, 1.5, -np.pi / 2, np.pi * 2, number_points=2, endpoint=True
    )
    yellow_line_2 = line(4.5, 10.5, 4.5, 21, endpoint=True, number_points=4)
    blue_line_2 = line(1.5, 13.5, 1.5, 21, number_points=3, endpoint=True)
    yellow_rad_3 = circular_arc(0, 21, 4.5, 0, np.pi, number_points=6, endpoint=True)
    blue_rad_3 = circular_arc(0, 21, 1.5, 0, np.pi, number_points=3, endpoint=True)
    yellow_line_3 = line(-4.5, 21, -4.5, 18, number_points=2, endpoint=True)
    yellow_rad_4 = circular_arc(
        -7.5, 18, 3, -np.pi / 2, 0, number_points=3, endpoint=True
    )
    blue_rad_4 = circular_arc(
        -7.5, 18, 6, -np.pi / 2, 0, number_points=4, endpoint=True
    )
    yellow_rad_5 = circular_arc(
        -7.5, 9, 6, np.pi / 2, np.pi, number_points=4, endpoint=True
    )
    blue_rad_5 = circular_arc(
        -7.5, 9, 3, np.pi / 2, np.pi, number_points=3, endpoint=True
    )
    yellow_line_4 = line(-13.5, 9, -13.5, -1.5, number_points=4, endpoint=True)
    blue_line_4 = line(-10.5, 9, -10.5, -1.5, number_points=4, endpoint=True)
    yellow_rad_6 = circular_arc(
        -7.5, -1.5, 6, -np.pi, -np.pi / 2, number_points=4, endpoint=True
    )
    blue_rad_6 = circular_arc(
        -7.5, -1.5, 3, -np.pi, -np.pi / 2, number_points=3, endpoint=True
    )
    yellow_line_5 = line(-7.5, -7.5, -4.5, -7.5, number_points=1, endpoint=True)
    blue_line_5 = line(-7.5, -4.5, -4.5, -4.5, number_points=1, endpoint=True)
    yellow_rad_7 = circular_arc(
        -4.5, -1.5, 6, -np.pi / 2, 0, number_points=3, endpoint=False
    )
    blue_rad_7 = circular_arc(
        -4.5, -1.5, 3, -np.pi / 2, 0, number_points=2, endpoint=False
    )
    yellow_line = np.concatenate(
        (
            yellow_line_1,
            yellow_rad_1,
            yellow_rad_2,
            yellow_line_2,
            yellow_line_3,
            yellow_line_4,
            yellow_line_5,
            yellow_rad_3,
            yellow_rad_4,
            yellow_rad_5,
            yellow_rad_6,
            yellow_rad_7,
        )
    )
    blue_line = np.concatenate(
        (
            blue_line_1,
            blue_rad_1,
            blue_rad_2,
            blue_line_2,
            blue_line_4,
            blue_line_5,
            blue_rad_3,
            blue_rad_5,
            blue_rad_4,
            blue_rad_6,
            blue_rad_7,
        )
    )
    center_line = np.vstack(
        (
            line(0, -1.5, 0, 9, number_points=10, endpoint=True),
            circular_arc(1.5, 9, 1.5, np.pi, np.pi / 2, number_points=3, endpoint=True),
            circular_arc(1.5, 12, 1.5, -np.pi / 2, 0, number_points=3, endpoint=True),
            line(3, 12, 3, 21, number_points=10, endpoint=True),
            circular_arc(0, 21, 3, 0, np.pi, number_points=10, endpoint=True),
            line(-3, 21, -3, 18, number_points=3, endpoint=True),
            circular_arc(-7.5, 18, 4.5, 0, -np.pi / 2, number_points=8, endpoint=True),
            circular_arc(
                -7.5, 9, 4.5, np.pi / 2, np.pi, number_points=8, endpoint=True
            ),
            line(-12, 9, -12, -1.5, number_points=12, endpoint=True),
            circular_arc(
                -7.5, -1.5, 4.5, -np.pi, -np.pi / 2, number_points=8, endpoint=True
            ),
            line(-7.5, -6, -4.5, -6, number_points=4, endpoint=True),
            circular_arc(
                -4.5, -1.5, 4.5, -np.pi / 2, 0, number_points=8, endpoint=True
            ),
        )
    )

    save_cones(
        "autoX_Vaudoise_Sponso_cones.csv", blue_line, yellow_line, big_orange_cones, []
    )
    save_center_line(
        "autoX_Vaudoise_Sponso_center_line.csv",
        center_line,
        1.5 * np.ones_like(center_line),
    )


if __name__ == "__main__":
    main()
