# TODO : Resize data on a scale between -1 and 1

from .animate import Animator
from .scatter import Scatter
from .tour import *
from typing import List
from vispy import scene, app
import pyglet


def create_animation(
    data: np.ndarray, tour: Generator, display, color: str = "black"
) -> None:

    canvas = scene.SceneCanvas(keys="interactive", bgcolor="white")
    canvas.size = (600, 600)
    view = canvas.central_widget.add_view()
    view.camera = scene.cameras.TurntableCamera(fov=0, parent=view.scene)

    animator = Animator(data, display, tour, parent=view.scene)

    timer = app.Timer()
    timer.connect(animator.on_timer)
    timer.start(1 / animator.framerate)
    canvas.events.key_press.connect(animator.on_key_press)
    canvas.events.key_release.connect(animator.on_key_release)

    canvas.show()
    canvas.app.run()


def scatter_plot(
    data: np.ndarray, tour: Generator, labels: List[str] = None, color: str = "gray"
) -> None:

    create_animation(data, tour, Scatter, color=color)
