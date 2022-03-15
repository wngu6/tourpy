"""
A visual class containing multiple axes.
"""

import numpy as np
from vispy.visuals import CompoundVisual, LineVisual, TextVisual

class HyperAxisVisual(CompoundVisual):

    def __init__(self, pos, color="black", labels=None):

        self.pos = np.zeros((pos.shape[0]*2, 3))
        for i in range(pos.shape[0]):
            self.pos[2*i+1] = pos[i]

        self._lines = LineVisual(pos=self.pos, method="gl", color=color, connect="segments", antialias=True)
        self._text = TextVisual(text=labels, color=color, bold=True, italic=True, pos=pos * 1.1, font_size=14, method="gpu")

        CompoundVisual.__init__(self, [self._lines, self._text])

    def set_data(self, pos):
        for i in range(pos.shape[0]):
            self.pos[2*i+1] = pos[i]
        self._lines.set_data(pos=self.pos)
        self._text.pos = pos * 1.1
        self._text.update()
