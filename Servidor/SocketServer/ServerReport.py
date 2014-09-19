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
  f.write(now + " - "+modulo+" - "+tipo+" - "+msg)
  f.close()
