"""
Contains functions related to the geodesic interpolation.
"""
from .utils import *
import numpy as np
import numpy.linalg as la

def geodesic_path(current, target):
    """
    Get all information required to perform the geodesic interpolation.

    Parameters
    ----------
    current : ndarray
        The initial projection matrix.
    target : ndarray
        The target projection matrix. It must match the dimensions of the initial projection matrix.

    Returns
    -------
    dict:
        A dictionary containing the relevant information to perform the geodesic interpolation.
    """
    geodesic = geodesic_info(current, target)

    def interpolate(pos):
        """

        Parameters
        ----------
        pos : float32
            An angle.
        """
        return step_fraction(geodesic, pos)

    return {
        "interpolate": interpolate,
        "Fa": current,
        "Fz": target,
        "Ba": geodesic["Ba"],
        "Bz": geodesic["Bz"],
        "tau": geodesic["tau"],
        "dist": proj_dist(current, target)
    }

def geodesic_info(Fa, Fz, epsilon = 1e-6):
    """
    Parameters
    ----------
    Fa : array like
        The initial projection matrix.
    Fz : array like
        The target projection matrix. It must match the dimensions of the initial projection matrix.

    Returns
    -------
    dict :
        A dictionary containing the...
    """
    Fa = orthonormalise(Fa)
    Fz = orthonormalise(Fz)

    Va, eig, Vz = la.svd(np.matmul(Fa.transpose(), Fz))
    Va = np.flip(Va, 1)
    eig = np.flip(eig, 0)
    Vz = np.flip(Vz, 1)

    # Compute frames of principle directions
    Ba = np.matmul(Fa, Va)
    Bz = np.matmul(Fz, Vz)

    # Form an orthogonal coordinate transformation
    Ba = orthonormalise(Ba)
    Bz = orthonormalise(Bz)
    Bz = orthonormalise_by(Bz, Ba)

    # Compute and check principal angles
    index = np.argwhere(eig > 1).reshape(-1,)
    eig[index] = 1
    tau = np.arccos(eig)
    Bz[:,index] = Ba[:,index]

    return {"Va": Va, "Ba": Ba, "Bz": Bz, "tau": tau}

def step_fraction(geodesic, fraction):
    """
    Function: Calculate the projection matrix between the initial and target frame.
    ...
    Parameters
    ----------
    geodesic : dictionary, float32
    fraction : float
        A floating point number used to obtain the interpolated projection matrix.

    Returns
    -------
    ndarray :
        An interpolated projection matrix.
    """
    G = geodesic["Ba"] * np.cos(fraction * geodesic["tau"]) + geodesic["Bz"] * np.sin(fraction * geodesic["tau"])

    return orthonormalise(np.matmul(G, geodesic["Va"].T))

def step_angle(interp, angle):
    """
    Interpolate between a pair of projection matrices.

    Parameters
    ----------
    interp : dict
        A dictionary containing...
    angle : float32
        An angle in radians.
    """
    return step_fraction(interp, angle / np.sqrt(np.sum(interp["tau"] ** 2)))

def proj_dist(x, y):
    """
    Calculate the distance between projection matrix x and y.

    Parameters
    ----------
    x : ndarray
        Any projection matrix.
    y : ndarray
        Any projection matrix.

    Returns
    -------
    float32 :
        A distance.
    """
    return np.sqrt(np.sum((np.matmul(x, x.T) - np.matmul(y, y.T)) ** 2))
