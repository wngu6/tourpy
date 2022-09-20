from vispy import scene
from .components import MarkersVisual
from .components import MultipleAxisVisual
from typing import List
from numpy import ndarray


Markers = scene.visuals.create_visual_node(MarkersVisual)
HyperAxis = scene.visuals.create_visual_node(MultipleAxisVisual)


class Scatter(object):
    def __init__(
        self,
        data: ndarray,
        proj: ndarray,
        color=None,
        labels: List[str] = None,
        parent=None,
    ):
        self.markers = Markers(data, color, parent=parent)
        self.hyperaxis = HyperAxis(proj, labels=labels, parent=parent)

    def set_data(self, data: ndarray, proj: ndarray) -> None:
        self.markers.set_data(data)
        self.hyperaxis.set_data(proj)

    def update(self):
        self.markers.update()
        self.hyperaxis.update()
