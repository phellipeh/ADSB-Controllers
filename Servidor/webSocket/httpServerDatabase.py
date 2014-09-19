import psycopg2
import sys
import json
import time

try:
    con2 = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='Radar')
    cur2 = con2.cursor()
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def GetRealtimeAirplaneList():
    #ts = int(time.time()) - 60
    #cur2.execute("SELECT * FROM HexDataBase WHERE timestamp > "+str(ts)+" ORDER BY timestamp")
    cur2.execute("SELECT * FROM HexDataBase")
    #timestamp, hexicao, icao, callsign, lat, lon, alt, climb, head, velocidadegnd, utf
    columns = (
     'id_reg', 'timestamp', 'hex', 'icao', 'id', 'latitude', 'longitude', 'altitude', 'climb', 'head', 'velocidadegnd', 'utf' 
    ) #inclinacao, angulo, origem

    results = []
    for row in cur2.fetchall():
         results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2)

def GetAirplaneTrack(planehex):
    cur2.execute("SELECT * FROM HexDataBase WHERE hexicao = '"+str(planehex)+"' ORDER BY timestamp")

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
