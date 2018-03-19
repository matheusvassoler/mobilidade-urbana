import getDirectionTwoGeographicalPoints
import recordDistancesDirectionsWhen
import importGeographicalPointsFromXLS
import databaseConnection

def roadsMappingServiceWhen(inputFile, city, state, ori, dest, date):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    if not con:
        print("Database connection ERROR!")
        exit()
    cursor = con.cursor()

    # Read from a XLS a matrix where each line is a pair of coords lat/long
    regions = importGeographicalPointsFromXLS.importGeographicalPointsFromXLS(inputFile)

    # Get the total of regions into region array
    nr = len(regions)

    # Create composed name of table
    tableName = "distances_" + city + "_" + state + "_" + "when"

    # Get last record in database
    sql = "SELECT * FROM " + tableName + " ORDER BY id DESC"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row != None:
        row = list(row)

    i = ori
    j = dest

    # Set origins coordinate
    temp = regions[i]
    origins = str(temp[1]) + "," + str(temp[0])
    print(origins)

    # Set destinations coordinate
    temp = regions[j]
    destinations = str(temp[1]) + ',' + str(temp[0])

    '''  Get the path for driving mode forward and backward  '''

    # Mode of travel
    tempmode = "driving"

    #A to B
    try:
        # Get the distance for forward path
        [distance, duration, paths]= getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode, date)

        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(i, j, origins, destinations, tempmode, distance, paths, city, state, duration, 0, date)
    except:
        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(i, j, origins, destinations, tempmode, '-1', [], city, state, '-1', 1, '')

    #B to A
    try:
        # Get the distance for backward path
        [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode, date)


        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, distance, paths, city, state, duration, 0, date)
    except:
        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, '-1', [], city, state, '-1', 1, '')


    '''  Get the path for walking mode forward and backward  '''

    # Mode of travel
    tempmode = "walking"

    #A TO B
    try:
        # Get the distance for forward path
        [distance, duration, paths]= getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode, date)

        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(i, j, origins, destinations, tempmode, distance, paths, city, state, duration, 0, date)
    except:
        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(i, j, origins, destinations, tempmode, '-1', [], city, state, '-1', 1, '')


    #B TO A
    try:
        # Get the distance for backward path
        [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode, date)


        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, distance, paths, city, state, duration, 0, date)
    except:
        # Record distance and path into database
        output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, '-1', [], city, state, '-1', 1, '')





roadsMappingServiceWhen("zonas-trafego-sjc-sp", "sjc", "sp", 0, 1, '10-12-2017 15:00:00')

#obs: None = now
#     if you want to execute in a determine day and time you have to put in this format:
#                                                                     'day-mouth-year hour:min:sec'