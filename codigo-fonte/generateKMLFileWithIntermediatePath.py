import PolylineCode
import databaseConnection
import os

def generateKMLFileWithIntermediatePath(numRecords, city, state):
    # Connect with database and check if connection have been performed successfully
    con = databaseConnection.connectdb()
    cursor = con.cursor()
    if not con:
        print("Database connection ERROR!")
        exit()

    directory = "./KML_files/" + city + "_" + state
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create composed name of table
    tableName = "distances_" + city + "_" + state

    # Create composed name of table where intermediate paths are
    intermediateTableName = "intermediate_distances_" + city + "_" + state

    # Get all the records in database that have been processed yet
    sql = "SELECT * FROM " + tableName + " where processed = 0  ORDER BY id"
    result = cursor.execute(sql)

    i = 0

    # Create an object of class Polyline to decode path
    #polyline = PolylineCode.decode_polyline()

    # Create a KML file for each not processed record
    # row = pg_fetch_row(result)
    row = cursor.fetchall()
    while i < len(row):

        id = row[i][0]
        id_origin = row[i][1]
        id_destination = row[i][2]
        mode = row[i][6]

        print(id)

        # Invert coordinates (lat, long to long, lat) for origin and destination. Also removes "(" and ")" from string
        origin = row[i][3]
        origin = origin.strip("(")
        origin = origin.strip(")")
        tmp = origin.split(",")
        origin = tmp[0] + ", " + tmp[1]

        destination = row[i][4]
        destination = destination.strip("(")
        destination = destination.strip(")")
        tmp = destination.split(",")
        destination = tmp[0] + ', ' + tmp[1]

        path_str = ""

        # Get the encoded path and transform it into a string
        encoded_points = row[i][7].split(" ")
        decoded_points = []
        numPaths = len(encoded_points)
        j = 0
        while j < numPaths:
            tmp = encoded_points[j]
            decoded_points = PolylineCode.decode_polyline(tmp)
            k = 0
            while k < len(decoded_points):
                tmp = decoded_points[k]
                path_str = path_str + str(tmp[1]) + "," + str(tmp[0]) + ",0.0"
                k += 1
            j += 1
        path_str = path_str.strip()

        # Create coordinates for origin and destination
        tmp = origin.split(",")
        path_origin = str(tmp[1]) + "," + str(tmp[0]) + ",0.00"
        tmp = destination.split(",")
        path_destination = str(tmp[1]) + "," + str(tmp[0]) + ",0.00"

        ###################################
        #INICIO AREA TO GET THE INTERMEDIATE PATH
        ###################################

        sql2 = "select * from " + intermediateTableName + " where id_distances_"+city+"_"+state+"='" + str(
            id) + "' order by id "
        result = cursor.execute(sql2)
        row2 = cursor.fetchall()
        print(row2)
        print(sql2)
        #input("Pressione qualquer coisa")

        i2 = 0
        content = []
        while i2 < len(row2):
            if((i == 0 or i == len(row)-1) and (i2 == 0 or i2 == len(row2)-1)):
                i2 += 1
                print(True)
                continue
            id_full_path2 = row2[i2][0]

            # Invert coordinates (lat,long to long,lat) for origin and destination. Also removes "(" and ")" from string
            origin2 = row2[i2][3]
            origin2 = origin2.strip("(")
            origin2 = origin2.strip(")")
            tmp2 = origin2.split(",")
            origin2 = tmp2[0] + ', ' + tmp2[1]
            nameorigin2 = origin2

            destination2 = row2[i2][4]
            destination2 = destination2.strip("(")
            destination2 = destination2.strip(")")
            tmp2 = destination2.split(",")
            destination2 = tmp2[0] + ', ' + tmp2[1]
            namedestination2 = destination2

            mode2 = row2[i2][5].strip()

            path_str2 = ""

            # Get the encoded path and transform it into a string
            encoded_points2 = row2[i2][6].split(" ")
            decoded_points2 = PolylineCode.decode_polyline(encoded_points2[0])
            k = 0
            print(encoded_points2)
            print(decoded_points2)
            while k < len(decoded_points2):
                tmp2 = decoded_points2[k]
                path_str2 = path_str2 + str(tmp2[1]) + "," + str(tmp2[0]) + ",0.0"
                k += 1
            path_str2 = path_str2.strip()

            # Create coordinates for origin and destination
            tmp2 = origin2.split(",")
            path_origin2 = str(tmp2[1]) + "," + str(tmp2[0]) + ",0.00"
            tmp2 = destination2.split(",")
            path_destination2 = str(tmp2[1]) + "," + str(tmp2[0]) + ",0.00"

            content.append([origin2, path_origin2, destination2, path_destination2])

            print("CONTENT ", content)
            #print(i2)
            #input("Pressione qualquer coisa")
            i2 += 1

        ###################################
        # FIM AREA TO GET THE INTERMEDIATE PATH
        ###################################

        # Create a file to write KML marked language
        file_name = "./KML_files/"+city+"_"+state+"/path-file-" + str(id) +"_("+id_origin+", "+id_destination+")_mode-"+mode+ ".kml"
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

        i3=0
        while i3 < len(content):
            fp.write("          <Placemark>\n")
            fp.write("              <styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("              <name>" + content[i3][0] + "</name>\n")
            fp.write("              <ExtendedData>\n")
            fp.write("              </ExtendedData>\n")
            fp.write("              <description><![CDATA[Origin]]></description>\n")
            fp.write("              <Point>\n")
            fp.write("                  <coordinates>" + content[i3][1] + "</coordinates>\n")
            fp.write("              </Point>\n")
            fp.write("          </Placemark>\n")

            fp.write("          <Placemark>\n")
            fp.write("              <styleUrl>#icon-503-DB4436</styleUrl>\n")
            fp.write("              <name>" + content[i3][2] + "</name>\n")
            fp.write("              <ExtendedData>\n")
            fp.write("              </ExtendedData>\n")
            fp.write("              <description><![CDATA[Origin]]></description>\n")
            fp.write("              <Point>\n")
            fp.write("                  <coordinates>" + content[i3][3] + "</coordinates>\n")
            fp.write("              </Point>\n")
            fp.write("          </Placemark>\n")
            i3 += 1

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
        fp.write("                      <href>http://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png</href>\n")
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
        # result2 = pg_query(con, sql2)'''
        #input("ALGO")
        i += 1


generateKMLFileWithIntermediatePath(5000, "rmrj", "rj")
