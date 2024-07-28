import numpy as np
from scipy.integrate import quad
import utils.plot as uplt


class Estimator:
    def __init__(self, density, ppcm, cphg):
        self.c = 0.0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.center = 0
        self.density = density
        self.ppqcm = ppcm ** 3
        self.cphg = cphg
        self.left_volume = 0
        self.right_volume = 0
        self.final_volume = 0
        self.weight = 0
        self.calorie = 0

    def update(self, x1, y1, x2, y2, center):
        self.x1, self.y1, self.x2, self.y2, self.center = x1, y1, x2, y2, center

    def f(self, y):
        if self.y1 == self.y2:  # Avoid division by zero
            return abs(self.x1 - self.center)
        x = self.x1 + (y - self.y1) * (self.x2 - self.x1) / (self.y2 - self.y1)
        return abs(x - self.center)

    # def f(self, y):
    #     return abs(self.x1 + (y - self.y1) * ((self.x1 - self.x2) * (self.y1 - self.y2)) - self.center)

    def integrand(self, y):
        return self.f(y) ** 2

    def get_volume(self, x1, y1, x2, y2, center):
        self.update(x1, y1, x2, y2, center)
        volume, err = quad(self.integrand, min(y1, y2), max(y1, y2))
        volume *= np.pi
        # print(f"From get_volume ({x1},{y1})->({x2 },{y2}): {volume}, Error: {error}")
        return volume

    def calc_volume(self, x, y, center):
        volume, error = 0, 0
        ln = len(x)
        for i in range(1, ln):
            new_volume = self.get_volume(x[i - 1], y[i - 1], x[i], y[i], center)
            volume += new_volume
        # print(f"From one_side_volume: {volume}, error: {error}")
        return volume

    def estimate(self, x: list[int], y: list[int], angle, save_dir):
        x_max, x_min = max(x), min(x)
        x_mid = (x_max + x_min) // 2

        sum_volume = (self.calc_volume(x, y, x_mid) // 2)

        # average = (left_volume + right_volume) / 2
        final_volume = (sum_volume / self.ppqcm) / (np.cos(np.radians(angle / 2)) ** 2)

        self.final_volume = final_volume
        self.weight = self.final_volume * self.density
        self.calorie = self.weight * self.cphg

        uplt.plot_segments( x, y, self.final_volume, self.weight, self.calorie, save_dir)
        return
