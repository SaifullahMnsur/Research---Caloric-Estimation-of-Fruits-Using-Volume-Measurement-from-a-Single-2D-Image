import matplotlib.pyplot as plt
import numpy as np

def plot_segments( x: list[int], y: list[int], volume: float, weight: float, calorie: float, path=None) -> None:
    """
    Plots the segmented points to replicate the shape

    Args:
        index (int): index of object found in the image
        x (list[int]): List of segmented points in x-axis
        y (list[int]): List of segmented points in y-axis
        path (str): path of saving the figure

    Returns:
        None
    """

    x_max, x_min = max(x), min(x)
    y_max, y_min = max(y), min(y)
    x_c, y_c = (x_max + x_min) / 2, (y_max + y_min) / 2
    
    max_dist = max(max(x)-min(x), max(y)-min(y)) / 2
    max_dist = max_dist * 1.1

    # np.append(x, x[0])
    # np.append(y, y[0])

    x.append(x[0])
    y.append(y[0])

    # Plotting the closed shape
    plt.figure()
    plt.plot(x, y, linestyle='--', color='b', markerfacecolor='k', markeredgecolor='k')
    plt.fill(x, y, alpha=0.3)  # Fill the shape
    plt.title(f'Apple Segmentation\nVolume: {volume:.2f} cm^3 - Weight: {weight:.2f} gm - Calories: {calorie:.2f} kcal')

    plt.xlim(x_c - max_dist, x_c + max_dist)
    plt.ylim(y_c - max_dist, y_c + max_dist)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()
    plt.grid(True)
    if path is not None:
        plt.savefig(f"{path}\\apple_graph.png")
    plt.show()
    plt.close()