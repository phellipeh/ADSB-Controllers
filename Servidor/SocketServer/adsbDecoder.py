#
# ADS-B Decoder in Python
# Felipe Sousa Rocha, 1/8/2024
#

import math
import adsbDecoderDatabase
import adsbDecoderMathAndDataLibrary

#
# TODO LIST
# - Identificar Velocidade e Direcao da Aeronave
# - Colocar todas as referencias as bibliotecas    OK
# - Identificar Nome do Voo
# - Verificar Paridade
# - Terminar o adsbDecoderDatabase
#

cs_tbl = ['@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
	  'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
	  'Z', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
	  ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0', '1', '2', '3', '4', '5',
	  '6', '7', '8', '9', ' ', ' ', ' ', ' ', ' ', ' ']

def ADSBParity(P, ICAO):
   # PI = ICAO[24]+ICAO[23]+ICAO[22]+ICAO[21]+ICAO[20]+ICAO[19]+ICAO[18]+ICAO[17]+ICAO[16]+ICAO[15]+ICAO[14]+ICAO[13]+ICAO[10]+ICAO[3]+1
   return True

def ADSBDataDecoder(data):
    ICAO = data[2]+data[3]+data[4]+data[5]+data[6]+data[7]

    '''if ADSBParity("", ICAO) == False:
        return False'''
    
    
    status = adsbDecoderDatabase.FindICAOExists(ICAO)

    if status == False:
        adsbDecoderDatabase.CreateAirplane(ICAO)
        print "Novo Airplane Criado " + str(ICAO)
    
    DFCA = adsbDecoderMathAndDataLibrary.toHex(data[:2])  #Primeiro Byte para DF+CA
    DF = adsbDecoderMathAndDataLibrary.full_bit_zero(bin(eval(DFCA)))[:5]
    DF = eval("0b" + DF) 
    CA = adsbDecoderMathAndDataLibrary.full_bit_zero(bin(eval(DFCA)))[5:]
    b_TC = adsbDecoderMathAndDataLibrary.full_bit_zero(bin(eval(adsbDecoderMathAndDataLibrary.toHex(data[8]+data[9]))))[:5] #Cinco bits para o Type Code
    TC = eval("0b"+b_TC)
    b_Mode = adsbDecoderMathAndDataLibrary.full_bit_zero(bin(eval(adsbDecoderMathAndDataLibrary.toHex(data[8]+data[9]))))[5:] #Tres bits para o mode

    if DF == 17:
        if TC > 8 and TC < 19:  # "Airborne Position message... Obtendo Dados (Altitude, Latitude e Longitude)"
            hex_adsb_packet = data[8:]
            bin_adsb_packet = adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[0],hex_adsb_packet[1])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[2],hex_adsb_packet[3])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[4],hex_adsb_packet[5])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[6],hex_adsb_packet[7])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[8],hex_adsb_packet[9])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[10],hex_adsb_packet[11])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[12],hex_adsb_packet[13])
            Altitude = "0b" + bin_adsb_packet[8:][:12]
            Latitude = eval("0b" + bin_adsb_packet[22:][:17])            
            Longitude =  eval("0b" + bin_adsb_packet[-17:])
            T = bin_adsb_packet[20:][0]
            F = bin_adsb_packet[21:][0]

            Altitude = Altitude[2:][:12]
            bits = Altitude[0]+Altitude[1]+Altitude[2]+Altitude[3]+ Altitude[4]+Altitude[5]+Altitude[6]+Altitude[8]+Altitude[9]+Altitude[10]+Altitude[11]
            oitavo_bit = Altitude[7]
            Altitude = 25 * eval("0b"+bits) - 1000
            
            if F == '0':
                adsbDecoderDatabase.UpdateAirplanePosition_T0(ICAO, [Latitude, Longitude, Altitude])
            elif F == '1':
                adsbDecoderDatabase.UpdateAirplanePosition_T1(ICAO, [Latitude, Longitude, Altitude])

            if adsbDecoderDatabase.VerifyAllPositionDataExists(ICAO) == True: #verifica exitencia dos dois dados e calcula rota
                Airplanes1, Airplanes2, Airplanes3, Airplanes4 = adsbDecoderDatabase.GetPositionData(ICAO)
                Airplanes1 = int(Airplanes1)
                Airplanes2 = int(Airplanes2)
                Airplanes3 = int(Airplanes3)
                Airplanes4 = int(Airplanes4)
                j = math.floor((59. * Airplanes1 - 60. * Airplanes2) / 131072. + 0.5)
                rlat0 = 6. * (adsbDecoderMathAndDataLibrary.modulo(j, 60.) + Airplanes1 / 131072.)
                rlat1 = rlat1 = 6.101694915254237288 * (adsbDecoderMathAndDataLibrary.modulo(j, 59.) + Airplanes2 / 131072.)
                
                if rlat0 > 270:
                    rlat0 = rlat0 - 360
                if rlat1 > 270:
                    rlat1 = rlat1 - 360

                NL0 = adsbDecoderMathAndDataLibrary.NL(rlat0)
                NL1 = adsbDecoderMathAndDataLibrary.NL(rlat1)
                                                        
                if NL0 != NL1:
                    return False

                m = math.floor((Airplanes3 * (NL0 - 1) - Airplanes4 * NL1) / 131072. + 0.5);

                if F == '0':
                    Latitude = rlat0
                    
                    if NL0 > 1:
                        ni = NL0
                    else:
                        ni = 1
                    
                    dlon = 360. / ni
                    rlon = dlon * (adsbDecoderMathAndDataLibrary.modulo(m, ni) + Airplanes3 / 131072.)
                    Longitude = rlon
                    
                    
                elif F == '1':
                    Latitude = rlat1
                    
                    if (NL1 - 1) > 1:
                        ni = (NL1 - 1)
                    else:
                        ni = 1
                    
                    dlon = 360. / ni
                    rlon = dlon * (adsbDecoderMathAndDataLibrary.modulo(m, ni) + Airplanes4 / 131072.)
                    Longitude = rlon

                ID, Altitude, Grau, T = adsbDecoderDatabase.getAirplaneFullLog(ICAO)
                Data = [ICAO, ID, Latitude, Longitude, Altitude, Grau, T]
                adsbDecoderDatabase.RealTimeFullAirplaneFeed(Data)

    if TC == 4:
            # "Airplane Identification Message... Obtendo Dados (ID)"
            callsign = []
            '''
	       cs = (rawdata[5] << 16) | (rawdata[6] << 8) | (rawdata[7])
	       callsign[0] = cs_tbl[(cs >> 18) & 0x3f]
	       callsign[1] = cs_tbl[(cs >> 12) & 0x3f]
	       callsign[2] = cs_tbl[(cs >> 6) & 0x3f]
	       callsign[3] = cs_tbl[cs & 0x3f]
	       
	       cs = (rawdata[8] << 16) | (rawdata[9] << 8) | rawdata[10]
	       callsign[4] = cs_tbl[(cs >> 18) & 0x3f]
	       callsign[5] = cs_tbl[(cs >> 12) & 0x3f]
	       callsign[6] = cs_tbl[(cs >> 6) & 0x3f]
	       callsign[7] = cs_tbl[cs & 0x3f]
            '''
            id_ = 
            adsbDecoderDatabase.UpdateAirplaneID(ICAO, [id_])

    if TC == 19:
        # "Airborne Velocity Message... Obtendo Dados (Velocidade e Angulo)"
         hex_adsb_packet = data[8:]
         hex_adsb_packet = hex_adsb_packet[:14]
         bin_adsb_packet = adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[0],hex_adsb_packet[1])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[2],hex_adsb_packet[3])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[4],hex_adsb_packet[5])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[6],hex_adsb_packet[7])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[8],hex_adsb_packet[9])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[10],hex_adsb_packet[11])+adsbDecoderMathAndDataLibrary.c(hex_adsb_packet[12],hex_adsb_packet[13])
         subtype = eval("0b"+bin_adsb_packet[5] + bin_adsb_packet[6] + bin_adsb_packet[7])
         
         if subtype == 1: 
	    ew_spd = rawdata[6] | ((rawdata[5] & 0x03) << 8);
	    '''ns_spd = ((rawdata[8] >> 5) & 0x07) | ((rawdata[7] & 0x7f) << 3)
	    
            if ew_spd == 0 and ns_spd == 0:
               return False

	    ew_dir = (rawdata[5] >> 2) & 0x01
	    ns_dir = (rawdata[7] >> 7) & 0x01
	    gnd_spd = math.floor(math.sqrt(ew_spd * ew_spd + ns_spd * ns_spd))
				
	    if ((!ew_dir) and (!ns_dir))
	       trk = (ew_spd == 0 ? 0 : 90 - 180. / math.pi * math.atan(ns_spd/ ew_spd))
					
	    if ((!ew_dir) and (ns_dir))
	       trk = (ew_spd == 0 ? 180 : 90 + 180. / math.pi * math.atan(ns_spd / ew_spd))

	    if ((ew_dir) and (ns_dir))
	       trk = (ew_spd == 0 ? 180 : 270 - 180. / math.pi * math.atan(ns_spd / ew_spd))

	    if ((ew_dir) adn (!ns_dir))
	       trk = (ew_spd == 0 ? 0 : 270 + 180. / math.pi * math.atan(ns_spd / ew_spd))

	    vr = ((rawdata[8] & 0x08) == 0 ? 1 : -1) * ((((rawdata[9] >> 2) & 0x3f) | (rawdata[8] & 0x07) << 6) - 1) * 64''
	      
            #adsbDecoderDatabase.UpdateAirplaneAngle(ICAO, [gnd_spd, trk, vr])'''

ADSBDataDecoder("8d4008f1994404339808D3")
