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

def modulo(x, y):
    r = x - y * math.floor(x / y)
    return r

def ADSBParity(P, ICAO):
   # PI = ICAO[24]+ICAO[23]+ICAO[22]+ICAO[21]+ICAO[20]+ICAO[19]+ICAO[18]+ICAO[17]+ICAO[16]+ICAO[15]+ICAO[14]+ICAO[13]+ICAO[10]+ICAO[3]+1
   pass

def NL(lat):
	if math.fabs(lat) < 10.47047130:
		return 59
	elif math.fabs(lat) < 14.82817437:
		return 58
	elif math.fabs(lat) < 18.18626357:
		return 57
	elif math.fabs(lat) < 21.02939493:
		return 56
	elif math.fabs(lat) < 23.54504487:
		return 55
	elif math.fabs(lat) < 25.82924707:
		return 54
	elif math.fabs(lat) < 27.93898710:
		return 53
	elif math.fabs(lat) < 29.91135686:
		return 52
	elif math.fabs(lat) < 31.77209708:
		return 51
	elif math.fabs(lat) < 33.53993436:
		return 50
	elif math.fabs(lat) < 35.22899598:
		return 49
	elif math.fabs(lat) < 36.85025108:
		return 48
	elif math.fabs(lat) < 38.41241892:
		return 47
	elif math.fabs(lat) < 39.92256684:
		return 46
	elif math.fabs(lat) < 41.38651832:
		return 45
	elif math.fabs(lat) < 42.80914012:
		return 44
	elif math.fabs(lat) < 44.19454951:
		return 43
	elif math.fabs(lat) < 45.54626723:
		return 42
	elif math.fabs(lat) < 46.86733252:
		return 41
	elif math.fabs(lat) < 48.16039128:
		return 40
	elif math.fabs(lat) < 49.42776439:
		return 39
	elif math.fabs(lat) < 50.67150166:
		return 38
	elif math.fabs(lat) < 51.89342469:
		return 37
	elif math.fabs(lat) < 53.09516153:
		return 36
	elif math.fabs(lat) < 54.27817472:
		return 35
	elif math.fabs(lat) < 55.44378444:
		return 34
	elif math.fabs(lat) < 56.59318756:
		return 33
	elif math.fabs(lat) < 57.72747354:
		return 32
	elif math.fabs(lat) < 58.84763776:
		return 31
	elif math.fabs(lat) < 59.95459277:
		return 30
	elif math.fabs(lat) < 61.04917774:
		return 29
	elif math.fabs(lat) < 62.13216659:
		return 28
	elif math.fabs(lat) < 63.20427479:
		return 27
	elif math.fabs(lat) < 64.26616523:
		return 26
	elif math.fabs(lat) < 65.31845310:
		return 25
	elif math.fabs(lat) < 66.36171008:
		return 24
	elif math.fabs(lat) < 67.39646774:
		return 23
	elif math.fabs(lat) < 68.42322022:
		return 22
	elif math.fabs(lat) < 69.44242631:
		return 21
	elif math.fabs(lat) < 70.45451075:
		return 20
	elif math.fabs(lat) < 71.45986473:
		return 19
	elif math.fabs(lat) < 72.45884545:
		return 18
	elif math.fabs(lat) < 73.45177442:
		return 17
	elif math.fabs(lat) < 74.43893416:
		return 16
	elif math.fabs(lat) < 75.42056257:
		return 15
	elif math.fabs(lat) < 76.39684391:
		return 14
	elif math.fabs(lat) < 77.36789461:
		return 13
	elif math.fabs(lat) < 78.33374083:
		return 12
	elif math.fabs(lat) < 79.29428225:
		return 11
	elif math.fabs(lat) < 80.24923213:
		return 10
	elif math.fabs(lat) < 81.19801349:
		return 9
	elif math.fabs(lat) < 82.13956981:
		return 8
	elif math.fabs(lat) < 83.07199445:
		return 7
	elif math.fabs(lat) < 83.99173563:
		return 6
	elif math.fabs(lat) < 84.89166191:
		return 5
	elif math.fabs(lat) < 85.75541621:
		return 4
	elif math.fabs(lat) < 86.53536998:
		return 3
	elif math.fabs(lat) < 87.00000000:
		return 2
	else:
		return 1

