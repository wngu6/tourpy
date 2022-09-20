import numpy as np
from vispy.gloo import VertexBuffer
from vispy.visuals import Visual
from vispy.visuals.shaders import Function

vert = """
#version 120
uniform float u_antialias;
uniform float u_px_scale;
uniform float u_scale;
attribute vec3 a_position;
attribute vec4 a_color;
attribute float a_size;
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;
void main() {
    v_size = a_size * u_px_scale * u_scale;
    v_linewidth = .0 * float(u_px_scale);
    v_antialias = .25;
    v_fg_color = vec4(a_color.rgba);
    v_bg_color = vec4(a_color.rgba);
    gl_Position = $transform(vec4(a_position, 1.0));
    gl_PointSize = v_size + 4.0 * (v_linewidth + 1.5 * v_antialias);
}
"""

frag = """
#version 120
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;
void main ()
{
    if (v_size <= 0.) discard;
    float size = v_size + 4.0 * (v_linewidth + 1.5 * v_antialias);
    float t = 0.5 * v_linewidth - v_antialias;
    float radius = $marker(gl_PointCoord, size);
    float dist = abs(radius) - t;
    vec4 edgecolor = vec4(v_fg_color.rgb, v_linewidth*v_fg_color.a);
    if (radius > 0.5 * v_linewidth + v_antialias) {
        discard;
    }
    else if (dist < 0.0) {
        gl_FragColor = vec4(v_fg_color.rgb, 0.5 * v_fg_color.a);
    }
    else
    {
        if (v_linewidth == 0.) {
            if (radius > -v_antialias) {
                float alpha = 1.0 + radius / v_antialias;
                alpha = exp(-alpha*alpha);
                gl_FragColor = vec4(v_bg_color.rgb, alpha*v_bg_color.a);
            } else {
                gl_FragColor = v_bg_color;
            }
        } else {
            float alpha = dist / v_antialias;
            alpha = exp(-alpha * alpha);
            if (radius > 0) {
                gl_FragColor = vec4(edgecolor.rgb, alpha * edgecolor.a);
            } else {
                gl_FragColor = mix(v_bg_color, edgecolor, alpha);
            }
        }
    }
}
"""

disc = """
float disc(vec2 pointcoord, float size) {
    float radius = length((pointcoord.xy - vec2(.5, .5)) * size);
    radius -= $v_size / 2.;
    return radius;
}
"""

_marker_dict = {"disc": disc}


class MarkersVisual(Visual):
    def __init__(self, data, color, symbol: str = "disc", size: int = 3):
        Visual.__init__(self, vert, frag)

        self.size = size
        self.symbol = symbol

        self.shared_program["a_position"] = np.float32(data)
        self.shared_program["a_size"] = np.repeat(self.size, data.shape[0]).astype(
            np.float32
        )
        self.shared_program["a_color"] = VertexBuffer(color.rgba)
        self._draw_mode = "points"

    def set_data(self, data):
        self.shared_program["a_position"] = np.float32(data)

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._marker_fun = Function(_marker_dict[symbol])
        self._marker_fun["v_size"] = self.size
        self.shared_program.frag["marker"] = self._marker_fun
        self.update()

    def _prepare_draw(self, view):
        self.set_gl_state(
            depth_test=True, blend_func=("src_alpha", "one_minus_src_alpha")
        )
        view.view_program["u_px_scale"] = view.transforms.pixel_scale
        view.view_program["u_scale"] = 1

    def _prepare_transforms(self, view):
        view.view_program.vert["transform"] = view.transforms.get_transform()
