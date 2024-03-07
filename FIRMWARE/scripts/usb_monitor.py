import serial
import time

ser = serial.Serial("COM6")
ser.write_timeout = 2
ser.timeout = 0
ser.bytesize = 8

while(True):
    print(ser.inWaiting())

    if (ser.inWaiting() != 0):
        print(ser.read(ser.inWaiting()))

    time.sleep(1)