import PyAdsbDecoder

f = file('log.txt', 'r')
for data in f:
  print "-----------------------\nPacote: "+data
  PyAdsbDecoder.ADSBDataDecoder(data) #retorna hex, alt, lat, e lon, (velocidade, nome, angulo)
  print "\n\n\n"
