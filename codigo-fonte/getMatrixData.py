import pandas as pd
import numpy as np
#import gravitationalModel

#This function gets the total of population and distance from each zone

def getMatrixData(city, state, sheet_name):

    #Reads the matrix that contain distances and time
    path1 = "./Matrix/"+"Matrix_"+city+"_"+state+".xlsx"
    dfDistanceTime = pd.read_excel(path1, sheet_name=sheet_name)

    #Reads the matrix that contain the population
    path2 = "./SJC_RMRJ_data/"+city.upper()+"_population.xlsx"
    dfPopulation = pd.read_excel(path2)

    #get total of regions into the matrix
    nr = dfPopulation.index.values.size

    #print(dfDistanceTime)
    #print(dfPopulation)
    #print(path1)

    i = 0
    j = 0
    pi = []
    pj = []
    dij = []

    while i < nr:
       while j < nr:
           if i != j:
               #print('{} {}'.format(i, j))
               pi.append(dfPopulation.iloc[i][1])
               pj.append(dfPopulation.iloc[j][1])
               if(dfDistanceTime.iloc[i][j] == 'X'):
                   dfDistanceTime.replace('X', np.NaN)
               else:
                   distance = float(dfDistanceTime.iloc[i][j].rstrip('km')) * 1000
               dij.append(distance)
           j += 1
       j = i + 1
       i += 1

    #print(pi)
    #print(pj)
    #print(dij)
    #print(dfDistanceTime)
    return [pi, pj, dij]


#getMatrixData('rmrj', 'rj', 'DrivingDistance')
