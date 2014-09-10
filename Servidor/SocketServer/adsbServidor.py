
#
# TODO LIST
# - Fatiar os Dados em JSON e armazenar no Banco de Dados

from socket import * 
import threading
import sys
import PyAdsbDecoder
import PyAdsbDecoderDatabase

host = 'localhost'
port = 5000
limite = 10

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
        data=conn.recv(4096)
        PyAdsbDecoder.ADSBDataDecoder(data) #retorna hex, alt, lat, e lon, (velocidade, nome, angulo)
        PyAdsbDecoderDatabase.DumpColetores(data)
        
#Socket server
while True:
    conn, addr = sock.accept()
    print time.strftime("%H:%M:%S") + " - Conexao com Client - IP:" + str(addr)
    start_new_thread(clientthread,(conn,))
