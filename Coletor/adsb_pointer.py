import sys
import socket
import sqlite3 as sql
from datetime import datetime
import serial

ip_servidor = 'localhost'
porta_servidor = 5000
status_conec_serv = False

#Inicia Serial
try:
    s_com = serial.Serial('/dev/ttyS1', 19200)
except:
    print "Nao Foi Possivel conectar-se ao Receptor..."
    sys.exit(0)

#Inicia Banco de Dados Temporario
try:
    con = sql.connect('datadumptemp.db')
    try:
        cur = con.cursor()
    except sql.OperationalError, msg:
        print msg
        return "return: Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

#Conecta ao Servidor
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_servidor, porta_servidor))
    status_conec_serv = True
except:
    print "Nao foi possivel conectar-se ao servidor..."
    print "Ativando Armazenamento Local de Dados..."

#Loop Captura e envio dos Dados
while true:
    line = s_com.readline()
    if status_conec_serv == True:
#############Formatar os Dados############# em json
        client_socket.send(line)
    else:
        #Armazena os dados no Bando de Dados

#############Inserir os Dados#############   
        
        cur.execute("CREATE TABLE IF NOT EXISTS "+data[0]+"(Id integer primary key autoincrement, Data TEXT, Time TEXT, Date TEXT);")
        cur.execute("INSERT INTO "+data[0]+" (Data, Time, Date) VALUES('"+data[1]+"', '"+hr+"', '"+hj+"')")
        con.commit()

        #Verifica Conexao Novamente
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_servidor, porta_servidor))
            status_conec_serv = True
            #Envia todos os dados Armazenados Localmente
            print "Conectado ao Servidor..."

#############Enviar os Dados############# em json
            
            print "Todos os dados armazenados localmente foram enviados"
        except:
            print "Dados Armazenados Localmente.. Ainda nao foi possivel conexao com o servidor..."
