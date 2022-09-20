from generator import Generator
from typing import List
import numpy as np
from itertools import combinations


class LittleTour(Generator):
    little: List
    step: int = 0

    def generate(self, current, data):
        if self.little is None:
            self.little = self.basis_little(data.shape[1], d)
        ans = self.little[self.step]
        self.step = self.step % (len(self.little) - 1) + 1
        return ans

    @staticmethod
    def basis_little(p: int, d: int = 3):
        b = np.eye(p)
        vars = np.array(list(combinations(np.arange(p), 3)))
        return [b[vars[i, :], :].T for i in range(vars.shape[0])]
