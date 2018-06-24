import getDirectionTwoGeographicalPoints
import recordDistancesDirections
import importGeographicalPointsFromXLS
import databaseConnection
import getFailedMappings
import importGeographicalPointsFromTXT

def roadsFailedMappingService(inputFile, city, state):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    if not con:
        print('Database connection ERROR!')
        exit();
    cursor = con.cursor()



    if inputFile == "zonas-trafego-sjc-sp":
        # Read from a XLS a matrix where each line is a pair of coords lat/long
        regions = importGeographicalPointsFromXLS.importGeographicalPointsFromXLS(inputFile)
    elif inputFile == "RJ":
        # Read from a XLS a matrix where each line is a pair of coords lat/long
        regions = importGeographicalPointsFromTXT.importGeographicalPointsFromTXT(inputFile)

    # Variable that contains the sheet name of the matrix (you can change it)
    sheetName = "WalkingDistance"

    #Variable that contains the model of travel, it is used by the API of Google Maps (you can change it)
    tempmode = "walking"

    #Key to use the API of Google Maps (you can change it)
    key = "AIzaSyB-kB6JZ-UkSFVGXX0eEIavyMGg-w2whnk"

    #Get a list that contains the tuples with de origin and destination pair of the failed mappings
    failedMappingList = getFailedMappings.getFailedMappings(city, state, sheetName)

    # Indetify the quantity of tuples in the list, it's necessary to verify the number de interaction over the loop
    listLen = len(failedMappingList)

    i = 0

    j = 0

    '''while j < len(regions):
        temp = regions[j]
        origins = str(temp[1]) + "," + str(temp[0])
        print(origins)
        j += 1'''

    cc = 1

    while i < listLen:
        # Setup initial index of origin and destination using the first tuple that inside the failedMappingList
        idx_origin = failedMappingList[i][0]
        idx_destination = failedMappingList[i][1]

        '''if idx_origin > idx_destination:
            aux = idx_origin
            idx_origin = idx_destination
            idx_destination = aux
            flag = True
        else:
            flag = False'''

        temp = regions[idx_origin]
        origins = str(temp[1]) + "," + str(temp[0])
        temp = regions[idx_destination]
        destinations = str(temp[1]) + ',' + str(temp[0])
        print(origins, " - ", destinations)
        print(apikey[keyUse])

        try:
            # Get the distance for forward path
            [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode, None, apikey[keyUse])
            #print(idx_origin, " - ", idx_destination)
            # Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(idx_origin, idx_destination, origins, destinations, tempmode, distance, paths, city, state, duration, 0)
        except:
            #Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(idx_origin, idx_destination, origins, destinations, tempmode, '-1', [], city, state, '-1', 1)

        if cc < 1900:
            cc += 1
        else:
            if keyUse == 19:
                cc == cc
                break;
            else:
                keyUse += 1
                cc = 1

        i += 1

    print(listLen)
    print(cc)

roadsFailedMappingService('RJ', 'rmrj', 'rj')
    

