from .tour import *
from .scatter import Scatter
from .cube import *
from vispy.scene.visuals import Line
import csv

import numpy as np

from sklearn.preprocessing import MinMaxScaler
from scipy.spatial import ConvexHull

class Animate:

    def __init__(self, data, c=None, labels=None, display=Scatter, tour_path=grand_tour(), start=None, parent=None, draw_boundary=None):
        self.curr_aps = 0
        self.base_aps = 1
        self.framerate = 144
        self.draw_boundary = draw_boundary
        self.scale = 1000

        self.s = MinMaxScaler(feature_range=(-1, 1))

        self.tour = Tour(data, tour_path, start)
        self.step = self.tour.proj * self.scale
        self.data = self.s.fit_transform(data)
        self.mat = np.matmul(self.data, self.step, dtype=np.float32)

        self.display = Scatter(self.mat, self.step, c=c, labels=labels, parent=parent)
        self.wires = get_wires(p=data.shape[1])
        self.vertices = get_vertices(p=data.shape[1])
        self.res = np.matmul(self.vertices, self.step, dtype=np.float32)
        if self.draw_boundary == "hull":
            self.hull_frame = get_hull(self.res, self.wires)
            self.frame = Line(pos=self.hull_frame, method="gl", connect="segments", parent=parent, color="black")
        elif self.draw_boundary == "wire":
            res = get_hypercube(self.res, self.wires)
            self.frame = Line(pos=res, method="gl", connect="segments", parent=parent, color="black")

    def on_timer(self, event):

        if self.curr_aps != 0:
            self.step = self.tour.interpolate(self.curr_aps / self.framerate) * self.scale
            self.mat = np.matmul(self.data, self.step, dtype=np.float32)
            self.display.set_data(self.mat, self.step)
            self.display.update()

            if self.draw_boundary == "hull":
                self.res = np.matmul(self.vertices, self.step, dtype=np.float32)
                self.hull_frame = get_hull(self.res, self.wires)
                self.frame.set_data(pos=self.hull_frame, connect="segments", color="black")
            elif self.draw_boundary == "wire":
                self.res = np.matmul(self.vertices, self.step, dtype=np.float32)
                res = get_hypercube(self.res, self.wires)
                self.frame.set_data(pos=res, connect="segments", color="black")

    def on_key_press(self, event):
        if event.key == "=": self.curr_aps = self.base_aps
        if event.key == "-": self.curr_aps = -self.base_aps

        if event.key == "F8":
            print(self.step / self.scale)
            np.savetxt("matrix.csv", self.step / self.scale, delimiter=",")
            print("Projection saved to: matrix.csv")

    def on_key_release(self, event):
        if event.key == "-" or event.key == "=": self.curr_aps = 0

    def on_mouse_press(self, event):
        # print(event.pos)
        pass
