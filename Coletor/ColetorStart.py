import os

'''
print 'Obtendo Versao do Sistema...'

f = file('versao.txt', '-r')
for linha in f:
  linha 
  os.system("wget http://update.radarlivre.ufc.br/"+modelo_e_endereco)
'''
print 'Iniciando Sistema Coletor...'
os.system("DBUploader.py&")
os.system("ADSBCapture.py")
