import numpy as np
from scipy.optimize import curve_fit
from getMatrixData import getMatrixData

def func(X, K, s):
    pi = X[0]
    pj = X[1]
    dij = X[2]
    return (K*pi*pj)/(pow(dij,s))

def calculation(resultQuantity):
    #Call the function that contains informations about pi, pj and dij
    #In this case we want the informations about the Sao Jose dos Campos city
    #We want only distance (dij), the matrix has distance and time, so it's passed an argument that specific the getting of the distances
    matrix = getMatrixData('sjc', 'sp', 'DrivingDistance', 'Driving')

    pi = np.asarray(matrix[0])
    pj = np.asarray(matrix[1])
    dij = np.asarray(matrix[2])
    F = np.asarray(matrix[3])

    for idx,val in enumerate(pi):
        print("[%d] pi: %d -- pj: %d -- dij: %d -- F: %d" %(idx,pi[idx],pj[idx], dij[idx], F[idx]))

    KEstimation = np.random.uniform(10e-7, 10e-2, resultQuantity)
    sEstimation = np.random.uniform(0.1, 0.4, resultQuantity)

    #Variable that contains all the values of the K got by curve_fit
    KList = []

    #Variable that contains all the values of the s got by curve fit
    sList = []


    for i in range(resultQuantity):
        p0 = [KEstimation[i], sEstimation[i]]

        K,s = curve_fit(func, [pi, pj, dij], F, p0=p0)

        KList.append(K.tolist())
        sList.append(s.tolist())


    print(KList)
    print(sList)
    print(len(KList))
    print(len(sList))
    print(KEstimation)
    print(sEstimation)

calculation(1000)
