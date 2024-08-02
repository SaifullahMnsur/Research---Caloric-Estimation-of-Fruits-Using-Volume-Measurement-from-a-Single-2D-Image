import numpy as np
from scipy.integrate import quad
import utils.plot as uplt


class Estimator:
    
    
    def __init__(self, density, ppcm, cphg):
        # coordinates:
        # top
        self.x1 = 0
        self.y1 = 0
        # bottom
        self.x2 = 0
        self.y2 = 0
        # center
        self.center = 0
        
        # calculation detailes
        self.density = density
        self.ppqcm = ppcm ** 3
        self.cphg = cphg
        
        # estimation results
        self._volume = None
        self._weight = None
        self._calorie = None    

    def update(self, x1, y1, x2, y2, center):
        self.x1, self.y1, self.x2, self.y2, self.center = x1, y1, x2, y2, center

    def f(self, y):
        if self.y1 == self.y2:  # Avoid division by zero
            return abs(self.x1 - self.center)
        x = self.x1 + (y - self.y1) * (self.x2 - self.x1) / (self.y2 - self.y1)
        return abs(x - self.center)

    def integrand(self, y):
        return self.f(y) ** 2

    def get_volume(self, x1, y1, x2, y2, center):
        self.update(x1, y1, x2, y2, center)
        volume, err = quad(self.integrand, min(y1, y2), max(y1, y2))
        volume *= np.pi
        return volume

    def calc_volume(self, x, y, center):
        volume, error = 0, 0
        ln = len(x)
        for i in range(1, ln):
            new_volume = self.get_volume(x[i - 1], y[i - 1], x[i], y[i], center)
            volume += new_volume
        return volume

    def estimate(self, x: list[int], y: list[int], object_fov, save_dir):
        # get the center point of the object in x axis
        # #with perpendicular to this the object will revolve around the y-axis to produce volume
        x_max, x_min = max(x), min(x)
        x_mid = (x_max + x_min) // 2

        sum_volume = (self.calc_volume(x, y, x_mid) // 2)

        # volume is measured for both left and right half's revolution, get the mean
        volume = (sum_volume / self.ppqcm) / (np.cos(np.radians(object_fov / 2)) ** 2)

        self._volume = volume
        self._weight = self._volume * self.density
        self._calorie = self.weight * self.cphg

        uplt.plot_segments( x, y, self._volume, self._weight, self._calorie, save_dir)
        return
    
    
    # properties here

    @property
    def volume(self):
        if self._volume is None:
            raise ValueError("volume is not initialized. Call 'estimate' method first")
        return self._volume
    @property
    def weight(self):
        if self._weight is None:
            raise ValueError("weight is not initialized. Call 'estimate' method first")
        return self._weight
    @property
    def calorie(self):
        if self._calorie is None:
            raise ValueError("calorie is not initialized. Call 'estimate' method first")
        return self._calorie
    