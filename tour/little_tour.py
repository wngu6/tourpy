from ..geodesic_path import new_geodesic_path
import numpy as np
from itertools import combinations

def little_tour(d = 3):

    class Generator:

        def __init__(self):
            self.little = None
            self.step = 0

        def generate(self, current, data):
            if self.little is None:
                self.little = basis_little(data.shape[1], d)
            ans = self.little[self.step]
            self.step = self.step % (len(self.little) - 1) + 1
            return ans

    generator = Generator()

    return new_geodesic_path(generator)

def basis_little(p, d = 3):

    b = np.eye(p)
    vars = np.array(list(combinations(np.arange(p),3)))

    return [b[vars[i,:],:].T for i in range(vars.shape[0])]
