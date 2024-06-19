from track_database.utils import load_cones, plot_cones, load_center_line
from track_database.tracks import load_track
import numpy as np
import matplotlib.pyplot as plt

track = load_track("bike_test_straight_19_06_24")
plot_cones(
    track.blue_cones, track.yellow_cones, np.empty((0, 2)), np.empty((0, 2)), show=False
)
plt.plot(track.center_line[:, 0], track.center_line[:, 1], "k--")
plt.scatter(track.center_line[:, 0], track.center_line[:, 1], c="k")
plt.show()