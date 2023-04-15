from machine import Pin
from time import sleep
from Encoder import encoder

ex1_pinA = 0 #channel A 
ex1_pinB = 1 #channel B
ex1_pinX = 2 #channel C

#uncomment when pins have been decided for all encoders
# ex2_pinA = 0 #channel A 
# ex2_pinB = 1 #channel B
# ex2_pinX = 2 #channel C

# ey_pinA = 0 #channel A 
# ey_pinB = 1 #channel B
# ey_pinX = 2 #channel C

# er_pinA = 0 #channel A 
# er_pinB = 1 #channel B
# er_pinX = 2 #channel C

#random pin i use to reset the encounder step count **temporary**
statePin = Pin(16, mode=Pin.IN)

encoder_x1 = encoder(ex1_pinA, ex1_pinB, ex1_pinX)
# encoder_x2 = encoder(ex2_pinA, ex2_pinB, ex2_pinX)
# encoder_y = encoder(ey_pinA, ey_pinB, ey_pinX)
# encoder_r = encoder(er_pinA, er_pinB, er_pinX)

#reset encoder count when pin gets sent low
statePin.irq(trigger=statePin.IRQ_FALLING, handler= encoder_x1.reset_steps)




pin = Pin("LED", Pin.OUT)

while True:
    pin.toggle()
    sleep(1)
