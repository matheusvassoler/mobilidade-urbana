import PolylineCode
import databaseConnection
import os

def generateKMLFileIntermediatePath(numRecords, city, state):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()
    if not con:
        print("Database connection ERROR!")
        exit()


    #Set directory location
    directory = "./KML_files/Intermediate"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "./KML_files/Intermediate/"+city+"_"+state
    if not os.path.exists(directory):
        os.makedirs(directory)

        # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Create composed name of table where intermediate paths are
    intermediateTableName = "intermediate_distances_" + city + "_" + state

    # Create the name of the foreing key into intermediate table
    idname = "id_distances_" + city + "_" + state

    # Get all the records in database that have not been processed yet
    sql = "SELECT * FROM " + tableName + " WHERE processed = 0 ORDER BY id"
    result = cursor.execute(sql)

    i = 0
    # Create a KML file for each not processed record
    row = cursor.fetchall()
    while i < len(row):
        id_full_path = row[i][0]
        id_origin = row[i][1]
        id_destination = row[i][2]
        mode = row[i][6]

        print(id_full_path)

        sql2 = "select * from "+intermediateTableName+" where id_distances_sjc_sp='"+str(id_full_path)+"' order by id "
        result = cursor.execute(sql2)
        row2 = cursor.fetchall()

        path_file = str(id_full_path)+"_("+id_origin+", "+id_destination+")_mode-"+mode
        directory2 = directory+"/"+path_file
        if not os.path.exists(directory2):
            os.makedirs(directory2)

        i2 = 0
        while i2 < len(row2):

            id_full_path2 = row2[i2][0]

            # Invert coordinates (lat,long to long,lat) for origin and destination. Also removes "(" and ")" from string
            origin = row2[i2][3]
            origin = origin.strip("(")
            origin = origin.strip(")")
            tmp = origin.split(",")
            origin = tmp[0] + ', ' + tmp[1]
            nameorigin = origin

            destination = row2[i2][4]
            destination = destination.strip("(")
            destination = destination.strip(")")
            tmp = destination.split(",")
            destination = tmp[0] + ', ' + tmp[1]
            namedestination = destination

            mode = row2[i2][5].strip()

            path_str = ""

            # Get the encoded path and transform it into a string
            encoded_points = row2[i2][6].split(" ")
            decoded_points = PolylineCode.decode_polyline(encoded_points[0])
            k = 0
            while k < len(decoded_points):
                tmp = decoded_points[k]
                path_str = path_str + str(tmp[1]) + "," + str(tmp[0]) + ",0.0"
                k += 1
            path_str = path_str.strip()

            # Create coordinates for origin and destination
            tmp = origin.split(",")
            path_origin = str(tmp[1]) + "," + str(tmp[0]) + ",0.00"
            tmp = destination.split(",")
            path_destination = str(tmp[1]) + "," + str(tmp[0]) + ",0.00"

            # Create a file to write KML marked language
            file_name = directory2+"/path-file-" + str(id_full_path2) + ".kml"
            fp = open(file_name, "w")
            fp.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            fp.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
            fp.write("  <Document>\n")
            fp.write("      <name>Directions from " + origin + " to " + destination + "</name>\n")
            fp.write("          <Placemark>\n")
            fp.write("              <styleUrl>#line-1267FF-5</styleUrl>\n")
            fp.write("              <name>Directions from " + origin + " to " + destination + "</name>\n")
            fp.write("              <ExtendedData>\n")
            fp.write("              </ExtendedData>\n")
            fp.write("              <LineString>\n")
            fp.write("                  <tessellate>1</tessellate>\n")
            fp.write("                  <coordinates>" + path_str + "</coordinates>\n")
            fp.write("              </LineString>\n")
            fp.write("          </Placemark>\n")
            fp.write("          <Placemark>\n")
            fp.write("              <styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("              <name>" + origin + "</name>\n")
            fp.write("              <ExtendedData>\n")
            fp.write("              </ExtendedData>\n")
            fp.write("              <description><![CDATA[Origin]]></description>\n")
            fp.write("              <Point>\n")
            fp.write("                  <coordinates>" + path_origin + "</coordinates>\n")
            fp.write("              </Point>\n")
            fp.write("          </Placemark>\n")
            fp.write("          <Placemark>\n")
            fp.write("              <styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("              <name>" + destination + "</name>\n")
            fp.write("              <ExtendedData>\n")
            fp.write("              </ExtendedData>\n")
            fp.write("              <description><![CDATA[Destination]]></description>\n")
            fp.write("              <Point>\n")
            fp.write("                  <coordinates>" + path_destination + "</coordinates>\n")
            fp.write("              </Point>\n")
            fp.write("          </Placemark>\n")
            fp.write("          <Style id='icon-503-DB4436'>\n")
            fp.write("              <IconStyle>\n")
            fp.write("                  <color>ff3644DB</color>\n")
            fp.write("                  <scale>1.1</scale>\n")
            fp.write("                  <Icon>\n")
            fp.write(
                "                      <href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>\n")
            fp.write("                  </Icon>\n")
            fp.write("              </IconStyle>\n")
            fp.write("          </Style>\n")
            fp.write("          <Style id='line-1267FF-5'>\n")
            fp.write("              <LineStyle>\n")
            fp.write("                  <color>ffFF6712</color>\n")
            fp.write("                  <width>5</width>\n")
            fp.write("              </LineStyle>\n")
            fp.write("          </Style>\n")
            fp.write("\t</Document>\n")
            fp.write("</kml>\n")

            fp.close()

            # Get all the records in database that have not been processed yet
            # sql2 = "UPDATE " + tableName + " SET processed = '1' WHERE id = " + id
            # result2 = pg_query(con, sql2)
            i2 += 1
        i += 1

generateKMLFileIntermediatePath(10, "sjc", "sp")
