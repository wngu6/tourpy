from .grand_tour import basis_init, basis_random
from ..geodesic import geodesic_info, step_angle
from ..geodesic_path import new_geodesic_path
import numpy as np
from scipy import optimize
import time

def search_geodesic(current, index, max_tries = 25, n = 5, step_size = 0.01, cur_index = None):
    """
    Parameters
    ----------
    current : ndarray
        The current projection matrix.
    index : function
        An index function.
    max_tries : int
        The maximum number of trials before aborting.
    n : int
        Number of random steps to take to find best direction.
    step_size : float
        The step size for evaluation for best direction.
    """

    if cur_index is None: cur_index = index(current)

    tries = 0

    while tries < max_tries:

        dir = find_best_dir(current, index, tries = n, dist=step_size)

        peak = find_path_peak(current, dir, index)
        print(peak["index"])

        pdiff = (peak["index"] - cur_index) / cur_index

        if pdiff > 0.001:
            return peak["basis"]

        tries += 1

    print("Final projection:\n")
    print(current)
    return None

def find_best_dir(old, index, dist = 0.01, tries = 5):
    bases = [basis_random(*old.shape) for i in range(tries)]

    def score(new):
        interpolator = geodesic_info(old, new)
        forward = step_angle(interpolator, dist)
        backward = step_angle(interpolator, -dist)

        return max(index(forward), index(backward))

    scores = [score(item) for item in bases]

    return bases[np.argmax(scores)]

def find_path_peak(old, new, index, max_dist = np.pi / 4):
    interpolator = geodesic_info(old, new)

    def index_pos(alpha):
        # Scipy only has minimizations, hence the negative sign.
        return -index(step_angle(interpolator, alpha))

    alpha = optimize.minimize_scalar(index_pos, bracket=(-max_dist, max_dist), tol=0.01, method="brent")

    return {
        "basis" : step_angle(interpolator, alpha["x"]),
        "index" : -alpha["fun"],
        "dist"  : abs(alpha["x"])
    }

def guided_tour(index_f, d = 3, alpha = 0.5, cooling = 0.99, max_tries = 25, max_i = np.inf, search_f=search_geodesic):

    class Generator:

        def __init__(self, index_f, search_f, alpha):
            self.index_f = index_f
            self.search_f = search_f
            self.alpha = alpha

        def generate(self, current, data):

            def index(proj):
                return self.index_f(np.matmul(data, proj, dtype=np.float32))

            if current is None: return basis_init(data.shape[1], d)

            self.cur_index = index(current)

            if self.cur_index > max_i:
                return None

            basis = self.search_f(current, index, max_tries = max_tries, cur_index = self.cur_index)
            self.alpha *= cooling

            return basis

    generator = Generator(index_f, search_f, alpha)

    return new_geodesic_path(generator)
