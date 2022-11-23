from matplotlib import pyplot as plt
import numpy as np

from track_database.tracks import line, circle, circular_arc


def load_origin(path: str):
    try:
        arr = np.fromregex(
            path,
            r"\(X=(-?[0-9]+.[0-9]+),Y=(-?[0-9]+.[0-9]+),Z=(-?[0-9]+.[0-9]+)\)",
            dtype=[("X", float), ("Y", float), ("Z", float)],
        )
        arr = arr.view(np.float64)[:2] / 100
        arr[1] *= -1
        return arr
    except FileNotFoundError:
        return np.array([0, 0])


def load_cones(path: str, offset: np.ndarray, rot: float = None):
    try:
        arr = np.fromregex(
            path,
            r"\(X=(-?[0-9]+.[0-9]+),Y=(-?[0-9]+.[0-9]+),Z=(-?[0-9]+.[0-9]+)\)",
            dtype=[("X", float), ("Y", float), ("Z", float)],
        )
        arr = arr.view(np.float64).reshape(-1, 3)
        arr = arr[:, :2] / 100
        arr[:, 1] *= -1
        arr -= np.expand_dims(offset, 0)
        if rot is not None:
            arr = arr.dot(
                np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]]).T
            )

        return arr
    except FileNotFoundError:
        return np.array([])


def load_cones_csv(root: str):
    arr = np.genfromtxt(root + "cones_with_small_orange.csv", delimiter=",", dtype=str)
    blue_cones = arr[arr[:, 0] == "blue"][:, 1:3].astype(float)
    yellow_cones = arr[arr[:, 0] == "yellow"][:, 1:3].astype(float)
    big_orange_cones = arr[arr[:, 0] == "big_orange"][:, 1:3].astype(float)
    small_orange_cones = arr[arr[:, 0] == "small_orange"][:, 1:3].astype(float)
    right_cones = arr[arr[:, 7] == "1"][:, 1:3].astype(float)
    left_cones = arr[arr[:, 8] == "1"][:, 1:3].astype(float)
    return (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        right_cones,
        left_cones,
    )


def create_center_line_file(root: str):
    (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        right_cones,
        left_cones,
    ) = load_cones_csv(root)
    center_line = 0.5 * (right_cones + left_cones)
    if root not in {"Acceleration/", "Skidpad/"}:
        widths = 1.5 * np.ones_like(blue_cones)
    else:
        # re-arrange the cones so that corresponding pair of cones are next to each other
        # this is to make the width calculation easier
        widths = np.array(
            [
                np.linalg.norm(right_cones - center_line, axis=1),
                np.linalg.norm(left_cones - center_line, axis=1),
            ]
        ).T
    print(root + "path_planning.csv")
    np.savetxt(
        root + "path_planning.csv",
        np.concatenate(
            (
                center_line,
                widths,
            ),
            axis=1,
        ),
        delimiter=",",
        fmt="%s",
    )


