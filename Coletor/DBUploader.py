import socket
import datetime
import time
import sqlite3 as sql
import json

ip_servidor = 'localhost'
porta_servidor = 5000
id_coletor = "RLC-0001A"
formato = 'ADSBHEXDATA' #JSONDATA or #XMLDATA or ADSBHEXDATA
latitude = 0
longitude = 0
log = True

con = sql.connect('datadumptemp.db')
try:
    cur = con.cursor()
    con.commit()
except sql.OperationalError, msg:
    if log == True:
        print msg
        print "Erro ao inserir os dados no banco de dados."
    exit()

def LimpaHex(limiteTS):
    cur.execute("DELETE FROM HexDataBase WHERE DateTime < '" +str(limiteTS)+"'")
    con.commit()

def TryConnect(): #Conecta ao Servidor
    lastid = 0
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_servidor, porta_servidor))
        print "Conectado"
        while True:
            cur.execute("SELECT * FROM HexDataBase")
            con.commit()
            recs = cur.fetchall()
            if str(recs) != '[]':
                for k in recs:
                    lastid = k[0]
                dt = time.time()
                array_send = [json.dumps(recs), dt, id_coletor, formato, latitude, longitude]
                senddata = str(json.dumps(array_send))
                try:
                    if log == True:
                        print "Enviando Dados."
                    client_socket.send(senddata)
                    LimpaHex(lastid)
                except Exception as ex:
                    if "no such table:" not in str(ex):
                        if log == True:
                            print ex
                        TryConnect()
                    else:
                        client_socket.close()
                        TryConnect()
            else:
                if log == True:
                    print "Nenhum dado no momento - No aguardo."
                try:
                    client_socket.send('Online: '+id_coletor)
                except:
                    client_socket.close()
                    TryConnect()
            time.sleep(0.5)
            
    except Exception as ex:
        if "no such table:" in str(ex):
            if log == True:
                print "Erro no DB: "+str(ex)
                print "Conexao Encerrada"
            client_socket.close()
        else:
            if log == True:
                print ex
                print "Nao foi possivel conectar-se ao servidor... Tentando novamente em 5seg..."
            time.sleep(5)
            client_socket.close()
            TryConnect()
        
if log == True:
    print "Iniciando Envio de Dados - Aguardando Conexao."
    
TryConnect()
             
