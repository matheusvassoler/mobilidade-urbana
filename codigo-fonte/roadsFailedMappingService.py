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
        exit()
    cursor = con.cursor()

    # list that contains the google's api key (you can change it)
    apikey = ['AIzaSyAr11wo7Q90rmf7ZReZFVz3OV50g5iW1hI', 'AIzaSyB-kB6JZ-UkSFVGXX0eEIavyMGg-w2whnk',
              'AIzaSyClzkVxwXbjphXktb1LZ_MJCprlJMEDvqw', 'AIzaSyDl3vAN7saDAubpUh2f4xb1wIWOhG_lxVc',
              'AIzaSyBSFnV2oNW-fR8yiMBzxZkTFKpyOLRM4-8', 'AIzaSyBg9nMa0mAAnZyoyCsCO7l7mDS3fciI32c',
              'AIzaSyDZke-btxWiEtGsNisNBicP5zsJhiG4XS0', 'AIzaSyD79s5kzm_4WJGJKnp6sv2lAADpGeGZEZ4',
              'AIzaSyDd1KnOEb6u79sJgT4cVV1JrSOcKkvFtBI', 'AIzaSyDwsqAZ-8wB_h23XhKAVshX0MZqa_ty4GI',
              'AIzaSyAz1ZrldhSNHUdXjvT9MTDUeiub4MeUND8', 'AIzaSyBQYl-sChyjHoc186BYpKrId6-9nf2Kf9A',
              'AIzaSyDAmvH9hkaw5NwDHt1_3VPuNX6KFqtcZTo', 'AIzaSyBUguv05oZBYjCZ7OJtxYlUUyzHoyOqlPU',
              'AIzaSyACauD8ibd4RDDCb_1C57xm2iJG4Wmj3c8', 'AIzaSyCIdkrYIOqYX3cogj7LnwAi7Kogk2pDcQc',
              'AIzaSyB4mwWf6m898vPQYd0lGG4-5NDQt0myS4o', 'AIzaSyDBRAo1aS3ihZbj9SnwWD07kA7q1B9XpLA',
              'AIzaSyAYoIztpjHUTGGuEKD25_1fnwsIdNEm3FA', 'AIzaSyAC8xAfiMw66cZTNqrp0WA8Y9h2hxGNAHg']

    # variable that control the use of the keys (you can change it)
    #The apiKey list starts with the keyUse value
    keyUse = 0

    if inputFile == "zonas-trafego-sjc-sp":
        # Read from a XLS a matrix where each line is a pair of coords lat/long
        regions = importGeographicalPointsFromXLS.importGeographicalPointsFromXLS(inputFile)
    elif inputFile == "RJ":
        # Read from a XLS a matrix where each line is a pair of coords lat/long
        regions = importGeographicalPointsFromTXT.importGeographicalPointsFromTXT(inputFile)

    # Variable that contains the sheet name of the matrix (you can change it)
    sheetName = "DrivingDistance"

    #Variable that contains the model of travel, it is used by the API of Google Maps (you can change it)
    tempmode = "driving"

    #Get a list that contains the tuples with de origin and destination pair of the failed mappings
    failedMappingList = getFailedMappings.getFailedMappings(city, state, sheetName)

    # Indetify the quantity of tuples in the list, it's necessary to verify the number de interaction over the loop
    listLen = len(failedMappingList)

    i = 0

    j = 0

    cc = 1
    while i < listLen:
        # Setup initial index of origin and destination using the first tuple that inside the failedMappingList
        idx_origin = failedMappingList[i][0]
        idx_destination = failedMappingList[i][1]

        temp = regions[idx_origin]
        origins = str(temp[1]) + "," + str(temp[0])
        temp = regions[idx_destination]
        destinations = str(temp[1]) + ',' + str(temp[0])
        print(origins, " - ", destinations)
        print(apikey[keyUse])

        try:
            # Get the distance for forward path
            [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode.upper(), None, apikey[keyUse])
            #print(idx_origin, " - ", idx_destination)
            # Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(idx_origin, idx_destination, origins, destinations, tempmode, distance, paths, city, state, duration, 0)
        except:
            #Record distance and path into database
            output = recordDistancesDirections.recordDistancesDirections(idx_origin, idx_destination, origins, destinations, tempmode, '-1', [], city, state, '-1', 1)

        #The daily quota of the API is 2500, but to avoid failures, only 1900 requests per key
        if cc < 1900:
            cc += 1
        else:
            #You can choose this number
            if keyUse == 13:
                cc == cc
                break
            else:
                keyUse += 1
                cc = 1

        i += 1

    print(listLen)
    print(cc)

roadsFailedMappingService('RJ', 'rmrj', 'rj')
    

