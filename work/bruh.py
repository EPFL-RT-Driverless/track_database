from matplotlib import pyplot as plt
import numpy as np


def load_origin(path: str):
    try:
        arr = np.fromregex(
            path,
            r"\(X=(-?[0-9]+.[0-9]+),Y=(-?[0-9]+.[0-9]+),Z=(-?[0-9]+.[0-9]+)\)",
            dtype=[("X", float), ("Y", float), ("Z", float)],
        )
        arr = arr.view(np.float64)[:2] / 100
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
        arr -= np.expand_dims(offset, 0)
        if rot is not None:
            arr = arr.dot(
                np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
            )
        return arr
    except FileNotFoundError:
        return np.array([])


for root in [
    "Acceleration/",
    "Skidpad/",
    "FSDSdefault/",
    "FSDScompetition1/",
    "FSDScompetition2/",
    "FSDScompetition3/",
]:
    origin = load_origin(root + "origin.txt")
    print(origin)
    rot = np.pi / 2
    rot = 0.0

    blue_cones = load_cones(root + "blue.txt", origin, rot)
    yellow_cones = load_cones(root + "yellow.txt", origin, rot)
    big_orange_cones = load_cones(root + "bigorange.txt", origin, rot)
    mini_orange_cones = load_cones(root + "miniorange.txt", origin, rot)
    origin = np.zeros(2)

    # print(big_orange_cones)
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
        *mini_orange_cones.T,
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

plt.show()
