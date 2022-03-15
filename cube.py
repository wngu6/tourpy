"""
Author: Schloerke
"""
import numpy as np
from scipy.spatial import ConvexHull

def get_wires(p = 3):
    vertices = np.arange(0, 2**p)
    frm = np.repeat(vertices, p)
    edges = 2**np.arange(0, p).reshape(1,-1)
    edges = np.repeat(edges, 2**p, axis=0).flatten()
    to = np.bitwise_xor(frm, edges)
    wires = np.dstack((frm, to)).squeeze()
    ind = np.argwhere(frm < to).reshape(-1,)
    wires = wires[ind]
    return wires

def get_vertices(p = 3):
    init = np.array([-1, 1])
    res = tuple([init for i in range(p)])
    res = np.array(np.meshgrid(*res))
    return res.reshape(p, 2**p).T

"""
Author: William
"""
def cube(p = 4):
    wire = get_wires(p = p)
    vert = get_vertices(p = p)
    frame = np.zeros(shape=(2*len(wire), p))
    for i in range(len(wire)):
        j = wire[i,0]
        k = wire[i,1]
        frame[2*i] = vert[j]
        frame[2*i+1] = vert[k]

    return frame

def get_hull(verts, wires):
    hull = ConvexHull(verts)
    ind = np.in1d(wires, hull.vertices).reshape(-1,2)
    ind = np.all(ind, axis=1)
    hull_wires = wires[ind]
    frame = np.zeros(shape=(2*len(hull_wires), 3))
    for i in range(len(hull_wires)):
        j = hull_wires[i,0]
        k = hull_wires[i,1]
        frame[2*i] = verts[j]
        frame[2*i+1] = verts[k]
    return frame

def get_hypercube(verts, wires):
    frame = np.zeros(shape=(2*len(wires), 3))
    for i in range(len(wires)):
        j = wires[i,0]
        k = wires[i,1]
        frame[2*i] = verts[j]
        frame[2*i+1] = verts[k]
    return frame
