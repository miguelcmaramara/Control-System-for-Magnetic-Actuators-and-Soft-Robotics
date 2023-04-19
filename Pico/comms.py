from machine import Pin, UART
import time

#create instance of uart object
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
pin = Pin("LED", Pin.OUT)

time.sleep(5)
print('wee')

while True:
    pin.low()
    if uart.any():
        data_bytes = uart.read()
        if data_bytes is not None:
            pin.high()
            data_str = data_bytes.decode('utf-8')
            print(data_str)
            # print(data_bytes)
            if data_bytes == b'y':
                for char in ['a', 'b', 'c', 'd',  'e']:
                    print(char)
                    uart.write(char.encode())
                break



    # # Send a message to the serial port
    # uart.write("Hello, world!\n".encode())

    # # Wait for a response
    # while uart.any() == 0:
    #     time.sleep_ms(10) # Wait for 10ms

    # # Read the response from the serial port
    # response = uart.readline()

    # # Print the response
    # print(response)