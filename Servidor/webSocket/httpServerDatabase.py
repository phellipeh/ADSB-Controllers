import psycopg2
import sys
import json

try:
    con2 = psycopg2.connect(host='localhost', user='postgres', password='root',dbname='Radar')
    cur2 = con2.cursor()
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def GetRealtimeAirplaneList():
    cur2.execute("SELECT * FROM HexDataBase")

    columns = (
     'hex', 'id', 'latitude', 'longitude', 'altitude', 'grau', 'timestamp'
    )

    results = []
    for row in cur2.fetchall():
         results.append(dict(zip(columns, row)))
    return json.dumps(results, indent=2)
