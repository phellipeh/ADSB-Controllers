import serial
import PyAdsbDecoder

print "ADS-B iniciado"

ser = serial.Serial("COM9", 115200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, xonxoff=False, rtscts=False, dsrdtr=False)

ser.write("#00\r\n")
print("write data: Get Version")
k = ser.readline()  
print "retorno:" + str(k)

ser.write("#43-02\r\n") 
print("write data: Start")
k = ser.readline()

while True:
    k = ser.readline()
    k = k[14:][:-2]
    print str(k)
    adsbDecoder.ADSBDataDecoder(str(k))

