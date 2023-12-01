import time
import serial
import threading
def receive_data(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            print(line.decode('utf-8').rstrip())
ser = serial.Serial('/dev/ttyACM0', 115200)
receive_thread = threading.Thread(target=receive_data, args=(ser,))
receive_thread.daemon = True
receive_thread.start()
while True:
    message = input("Enter a message: ")
    ser.write(message.encode('utf-8')+ b'\n')
    time.sleep(0.1)