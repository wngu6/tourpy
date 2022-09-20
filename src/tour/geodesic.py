"""
Contains functions related to the geodesic interpolation.
"""
from .utils import *
import numpy as np
import numpy.linalg as la
from typing import TypedDict, Callable


class Geodesic(TypedDict):
    Va: np.ndarray
    Ba: np.ndarray
    Bz: np.ndarray
    tau: np.float32


class Interpolation(TypedDict):
    interpolate: Callable
    Fa: np.ndarray
    Fz: np.ndarray
    Ba: np.ndarray
    Bz: np.ndarray
    tau: float
    dist: float


# Get all information required to perform the geodesic interpolation.
def geodesic_path(current: np.ndarray, target: np.ndarray) -> Interpolation:

    geodesic = geodesic_info(current, target)

    return {
        "interpolate": lambda pos: step_fraction(geodesic, pos),
        "Fa": current,
        "Fz": target,
        "Ba": geodesic["Ba"],
        "Bz": geodesic["Bz"],
        "tau": geodesic["tau"],
        "dist": proj_dist(current, target),
    }


def geodesic_info(Fa: np.ndarray, Fz: np.ndarray, epsilon: float = 1e-6) -> Geodesic:

    Fa = orthonormalise(Fa)
    Fz = orthonormalise(Fz)

    Va, eig, Vz = la.svd(Fa.T @ Fz)
    Va = np.flip(Va, 1)
    eig = np.flip(eig, 0)
    Vz = np.flip(Vz, 1)

    # Compute frames of principle directions
    Ba = Fa @ Va
    Bz = Fz @ Vz

    # Form an orthogonal coordinate transformation
    Ba = orthonormalise(Ba)
    Bz = orthonormalise(Bz)
    Bz = orthonormalise_by(Bz, Ba)

    # Compute and check principal angles
    index = np.argwhere(eig > 1).reshape(
        -1,
    )
    eig[index] = 1
    tau = np.arccos(eig)
    Bz[:, index] = Ba[:, index]

    return {"Va": Va, "Ba": Ba, "Bz": Bz, "tau": tau}


def step_fraction(geodesic: Geodesic, fraction: float) -> np.ndarray:
    # Function: Calculate the projection matrix between the initial and target frame.

    G = geodesic["Ba"] * np.cos(fraction * geodesic["tau"]) + geodesic["Bz"] * np.sin(
        fraction * geodesic["tau"]
    )

    return orthonormalise(G @ geodesic["Va"].T)


def step_angle(interp: Interpolation, angle: float) -> float:
    return step_fraction(interp, angle / np.sqrt(np.sum(interp["tau"] ** 2)))


# Calculate the distance between projection matrix x and y.
def proj_dist(x: np.ndarray, y: np.ndarray) -> float:
    return np.sqrt(np.sum((x @ x.T - y @ y.T) ** 2))
