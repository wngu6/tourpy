from generator import Generator
from grand_tour import basis_init, basis_random
import numpy as np


class DependenceTour(Generator):
    def __init__(self, pos: np.ndarray):
        self.d = np.amax(pos) + 1
        self.pos = pos

    def generate(self, current: np.ndarray, data: np.ndarray):
        if current is None:
            return basis_init(data.shape[1], self.d)

        mat = np.zeros(shape=(len(self.pos), self.d))
        for i in range(d):
            a = basis_random(np.sum(pos == i), d=1).reshape(
                -1,
            )
            mat[self.pos == i, i] = a

        return mat
