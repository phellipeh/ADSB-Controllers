import PyAdsbDecoder
import CRCCalc

f = file('log.txt', 'r')
'''
for data in f:
  print "-----------------------"
  print "Pacote: "+data

  if len(data) == 14+1:
     print "Pacote 56 Bits"
     if CRCCalc.parity56(data) == False:
         print "CRC - Invalido!"
     else:
         print "CRC - Valido!"
       
  
  print "\n\n"
'''
