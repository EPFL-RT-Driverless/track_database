from matplotlib import pyplot as plt
import numpy as np


def load_fsds_origin(path: str):
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


def load_fsds_cones(path: str, offset: np.ndarray, rot: float = None):
    try:
        arr = np.fromregex(
            path,
            r"\(X=(-?[0-9]+.[0-9]+),Y=(-?[0-9]+.[0-9]+),Z=(-?[0-9]+.[0-9]+)\)",
            dtype=[("X", float), ("Y", float), ("Z", float)],
        )
        # no need to also specify a "Translation" flag because the "Rotation"s also
        # contain a w field (for quaternion)
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


def load_fsds_files(root: str):
    origin = load_fsds_origin(root + "origin.txt")
    rot = np.pi / 2
    blue_cones = load_fsds_cones(root + "blue.txt", origin, rot)
    yellow_cones = load_fsds_cones(root + "yellow.txt", origin, rot)
    if len(blue_cones) != len(yellow_cones):
        print("Different number of blue and yellow cones for {}".format(root))
    big_orange_cones = load_fsds_cones(root + "bigorange.txt", origin, rot)
    small_orange_cones = load_fsds_cones(root + "smallorange.txt", origin, rot)
    origin = np.zeros(2)
    return (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        origin,
    )


def write_cones_csv(
    root: str, blue_cones, yellow_cones, big_orange_cones, small_orange_cones
):
    with open(root + "cones.csv", "w") as f:
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
                    int(cone[0 if np.isclose(np.pi / 2, np.pi / 2) else 1] > 0),
                    int(cone[0 if np.isclose(np.pi / 2, np.pi / 2) else 1] < 0),
                )
            )
        for cone in small_orange_cones:
            f.write(
                "small_orange,{},{},0.0,0.0,0.0,0.0,{},{}\n".format(
                    cone[0],
                    cone[1],
                    int(cone[0 if np.isclose(np.pi / 2, np.pi / 2) else 1] > 0),
                    int(cone[0 if np.isclose(np.pi / 2, np.pi / 2) else 1] < 0),
                )
            )


def main(root: str, show: bool = False):
    (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        origin,
    ) = load_fsds_files(root)

    # export stuff in csv format: cone_type, X, Y, Z, std_X, std_Y, std_Z, right, left
    write_cones_csv(
        root, blue_cones, yellow_cones, big_orange_cones, small_orange_cones
    )

    # plot cones
    plot_cones(
        blue_cones, yellow_cones, big_orange_cones, small_orange_cones, origin, show
    )


def plot_cones(
    blue_cones,
    yellow_cones,
    big_orange_cones,
    small_orange_cones,
    origin=np.zeros(2),
    show=True,
):
    plt.figure()
    plt.scatter(blue_cones[:, 0], blue_cones[:, 1], s=7, c="b", marker="^")
    plt.scatter(yellow_cones[:, 0], yellow_cones[:, 1], s=7, c="y", marker="^")
    plt.scatter(
        big_orange_cones[:, 0], big_orange_cones[:, 1], s=14, c="orange", marker="^"
    )
    try:
        plt.scatter(
            small_orange_cones[:, 0],
            small_orange_cones[:, 1],
            s=7,
            c="orange",
            marker="^",
        )
    except IndexError:
        pass
    plt.scatter(origin[0], origin[1], c="g", marker="x")
    plt.axis("equal")
    plt.tight_layout()
    if show:
        plt.show()


def load_cones_csv(root: str):
    arr = np.genfromtxt(root + "cones.csv", delimiter=",", dtype=str, skip_header=1)
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


if __name__ == "__main__":
    for root in [
        "Acceleration/",
        "FSDSdefault/",
        "FSDScompetition1/",
        "FSDScompetition2/",
        "FSDScompetition3/",
    ]:
        main(root, False)
    (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        right_cones,
        left_cones,
    ) = load_cones_csv("FormulaElectricBelgium/")
    plot_cones(
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        np.zeros(2),
        False,
    )
    plt.show()
