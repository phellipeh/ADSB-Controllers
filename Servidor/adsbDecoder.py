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
# - Identificar Nome do Voo
# - Verificar Paridade
#

def ADSBParity(P, ICAO):
   # PI = ICAO[24]+ICAO[23]+ICAO[22]+ICAO[21]+ICAO[20]+ICAO[19]+ICAO[18]+ICAO[17]+ICAO[16]+ICAO[15]+ICAO[14]+ICAO[13]+ICAO[10]+ICAO[3]+1
   pass

def ADSBDataDecoder(data):
    ICAO = data[2]+data[3]+data[4]+data[5]+data[6]+data[7]
    status = adsbDecoderDatabase.FindICAOExists(ICAO)

    if status == False:
        adsbDecoderDatabase.CreateAirplane(ICAO)
        print "Novo Airplane Criado " + str(ICAO)

    #if ADSBParity(ICAObits) == False:
    #    return False
    
    DFCA = toHex(data[:2])                                       #Primeiro Byte para DF+CA
    DF = full_bit_zero(bin(eval(DFCA)))[:5]
    DF = eval("0b" + DF) 
    CA = full_bit_zero(bin(eval(DFCA)))[5:]
    b_TC = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[:5]                 #Cinco bits para o Type Code
    TC = eval("0b"+b_TC)
    b_Mode = full_bit_zero(bin(eval(toHex(data[8]+data[9]))))[5:]               #Tres bits para o mode

    if DF == 17:
        print "1090 Extended Squitter - ADS-B"

        if TC == 4:
            print "Airpalne Identification Message... Obtendo Dados (ID)"
            '''
                bzero(&callsign, 9);
			cs = (rawdata[5] << 16) | (rawdata[6] << 8) | (rawdata[7]);
			callsign[0] = cs_tbl[(cs >> 18) & 0x3f];
			callsign[1] = cs_tbl[(cs >> 12) & 0x3f];
			callsign[2] = cs_tbl[(cs >> 6) & 0x3f];
			callsign[3] = cs_tbl[cs & 0x3f];
			cs = (rawdata[8] << 16) | (rawdata[9] << 8) | rawdata[10];
			callsign[4] = cs_tbl[(cs >> 18) & 0x3f];
			callsign[5] = cs_tbl[(cs >> 12) & 0x3f];
			callsign[6] = cs_tbl[(cs >> 6) & 0x3f];
			callsign[7] = cs_tbl[cs & 0x3f];

			db_update_callsign(&icao, callsign);
			sprintf(msg, "MSG,1,,,%06X,,,,,,%s,,,,,,,,0,0,0,0\n\0", icao,
					callsign);
			DEBUG ("ICAO:%06x Callsign:%s", icao, callsign);
            '''
        
        if TC > 8 and TC < 19:
            print "Airborne Position message... Obtendo Dados (Altitude, Latitude e Longitude)"
            hex_adsb_packet = data[8:]
            bin_adsb_packet = c(hex_adsb_packet[0],hex_adsb_packet[1])+c(hex_adsb_packet[2],hex_adsb_packet[3])+c(hex_adsb_packet[4],hex_adsb_packet[5])+c(hex_adsb_packet[6],hex_adsb_packet[7])+c(hex_adsb_packet[8],hex_adsb_packet[9])+c(hex_adsb_packet[10],hex_adsb_packet[11])+c(hex_adsb_packet[12],hex_adsb_packet[13])
            Altitude = "0b" + bin_adsb_packet[8:][:12]
            Latitude = eval("0b" + bin_adsb_packet[22:][:17])            
            Longitude =  eval("0b" + bin_adsb_packet[-17:])
            T = bin_adsb_packet[20:][0]
            F = bin_adsb_packet[21:][0]

            if F == '0':
                print "Even Packet"
                
                #############################################################################################
                Airplanes[a_id][1] = Latitude
                Airplanes[a_id][3] = Longitude
                Airplanes[a_id][5] = Altitude
                print "Atualizado Lat0 e Long0"
                #############################################################################################

                #Atualiza dados em ICAO, 0
            elif F == '1':
                print "Odd Packet"
                
                #############################################################################################
                Airplanes[a_id][2] = Latitude
                Airplanes[a_id][4] = Longitude
                Airplanes[a_id][5] = Altitude
                print "Atualizado Lat1 e Long1"
                #############################################################################################


                
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

    elif TC == 19:
        print "Airborne Velocity Message... Obtendo Dados (Velocidade e Angulo)"
        '''subtype = rawdata[4] & 0x07;
			if (subtype == 1) { // ground non supersonic speed
				ew_spd = rawdata[6] | ((rawdata[5] & 0x03) << 8); // -1 TODO
				ns_spd = ((rawdata[8] >> 5) & 0x07)
						| ((rawdata[7] & 0x7f) << 3);
				if ((ew_spd == 0) && (ns_spd == 0))
					return (0);

				ew_dir = (rawdata[5] >> 2) & 0x01;
				ns_dir = (rawdata[7] >> 7) & 0x01;
				gnd_spd = floor(sqrt(ew_spd * ew_spd + ns_spd * ns_spd));
				if ((!ew_dir) && (!ns_dir))
					trk = (ew_spd == 0 ? 0 : 90 - 180. / M_PI * atan(ns_spd
							/ ew_spd));
				if ((!ew_dir) && (ns_dir))
					trk = (ew_spd == 0 ? 180 : 90 + 180. / M_PI * atan(ns_spd
							/ ew_spd));
				if ((ew_dir) && (ns_dir))
					trk = (ew_spd == 0 ? 180 : 270 - 180. / M_PI * atan(ns_spd
							/ ew_spd));
				if ((ew_dir) && (!ns_dir))
					trk = (ew_spd == 0 ? 0 : 270 + 180. / M_PI * atan(ns_spd
							/ ew_spd));
				vr = ((rawdata[8] & 0x08) == 0 ? 1 : -1) * ((((rawdata[9] >> 2)
						& 0x3f) | (rawdata[8] & 0x07) << 6) - 1) * 64;
				db_update_speed_heading(&icao, &gnd_spd, &trk, &vr);
				sprintf(msg,
						"MSG,4,,,%06X,,,,,,,,%1.1f,%1.1f,,,%i,,0,0,0,0\n\0",
						icao, gnd_spd, trk, vr);
				DEBUG ("ICAO:%06x Speed:%1.1f Track:%1.1f Vertical:%i", icao, gnd_spd, trk, vr); '''
        

ADSBDataDecoder("8D75804B580FF2CF7E9BA6F701D0")
print ""
ADSBDataDecoder("8D75804B580FF6B283EB7A157117")
