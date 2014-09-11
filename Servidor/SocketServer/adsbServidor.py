
#
# TODO LIST
# - Fatiar os Dados em JSON e armazenar no Banco de Dados

from socket import * 
import thread
import sys
import PyAdsbDecoder
import PyAdsbDecoderDatabase
import time
import json

host = 'localhost'
port = 5000
limite = 10
data = ''

#Socket Server
print "Iniciando Socket Server... ",
try:
    sock = socket()
    sock.bind((host, port))
    sock.listen(limite)
    print "OK! Porta: "+str(port)
except Exception as ex:
    print "Erro! Nao foi possivel iniciar servidor na porta...\n" + str(ex)
    sys.exit(1)

def clientthread(conn):
    while True:
        try:
            data=conn.recv(4096)
        except:
            print "O Receptor esta OFF - Conexao Encerrada"
            sock.close()
        
        PyAdsbDecoderDatabase.DumpColetores(data)
        dp = json.loads(data)
        print dp
        
        if dp[3] == 'ADSBHEXDATA':
            dp2 = json.loads(dp[0])
            for z in dp2:
                print "adsbpack"+z[0]
                PyAdsbDecoder.ADSBDataDecoder(z[0]) #retorna hex, alt, lat, e lon, (velocidade, nome, angulo)
        
        
#Socket server
while True:
    conn, addr = sock.accept()
    print time.strftime("%H:%M:%S") + " - Conexao com Client - IP:" + str(addr)
    thread.start_new_thread(clientthread,(conn,))
