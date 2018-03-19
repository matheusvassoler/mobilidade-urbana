import databaseConnection
import getDirectionTwoGeographicalPoints
import importGeographicalPointsFromXLS
import importGeographicalPointsFromTXT
import psycopg2

def UpdateErrorRecords(inputFile ,city, state):
    con = databaseConnection.connectdb()
    if not con:
        print("Database connection ERROR!")
        exit()
    cursor = con.cursor()

    tableName = "distances_"+city+"_"+state

    sql = "SELECT * FROM "+tableName+" WHERE processed=1 ORDER BY id"

    # Read from a XLS a matrix where each line is a pair of coords lat/long
    regions = importGeographicalPointsFromTXT.importGeographicalPointsFromTXT(inputFile)

    cursor.execute(sql)
    row = cursor.fetchall()
    if row != None:
        row = list(row)

    if row == None:
        exit()
    i = 0

    #Fix error in table distances
    while(i < len(row)):
        id = row[i][0]
        id_origin = int(row[i][1])
        id_destination = int(row[i][2])
        tempmode = row[i][6]

        temp = regions[id_origin]
        origin = str(temp[1]) + "," + str(temp[0])

        temp = regions[id_destination]
        destination = str(temp[1]) + "," + str(temp[0])

        validate = 1

        try:
            [distance, duration, paths] = getDirectionTwoGeographicalPoints.getDirectionTwoGeographicalPoints(origin,
                                                                                                              destination,
                                                                                                              tempmode,
                                                                                                              None)
            validate = 0
        except:
            validate = 1

        if validate == 0:

            numDirections = len(paths)

            # Include each path block in path string
            k = 0

            path_str = ""
            while k < numDirections:
                # Get the number of points in current path block
                tmp = paths[k]
                encoded_points = tmp[4]

                # Create an string with all coded path points. Each block is separated by " "
                path_str = path_str + " " + encoded_points

                k += 1

            # Remove white spaces in the begin and at the end of string
            path_str = path_str.strip()

            # UPDATE record into distance table
            sql = "UPDATE " + tableName + " SET origin='"+str(origin)+"', destination='"+str(destination)+\
                        "', distance_meters='"+str(distance)+"', duration='"+str(duration)+"', path='"+str(path_str)+"', processed='0' WHERE id="+str(id)


            print("Update Success id="+str(id))
            # Check if query have benn performed successfully
            result = cursor.execute(sql)
            con.commit()

            intermediateTableName = "intermediate_distances_"+city+"_"+state

            sql = "SELECT * FROM "+ intermediateTableName +" WHERE id_"+ tableName +"='"+ str(id) +"'"
            cursor.execute(sql)
            row2 = cursor.fetchall()

            if distance != -1 and row2 != None:
                w = 0
                while w < numDirections:
                    # Get the number of points in current path block
                    temp = paths[w]
                    distance = temp[0]
                    duration = temp[1]
                    start_location = temp[2]
                    end_location = temp[3]
                    encoded_points = temp[4]
                    travel_mode = temp[5]
                    processed=0

                    # Insert record into intermediate distance table
                    tt = 'id_' + tableName
                    sql = "INSERT INTO " + intermediateTableName + " (" + tt + ", duration_seconds, start_point, end_point, mode, path, distance_meters, processed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (str(id), str(duration), str(start_location), str(end_location), str(travel_mode), str(encoded_points), str(distance), processed))
                    con.commit()

                    if result == None:
                        # print("Success in intermediate distances insertion!!")
                        varreturn = True
                    else:
                        msg = "Error in intermediate distances insertion!! " + sql
                        print(msg)
                        varreturn = False
                    w += 1

                if varreturn == True:
                    print("Success in intermediate distances insertion!!")
                    sql = "UPDATE " + tableName + " SET intermediate_paths_ok = '1' WHERE id = " + str(id)
                    print(sql)
                    cursor.execute(sql)
                    con.commit()

                print("---------------------------------------------------------------------------")
        i += 1


UpdateErrorRecords("RJ", "rmrj", "rj")