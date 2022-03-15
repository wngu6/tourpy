from .grand_tour import basis_init, basis_random
from ..geodesic_path import new_geodesic_path
import numpy as np

def dependence_tour(pos):

    pos = np.array(pos)

    d = np.amax(pos) + 1

    class Generator:

        def generate(self, current, data):
            if current is None: return basis_init(data.shape[1], d)

            mat = np.zeros((len(pos), d))
            for i in range(d):
                a = basis_random(np.sum(pos == i), d = 1).reshape(-1,)
                mat[pos == i, i] = a
            
            return mat

    generator = Generator()

    return  new_geodesic_path(generator)
