from track_database.primitives import line
from track_database.utils import save_center_line, save_cones
import numpy as np

def main():
    yellow_line = line(1.5, 0., 1.5, 30., 11, True)
    blue_line = line(-1.5, 0., -1.5, 30., 11, True)
    center_line = line(0., 0., 0., 30., 11, True)

    save_cones("bike_test_straight_3m_cones.csv", blue_line, yellow_line, [], [])
    save_center_line("bike_test_straight_3m_center_line.csv", center_line, 1.5 * np.ones_like(center_line))


if __name__ == "__main__":
    main()



