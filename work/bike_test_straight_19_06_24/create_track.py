from track_database.primitives import line
from track_database.utils import save_center_line, save_cones
import numpy as np

def main():
    yellow_line = line(0.9, 0, 0.9, 48.4, 22)
    blue_line = line(-0.9, 0, -0.9, 48.4, 22)
    center_line = line(0, 0, 0, 48.4, 22)
    big_orange_cones = np.array([[0.9, 48.4], [0.9, 48.4], [-0.9, 48.4], [-0.9, 48.4]])

    save_cones("track_database/data/bike_test_straight_19_06_24/bike_test_straight_19_06_24_cones.csv", blue_line, yellow_line, big_orange_cones, [])
    save_center_line("track_database/data/bike_test_straight_19_06_24/bike_test_straight_19_06_24_center_line.csv", center_line, 0.9 * np.ones_like(center_line))

if __name__ == "__main__":
    main()