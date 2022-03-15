import numpy as np
from ..utils import orthonormalise
from ..geodesic_path import new_geodesic_path

def grand_tour(d = 3):

    class Generator:

        def generate(self, current, data):
            return basis_init(data.shape[1], d) if current is None else basis_random(data.shape[1], d)

    generator = Generator()

    return new_geodesic_path(generator)

def basis_random(n, d = 3):
    return orthonormalise(np.random.normal(size=(n, d)))

def basis_init(n, d):
    mat = np.zeros(shape=(n, d))
    for i in range(d):
        mat[i,i] = 1
    return mat
