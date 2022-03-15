import numpy as np
from ..geodesic_path import new_geodesic_path

def planned_tour(basis_set, cycle=True):

    class Generator:

        def __init__(self):
            self.index = 1
            self.basis_set = basis_set
            self.cycle = cycle

        def generate(self, current, data):
            if self.cycle:
                current = self.index
                self.index = self.index % self.basis_set.shape[0] + 1
                print(self.basis_set[current - 1])
                return self.basis_set[current - 1]
            else:
                self.index += 1
                if self.index > self.basis_set.shape[1]:
                    return None

    generator = Generator()

    return new_geodesic_path(generator)
