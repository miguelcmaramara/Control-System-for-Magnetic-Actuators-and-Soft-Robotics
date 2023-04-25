from machine import Pin, UART
from time import sleep
from Encoder import encoder
# from write import writeSteps

pin = Pin("LED", Pin.OUT)
run_state = False
method = ''

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

ex1_pinA = 14 #channel A 
ex1_pinB = 15 #channel B
# ex1_pinX = 2 #channel C

#uncomment when pins have been decided for all encoders
ex2_pinA = 19 #channel A 
ex2_pinB = 18 #channel B
# ex2_pinX = 2 #channel C

ey_pinA = 21 #channel A 
ey_pinB = 20 #channel B
# ey_pinX = 2 #channel C

er_pinA = 10 #channel A 
er_pinB = 11 #channel B
# er_pinX = 2 #channel C

#random pin i use to reset the encounder step count **temporary**
statePin = Pin(16, mode=Pin.IN)

encoder_x1 = encoder(ex1_pinA, ex1_pinB)
encoder_x2 = encoder(ex2_pinA, ex2_pinB )
encoder_y = encoder(ey_pinA, ey_pinB)
encoder_r = encoder(er_pinA, er_pinB)

encoder_list = [encoder_x1, encoder_x2, encoder_y, encoder_r]

def writeSteps(pin, ex1, ex2, ey, er):
    if run_state == True:
        encoder_x1.do_Encoder()
        message = str(encoder_x1.get_steps()) + ',' + str(encoder_x2.get_steps()) + ',' + str(encoder_y.get_steps()) + ',' +  str(encoder_r.get_steps()) + '\n'       
        print(message)
        uart.write(message.encode())
        return
#send data to mama pi when there is a step
# encoder_x1.pin_A.irq(trigger=encoder_x1.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1,))
encoder_x1.pin_A.irq(trigger=encoder_x1.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r ))
encoder_x2.pin_A.irq(trigger=encoder_x2.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r ))
encoder_y.pin_A.irq(trigger=encoder_y.pin_A.IRQ_FALLING, handler= lambda pin : writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r ))
encoder_r.pin_A.irq(trigger=encoder_r.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r))



while True:
    if uart.any():
        data_bytes = uart.read()
        if data_bytes is not None:
        #     print(data_bytes)
            data_str = data_bytes.decode('utf-8')
            
            if data_str[0] == 's':
                method = data_str[1]
                rate = data_str[1:]
                for enc in encoder_list:
                    enc.reset_steps()

                uart.write(('s').encode())
                print('s')
                run_state = True

            if data_str[0] == 'e':
                for enc in encoder_list:
                    enc.reset_steps()
                uart.write('e'.encode())
                print('e')
                run_state = False
            
        
    pin.toggle()
    sleep(1)
