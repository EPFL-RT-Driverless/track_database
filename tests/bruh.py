import matplotlib.pyplot as plt
from track_database import *

center_line, left_cones, right_cones = skidpad()

plt.plot(center_line[0, :], center_line[1, :], "r+")
plt.plot(left_cones[0, :], left_cones[1, :], "b+")
plt.plot(right_cones[0, :], right_cones[1, :], "y+")
plt.axis("equal")
plt.show()
