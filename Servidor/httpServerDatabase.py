import sqlite3 as sql

try:
    con = sql.connect('ServerDataBase.db')
    try:
        cur = con.cursor()
        con.commit()
    except sql.OperationalError, msg:
        print msg
        return "return: Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def GetRealtimeAirplaneList():
    rtTimeStamp = Timestamp - 3
    recs = curs.fetchall()
    cur.execute("SELECT * FROM HexDataBase WHERE Timestamp > "+rtTimeStamp+" ")
    rows = [ dict(rec) for rec in recs ]
    return json.dumps(rows)
