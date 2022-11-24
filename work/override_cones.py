from fsds_to_cones import *


def main():
    root = "FSDSdefault/"
    angle = np.pi / 2 - 1.6856144444524332
    # angle = 0.0
    # offset = np.array([-1.26, 0.0])
    offset = np.zeros(2)
    (
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        right_cones,
        left_cones,
    ) = load_cones_csv(root)
    blue_cones -= offset
    yellow_cones -= offset
    big_orange_cones -= offset
    rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]).T
    blue_cones = np.dot(blue_cones, rot)
    yellow_cones = np.dot(yellow_cones, rot)
    big_orange_cones = np.dot(big_orange_cones, rot)

    write_cones_csv(
        root, blue_cones, yellow_cones, big_orange_cones, small_orange_cones
    )
    plot_cones(
        blue_cones,
        yellow_cones,
        big_orange_cones,
        small_orange_cones,
        np.zeros(2),
        True,
    )


if __name__ == "__main__":
    main()
