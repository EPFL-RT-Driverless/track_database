# Copyright (c) Tudor Oancea, EPFL Racing Team Driverless 2022
import matplotlib.pyplot as plt
import numpy as np

from track_database import *
from track_database.utils import *

if __name__ == "__main__":
    for track_name in available_tracks:
        track = load_track(track_name)
        # plt.figure()
        plt.title(track_name)
        plot_cones(
            track.blue_cones,
            track.yellow_cones,
            track.big_orange_cones,
            track.small_orange_cones,
            origin=np.zeros(2),
            show=False,
        )
        plt.tight_layout()
    plt.show()
