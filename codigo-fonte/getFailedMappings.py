import pandas as pd

#To can run this code is necessary to invoke the method, passing as argument, city, state, sheet_name of the matrix
#This method search in the matrix data with value X, X means failed mapping
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

    '''
    #A loop to interate over dataframe to get the failedMappings(X)
    for index, row in df.iterrows():
        for i in range(0, columnLen):
            if(row[i] == 'X'):
                #get idOrigin and idDestination contained in the matrix
                idOrigin = index
                idDestination = i

                #First, add the pair in a tuple, after add the tuple in the list called failedMappingList
                failedMappingList.append((idOrigin, idDestination))
    '''

    print(failedMappingList)

    return failedMappingList

getFailedMappings("sjc", "sp", "DrivingDistance")