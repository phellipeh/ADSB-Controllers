#
# ADS-B Decoder in Python
# Felipe Sousa Rocha, 1/8/2024
#

def toHex(x):
    return hex(eval("0x" + x))

def toBin(x):
    return bin(eval("0b" + x))

def ADSBDataDecoder(data):
    #Primeiro Byte para DF+CA
    DFCA = toHex(data[0]+data[1])

    #Dois bytes para ICAO
    ICAO = "0x"+data[2]+data[3]+" 0x"+data[4]+data[5]+" 0x"+data[6]+data[7]

    #Cinco Bytes para ADSB Data
    ADSB_Data = "0x"+data[8]+data[9]+" 0x"+data[10]+data[11]+" 0x"+data[12]+data[13]+" 0x"+data[14]+data[15]+" 0x"+data[16]+data[17]+" 0x"+data[18]+data[19]+" 0x"+data[20]+data[21]

    b_DFCA = bin(eval(DFCA))
    DF = b_DFCA[2]+b_DFCA[3]+b_DFCA[4]+b_DFCA[5]+b_DFCA[6]
    CA = b_DFCA[7]+b_DFCA[8]+b_DFCA[9]

    TC = toHex(data[8]+data[9])
    b_TC = bin(eval(TC))
    b_TC = b_TC[2]+b_TC[3]+b_TC[4]+b_TC[5]+b_TC[6]

    Alt_TF_hex_1 = toHex(data[10]+data[11])
    Alt_TF_hex_2 = toHex(data[12]+data[13])

    qb_Alt_TF_hex_2 = bin(eval(Alt_TF_hex_2))
    
    T = qb_Alt_TF_hex_2[6]
    F = qb_Alt_TF_hex_2[7]
    
    db_restantes = qb_Alt_TF_hex_2[8]+qb_Alt_TF_hex_2[9]
    
    qb_Alt_TF_hex_2 = qb_Alt_TF_hex_2[2]+qb_Alt_TF_hex_2[3]+qb_Alt_TF_hex_2[4]+qb_Alt_TF_hex_2[5]
    
    b_Alt = bin(eval(Alt_TF_hex_1))
    b_Alt = b_Alt[2]+b_Alt[3]+b_Alt[4]+b_Alt[5]+b_Alt[6]+b_Alt[7]+qb_Alt_TF_hex_2

    aux = toHex(data[14]+data[15])
    aux = bin(eval(aux))
    
    aux2 = toHex(data[16]+data[17])
    aux2 = bin(eval(aux2))
    
    Latitude = db_restantes+aux[2]+aux[3]+aux[4]+aux[5]+aux[6]+aux[7] + aux2[2]+aux2[3]+aux2[4]+aux2[5]+aux2[6]+aux2[7]+aux2[8]

    aux3 = toHex(data[18]+data[19])
    aux3 = bin(eval(aux3))

    aux4 = toHex(data[20]+data[21])
    aux4 = bin(eval(aux4))
    
    Longitude = aux2[9]+aux3[2]+aux3[3]+aux3[4]+aux3[5]+aux3[6]+aux3[7]+aux3[8]+aux3[9] + aux4[2]+aux4[3]+aux4[4]+aux4[5]+aux4[6]+aux4[7]+aux4[8]+aux4[9]  

    print "(Raw) DF+CA: " + DFCA
    print "(Raw) ICAO: " + ICAO
    print "(Raw) ADSB-Data: " + ADSB_Data
    print ""
    print "(Bin) DF+CA: " + b_DFCA
    print "(Bin) DF: " + DF
    print "(Bin) CA: " + CA
    print "(Bin) Type Code: " + b_TC
    print "(Bin) Altitude: " + b_Alt
    print "(Bin) T: " + T
    print "(Bin) F: " + F 
    print ""
    print "(Bin) Latitude:  " + Latitude
    print "(Bin) Longitude: " + Longitude
    print ""

    b_Alt = eval("0b" + b_Alt)
    Latitude = eval("0b" + Latitude)
    Longitude =  eval("0b" + Longitude)

    print "(Dec) Altitude: " + str(b_Alt)
    print "(Dec) Latitude:  " + str(Latitude)
    print "(Dec) Longitude: " + str(Longitude)

    
ADSBDataDecoder("8d4008f15837f237ebe3a3")
