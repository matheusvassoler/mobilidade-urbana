import getDirectionTwoGeographicalPoints
import recordDistancesDirections
import importGeographicalPointsFromXLS
import databaseConnection

#Used to get all datas of a point at other point. (use the RecordDistancesDirections,
# getDirectionTwoGeographicalPoints, importGeographicalPOintsFromXLS)
def roadsMappingService(pp, inputFile, city, state, date):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    if not con:
        print("Database connection ERROR!")
        exit()
    cursor = con.cursor()

    apikey = "AIzaSyAr11wo7Q90rmf7ZReZFVz3OV50g5iW1hI"

    # Read from a XLS a matrix where each line is a pair of coords long/lat
    regions = importGeographicalPointsFromXLS.importGeographicalPointsFromXLS(inputFile)

    # Get the total of regions into region array
    nr = len(regions)

    # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Get last record in database
    sql = "SELECT * FROM " + tableName + " ORDER BY id DESC"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row != None:
        row = list(row)

    # Setup initial index of origin and destination (in regions matrix) as the last index in database
    if row == None:
        idx_origin = 0
        idx_destination = 1
    else:
        idx_origin = int(row[1])
        idx_destination = int(row[2])

        #verify where stopped in the last execution, because the code include i,j and j,i for each
        #loop. Since then, if i=1 and j=2, the last include data is i=2 and j=1 when finalize the loop.
        if idx_origin > idx_destination:
            aux = idx_origin
            idx_origin = idx_destination
            idx_destination = aux

        idx_destination += 1

    # Create pairs (origin and destination) for all the regions into regions array. For each point we have lat, long coordinates (respectively)
    cc = 1
    i = idx_origin
    while i < nr - 1:
        temp = regions[i]
        origins = str(temp[1]) + "," + str(temp[0])
        #print(origins)

        # Check if J index should start from I + 1 or using database recovered index
        if i == idx_origin:
            j = idx_destination
        else:
            j = i + 1

        while j < nr:
            temp = regions[j]
            destinations = str(temp[1]) + ',' + str(temp[0])

            '''  Get the path for driving mode forward and backward  '''

            # Mode of travel
            tempmode = "driving"

            #A to B
            try:
                # Get the distance for forward path
                [distance, duration, paths]= getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode, date, apikey)

                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(i, j, origins, destinations, tempmode, distance, paths, city, state, duration, 0)
            except:
                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(i, j, origins, destinations, tempmode, '-1', [], city, state, '-1', 1)

            #B to A
            try:
                # Get the distance for backward path
                [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode, date, apikey)


                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(j, i, destinations, origins, tempmode, distance, paths, city, state, duration, 0)
            except:
                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(j, i, destinations, origins, tempmode, '-1', [], city, state, '-1', 1)


            '''  Get the path for walking mode forward and backward  '''

            # Mode of travel
            tempmode = "walking"

            #A TO B
            try:
                # Get the distance for forward path
                [distance, duration, paths]= getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode, date, apikey)

                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(i, j, origins, destinations, tempmode, distance, paths, city, state, duration, 0)
            except:
                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(i, j, origins, destinations, tempmode, '-1', [], city, state, '-1', 1)


            #B TO A
            try:
                # Get the distance for backward path
                [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode, date, apikey)


                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(j, i, destinations, origins, tempmode, distance, paths, city, state, duration, 0)
            except:
                # Record distance and path into database
                output = recordDistancesDirections.recordDistancesDirections(j, i, destinations, origins, tempmode, '-1', [], city, state, '-1', 1)


            # Check if the script has already been executed the correct number of times. If yes stop the code. This process have been implemented because Google API has a limit of querys daily
            if cc < pp:
                cc += 1
            else:
                cc = cc
                break
            j += 1

        if cc >= pp:
            break
        i += 1

# Execute the function (How the insertion is did 4 times each loop, the first parameter is the number of loops)
# free request per day is equal 2500. put 625 thus are 4 request each loop
roadsMappingService(625, "zonas-trafego-sjc-sp", "sjc", "sp", None)

#obs: None = now
#     if you want to execute in a determine day and time you have to put in this format:
#                                                                     'day-mouth-year hour:min:sec'