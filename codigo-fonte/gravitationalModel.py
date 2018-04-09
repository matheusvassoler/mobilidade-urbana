import numpy as np
from scipy.optimize import curve_fit

def func(X, K, s):
    pi = X[0]
    pj = X[1]
    dij = X[2]
    return (K*pi*pj)/(pow(dij,s))

pi = np.linspace(0, 4, 50)
pj = np.linspace(10, 14, 50)
dij = np.linspace(100, 654, 50)
F = func([pi,pj,dij], 2.2, 1.5)

F_noise = 0.2 * np.random.normal(size=pi.size)
F = F + F_noise
np.random.seed(179)


K, s = curve_fit(func, [pi, pj, dij], F)
print(K)


# popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))
# print(popt)

