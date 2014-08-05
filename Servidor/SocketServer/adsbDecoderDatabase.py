import psycopg2
import datetime
import time

#
# Temporary DataBase
#

try:
    con2 = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='Radar')
    try:
        cur2 = con2.cursor()
        cur2.execute("CREATE TABLE IF NOT EXISTS LoadedHexDump (HexICAO TEXT, id_ TEXT, Lat0 TEXT, Lon0 TEXT, Lat1 TEXT, Lon1 TEXT, Grau TEXT, Alt TEXT, UTF TEXT, Timestamp TEXT);")
        con2.commit()
    except sql.OperationalError, msg:
        print msg
        print "return: Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local Para adsbDecoder..."
    sys.exit(0)

def CreateAirplane(ICAO):
    ts = int(time.time())
    cur2.execute("INSERT INTO LoadedHexDump (HexICAO, id_, Lat0, Lon0, Lat1, Lon1, Grau, Alt, UTF, Timestamp) VALUES('"+ICAO+"', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', '"+str(ts)+"')")
    con2.commit()   

def getAirplaneFullLog(ICAO):
    cur2.execute("SELECT id_, Alt, Grau, UTF FROM LoadedHexDump WHERE HexICAO = '"+ICAO+"'")
    con2.commit()
    return cur2.fetchone()

#Update MESMO!
def UpdateAirplanePosition_T0(ICAO, Data):
    cur2.execute("UPDATE LoadedHexDump SET Lat0 = '"+str(Data[0])+"', Lon0 = '"+str(Data[1])+"', Alt = '"+str(Data[2])+"' WHERE HexICAO = '"+ICAO+"'")
    con2.commit()

def UpdateAirplanePosition_T1(ICAO, Data):
    cur2.execute("UPDATE LoadedHexDump SET Lat1 = '"+str(Data[0])+"', Lon1 = '"+str(Data[1])+"', Alt = '"+str(Data[2])+"' WHERE HexICAO = '"+ICAO+"'")
    con2.commit()

def UpdateAirplaneID(ICAO, Data):
    cur2.execute("UPDATE LoadedHexDump SET id_ = '"+str(Data[0])+"' WHERE HexICAO = '"+ICAO+"'")
    con2.commit()

def UpdateAirplaneAngle(ICAO, Data):
    cur2.execute("UPDATE LoadedHexDump SET Grau = '"+str(Data[0])+"' WHERE HexICAO = '"+ICAO+"'")
    con2.commit()

def VerifyAllPositionDataExists(ICAO):
    cur2.execute("SELECT * FROM LoadedHexDump WHERE HexICAO = '"+ICAO+"' AND Lat0 != 'NULL' AND Lat1 != 'NULL' AND Lon0 != 'NULL' AND Lon1 != 'NULL'")
    if cur2.fetchone() == None:
        return False
    else:
        return True

def GetPositionData(ICAO):
    cur2.execute("SELECT Lat0, Lat1, Lon0, Lon1 FROM LoadedHexDump WHERE HexICAO = '"+ICAO+"'")
    con2.commit()
    return cur2.fetchone()
      
def FindICAOExists(ICAO):
    cur2.execute("SELECT id_, Alt, Grau, UTF FROM LoadedHexDump WHERE HexICAO = '"+ICAO+"'")
    if cur2.fetchone() != None:
        return True
    else:
        return False
    #verifica se existe e retorna boolean
    
#
#DataBase Final
#

import psycopg2

try:
    con = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='Radar')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS HexDataBase (HexICAO TEXT, id_ TEXT, Lat TEXT, Lon TEXT, Alt TEXT, Grau TEXT, UTF TEXT, Timestamp TEXT);")
    con.commit()
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def RealTimeFullAirplaneFeed(Data):
    ts = int(time.time())
    cur.execute("INSERT INTO HexDataBase (HexICAO, id_ , Lat, Lon, Alt, Grau, UTF, Timestamp) VALUES ('"+Data[0]+"', '"+Data[1]+"', '"+str(Data[2])+"', '"+str(Data[3])+"', '"+str(Data[4])+"', '"+str(Data[5])+"', '"+str(Data[6])+"', '"+str(ts)+"')")
    con.commit()
