from track_database.utils import load_cones, plot_cones, load_center_line
import numpy as np
import matplotlib.pyplot as plt

blue_cones, yellow_cones, big_orange_cones, _, _, _ = load_cones("21_05_2023_cones.csv")
plot_cones(blue_cones, yellow_cones, np.empty((0, 2)), np.empty((0, 2)), show=False)
center_line, _ = load_center_line("21_05_2023_center_line.csv")
plt.plot(center_line[:, 0], center_line[:, 1], "k--")
plt.scatter(center_line[:, 0], center_line[:, 1], c="k")
plt.show()
