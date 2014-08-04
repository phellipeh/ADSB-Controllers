import sqlite3 as sql

#
# Temporary DataBase
#

try:
    con2 = sql.connect('ADSBDecodedDataBase.db')
    try:
        cur2 = con2.cursor()
        cur2.execute("CREATE TABLE IF NOT EXISTS LoadedHexDump (Hex TEXT, F TEXT, Lat0 TEXT, Lon0 TEXT, Lat1 TEXT, Lon1 TEXT, Alt TEXT, DateTime TEXT);")
        con2.commit()
    except sql.OperationalError, msg:
        print msg
        return "return: Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def CreateAirplane(ICAO):
    cur2.execute("INSERT INTO LoadedHexDump (HexICAO, F, Lat0, Lon0, Lat1, Lon1, Alt, UTF, Timestamp) VALUES('"+air_data[0]+"', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')")
    con.commit()   

def UpdateAirplanePosition_T0(ICAO, Data):

def UpdateAirplanePosition_T1(ICAO, Data):

def UpdateAirplaneID(ICAO, Data):

def UpdateAirplaneSpeedAndAngle(ICAO, Data):
    
def FindICAOExists(ICAO):
    #verifica se existe e retorna boolean

#
#DataBase Final
#

try:
    con = sql.connect('ServerDataBase.db')
    try:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS HexDataBase (Hex TEXT, Lat TEXT, Lon TEXT, Alt TEXT, Grau TEXT, DateTime TEXT);")
        con.commit()
    except sql.OperationalError, msg:
        print msg
        return "return: Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def RealTimeFullAirplaneFeed(Data):
    datetime_ = datetime.datetime.utcnow()
    cur.execute("INSERT INTO HexDataBase (HexICAO, Lat, Lon, Alt, Grau, UTF, Timestamp) VALUES('"+air_data[0]+"', '"+air_data[1]+"', '"+air_data[2]+"', '"+air_data[3]+"', '"+str(datetime_)+"')")
    con.commit()
    