Airplanes = [
        ["ICAO", "Lat0", "Lat1", "Long0", "Long1", "Alt", "UTF"]
    ]

def findICAOExists(ICAO):
    retorno = False
    for x in range(0, len(Airplanes)):
        if Airplanes[x][0] == ICAO:
            retorno = True
        else:
            retorno = False
    return retorno, x

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

            status, a_id = findICAOExists(ICAO)
            
            if status == False:
                Airplanes.append([ICAO, "NULL", "NULL", "NULL", "NULL", "NULL", T])
                a_id = len(Airplanes)-1
                print "Novo Airplane Criado " + str(a_id)
    
            if F == '0':
                print "Even Packet"
                Airplanes[a_id][1] = Latitude
                Airplanes[a_id][3] = Longitude
                Airplanes[a_id][5] = Altitude
                print "Atualizado Lat0 e Long0"
                #Atualiza dados em ICAO, 0
            elif F == '1':
                print "Odd Packet"
                Airplanes[a_id][2] = Latitude
                Airplanes[a_id][4] = Longitude
                Airplanes[a_id][5] = Altitude
                print "Atualizado Lat1 e Long1"
                #Atualiza dados em ICAO, 1

            print "ICAO Hex Address: " + ICAO

            #verifica exitencia dos dois dados e calcula rota
            if Airplanes[a_id][1] != "NULL" and Airplanes[a_id][2] != "NULL" and Airplanes[a_id][3] != "NULL" and Airplanes[a_id][4] != "NULL":
                j = math.floor((59. * Airplanes[a_id][1] - 60. * Airplanes[a_id][2]) / 131072. + 0.5)
                rlat0 = 6. * (modulo(j, 60.) + Airplanes[a_id][1] / 131072.)
                rlat1 = rlat1 = 6.101694915254237288 * (modulo(j, 59.) + Airplanes[a_id][2] / 131072.)
                
                if rlat0 > 270:
                    rlat0 = rlat0 - 360

                if rlat1 > 270:
                    rlat1 = rlat1 - 360

                NL0 = NL(rlat0)
                NL1 = NL(rlat1)
                                                        
                if NL0 != NL1:
                    return False

                m = math.floor((Airplanes[a_id][3] * (NL0 - 1) - Airplanes[a_id][4] * NL1) / 131072. + 0.5);

                if F == '0':
                    Latitude = rlat0
                    
                    if NL0 > 1:
                        ni = NL0
                    else:
                        ni = 1
                    
                    dlon = 360. / ni
                    rlon = dlon * (modulo(m, ni) + Airplanes[a_id][3] / 131072.)
                    Longitude = rlon

                elif F == '1':
                    Latitude = rlat1
                    
                    if (NL1 - 1) > 1:
                        ni = (NL1 - 1)
                    else:
                        ni = 1
                    
                    dlon = 360. / ni
                    rlon = dlon * (modulo(m, ni) + Airplanes[a_id][4] / 131072.)
                    Longitude = rlon

                    Altitude = Altitude[2:][:12]
                    bits = Altitude[0]+Altitude[1]+Altitude[2]+Altitude[3]+ Altitude[4]+Altitude[5]+Altitude[6]+Altitude[8]+Altitude[9]+Altitude[10]+Altitude[11]
                    oitavo_bit = Altitude[7]
                    Altitude = 25 * eval("0b"+bits) - 1000;

                
                print "Altitude: " + str(Altitude) + " pes"
                print "Latitude: " + str(Latitude)
                print "Longitude: " + str(Longitude)

            #math.floor(((59 * Lat(0) - 60 * Lat(1)) / 131072) + 0.5)

ADSBDataDecoder("8D75804B580FF2CF7E9BA6F701D0")
print ""
ADSBDataDecoder("8D75804B580FF6B283EB7A157117")
