'''
  Tipos:
  0 - General Exception
  1 - Alerta
  2 - Queda
'''

from datetime import datetime

def report(modulo, tipo, msg):
  f = file('report.log', 'a')
  now = datetime.now()
  f.write(str(now) + " - "+modulo+" - "+tipo+" - "+msg+"\n")
  f.close()
