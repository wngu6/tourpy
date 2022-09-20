import numpy as np


def holes(mat: np.ndarray) -> float:
    num = 1 - 1 / mat.shape[0] * np.sum(np.exp(-0.5 * np.sum(mat**2, axis=1)))
    den = 1 - np.exp(-mat.shape[1] / 2)
    return num / den


def cmass(mat: np.ndarray) -> float:
    num = 1 - 1 / mat.shape[0] * np.sum(np.exp(-0.5 * np.sum(mat**2, axis=1)))
    den = 1 - np.exp(-mat.shape[1] / 2)
    return 1 - num / den
