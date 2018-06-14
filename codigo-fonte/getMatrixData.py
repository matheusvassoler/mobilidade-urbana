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

    #get total of regions into the matrix. It's necessary to interate over the matrix that contais the populations of each zone
    nr = dfPopulation.index.values.size

    #print(dfDistanceTime)
    #print(dfPopulation)
    #print(path1)

    #Set i(origin) and j(destination) with 0, because in the matrix, row and column start with 0
    i = 0
    j = 0

    #We need three lists, one to store pi(quantity of people in zone i), other to store pj(quantity of people in zone j)
    #And finally the third list to store dij(distance between i and j)
    pi = []
    pj = []
    dij = []

    while i < nr:
       while j < nr:
           #Verify if i is different of j, because is impossible get data between equal zone (example, distane between i and i)
           if i != j:
               #Using iloc, the data is obtained from dataframe and is added in the list
               pi.append(dfPopulation.iloc[i][1])
               pj.append(dfPopulation.iloc[j][1])
               #In matrix, exist failed mappings, so it's necessary to treat the data, replace X for NaN.
               #This is did using numpy library
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
