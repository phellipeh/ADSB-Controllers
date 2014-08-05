
#
# TODO LIST
# - Fatiar os Dados em JSON e armazenar no Banco de Dados

import sockets
import sqlite3 as sql
import threading
import sys
import adsbDecoder

host = "localhost"
port = 3000
limit = 10

#Socket Server
print "Iniciando Socket Server... ",
try:
    sock = socket()
    sock.bind((host, port))
    sock.listen(limite)
    print "OK! Porta: "+str(port)
except Exception:
    print "Erro! Nao foi possivel iniciar servidor na porta" + str(Exception)
    sys.exit(1)

def clientthread(conn):
    while True:
        data=conn.recv(4096)
        ADSBDataDecoder(data) #retorna hex, alt, lat, e lon, (velocidade, nome, angulo)
        
#Socket server
while True:
    conn, addr = sock.accept()
    print time.strftime("%H:%M:%S") + " - Conexao com Client - IP:" + str(addr)
    start_new_thread(clientthread,(conn,))
