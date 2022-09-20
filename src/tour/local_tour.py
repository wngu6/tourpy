from generator import Generator
from geodesic import step_angle, geodesic_info
from grand_tour import basis_random
import numpy as np


class LocalTour(Generator):
    state: bool = True

    def __init__(self, start: np.ndarray, angle: float = np.pi * 0.25):
        self.start = start
        self.angle = angle

    def generate(self, current, data):
        if self.state:
            new_basis = self.start
        else:
            new = basis_random(self.start.shape[0], d=self.start.shape[1])
            dist = np.random.uniform(low=0, high=self.angle)
            new_basis = step_angle(geodesic_info(self.start, new), dist)

        self.state = not self.state

        return new_basis
