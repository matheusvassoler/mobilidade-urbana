from gPointConverter import GPointerConverteClass

import pandas as pd

#This function is used to return the coordinates of the locals (use class gPointConverter)
def importGeographicalPointsFromTXT(fileName):
    # Create a path for input file (input files are stored into folder INPUT)
    path = "input/" + fileName + ".txt"

    # Create a vector named coordenates where each line is a par of [long,lat]
    coordinates = []

    # Use py class to convert between UTM to lat/long
    converter = GPointerConverteClass

    f = open(path, 'r')

    parts = []
    for line in f:
        try:
            parts = line.split('\t')
            xcentroid = float(parts[0].replace(",", "."))
            ycentroid = float(parts[1].replace(",", "."))
            tt = converter.convertUtmToLatLng(xcentroid, ycentroid, 23)
            lat = tt[0]
            long = tt[1]
            coordinates.append([long, lat])
        except:
            print("error in the file")

    f.close()

    return coordinates