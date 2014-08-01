import sockets
import sqlite3
import threading
import sys

host = "localhost"
port = 3000
limit = 10

def InsertOnDatabase(data):
#############Fatiar os Dados em JSON e armazenar no Banco de Dados#############
    pass

#Banco de Dados
try:
    con = sql.connect('ServerDataBase.db')
    try:
        cur = con.cursor()
    except sql.OperationalError, msg:
        print msg
        return "return: Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

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
        t=conn.recv(1024)
        InsertOnDatabase(t)
        
#Socket server
while True:
    conn, addr = sock.accept()
    print time.strftime("%H:%M:%S") + " - Conexao com Client - IP:" + str(addr)
    start_new_thread(clientthread,(conn,))
