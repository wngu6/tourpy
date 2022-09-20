from .geodesic import geodesic_path, proj_dist, Interpolation
from numpy import ndarray


class Generator(object):
    def generate(self) -> None:
        raise NotImplementedError

    def tour_path(self, current: ndarray, data: ndarray) -> Interpolation:

        if current is None:
            return self.generate(None, data)

        dist = 0
        tries = 0

        while dist < 1e-3:
            target = self.generate(current, data)

            if target is None:
                return None

            tries += 1
            if tries > 10:
                return None

            dist = proj_dist(current, target)

        return geodesic_path(current, target)
