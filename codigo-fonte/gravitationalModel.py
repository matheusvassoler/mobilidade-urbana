import numpy as np
from scipy.optimize import curve_fit
from getMatrixData import getMatrixData

def func(X, K, s):
    pi = X[0]
    pj = X[1]
    dij = X[2]
    return (K*pi*pj)/(pow(dij,s))

def calculation():
    #Call the function that contains informations about pi, pj and dij
    #In this case we want the informations about the Sao Jose dos Campos city
    #We want only distance (dij), the matrix has distance and time, so it's passed an argument that specific the getting of the distances
    matrix = getMatrixData('rmrj', 'rj', 'DrivingDistance')

    pi = np.asarray(matrix[0])
    pj = np.asarray(matrix[1])
    dij = np.asarray(matrix[2])

    F = func([pi,pj,dij], 2.2, 1.5)

    F_noise = 0.2 * np.random.normal(size=pi.size)
    F = F + F_noise
    np.random.seed(179)

    K, s = curve_fit(func, [pi, pj, dij], F)
    print(s)

calculation()
