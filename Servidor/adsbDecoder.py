#
# ADS-B Decoder in Python
# Felipe Sousa Rocha, 1/8/2024
#

import math

#
# TODO LIST
# - Calculo da Latitude                             Vai para o WebClient
# - Calculo da Longitude                            Vai para o WebClient
# - Identificar outros extended squitter packets    OK
# - Identificar Velocidade e Direcao da Aeronave    Cancel
# - Identificar Nome do Voo                         Cancel
# - Identificar Funcoes do ICAO, DF, CA             OK
# - Verificar Paridade

def toHex(x):
    return hex(eval("0x" + x))

def toBin(x):
    return bin(eval("0b" + x))

def full_bit_zero(data):
    data = data[2:]
    falta = 8 - len(data)
    for x in range(0, falta):
        data= '0' + data
    return data

def c(d1, d2):
    return full_bit_zero(bin(eval(toHex(d1+d2))))

def mod(a, b):
    return a % b

def ADSBParity(P, ICAO):
   # PI = ICAO[24]+ICAO[23]+ICAO[22]+ICAO[21]+ICAO[20]+ICAO[19]+ICAO[18]+ICAO[17]+ICAO[16]+ICAO[15]+ICAO[14]+ICAO[13]+ICAO[10]+ICAO[3]+1
   pass


    

def ADSBDataDecoder(data):
    ICAO = data[2]+data[3]+data[4]+data[5]+data[6]+data[7]

    #if ADSBParity(ICAObits) == False:
    #    return False
    
    DFCA = toHex(data[:2])                                       #Primeiro Byte para DF+CA
    DF = full_bit_zero(bin(eval(DFCA)))[:5]
    DF = eval("0b" + DF) 
    CA = full_bit_zero(bin(eval(DFCA)))[5:]
   
    b_TC = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[:5]                 #Cinco bits para o Type Code
    b_Mode = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[5:]               #Tres bits para o mode

    if DF == 17:
        print "1090 Extended Squitter - ADS-B"
        if b_TC == "01011":
            print "Airborne Position message... Obtendo Dados (Altitude, Latitude e Longitude)"
            hex_adsb_packet = data[8:]
            bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13])

            Altitude = "0b" + bin_adsb_packet[8:][:12]
            Latitude = eval("0b" + bin_adsb_packet[22:][:17])            
            Longitude =  eval("0b" + bin_adsb_packet[-17:])

            T = bin_adsb_packet[20:][0]
            F = bin_adsb_packet[21:][0]

            if T == '1':
                print "UTC Syncronized"
            
            if F == '0':
                print "Even Packet"
            elif F == '1':
                print "Odd Packet"

            print "ICAO Hex Address: " + ICAO
            print "(nao calculado)  Altitude: " + str(Altitude)
            print "(nao calculado)  Latitude: " + str(Latitude)
            print "(nao calculado) Longitude: " + str(Longitude)

            #math.floor(((59 * Lat(0) - 60 * Lat(1)) / 131072) + 0.5)

ADSBDataDecoder("8D75804B580FF2CF7E9BA6F701D0")
print ""
ADSBDataDecoder("8D75804B580FF6B283EB7A157117")
