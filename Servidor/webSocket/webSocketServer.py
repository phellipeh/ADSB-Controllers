from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import httpServerDatabase

class ADSBDataEcho(WebSocket):

        def handleMessage(self):
            if self.data == 'GET':
                self.sendMessage(str(httpServerDatabase.GetRealtimeAirplaneList()))

        def handleConnected(self):
            print self.address, ' Conectado'
            self.sendMessage(str(httpServerDatabase.GetRealtimeAirplaneList()))
            

        def handleClose(self):
            print self.address, ' Desconectado'

server = SimpleWebSocketServer('', 9999, ADSBDataEcho)
server.serveforever()
