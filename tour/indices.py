import numpy as np

def holes():

    def function(mat):
        num = 1 - 1 / mat.shape[0] * np.sum(np.exp(-0.5 * np.sum(mat ** 2, axis=1)))
        den = 1 - np.exp(-mat.shape[1] / 2)

        return num / den

    return function

def cmass():

    def function(mat):
        num = 1 - 1 / mat.shape[0] * np.sum(np.exp(-0.5 * np.sum(mat ** 2, axis=1)))
        den = 1 - np.exp(-mat.shape[1] / 2)
        return 1 - num / den

    return function
