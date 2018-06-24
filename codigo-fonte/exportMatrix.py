import pandas as pd
import databaseConnection
import os

def exportMatrix(city, state):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()
    if not con:
        print("Database connection ERROR!")
        exit()

    # Create a directory called Matrix
    directory = "./Matrix"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Get all the records in database that have not been processed yet
    sql = "SELECT * FROM " + tableName + " ORDER BY CAST(idx_origin AS int), CAST(idx_destionation AS int) DESC, CAST(id AS int) DESC"
    print(sql)
    result = cursor.execute(sql)

    # Create a .XMLS for each situation (driving and walking) with a variable(time and distance)
    dfWalkingDistance = pd.DataFrame()
    dfWalkingTime = pd.DataFrame()
    dfDrivingDistance = pd.DataFrame()
    dfDrivingTime = pd.DataFrame()

    # Create a variable to store the max idx_origin and idx_destination
    row = cursor.fetchall()
    maxIdx = int(row[0][2])

    i = 0

    nada = [0 for i in range(maxIdx+1)]

    for x in range(maxIdx+1):
        nada[x] = 'X'

    for x in range(maxIdx+1):
        dfDrivingTime.insert(x, x, nada)
        dfDrivingDistance.insert(x, x, nada)
        dfWalkingDistance.insert(x, x, nada)
        dfWalkingTime.insert(x, x, nada)

    #Put All datas in the .XMLS
    while i < len(row):
            idOrigin = int(row[i][1])
            idDestination = int(row[i][2])
            time = str(round((float(row[i][8])/3600), 2)) + 'h'
            distance = str(round((float(row[i][5])/1000), 2))+'km'
            processed = int(row[i][10])
            mode = row[i][6]

            if(processed == 0):
                if(mode == 'walking'):
                    #WALKING DISTANCE
                    dfWalkingDistance[idDestination][idOrigin] = distance
                    # WALKING TIME
                    dfWalkingTime[idDestination][idOrigin] = time
                else:
                    # DRIVING DISTANCE
                    dfDrivingDistance[idDestination][idOrigin] = distance
                     # DRIVING TIME
                    dfDrivingTime[idDestination][idOrigin] = time

            print('include line ' + str(i))
            i += 1
    for x in range(maxIdx+1):
        dfWalkingDistance[x][x] = '0km'
        dfWalkingTime[x][x] = '0h'
        dfDrivingDistance[x][x] = '0km'
        dfDrivingTime[x][x] = '0h'
        print("X: {}".format(x))

    # Create a path to save a Pandas Excel
    excelName = "./Matrix/Matrix_" + city + "_" + state + '.xlsx'

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(excelName, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    dfWalkingDistance.to_excel(writer, sheet_name='WalkingDistance')
    dfWalkingTime.to_excel(writer, sheet_name='WalkingTime')
    dfDrivingDistance.to_excel(writer, sheet_name='DrivingDistance')
    dfDrivingTime.to_excel(writer, sheet_name='DrivingTime')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

exportMatrix("rmrj", "rj")