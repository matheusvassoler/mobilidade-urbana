import pandas as pd
import numpy as np
#import gravitationalModel

#This function gets the total of population and distance from each zone

def getMatrixData(city, state, sheet_name, sheet_name2):

    #Reads the matrix that contain distances and time
    path1 = "./Matrix/"+"Matrix_"+city+"_"+state+".xlsx"
    dfDistanceTime = pd.read_excel(path1, sheet_name=sheet_name)
    #print(dfDistanceTime)

    #Reads the matrix that contain the population
    path2 = "./SJC_RMRJ_data/"+city.upper()+"_population.xlsx"
    dfPopulation = pd.read_excel(path2)

    # Reads the matrix that contain the real flow of people between zones
    path3 = "./SJC_RMRJ_data/real_flow_people_" + city.upper() + ".xlsx"
    dfRealFlow = pd.read_excel(path3, sheet_name=sheet_name2)

    if city.upper() == "SJC":
        dfRealFlow.index = dfRealFlow.index - 1
        dfRealFlow.columns = dfRealFlow.columns - 1

    # Get the name of each column and row
    columnsDfRealFlow = dfRealFlow.columns.values
    rowsDfRealFlow = dfRealFlow.index.values

    #get total of regions into the matrix. It's necessary to interate over the matrix that contais the populations of each zone
    nr = dfPopulation.index.values.size

    #Set i(origin) and j(destination) with 0, because in the matrix, row and column start with 0
    i = 0
    j = 0

    #We need three lists, one to store pi(quantity of people in zone i), other to store pj(quantity of people in zone j)
    #And finally the third list to store dij(distance between i and j)
    pi = []
    pj = []
    dij = []
    f = []

    while i < nr:
        if(i in dfRealFlow.index.values):
            while j < nr:
                if(j in dfRealFlow.columns.values):
                    if(i != j):
                        # Verify if i is different of j, because is impossible get data between equal zone (example, distane between i and i)
                        #if i != j:
                        # Using loc, the data is obtained from dataframe and is added in the list
                        pi.append(dfPopulation.loc[i][1])
                        pj.append(dfPopulation.loc[j][1])
                        f.append(dfRealFlow.loc[i][j])
                        #print(i,",",j," - ", i+1,",",j+1)
                        #print(dfPopulation.loc[i][1])
                        # In matrix, exist failed mappings, so it's necessary to treat the data, replace X for NaN.
                        # This is did using numpy library
                        if (dfDistanceTime.loc[i][j] == 'X'):
                            dfDistanceTime.replace('X', np.NaN)
                        else:
                            distance = float(dfDistanceTime.iloc[i][j].rstrip('km')) * 1000
                        dij.append(distance)
                    j += 1
                else:
                    j += 1
            j = i + 1
            i += 1
        else:
            i += 1

    #print(dfRealFlow)
    return [pi, pj, dij, f]


getMatrixData('rmrj', 'rj', 'DrivingDistance', 'Driving')
