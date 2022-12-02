import numpy as np
import matplotlib.pyplot as plt
import trajectory_planning_helpers as tph


def load_cones_csv(root: str):
    arr = np.genfromtxt(root + "cones.csv", delimiter=",", dtype=str)
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


def import_center_line(root: str):
    bruh = np.genfromtxt(root + "center_line.csv", delimiter=",", skip_header=1)
    center = bruh[:, :2]
    width = bruh[:, 2:]
    return center, width


def main(root: str):
    (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        right_cones,
        left_cones,
    ) = load_cones_csv(root)
    # find the center line
    center = (right_cones + left_cones) / 2
    # find the width
    width = np.array(
        [
            np.linalg.norm(right_cones - center, axis=1),
            np.linalg.norm(left_cones - center, axis=1),
        ]
    ).T
    if root == "Acceleration/":
        center = np.vstack((np.zeros(2), center[:-1]))
        width = np.vstack((1.75 * np.ones(2), width[:-1]))
    # else:
    #     center = np.vstack((center[0] / 2, center))
    #     center = np.vstack((np.zeros(2), center))
    #     width = np.vstack((1.70 * np.ones((2, 2)), width))

    print("max width: ", np.max(width))
    print("min width: ", np.min(width))

    # spline interpolate the center line
    x_coeff, y_coeff, M, normvecs = tph.calc_splines(
        path=center,
        closed=root not in {"Acceleration/", "Skidpad/"},
        psi_s=np.pi / 2,
        psi_e=np.pi / 2,
    )
    phi_init = tph.calc_head_curv_an(x_coeff, y_coeff, np.array([0]), np.array([0.0]))[
        0
    ][0]
    print("initial heading = ", phi_init)
    X_ppoly, Y_ppoly = tph.create_ppoly(
        x_coeff, y_coeff, periodic=root not in {"Acceleration/", "Skidpad/"}
    )
    center_line = np.array(
        [
            X_ppoly(np.linspace(0, x_coeff.shape[0], 1000)),
            Y_ppoly(np.linspace(0, y_coeff.shape[0], 1000)),
        ]
    ).T
    # plt.figure()
    # plt.subplot(1, 2, 1)
    # plt.plot(center_line[:, 0], "k")
    # plt.subplot(1, 2, 2)
    # plt.plot(center_line[:, 1], "k")
    #
    # plt.figure()
    plt.scatter(blue_cones[:, 0], blue_cones[:, 1], s=7, c="b", marker="^")
    plt.scatter(yellow_cones[:, 0], yellow_cones[:, 1], s=7, c="y", marker="^")
    plt.scatter(
        big_orange_cones[:, 0], big_orange_cones[:, 1], s=15, c="orange", marker="^"
    )
    plt.scatter(
        small_orange_cones[:, 0], small_orange_cones[:, 1], s=7, c="orange", marker="^"
    )
    # plt.plot(center[:, 0], center[:, 1], c="k")
    plt.plot(center_line[:, 0], center_line[:, 1], c="k")
    plt.plot([0], [0], "gx")
    plt.axis("equal")
    plt.show()

    # save the center line and widths to a csv
    np.savetxt(
        root + "center_line.csv",
        np.hstack((center, width)),
        delimiter=",",
        header="x,y,right_width,left_width",
    )
    # load it back in and plot it
    # center, width = import_center_line(root)
    # plt.plot(center[:, 0], center[:, 1], c="k")
    # plt.plot([0], [0], "gx")
    # plt.axis("equal")
    # plt.show()


if __name__ == "__main__":
    # main("Acceleration/")
    # main("FSDScompetition1/")
    # main("FSDScompetition2/")
    # main("FSDScompetition3/")
    main("FSDSdefault/")
