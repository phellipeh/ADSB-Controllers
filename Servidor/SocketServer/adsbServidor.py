import select
from socket import * 
import thread
import sys
import PyAdsbDecoder
import PyAdsbDecoderDatabase
import time
import json
import ServerReport
import signal

if __name__ == "__main__":

    CONNECTION_LIST = []
    RECV_BUFFER = 4096 
    PORT = 5000

    try:
        server_socket = socket()
        server_socket.bind(("localhost", PORT))
        server_socket.listen(10)
        CONNECTION_LIST.append(server_socket)
        print "Servidor iniciado na porta: " + str(PORT)
    except Exception as ex:
        ServerReport.report('adsbServidor', '0', str(ex))
 
    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        try:
                            if 'Online: ' not in data:
                                #PyAdsbDecoderDatabase.DumpColetores(data)
                                dp = json.loads(data)
                                print data
                            
                                if dp[3] == 'ADSBHEXDATA':

                                    # Obter Timestamp Frame vindo do Coletor
                                    # Obter Lat e Long o Coletor e repassar para o DataDecoder
                                    
                                    dp2 = json.loads(dp[0]) #obtem o conteudo do pacote
                                    for z in dp2:
                                        PyAdsbDecoder.ADSBDataDecoder(z[0])

                                if dp[3] == 'JSONDATA':
                                    print "Nao implementado"
                                        
                        except Exception as ex:
                            print ex
                            
                except:
                    print "Client (%s, %s) is offline" % addr
                    ServerReport.report('adsbServidor', '2', 'Queda de Conexao com Coletor - '+str(addr))
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
         
    server_socket.close()
