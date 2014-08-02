#
# ADS-B Decoder in Python
# Felipe Sousa Rocha, 1/8/2024
#

import math

#
# TODO LIST
# - Calculo da Latitude
# - Calculo da Longitude
# - Identificar outros extended squitter packets
# - Identificar Velocidade e Direcao da Aeronave
# - Identificar Nome do Voo
# - Identificar Funcoes do ICAO, DF, CA

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

def ADSBDataDecoder(data):
    DFCA = toHex(data[:2])                                       #Primeiro Byte para DF+CA
    DF = full_bit_zero(bin(eval(DFCA)))[:5]
    DF = eval("0b" + DF) 
    CA = full_bit_zero(bin(eval(DFCA)))[5:]
   
    ICAO = "0x"+data[2]+data[3]+" 0x"+data[4]+data[5]+" 0x"+data[6]+data[7]     #Tres bytes para ICAO
    b_TC = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[:5]                 #Cinco bits para o Type Code
    b_Mode = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[5:]               #Tres bits para o mode

    if DF == 17:
        print "1090 Extended Squitter - ADS-B"
    
        if b_TC == "01011":
            print "Airborne Position message... Obtendo Dados (Altitude, Latitude e Longitude)"
            hex_adsb_packet = data[10:]
            bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])

            Altitude = "0b" + bin_adsb_packet[:12]
            Latitude = eval("0b" + bin_adsb_packet[14:][:17])
            Longitude =  eval("0b" + bin_adsb_packet[31:][:17])
            T = bin_adsb_packet[:13][:1]
            F = bin_adsb_packet[:14][:1]
            
            print "T: "+T
            
            if F == '0':
                print "Even Packet"
            elif F == '1':
                print "Odd Packet"
            
            print "(nao calculado)  Altitude: " + str(Altitude)
            print "(nao calculado)  Latitude: " + str(Latitude)
            print "(nao calculado) Longitude: " + str(Longitude)

            #math.floor(((59 * Lat(0) - 60 * Lat(1)) / 131072) + 0.5)

ADSBDataDecoder("8d4008f15837f237ebe3a3")
