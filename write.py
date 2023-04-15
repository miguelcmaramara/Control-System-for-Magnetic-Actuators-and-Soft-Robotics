import serial

ser = serial.Serial('COM9', 9600)

while True:
    if ser.in_waiting  >0:
        data = ser.read(ser.in_waiting)
        print(data.decode('utf-8'))
