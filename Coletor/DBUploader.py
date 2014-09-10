import socket
import time
import sqlite3 as sql

ip_servidor = 'localhost'
porta_servidor = 5000
status_conec_serv = False
id_coletor = "RLC-0001A"
client_socket = ''

con = sql.connect('datadumptemp.db')
try:
    cur = con.cursor()
    con.commit()
except sql.OperationalError, msg:
    print msg
    print "Erro ao inserir os dados no banco de dados."

def LimpaHex():
    cur.execute("DELETE * FROM HexDataBase")
    con.commit()

def EnviaHex():
    cur.execute("SELECT * FROM HexDataBase")
    con.commit()
    recs = cur.fetchall()
    datetime_ = datetime.datetime.utcnow()
    array_send = [line, datetime_, datetime.datetime.utcnow(), id_coletor]
    client_socket.send(json.dumps(array_send))
    for rec in recs:
        try:
            client_socket.send(json.dumps(rec))
        except:
            TryConnect()
    LimpaHex()

def TryConnect(): #Conecta ao Servidor
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_servidor, porta_servidor))
        EnviaHex()
    except:
        print "Nao foi possivel conectar-se ao servidor... Tentando novamente em 5seg..."
        time.sleep(5)
        TryConnect()

TryConnect()
             
