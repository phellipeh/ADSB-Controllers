from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import httpServerDatabase

class ADSBDataEcho(WebSocket):

        def handleMessage(self):
            if self.data == 'GET':
                try:
                        self.sendMessage("get_return:"+str(httpServerDatabase.GetRealtimeAirplaneList()))
                except Exception as ex:
                        print "Exception: " + str(ex)

            elif self.data == 'GETAirports':
                try:
                        self.sendMessage("return_airport:"+str(httpServerDatabase.GetListAirports()))
                except Exception as ex:
                        print "Exception: " + str(ex)

            elif 'getroute(' in self.data:
                icao = self.data.replace("getroute(","")
                icao = icao.replace(")","")
                try:
                        self.sendMessage("getroute_return:"+str(httpServerDatabase.GetAirplaneTrack(icao)))
                except Exception as ex:
                        print "Exception: " + str(ex)

            elif 'buscar(' in self.data:
                    FlightName = self.data.replace("buscar(","")
                    FlightName = FlightName.replace(")","")
                    self.sendMessage("search_return:"+SearchFlight(FlightName))

        def handleConnected(self):
            print self.address, ' Conectado'

        def handleClose(self):
            print self.address, ' Desconectado'


print "Iniciando..."
try:
 server = SimpleWebSocketServer('', 9999, ADSBDataEcho)
 print "Servidor Iniciado na porta 9999"
 server.serveforever()
except Exception as ex:
 print "Exception: " + str(ex)