def main(root: str, show: bool = False):

    origin = load_origin(root + "origin.txt")
    rot = np.pi / 2
    # rot = 0.0
    blue_cones = load_cones(root + "blue.txt", origin, rot)
    yellow_cones = load_cones(root + "yellow.txt", origin, rot)
    if len(blue_cones) != len(yellow_cones):
        print("Different number of blue and yellow cones for {}".format(root))
    big_orange_cones = load_cones(root + "bigorange.txt", origin, rot)
    small_orange_cones = load_cones(root + "smallorange.txt", origin, rot)
    origin = np.zeros(2)

    # export stuff in csv format: cone_type, X, Y, Z, std_X, std_Y, std_Z, right, left
    def wr(f):
        f.write("cone_type,X,Y,Z,std_X,std_Y,std_Z,right,left\n")
        for cone in blue_cones:
            f.write("blue,{},{},0.0,0.0,0.0,0.0,0,1\n".format(cone[0], cone[1]))
        for cone in yellow_cones:
            f.write("yellow,{},{},0.0,0.0,0.0,0.0,1,0\n".format(cone[0], cone[1]))
        for cone in big_orange_cones:
            f.write(
                "big_orange,{},{},0.0,0.0,0.0,0.0,{},{}\n".format(
                    cone[0],
                    cone[1],
                    int(cone[0 if np.isclose(rot, np.pi / 2) else 1] > 0),
                    int(cone[0 if np.isclose(rot, np.pi / 2) else 1] < 0),
                )
            )

    with open(root + "cones.csv", "w") as f:
        wr(f)
    with open(root + "cones_with_small_orange.csv", "w") as f:
        wr(f)
        for cone in small_orange_cones:
            f.write(
                "small_orange,{},{},0.0,0.0,0.0,0.0,{},{}\n".format(
                    cone[0],
                    cone[1],
                    int(cone[0 if np.isclose(rot, np.pi / 2) else 1] > 0),
                    int(cone[0 if np.isclose(rot, np.pi / 2) else 1] < 0),
                )
            )

    plt.figure()
    plt.plot(*blue_cones.T, color="blue", marker="^", linestyle="", label="Blue cones")
    plt.plot(
        *yellow_cones.T, color="yellow", marker="^", linestyle="", label="Yellow cones"
    )
    plt.plot(
        *big_orange_cones.T,
        color="orange",
        marker="^",
        linestyle="",
        label="Big Orange cones"
    )
    plt.plot(
        *small_orange_cones.T,
        color="magenta",
        marker="^",
        linestyle="",
        label="Small Orange cones"
    )
    plt.plot(*origin, color="green", marker="x", linestyle="", label="Origin")
    plt.legend()
    plt.title(root)
    plt.axis("equal")
    plt.tight_layout()
    if show:
        plt.show()


if __name__ == "__main__":
    # for root in [
    #     "Acceleration/",
    #     "Skidpad/",
    #     "FSDSdefault/",
    #     "FSDScompetition1/",
    #     "FSDScompetition2/",
    #     "FSDScompetition3/",
    # ]:
    #     main(root, False)
    # plt.show()

    root = "Skidpad/"
    create_center_line_file(root)
    (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        right_cones,
        left_cones,
    ) = load_cones_csv(root)

    plt.plot(right_cones[:, 0], right_cones[:, 1], color="red", label="Right cones")
    plt.plot(left_cones[:, 0], left_cones[:, 1], color="green", label="Left cones")
    plt.plot(
        *blue_cones.T,
        color="blue",
        marker="^",
        linestyle="",
        label="Blue cones",
        zorder=2
    )
    plt.plot(
        *yellow_cones.T, color="yellow", marker="^", linestyle="", label="Yellow cones"
    )
    plt.plot(
        *big_orange_cones.T,
        color="orange",
        marker="^",
        linestyle="",
        label="Big Orange cones"
    )
    plt.plot(
        *small_orange_cones.T,
        color="magenta",
        marker="^",
        linestyle="",
        label="Small Orange cones"
    )
    bruh1 = left_cones[3:17, :]
    bruh2 = np.delete(right_cones[3:18, :], 1, 0)
    print(np.linalg.norm(bruh1 - bruh2, axis=1))
    center = 0.5 * (bruh1 + bruh2)
    plt.plot(center[:, 0], center[:, 1], color="black", label="Center")
    center = np.delete(center, 8, 0)
    # link opposite center points
    for i in range(0, 6):
        plt.plot(
            [center[i, 0], center[i + 7, 0]],
            [center[i, 1], center[i + 7, 1]],
            color="black",
        )
    radius = np.mean(np.linalg.norm(center[0:6, :] - center[7:13, :], axis=1) / 2)
    center_point = np.mean(0.5 * (center[0:6, :] + center[7:13, :]), axis=0)
    plt.plot(center_point[0], center_point[1], color="black", marker="x")
    print(radius)
    print(center_point)

    plt.legend()
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def skidpad(short: bool = True):
    # skidpad center at y=14.40
    # end of center line at y=31.41
    # radius of skidpad is 9.26
    bruh = np.sqrt(9.26**2 - (9.26 - 1.75) ** 2)
    left_cones = np.concatenate(
        (
            line(-1.5, 0.0, -1.5, 15.0 - bruh, number_points=2, endpoint=False),
            circular_arc(
                x_center=9.125,
                y_center=14.4,
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
    right_cones = np.concatenate(
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
