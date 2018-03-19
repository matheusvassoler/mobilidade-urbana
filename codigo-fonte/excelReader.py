import databaseConnection
import pandas as pd


def includeZonasDatabase(fileExcel):
    postgre = databaseConnection.connectdb()
    cursor = postgre.cursor()




    # Usar o caminho do arquivo zonas-trafego-sjc-sp-csv.csv
    df = pd.read_excel(fileExcel)

    # salva no banco de dados os dados da tabela do excel
    for row in df.iterrows():
        val0, val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12 = row[1]
        cursor.execute("INSERT INTO excel (zonatrafego, pop_ibge, dom_ibge, macrozona, nome_zt, pop_od, dom_od, perc_pop, perc_dom, area_km, x_centroid, y_centroid, pop_area) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(str(val0), str(val1), str(val2), str(val3), str(val4), str(val5), str(val6), str(val7), str(val8), str(val9), str(val10), str(val11), str(val12)))

    postgre.commit()
    cursor.close()


class Spreadsheet_Excel_Reader:

    sheets = []
    colnames = []

    def getCol(self, col):
        if (isinstance(col,str)):
            col = col.lower()
        if (col in self.colnames):
            col = self.colnames[col]
        return col

    def rowcount(self, sheet):
        return self.sheets[sheet]['numRows']

    def val(self, row, col, sheet = 0):
        col = self.getCol(col)
        if row in self.sheets[sheet]['cells'] and col in self.sheets[sheet]['cells'][row]:
            return self.sheets[sheet]['cells'][row][col]
        else:
            return ""

    def xValue(self, row):
        postgres = databaseConnection.connectdb()
        cursor = postgres.cursor()
        cursor.execute("SELECT x_centroid FROM excel where id = %d" %row)
        return cursor.fetchone()

    def yValue(self, row):
        postgre = databaseConnection.connectdb()
        cursor = postgre.cursor()
        cursor.execute("SELECT y_centroid FROM excel where id = %d" %row)
        return cursor.fetchone()