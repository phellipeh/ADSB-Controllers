#
# TODO LIST)
# - Salvar Dados toda hora
#

import sys
import sqlite3 as sql
import datetime
import serial
import json

#Inicia Serial
try:
    s_com = serial.Serial("COM9", 115200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, xonxoff=False, rtscts=False, dsrdtr=False)
except:
    print "Nao Foi Possivel conectar-se ao Receptor..."
    sys.exit(0)

#Inicia Banco de Dados Temporario
try:
    con = sql.connect('datadumptemp.db')
    try:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS HexDataBase (Hex TEXT, Data TEXT, DateTime TEXT);")
        con.commit()
    except sql.OperationalError, msg:
        print msg
        print "Erro ao inserir os dados no banco de dados."
except:
    print "Nao Foi Possivel conectar-se ao Banco de Dados Local..."
    sys.exit(0)

def SalvaHex(HexData):
    datetime_ = datetime.datetime.utcnow()
    cur.execute("INSERT INTO HexDataBase (Hex, DateTime) VALUES('"+HexData+"', '"+str(datetime_)+"')")
    con.commit()

print("Obtendo Versao do Receptor...")
s_com.write("#00\r\n")
k = s_com.readline()  
print "Retorno do Receptor: " + str(k)

print("Iniciando Recepcao de Dados...")
s_com.write("#43-02\r\n")
k = s_com.readline()
print "Retorno do Receptor: "+str(k)

#Loop Captura e envio dos Dados
while True:
    line = s_com.readline()
    data = line[14:]
    data = data[:-1]
    try:
     SalvaHex(line)  
    except:
     print "Erro ao Salvar Dados no Banco...."
