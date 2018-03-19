import databaseConnection

#That function is used to update and insert in postgres`s tables (intermiate_distance... and
# distances_...) (used in roadsMAppingService)
def recordDistancesDirectionsWhen(i, j, origins, destinations, tempmode, distance, paths, city, state, duration, processed, date):


    # Connect with database and check if connection have benn performed sucessfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()

    if con == False:
        print("Database connection ERROR!")
        exit()

    # Create composed name of table
    tableName = "distances_" + city + "_" + state + "_when"

    # Create composed name of table to use in tt variable
    tableName2 = "distances_" + city + "_" + state

    # Create composed name of table where intermediate paths are
    intermediateTableName = "intermediate_distances_" + city + "_" + state + "_when"

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
    sql = "INSERT INTO " + tableName + " (idx_origin, idx_destination, origin, destination, distance_meters, mode, path, duration, processed, whentime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # Check if query have benn performed successfully
    result = cursor.execute(sql, (str(i), str(j), str(origins), str(destinations), str(distance), str(tempmode), str(path_str), str(duration), processed, str(date)))

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
                tt = 'id_' + tableName2
                sql = "INSERT INTO " + intermediateTableName + " (" + tt + ", duration_seconds, start_point, end_point, mode, path, distance_meters, processed, whentime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (str(id_inserted_row), str(duration), str(start_location), str(end_location), str(travel_mode), str(encoded_points), str(distance), processed, str(date)))
                con.commit()

                if result == None:
                    print("Success in intermediate distances insertion!!")
                    varreturn = True
                else:
                    msg = "Error in intermediate distances insertion!! " + sql
                    print(msg)
                    varreturn = False
                w += 1
            print("TESTE")
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

recordDistancesDirectionsWhen(0, 1, '-23.190637250293204,-45.886701608658385', '-23.202251682962157,-45.85807214575006', 'driving', 4991, [[121, 37, '-23.1906501,-45.8868201', '-23.1895721,-45.8869473', 'plplCrgawG]BcBJi@Dk@B', 'DRIVING'], [467, 112, '-23.1895721,-45.8869473', '-23.1866982,-45.8836194', 'xeplClhawGs@y@_BkBIMKKY_@uEwFCEiAsAGGUSUYOQGIIU', 'DRIVING'], [374, 50, '-23.1866982,-45.8836194', '-23.186378,-45.8800484', 'zsolCrs`wGIYMeAIm@C[K{@K}@Ea@Is@OkBAQC]AM?I?I@ELaANy@DO', 'DRIVING'], [246, 21, '-23.186378,-45.8800484', '-23.1882702,-45.8790132', 'zqolCh}_wG?EDU@C@EFQBEBCDEDCFA@AdAYTGd@MB?v@WB?VIh@ORG`@KNI', 'DRIVING'], [651, 137, '-23.1882702,-45.8790132', '-23.1929285,-45.8752322', 't}olCxv_wG^QTKVOTMf@WZOXOLG~As@NGrB{ALIXSFIDGx@}@x@{@DCDEp@m@`@a@\\YPOPODCb@g@z@w@TWTQPS', 'DRIVING'], [457, 58, '-23.1929285,-45.8752322', '-23.1910376,-45.8712648', 'xzplCd__wGa@gAKY_@y@_@{@MYKYc@oAi@}AISs@wBM[k@{Ak@{A', 'DRIVING'], [387, 61, '-23.1910376,-45.8712648', '-23.1935057,-45.8686082', '~nplCjf~vGdBgBz@aAj@o@j@o@FEz@q@RWTWX]@AZ[b@m@NWHOFGFE', 'DRIVING'], [61, 5, '-23.1935057,-45.8686082', '-23.1939899,-45.8683317', 'l~plCxu}vGZQ@?JGLGHGBARIBA@?', 'DRIVING'], [883, 62, '-23.1939899,-45.8683317', '-23.2005533,-45.8637032', 'laqlC`t}vG\\WXUVWFGLOZc@`@e@rCmDvA{Ah@e@t@i@f@[l@Yv@]tAe@dAa@nCcA`FeBVIn@Wl@]\\U', 'DRIVING'], [622, 56, '-23.2005533,-45.8637032', '-23.205366,-45.8610754', 'ljrlCbw|vGNSLQPQ`AaAb@c@fBoBj@m@l@e@t@c@n@YRGRGTEZIb@Ep@Kb@Gz@Mj@Ih@Gt@G`@CV?VCH?LA', 'DRIVING'], [458, 85, '-23.205366,-45.8610754', '-23.2028588,-45.8583237', 'phslCvf|vGHCFAHCLGHIBC@EBGBGAG?A?AAEACCCCCACECCACAE?AGACCGGEWU]Yq@q@UQqAeAeAu@c@Yq@i@s@i@q@g@q@g@', 'DRIVING'], [142, 23, '-23.2028588,-45.8583237', '-23.202211,-45.8571439', 'zxrlCnu{vGKIIEUm@uAmD', 'DRIVING'], [55, 14, '-23.202211,-45.8571439', '-23.2018674,-45.8575268', 'xtrlCbn{vGa@f@a@d@', 'DRIVING'], [67, 14, '-23.2018674,-45.8575268', '-23.2023558,-45.8579151', 'trrlCpp{vGrA`ALJ', 'DRIVING']], 'sjc', 'sp', 764, 0, '20-03-2018 15:00:00')