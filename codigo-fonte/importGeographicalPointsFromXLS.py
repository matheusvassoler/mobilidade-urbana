from gPointConverter import GPointerConverteClass

import pandas as pd

#This function is used to return the coordinates of the locals (use class gPointConverter)
def importGeographicalPointsFromXLS(fileName):
    # Create a path for input file (input files are stored into folder INPUT)
    path = "input/" + fileName + ".xls"

    # Usar o caminho do arquivo zonas-trafego-sjc-sp-csv.csv
    df = pd.read_excel(path)

    # Use py class to convert between UTM to lat/long
    converter = GPointerConverteClass

    # Create a vector named coordenates where each line is a par of [long,lat]
    coordinates = []
    for row in df.iterrows():
        line = row[1]
        xcentroid = float(line['X_Centroid,N,11,4'])
        ycentroid = float(line['Y_Centroid,N,12,4'])
        tt = converter.convertUtmToLatLng(xcentroid, ycentroid, 23)
        lat = tt[0]
        long = tt[1]
        coordinates.append([long, lat])
    return coordinates

