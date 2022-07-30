import numpy as np


def line(
    x_1: float,
    y_1: float,
    x_2: float,
    y_2: float,
    number_points: int,
    endpoint: bool = True,
    startpoint: bool = True,
) -> np.ndarray:
    """
    Generates a line between two points.
    :param x_1: x coordinate of the first point.
    :param y_1: y coordinate of the first point.
    :param x_2: x coordinate of the second point.
    :param y_2: y coordinate of the second point.
    :param number_points: number of points to generate.
    :param endpoint: whether to include the endpoints in the line.
    :param startpoint: whether to include the startpoints in the line.
    :return: x and y coordinates of the line.
    """
    assert startpoint or endpoint
    assert number_points > 0

    if not startpoint:
        x_line = np.linspace(x_2, x_1, number_points, endpoint=startpoint)[::-1]
        y_line = np.linspace(y_2, y_1, number_points, endpoint=startpoint)[::-1]

    else:
        x_line = np.linspace(x_1, x_2, number_points, endpoint=endpoint)
        y_line = np.linspace(y_1, y_2, number_points, endpoint=endpoint)

    x_line = x_line.reshape(1, -1)
    y_line = y_line.reshape(1, -1)
    return np.concatenate((x_line, y_line), axis=0)


def circle(
    x_center: float,
    y_center: float,
    radius: float,
    number_points: int,
    trigonometric_sense: bool = True,
    endpoint: bool = True,
) -> np.ndarray:
    """
    Generates a circle.
    :param x_center: x coordinate of the center.
    :param y_center: y coordinate of the center.
    :param radius: radius of the circle.
    :param number_points: number of points to generate.
    :param trigonometric_sense: if True, the circle is generated in the trigonometric sense.
    :param endpoint: whether to include the endpoints in the circle.
    :return: x and y coordinates of the circle.
    """
    assert radius > 0.0
    if trigonometric_sense:
        theta = np.linspace(0, 2 * np.pi, number_points, endpoint=endpoint)
    else:
        theta = np.linspace(2 * np.pi, 0, number_points, endpoint=endpoint)
    x_circle = x_center + radius * np.cos(theta)
    y_circle = y_center + radius * np.sin(theta)
    return np.concatenate((x_circle.reshape(1, -1), y_circle.reshape(1, -1)), axis=0)
