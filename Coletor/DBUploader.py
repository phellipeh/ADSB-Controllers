import socket
import datetime
import time
import sqlite3 as sql
import json

ip_servidor = 'localhost'
porta_servidor = 5000
id_coletor = "RLC-0001A"
formato = 'RAW-ADS-B'
latitude = 0
longitude = 0

con = sql.connect('datadumptemp.db')
try:
    cur = con.cursor()
    con.commit()
except sql.OperationalError, msg:
    print msg
    print "Erro ao inserir os dados no banco de dados."

def LimpaHex(limiteTS):
    cur.execute("DELETE * FROM HexDataBase WHERE id_reg <" +limiteTS)
    print "1"
    con.commit()

def TryConnect(): #Conecta ao Servidor
    lastid = 0
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_servidor, porta_servidor))
        while True:
            cur.execute("SELECT * FROM HexDataBase")
            con.commit()
            recs = cur.fetchall()
            for k in recs:
                lastid = k[0]
            dt = time.time()
            array_send = [json.dumps(recs), dt, id_coletor, formato, latitude, longitude]
            senddata = str(json.dumps(array_send))
            try:
                client_socket.send(senddata)
                LimpaHex(lastid)
            except Exception as ex:
                print "2"
                print ex
                TryConnect()
            time.sleep(0.5)
    except Exception as ex:
        print ex
        print "Nao foi possivel conectar-se ao servidor... Tentando novamente em 5seg..."
        time.sleep(5)
        TryConnect()

TryConnect()
             
