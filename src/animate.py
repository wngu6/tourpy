import time
import numpy as np
from typing import List

from .tour import GrandTour, Tour, Generator
from vispy.color import ColorArray


class Animator(object):

    current_aps: float = 0.0
    base_aps: float = 1.0
    framerate: int = 144

    def __init__(
        self,
        data: np.ndarray,
        display,
        tour: Generator,
        color: str = None,
        labels: List[str] = None,
        parent=None,
    ):
        print(tour)
        self.data = data
        self.generator = tour()
        self.tour = Tour(data, self.generator)
        self.step = self.tour.proj()
        self.mat = self.data @ self.step

        self.display = display(
            self.mat,
            self.step,
            color=ColorArray(["blue" for _ in range(data.shape[0])]),
            parent=parent,
        )

    def on_timer(self, event):

        if self.current_aps != 0:
            self.step = self.tour.interpolate(self.current_aps / self.framerate)
            self.mat = self.data @ self.step
            self.display.set_data(self.mat, self.step)
            self.display.update()

    def on_key_press(self, event):
        if event.key == "=":
            self.current_aps = self.base_aps
        if event.key == "-":
            self.current_aps = -self.base_aps

    def on_key_release(self, event):
        if event.key == "-" or event.key == "=":
            self.current_aps = 0
