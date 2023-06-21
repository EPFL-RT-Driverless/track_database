from track_database.utils import load_cones, plot_cones, load_center_line
from track_database.tracks import load_track
import numpy as np
import matplotlib.pyplot as plt

track = load_track("21_05_2023")
# blue_cones, yellow_cones, big_orange_cones, _, _, _ = load_cones("21_05_2023.csv")
plot_cones(
    track.blue_cones, track.yellow_cones, np.empty((0, 2)), np.empty((0, 2)), show=False
)
# center_line, _ = load_center_line("21_05_2023_center_line.csv")
plt.plot(track.center_line[:, 0], track.center_line[:, 1], "k--")
plt.scatter(track.center_line[:, 0], track.center_line[:, 1], c="k")
plt.show()
