import psycopg2
import sys
import json
import time

try:
    con2 = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='radar')
    cur2 = con2.cursor()
except Exception as ex:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    print ex
    sys.exit(0)

results = []
hexIcao = []

def findArray(zi):
    for i in hexIcao:
        if i == zi:
            return True
    return False

def GetRealtimeAirplaneList():
    ts = int(time.time()) - 60
    cur2.execute("SELECT * FROM HexDataBase WHERE timestamp >= "+str(ts)+" ORDER BY timestamp DESC")
    #cur2.execute("SELECT * FROM HexDataBase ORDER BY timestamp DESC")
    columns = (
     'id_reg', 'timestamp', 'hex', 'icao', 'id', 'latitude', 'longitude', 'altitude', 'climb', 'head', 'velocidadegnd', 'utf' 
    )
    
    for row in cur2.fetchall():
        if findArray(row[2]) == False:
            results.append(row)
            hexIcao.append(row[2])
    
    s = []
    for resultz in results:
        s.append(dict(zip(columns, resultz)))
    del results[:]
    del hexIcao[:]
    resultz = []    
    return json.dumps(s, indent=2)

def GetAirplaneTrack(planehex):
    cur2.execute("SELECT * FROM HexDataBase WHERE hexicao = '"+str(planehex)+"' ORDER BY timestamp DESC")

    columns = (
     'id_reg', 'timestamp', 'hex', 'icao', 'id', 'latitude', 'longitude', 'altitude', 'climb', 'head', 'velocidadegnd', 'utf'
    )

    results = []
    for row in cur2.fetchall():
         results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2)

def SearchFlight(FlightName):
    cur2.execute("SELECT * FROM HexDataBase WHERE id_ = '"+str(FlightName)+"' ORDER BY timestamp DESC LIMIT 1")

    columns = (
     'hex', 'latitude', 'longitude'
    )

    results = []
    for row in cur2.fetchall():
         results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2)

def GetListAirports():
    cur2.execute("SELECT * FROM airportlist")
    #timestamp, hexicao, icao, callsign, lat, lon, alt, climb, head, velocidadegnd, utf
    columns = (
     'icao', 'name', 'state', 'city', 'latitude', 'longitude' 
    ) #inclinacao, angulo, origem

    results = []
    for row in cur2.fetchall():
         results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2)
