import matplotlib.pyplot as plt
from track_database import *

# load freshly generated skidpad ======================================================
# center_line, left_cones, right_cones = skidpad()

# load skidpad from file ===================================================
# center_line, left_cones, right_cones = load_track(
#     "../track_database/data/default_skidpad.csv"
# )

# load default skidpad from file ===================================================
# center_line, left_cones, right_cones = import_default_skidpad()

# load default FS track from file ===================================================
center_line, left_cones, right_cones = import_default_fs_track()

plt.plot(center_line[0, :], center_line[1, :], "r-")
plt.plot(left_cones[0, :], left_cones[1, :], "b+")
plt.plot(right_cones[0, :], right_cones[1, :], "y+")
plt.axis("equal")
plt.show()
