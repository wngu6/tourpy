import numpy as np
from .grand_tour import basis_random
from ..geodesic import *
from ..geodesic_path import new_geodesic_path

def local_tour(start, angle = np.pi / 4):

    class Generator:

        def __init__(self):
            self.state = True

        def generate(self, current, data):
            if self.state:
                new_basis = start
            else:
                new = basis_random(start.shape[0], d=start.shape[1])
                dist = np.random.uniform(low=0, high=angle)
                new_basis = step_angle(geodesic_info(start, new), dist)

            self.state = not self.state

            return new_basis

    generator = Generator()

    return new_geodesic_path(generator)
