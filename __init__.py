from vispy import scene, app
from .animate import *
import numpy as np

from vispy.util import keys
from vispy.color import ColorArray, Colormap
import pyglet
from datetime import datetime

canvas = scene.SceneCanvas(keys="interactive", bgcolor="white")
canvas.size = (600, 600)
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(fov=0, parent=view.scene)

def on_save(event):
    if event.key == "S" and keys.CONTROL in event.modifiers:
        now = datetime.now()
        filename = now.strftime("%d-%m-%y-%H:%M:%S.png")
        pyglet.image.get_buffer_manager().get_color_buffer().save(filename)

canvas.events.key_press.connect(on_save)

timer = app.Timer()

def scatter(data, c=None, labels=None, draw_boundary=None, tour_path=grand_tour()):

    animate = Animate(data, c=c, labels=labels, parent=view.scene, draw_boundary=draw_boundary, tour_path=tour_path)
    timer.connect(animate.on_timer)
    timer.start(1 / animate.framerate)
    canvas.events.key_press.connect(animate.on_key_press)
    canvas.events.key_release.connect(animate.on_key_release)
    canvas.events.mouse_press.connect(animate.on_mouse_press)

    canvas.show()
    canvas.app.run()

def get_projection(f):
    proj = np.genfromtxt(f, delimiter=",")
    initial = np.eye(proj.shape[0], M=3)
    return np.stack((initial, proj))
