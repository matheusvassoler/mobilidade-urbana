import pandas as pd

#To can run this code is necessary to invoke the method, passing as argument, city, state, sheet_name of the matrix
#This method search in the matrix data with value X, X means failed mapping
#To run this code, it's necessary to create the matrix that contains duration and time between zones. This can be done in the archive called exportMatrix.py
#Before of running the code tt's necessary to remove all failed data from database (This can be done by searching for the failed data by the duration or distance_meters column with value '-1')
#After remove, it's necessary to recreate the matrix
#Attention: Some data will have value -1 to duration and distance_meters, because in the some cases it's impossible to make the route between zones (Example, impossible paths in walking mode)

def getFailedMappings(city, state, sheet_name):
    path = "./Matrix/"+"Matrix_"+city+"_"+state+".xlsx"
    df = pd.read_excel(path, sheet_name=sheet_name)

    #Identify the number of column in dataframe to can to interate in a for loop
    columnLen = df.columns.values.size

    #Identify the numbr of row in dataframe to can to interate in a whie looop
    rowLen = df.index.values.size

    i=0
    j=0

    #List that contais tuples with failed mappings
    failedMappingList = []

    while i < rowLen:
        while j < columnLen:
            if(df.iloc[i][j] == 'X'):
                #Get idOrigin and idDestination contained in the matrix
                idOrigin = i
                idDestination = j

                # First, add the pair in a tuple, after add the tuple in the list called failedMappingList
                failedMappingList.append((idOrigin, idDestination))
            j += 1
        j = 0
        i += 1

    return failedMappingList

#getFailedMappings("sjc", "sp", "DrivingDistance")