#
# ADS-B Decoder in Python
# Felipe Sousa Rocha, 1/8/2024
#

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

def ADSBDataDecoder(data):
    DFCA = toHex(data[:2])                                                      #Primeiro Byte para DF+CA
    ICAO = "0x"+data[2]+data[3]+" 0x"+data[4]+data[5]+" 0x"+data[6]+data[7]     #Tres bytes para ICAO
    b_TC = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[:5]                 #Um Byte para o Type Code
    
    if b_TC == "01011":
        print "Airborne Position message... Obtendo Dados (Altitude, Latitude e Longitude)"
        hex_adsb_packet = data[10:]
        bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])

        Altitude = eval("0b" + bin_adsb_packet[:12])
        '''Latitude = eval("0b" + Latitude)
        Longitude =  eval("0b" + Longitude)
'''
        print "Altitude: " + str(Altitude)
        print "(Dec) Latitude:  " + str(Latitude)
        print "(Dec) Longitude: " + str(Longitude)

    


        
    elif b_TC == "10011":
        print "Airborne Velocity message"

    
    
ADSBDataDecoder("8d4008f15837f237ebe3a3")
