import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import pandas as pd

data = np.loadtxt("bruh.csv", delimiter=",", skiprows=1)
n = data.shape[0]
left = data[: n // 2, :].T
left = np.concatenate((left, left[:, 0].reshape(2, 1)), axis=1)
left[1,:] = left[1,:]*10.0 
right = data[n // 2 :, :].T
right = np.concatenate((right, right[:, 0].reshape(2, 1)), axis=1)
right[1,:]  = right[1,:]*10.0
center = (left + right) / 2

x = CubicSpline(
    np.linspace(0.0, 1.0, center.shape[1]), center[0, :], bc_type="periodic"
)
y = CubicSpline(
    np.linspace(0.0, 1.0, center.shape[1]), center[1, :], bc_type="periodic"
)

plt.plot(left[0, :], left[1, :], "b-+")
plt.plot(right[0, :], right[1, :], "y-+")
plt.plot(
    x(np.linspace(0.0, 1.0, 3 * center.shape[1])),
    y(np.linspace(0.0, 1.0, 3 * center.shape[1])),
    "g-",
)
plt.show()


df = pd.DataFrame(
    np.concatenate((left, right, center), axis=0).T,
    columns=["X_left", "Y_left", "X_right", "Y_right", "X_center", "Y_center"],
)
df.to_csv("fs_track.csv", index=False)
