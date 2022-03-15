from sklearn import preprocessing
import numpy as np

def orthonormalise(mat):
    mat = preprocessing.normalize(mat, norm="l2", axis=0)
    for i in range(mat.shape[1]):
        mati = mat[:,i]
        for j in range(i):
            matj = mat[:,j]
            mati -= mati.dot(matj) * matj
    return preprocessing.normalize(mat, norm="l2", axis=0)

def orthonormalise_by(x, y):
    x = preprocessing.normalize(x, norm="l2", axis=0)
    for i in range(x.shape[1]):
        x[:,i] = x[:,i] - np.inner(x[:,i], y[:,i]) * y[:,i]

    return preprocessing.normalize(x, norm="l2", axis=0)
