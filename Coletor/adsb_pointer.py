#
# TODO LIST
# - Formatar os Dados em json (para streaming)
# - Inserir os Dados (no cache)
# - Enviar os Dados em json (do Cache)
#

import sys
import socket
import sqlite3 as sql
import datetime
import serial
import json

ip_servidor = 'localhost'
porta_servidor = 5000
status_conec_serv = False

#Inicia Serial
try:
    s_com = serial.Serial('COM1', 19200)
except:
    print "Nao Foi Possivel conectar-se ao Receptor..."
    sys.exit(0)

#Inicia Banco de Dados Temporario
try:
    con = sql.connect('datadumptemp.db')
    try:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS HexDataBase (Hex TEXT, Data TEXT, DateTime TEXT);")
        con.commit()
    except sql.OperationalError, msg:
        print msg
        print "Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def SalvaHex(HexData):
    datetime_ = datetime.datetime.utcnow()
    cur.execute("INSERT INTO HexDataBase (Hex, DateTime) VALUES('"+HexData+"', '"+str(datetime_)+"')")
    con.commit()

def RecuperaHex():
    cur.execute("SELECT * FROM HexDataBase")
    con.commit()
    recs = cur.fetchall()
    rows = [ dict(rec) for rec in recs ]
    return json.dumps(rows)

def LimpaHex():
    cur.execute("DELETE * FROM HexDataBase ")
    con.commit()

#Conecta ao Servidor
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_servidor, porta_servidor))
    status_conec_serv = True
except:
    print "Nao foi possivel conectar-se ao servidor..."
    print "Ativando Armazenamento Local de Dados..."

#Loop Captura e envio dos Dados
while True:
    line = s_com.readline()
    if status_conec_serv == True:
        try:
            datetime_ = datetime.datetime.utcnow()
            array_send = [line, datetime_ = datetime.datetime.utcnow()]
            client_socket.send(json.dumps(array_send))
        except:
            status_conec_serv = False
            SalvaHex(line)
    else:
        SalvaHex(line) #Armazena os dados no Bando de Dados
        
        try: #Verifica Conexao Novamente
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_servidor, porta_servidor))
            status_conec_serv = True
            #Envia todos os dados Armazenados Localmente
            print "Conectado ao Servidor..."
            client_socket.send(RecuperaHex())
            LimpaHex()
            print "Todos os dados armazenados localmente foram enviados"
        except:
            print "Dados Armazenados Localmente.. Ainda nao foi possivel conexao com o servidor..."
