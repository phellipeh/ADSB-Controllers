import psycopg2
import CRCCalc
import datetime
import sys
import time


#ID, TIMESTAMP, ICAO, CALLSING, LAT, LON, ALT, INCLINACAO, ORIENTACAO, VELOCIDADE_GND, UTF, 
#ID, TIMESTAMP, ICAO, CALLSING, LAT0, LON0, LAT1, LON1, ALT, INCLINACAO, ORIENTACAO, VELOCIDADE_GND, UTF

#id, timestamp, hexicao, icao, callsign, lat0, lon0, lat1, lon1, alt, climb, head, velocidadegnd, utf

#
# Temporary DataBase
#
try:
    con2 = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='Radar')
    try:
        cur2 = con2.cursor()
        cur2.execute('CREATE TABLE IF NOT EXISTS LoadedHexDump(id_reg serial primary key, timestamp bigint, hexicao text, icao text, callsign text, lat0 double precision, lon0 double precision, lat1 double precision, lon1 double precision, alt integer, climb integer, head integer, velocidadegnd double precision, utf text);')
        con2.commit()
    except Exception as ex:
        print ex
        print "return: Erro ao inserir os dados no banco de dados."
        sys.exit(0)
except Exception as ex:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local Para adsbDecoder..."
    print ex
    sys.exit(0)

def CreateAirplane(ICAO):
    ts = int(time.time())
    cur2.execute("INSERT INTO LoadedHexDump (timestamp, hexicao, icao, callsign, lat0, lon0, lat1, lon1, alt, climb, head, velocidadegnd, utf) VALUES('"+str(ts)+"', '"+ICAO+"', 'NULL', 'NULL', '0', '0', '0', '0', '0', '0', '0', '0', 'NULL')")
    con2.commit()   

def getAirplaneFullLog(ICAO):
    cur2.execute("SELECT callsign, alt, climb, head, velocidadegnd, utf FROM LoadedHexDump WHERE hexicao = '"+ICAO+"'")
    con2.commit()
    return cur2.fetchone()

def UpdateAirplanePosition_T0(ICAO, Data):
    cur2.execute("UPDATE LoadedHexDump SET lat0 = '"+str(Data[0])+"', lon0 = '"+str(Data[1])+"', alt = '"+str(Data[2])+"' WHERE hexicao = '"+ICAO+"'")
    con2.commit()

def UpdateAirplanePosition_T1(ICAO, Data):
    cur2.execute("UPDATE LoadedHexDump SET lat1 = '"+str(Data[0])+"', lon1 = '"+str(Data[1])+"', alt = '"+str(Data[2])+"' WHERE hexicao = '"+ICAO+"'")
    con2.commit()

def UpdateAirplaneID(ICAO, Data):
    cur2.execute("UPDATE LoadedHexDump SET callsign = '"+str(Data)+"' WHERE hexicao = '"+ICAO+"'")
    con2.commit()

def UpdateAirplaneAngle(ICAO, Data): 
    cur2.execute("UPDATE LoadedHexDump SET head = '"+str(Data[1])+"', velocidadegnd = '"+str(Data[0])+"', climb = '"+str(Data[2])+"' WHERE hexicao = '"+ICAO+"'")
    con2.commit()

def VerifyAllPositionDataExists(ICAO):
    cur2.execute("SELECT * FROM LoadedHexDump WHERE hexicao = '"+ICAO+"' AND lat0 != '0' AND lat1 != '0' AND lon0 != '0' AND lon1 != '0'")
    if cur2.fetchone() == None:
        return False
    else:
        return True

def GetPositionData(ICAO):
    cur2.execute("SELECT lat0, lat1, lon0, lon1 FROM LoadedHexDump WHERE hexicao = '"+ICAO+"'")
    con2.commit()
    return cur2.fetchone()

def FindICAOExists(ICAO):
    cur2.execute("SELECT callsign, alt, head, utf FROM LoadedHexDump WHERE hexicao = '"+ICAO+"'")
    if cur2.fetchone() != None:
        return True
    else:
        return False

#
#DataBase Final
#

#id, timestamp, hexicao, icao, callsign, lat, lon, alt, climb, head, velocidadegnd, utf

try:
    con = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='Radar')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS HexDataBase (id_reg serial primary key, timestamp bigint, hexicao TEXT, icao text, callsign TEXT, lat double precision, lon double precision, alt integer, climb integer, head integer, velocidadegnd double precision, utf text);")
    con.commit()
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def getLastPositionReport(ICAO):
    cur.execute("SELECT lat, lon FROM HexDataBase WHERE HexICAO = '"+ICAO+"' ORDER BY timestamp LIMIT 1")
    if cur.fetchone() != None:
        try:
         return (cur.fetchone())
        except:
         print "erro"
    else:
        ret = [0, 0]
        return ret

def RealTimeFullAirplaneFeed(Data):
    ts = int(time.time())
    cur.execute("INSERT INTO HexDataBase (timestamp, hexicao, icao, callsign, lat, lon, alt, climb, head, velocidadegnd, utf) VALUES ('"+str(ts)+"', '"+Data[0]+"', 'NULL', '"+Data[1]+"', '"+str(Data[2])+"', '"+str(Data[3])+"', '"+str(Data[4])+"', '"+str(Data[5])+"', '"+str(Data[6])+"', '"+str(Data[7])+"', '"+str(Data[8])+"')")
    con.commit()
#
# Log das informacoes
#

try:
    con2 = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='Radar')
    try:
        cur2 = con2.cursor()
        cur2.execute("CREATE TABLE IF NOT EXISTS ColetorDataRegistred (IDColetor TEXT, Format TEXT, Data TEXT, Timestamp bigint);")
        con2.commit()
    except Exception as ex:
        print ex
        print "return: Erro ao inserir os dados no banco de dados."
        sys.exit(0)
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local Para adsbDecoder..."
    sys.exit(0)

def DumpColetores(Data):
    ts = int(time.time())
    cur.execute("INSERT INTO ColetorDataRegistred (IDColetor, Format, Data, Timestamp) VALUES ('"+Data[0]+"', '"+Data[1]+"', '"+Data[2]+"' ,'"+str(ts)+"')")
    con.commit()
