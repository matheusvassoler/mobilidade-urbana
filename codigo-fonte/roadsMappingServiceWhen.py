import getDirectionTwoGeographicalPoints
import recordDistancesDirectionsWhen
import importGeographicalPointsFromXLS
import databaseConnection

def roadsMappingServiceWhen(pp, inputFile, city, state, ori, dest, date1, date2):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    if not con:
        print("Database connection ERROR!")
        exit()
    cursor = con.cursor()

    #list that contains the google's api key
    apikey = ['AIzaSyAr11wo7Q90rmf7ZReZFVz3OV50g5iW1hI', 'AIzaSyB-kB6JZ-UkSFVGXX0eEIavyMGg-w2whnk', 'AIzaSyClzkVxwXbjphXktb1LZ_MJCprlJMEDvqw', 'AIzaSyDl3vAN7saDAubpUh2f4xb1wIWOhG_lxVc',
              'AIzaSyBSFnV2oNW-fR8yiMBzxZkTFKpyOLRM4-8', 'AIzaSyBg9nMa0mAAnZyoyCsCO7l7mDS3fciI32c', 'AIzaSyDZke-btxWiEtGsNisNBicP5zsJhiG4XS0']

    #variable that control the use of the keys
    keyUse = 0

    #Variable that count the days
    countDay = 0


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

    # Setup initial index of origin and destination (in regions matrix) as the last index in database
    if row == None:
        idx_origin = 0
        idx_destination = 1

        # Split the datetime (date and time) to get month and year
        idx_datetime = date1
        firstDay = True
        idx_datetime_split = date1.split()
        idx_date = idx_datetime_split[0]
        idx_month = idx_date.split('-')[1]
        idx_year = idx_date.split('-')[2]

        # As the row is none the time starts with 0 to go until 23
        time = 0

        changeOriginDestination = True
    else:
        idx_origin = int(row[1])
        idx_destination = int(row[2])
        idx_datetime_split = row[11].split()
        idx_date = idx_datetime_split[0]
        idx_time = idx_datetime_split[1]
        #print(idx_time)

        idx_day = int(idx_date.split('-')[0].lstrip('0'))
        idx_month = idx_date.split('-')[1]
        idx_year = idx_date.split('-')[2]

        #print(int(idx_time[0:2].split(':')[0].lstrip('0')))

        if not(idx_time[0:2].split(':')[0].lstrip('0') == ''):
            time = int(idx_time[0:2].split(':')[0].lstrip('0'))
        else:
            time = 0

        if idx_day == int(date1[0:2].lstrip('0')):
            firstDay = True
        else:
            firstDay = False

        # verify where stopped in the last execution, because the code include i,j and j,i for each
        # loop. Since then, if i=1 and j=2, the last include data is i=2 and j=1 when finalize the loop.
        if idx_origin > idx_destination:
            aux = idx_origin
            idx_origin = idx_destination
            idx_destination = aux
            time += 1
            changeOriginDestination = True
        else:
            #aux = idx_origin
            #idx_origin = idx_destination
            #idx_destination = aux
            changeOriginDestination = False
            print(idx_origin)
            print(idx_destination)

        if (idx_day == 5 and time == 24) and changeOriginDestination:
            firstDay = False
            print("ENTROU")
            time = 0

        if (idx_day == 8 and time == 24) and changeOriginDestination:
            idx_destination += 1
            time = 0
            firstDay = True

    # Create pairs (origin and destination) for all the regions into regions array. For each point we have lat, long coordinates (respectively)
    cc = 1
    i = idx_origin
    while i < nr - 1:
        temp = regions[i]
        origins = str(temp[1]) + "," + str(temp[0])

        # Check if J index should start from I + 1 or using database recovered index
        if i == idx_origin:
            j = idx_destination
        else:
            j = i + 1

        while j < nr:
            temp = regions[j]
            destinations = str(temp[1]) + ',' + str(temp[0])

            while countDay < 2:

                while time < 24:

                    if firstDay:
                        day = int(date1[0:2].lstrip('0'))
                    else:
                        day = int(date2[0:2].lstrip('0'))

                    if day < 10:
                        day = "0" + str(day)

                    if time < 10:
                        hour = "0" + str(time)
                    else:
                        hour = str(time)

                    print(apikey[keyUse])


                    full_date = str(day) + "-" + str(idx_month) + "-" + str(idx_year) + " " + hour + ":00:00"


                    ''' Get the path for driving mode forward and backward  '''

                    # Mode of travel
                    tempmode = "driving"

                    if(changeOriginDestination == False):
                        # B to A
                        try:
                            # Get the distance for backward path
                            [distance, duration,
                             paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode, full_date, apikey[ keyUse])
                            print("CERTO22222222!!!!")

                            # Record distance and path into database
                            output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, distance, paths, city, state, duration, 0, full_date)

                        except:
                            # Record distance and path into database
                            output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, '-1', [], city, state, '-1', 1, '')
                            print("ERRADO2222222!!!!!!!")
                        changeOriginDestination = True
                    else:
                        #A to B
                        try:
                            # Get the distance for forward path
                            [distance, duration, paths]= getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origins, destinations, tempmode, full_date, apikey[keyUse])
                            print("CERTO1111111!!!!")
                            # Record distance and path into database
                            output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(i, j, origins, destinations, tempmode, distance, paths, city, state, duration, 0, full_date)
                        except:
                            # Record distance and path into database
                            output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(i, j, origins, destinations, tempmode, '-1', [], city, state, '-1', 1, '')
                            print("ERRADO1111111!!!!!!!")

                        #B to A
                        try:
                            # Get the distance for backward path
                            [distance, duration,
                             paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(destinations, origins, tempmode, full_date, apikey[keyUse])
                            print("CERTO22222222!!!!")

                            # Record distance and path into database
                            output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, distance, paths, city, state, duration, 0, full_date)

                        except:
                            # Record distance and path into database
                            output = recordDistancesDirectionsWhen.recordDistancesDirectionsWhen(j, i, destinations, origins, tempmode, '-1', [], city, state, '-1', 1, '')
                            print("ERRADO2222222!!!!!!!")

                    print(cc)
                    if cc < pp:
                        cc += 1
                    else:
                        if keyUse == 0:
                            cc = cc
                            break
                        else:
                           keyUse += 1
                           cc = 1


                    time += 1
                    if time == 24:
                        if firstDay:
                            firstDay = False
                        else:
                            firstDay = True

                countDay += 1

                time = 0
                if cc >= pp:
                    break

            countDay = 0

            time = 0
            if cc >= pp:
                break

            j += 1

        if cc >= pp:
            break
        i += 1





roadsMappingServiceWhen(900, "zonas-trafego-sjc-sp", "sjc", "sp", 0, 1, '26-06-2018 00:00:00', "29-06-2018 00:00:00")

#obs: None = now
#     if you want to execute in a determine day and time you have to put in this format:
#                                                                     'day-mouth-year hour:min:sec'