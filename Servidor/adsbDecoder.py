#
# ADS-B Decoder in Python
# Felipe Sousa Rocha, 1/8/2024
#

def toHex(x):
    return hex(eval("0x" + x))

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
    print qb_Alt_TF_hex_2
    T = qb_Alt_TF_hex_2[6]
    F = qb_Alt_TF_hex_2[7]
    db_restantes = qb_Alt_TF_hex_2[8]+qb_Alt_TF_hex_2[9]
    
    qb_Alt_TF_hex_2 = qb_Alt_TF_hex_2[2]+qb_Alt_TF_hex_2[3]+qb_Alt_TF_hex_2[4]+qb_Alt_TF_hex_2[5]
    
    b_Alt = bin(eval(Alt_TF_hex_1))
    b_Alt = b_Alt[2]+b_Alt[3]+b_Alt[4]+b_Alt[5]+b_Alt[6]+b_Alt[7]+qb_Alt_TF_hex_2

    print "(Raw) DF+CA: " + (DFCA)
    print "(Raw) ICAO: " + ICAO
    print "(Raw) ADSB-Data: " + ADSB_Data
    print ""
    print "(Bin) DF+CA: " + b_DFCA
    print "(Bin) DF: " + DF
    print "(Bin) CA: " + CA
    print ""
    print "(Bin) Type Code: " + b_TC
    print "(Bin) Altitude: " + b_Alt
    print "(Bin) T: " + T
    print "(Bin) F: " + F 
    print ""
    

ADSBDataDecoder("8d4008f15837f237ebe3a3")
