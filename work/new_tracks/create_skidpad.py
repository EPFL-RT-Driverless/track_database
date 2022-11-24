from fsds_to_cones import *
from track_database.primitives import *


def new_skidpad(short: bool = True):
    # start of 15m, end of 25m
    blue_cones = np.concatenate(
        (
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
        ),
        axis=0,
    )
    yellow_cones = np.concatenate(
        (
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
        ),
        axis=0,
    )
    small_orange_cones = np.array([[1.5, 4.0], [1.5, 6.0], [-1.5, 4.0], [-1.5, 6.0]])
    small_orange_cones = np.vstack(
        (
            small_orange_cones,
            line(-1.5, 15.0 + 9.0, -1.5, 35.0, number_points=6, startpoint=True),
            line(1.5, 15.0 + 9.0, 1.5, 35.0, number_points=6, startpoint=True),
        )
    )
    small_orange_cones = np.vstack(
        (
            small_orange_cones,
            np.array(
                [
                    [small_orange_cones[-1, 0] / 2, small_orange_cones[-1, 1]],
                    [-small_orange_cones[-1, 0] / 2, small_orange_cones[-1, 1]],
                ]
            ),
        )
    )
    big_orange_cones = np.array([[1.5, 15.5], [-1.5, 15.5], [1.5, 14.5], [-1.5, 14.5]])

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
            endpoint=True,
        )
    )
    center_line_parts.append(
        line(0.0, 15.0, 0.0, 35.0, number_points=10, startpoint=False)
    )
    center_line = np.concatenate(
        center_line_parts,
        axis=0,
    )
    widths = 1.5 * np.ones_like(center_line)
    return (
        center_line,
        widths,
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
    )


def main():
    (
        center_line,
        widths,
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
    ) = new_skidpad(short=True)
    plt.plot(center_line[:, 0], center_line[:, 1], "k-")
    plt.scatter(blue_cones[:, 0], blue_cones[:, 1], s=7, c="b", marker="^")
    plt.scatter(yellow_cones[:, 0], yellow_cones[:, 1], s=7, c="y", marker="^")
    plt.scatter(
        big_orange_cones[:, 0], big_orange_cones[:, 1], s=14, c="orange", marker="^"
    )
    plt.scatter(
        small_orange_cones[:, 0],
        small_orange_cones[:, 1],
        s=7,
        c="orange",
        marker="^",
    )
    plt.scatter([0], [0], c="g", marker="x")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

    write_cones_csv(
        "final_data/short_skidpad/",
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
    )
    np.savetxt(
        "final_data/short_skidpad/center_line.csv",
        np.hstack((center_line, widths)),
        delimiter=",",
        header="x,y,right_width,left_width",
    )


if __name__ == "__main__":
    main()
