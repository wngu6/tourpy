from .generator import Generator
from .utils import orthonormalise

import numpy as np


def basis_random(n: int, d: int = 3) -> np.ndarray:
    return orthonormalise(np.random.normal(size=(n, d)))


def basis_init(n: int, d: int) -> np.ndarray:
    mat = np.zeros(shape=(n, d))
    for i in range(d):
        mat[i, i] = 1
    return mat


class GrandTour(Generator):
    d: int

    def __init__(self, d: int = 3):
        self.d = d

    def generate(self, current, data):
        return (
            basis_init(data.shape[1], self.d)
            if current is None
            else basis_random(data.shape[1], self.d)
        )
