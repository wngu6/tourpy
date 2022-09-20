from .grand_tour import GrandTour
from .generator import Generator
from typing import Callable
import numpy as np


class Tour(object):

    data: np.ndarray
    _proj: np.ndarray
    target: np.ndarray
    cur_dist: float
    geodesic: dict
    generator: Generator

    def __init__(
        self, data: np.ndarray, generator: Generator, start: np.ndarray = None
    ):

        self.generator = generator

        self.data = data

        self._proj = (
            self.generator.tour_path(start, self.data) if start is None else start
        )

        self.target = None

        self.current_dist = 0
        self.target_dist = 0

    def proj(self) -> np.ndarray:
        return self._proj

    def interpolate(self, step_size: float) -> np.ndarray:
        """
        Method : Calculate the interpolated projection matrix.
        """

        self.current_dist += step_size

        # if step_size > 0 and np.isfinite(step_size) and self.cur_dist >= self.target_dist:
        #    self.proj = self.geodesic["interpolate"](1.0)

        if self.current_dist >= self.target_dist:

            self.geodesic = self.generator.tour_path(self.proj(), self.data)

            self.target_dist = self.geodesic["dist"]
            self.target = self.geodesic["Fz"]
            self.current_dist = 0

            if not np.isfinite(step_size):
                self.current_dist = self.target_dist

        # The rewind has reached or surpassed the initial point.
        elif self.current_dist <= 0:
            self.current_dist = 0

        self._proj = self.geodesic["interpolate"](self.current_dist / self.target_dist)

        return self.proj()
