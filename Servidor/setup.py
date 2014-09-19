import os
import time
import shutil
import string
from ctypes import windll

'''

You can achieve without external tools this by creating a temporary VBScript:

@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\myshortcut.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "D:\myfile.extension" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%
(Idea taken from here.)

This will create myshortcut.lnk on the Desktop, pointing to D:\myfile.extension.

You can supply additional properties before saving the link by modifying the following values:

oLink.Arguments
oLink.Description
oLink.HotKey
oLink.IconLocation
oLink.WindowStyle
oLink.WorkingDirectory


'''

#Criar e inserir em DB dados sobre voos e aeroportos

# Fazer verificacao de componentes do sistema (memoria, proc, proc bits)
setup_path = [':\RadarLivre', '/usr/RadarLivreServer']

def copyFile(src, dest):
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

def detectpsycopg2():
  try:
    import psycopg2
    print "Biblioteca Psycopg2 - OK!"
  except:
    print "Instalacao Calcelada!\n\nEste computador nao possui a Biblioteca Psycopg2 instalado.\nEfetue a instalacao da biblioteca para prosseguir com a instalacao do sistema."
    raw_input('Pressione uma tecla para sair...')
    exit()

def detectpostgre():
  has = True
  if has == True:
    print "PostgreSQL Database - OK!"
  else:
    print "Instalacao Calcelada!\n\nEste computador nao possui o PostgreSQL instalado.\nEfetue a instalacao da biblioteca para prosseguir com a instalacao do sistema."
    raw_input('Pressione uma tecla para sair...')
    exit()

def detectpyversion():
  has = True
  if has == True:
    print "Python 2.7 - OK!"
  else:
    print "Instalacao Calcelada!\n\nEste computador nao possui a versao 2.7 do Python. Efetue a instalacao para prosseguir."
    raw_input('Pressione uma tecla para sair...')
    exit()

def Menu1():
  print "Instalacao do Radar Livre"

def DetectarComponentes():
  detectpyversion()
  detectpostgre()
  detectpsycopg2()

''' sc config MyProgramName binpath= "cmd.exe /c C:\MyFolder\MyProgram.exe" type= own start= auto DisplayName= "My Sample Program" '''

'''
$ cat /etc/event.d/mudat 
start on runlevel 2 
exec echo "Entering multiuser mode on " $(date) > /tmp/mudat.out
'''


def DefinirComoStartService():
  if os.name == 'nt':
      pass    
  else:
      pass

def IniciarInstalacao(setuppath):
  print "\n\nLocal de Instalacao: " + setuppath
  print "Espaco Utilizado " + str((get_size('./httpServer')+get_size('./SocketServer')+get_size('./webSocket'))) + " kb\n\n"

  os.makedirs(setuppath)  

  setStart = raw_input("Executar programa ao iniciar o sistema operacional? (S/N): ")
  if setStart == 's' or setStart == 'S':
    DefinirComoStartService()

  #funcao de copiar arquivos
  
  #exibir msg

def DetectarInstalacao(setuppath):

  if os.path.exists(setuppath):
     setUn = raw_input("Deseja remover o Radar Livre do Computador? (S/N): ")
     if setUn == 's' or setUn == 'S':
       IniciarUnstalacao(setuppath) # sc delete MyProgramName
     else:
       exit()

def main():
  print "Instalacao do Radar Livre...\n----------------------------\n"
  #DetectarInstalacao()
  print "Executando Busca por componentes para o funcionamento do sistema.."
  DetectarComponentes()
  
  if os.name == 'nt':
    print "\nInsira a Letra do Disco onde voce deseja efetuar a instalacao do sistema... Ex: C para C:\\"
    disco = str(raw_input("> "))
    setuppath = disco + setup_path[0]
    IniciarInstalacao(setuppath)
  elif os.name == 'posix':
    IniciarInstalacao(setup_path[1])
    
main()
