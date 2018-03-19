import psycopg2

def connectdb():
    host = "127.0.0.1"
    port = "5432"
    dbName = "hazard-mobility"
    user = "postgres"
    password = "123456"

    # query = "host=" + host + " port=" + port + " dbname=" + dbName + " user=" + user + " password=" + password
    query = "host=" + host + " port=" + port + " dbname=" + dbName + " user=" + user + " password="+ password
    handle = psycopg2.connect(query)
    return handle
