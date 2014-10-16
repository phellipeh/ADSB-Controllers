import PyAdsbDecoder

print "Lendo o Log"

f = file("adsblog.log", "r")
for linha in f:
    linha = linha.replace('\n', '')
    print len(linha)
    PyAdsbDecoder.ADSBDataDecoder(str(linha))

