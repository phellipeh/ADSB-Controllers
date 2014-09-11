import os

def Update():
  pass
  '''
print 'Obtendo Versao do Sistema...'

f = file('versao.txt', '-r')
for linha in f:
  linha 
  os.system("wget http://update.radarlivre.ufc.br/"+modelo_e_endereco)
'''

Update()
print 'Iniciando Sistema Coletor...'

if os.name == 'nt':
  os.system("START ADSBCapture.py")
  os.system("START DBUploader.py")
else:
  os.system("ADSBCapture.py&")
  os.system("DBUploader.py")

