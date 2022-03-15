from vispy import scene
from .markers import MarkersVisual
from .hyperaxis import HyperAxisVisual

Markers = scene.visuals.create_visual_node(MarkersVisual)
HyperAxis = scene.visuals.create_visual_node(HyperAxisVisual)

class Scatter:

    def __init__(self, data, proj, c=None, labels=None, parent=None):
        self.markers = Markers(data, c, parent=parent)
        self.hyperaxis = HyperAxis(proj, labels=labels, parent=parent)

    def set_data(self, data, proj):
        self.markers.set_data(data)
        self.hyperaxis.set_data(proj)

    def update(self):
        self.markers.update()
        self.hyperaxis.update()
