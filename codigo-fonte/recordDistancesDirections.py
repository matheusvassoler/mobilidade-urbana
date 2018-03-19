import databaseConnection

#That function is used to update and insert in postgres`s tables (intermiate_distance... and
# distances_...) (used in roadsMAppingService)
def recordDistancesDirections(i, j, origins, destinations, tempmode, distance, paths, city, state, duration, processed):

    # Connect with database and check if connection have benn performed sucessfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()

    if con == False:
        print("Database connection ERROR!")
        exit()

    # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Create composed name of table where intermediate paths are
    intermediateTableName = "intermediate_distances_" + city + "_" + state

    # Variable pointing out return value
    varreturn = True

    # Create variable to keep an string with full path from origin to destination
    path_str = ""

    # Get the number of parts into full path
    numDirections = len(paths)

    # Include each path block in path string
    k = 0


    while k < numDirections:
        # Get the number of points in current path block
        tmp = paths[k]
        encoded_points = tmp[4]

        # Create an string with all coded path points. Each block is separated by " "
        path_str = path_str + " " + encoded_points

        k += 1


    # Remove white spaces in the begin and at the end of string
    path_str = path_str.strip()

    # Insert record into distance table
    sql = "INSERT INTO " + tableName + " (idx_origin, idx_destination, origin, destination, distance_meters, mode, path, duration, processed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # Check if query have benn performed successfully
    result = cursor.execute(sql, (str(i), str(j), str(origins), str(destinations), str(distance), str(tempmode), str(path_str), str(duration), processed))

    con.commit()
    if result == None:
        print("Success in distances insertion!!")
        varreturn = True

        if distance != -1:
            # Get the id of just include record
            sql = "SELECT currval(pg_get_serial_sequence('" + tableName + "','id'));"
            result = cursor.execute(sql)
            row = cursor.fetchone()
            row = str(row)
            row = row.strip("[")
            row = row.strip("(")
            row = row.strip("]")
            row = row.strip(")")
            row = row.strip(",")
            id_inserted_row = row

            # Include each path block in database
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

                # Insert record into intermediate distance table
                tt = 'id_' + tableName
                sql = "INSERT INTO " + intermediateTableName + " (" + tt + ", duration_seconds, start_point, end_point, mode, path, distance_meters, processed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (str(id_inserted_row), str(duration), str(start_location), str(end_location), str(travel_mode), str(encoded_points), str(distance), processed))
                con.commit()

                if result == None:
                    print("Success in intermediate distances insertion!!")
                    varreturn = True
                else:
                    msg = "Error in intermediate distances insertion!! " + sql
                    print(msg)
                    varreturn = False
                w += 1

            if varreturn == True:
                print("Success in intermediate distances insertion!!")
                sql = "UPDATE " + tableName + " SET intermediate_paths_ok = '1' WHERE id = " + id_inserted_row
                print(sql)
                cursor.execute(sql)
                con.commit()

    else:
        msg = "Error in distances insertion!! " + sql
        print(msg)
        varreturn = False

    return varreturn
