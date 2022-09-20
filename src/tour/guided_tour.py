from generator import Generator
from typing import Callable, TypedDict
import numpy as np
from grand_tour import basis_init, basis_random
from geodesic import geodesic_info, step_angle
from scipy import optimize


class Peak(TypedDict):
    basis: float
    index: float
    dist: float


IndexFunction = Callable[[np.ndarray], float]


class GuidedTour(Generator):
    def __init__(
        self,
        index_f: IndexFunction,
        search_f: Callable,
        alpha: float = 0.5,
        d: int = 3,
        cooling: float = 0.99,
        max_tries: int = 25,
        max_i=np.inf,
    ):
        self.index_f = index_f
        self.search_f = search_f
        self.alpha = alpha
        self.d = d
        self.max_i = max_i
        self.max_tries = max_tries
        self.cooling = cooling

    def generate(self, current: np.ndarray, data: np.ndarray):

        index = lambda proj: self.index_f(data @ proj)

        if current is None:
            return basis_init(data.shape[1], self.d)

        self.current_index = index(current)

        if self.current_index > self.max_i:
            return None

        basis = self.search_f(
            current, index, max_tries=self.max_tries, current_index=self.current_index
        )

        self.alpha *= cooling

        return basis

    def search_geodesic(
        self, index: Callable, current, n: int = 5, step_size: float = 0.01
    ):

        if self.current_index is None:
            current_index = index(current)

        tries = 0

        while tries < self.max_tries:

            dir = self.find_best_dir(current, index, tries=n, dist=step_size)

            peak = self.find_path_peak(current, dir, index)

            pdiff = (peak["index"] - current_index) / current_index

            if pdiff > 0.001:
                return peak["basis"]

            tries += 1

        return None

    @staticmethod
    def find_best_dir(
        old: np.ndarray, index: IndexFunction, dist: float = 0.01, tries: int = 5
    ):
        bases = [basis_random(*old.shape) for i in range(tries)]

        def score(new: np.ndarray) -> float:
            interpolator = geodesic_info(old, new)
            forward = step_angle(interpolator, dist)
            backward = step_angle(interpolator, -dist)

            return max(index(forward), index(backward))

        scores = [score(item) for item in bases]

        return bases[np.argmax(scores)]

    @staticmethod
    def find_path_peak(
        old: np.ndarray,
        new: np.ndarray,
        index: Callable,
        max_dist: float = np.pi * 0.25,
    ) -> Peak:
        interpolator = geodesic_info(old, new)

        index_pos = lambda alpha: -index(step_angle(interpolator, alpha))

        alpha = optimize.minimize_scalar(
            index_pos, bracket=(-max_dist, max_dist), tol=0.01, method="brent"
        )

        return {
            "basis": step_angle(interpolator, alpha["x"]),
            "index": -alpha["fun"],
            "dist": abs(alpha["x"]),
        }
