import RPi.GPIO as GPIO
import time
import math

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)

pin_A =23 
pin_B = 24
pin_X = 22

Encodeer_count = 0

GPIO.setup (Pin_A, GPIO.IN,)
GPIO.setup (Pin_B, GPIO.IN,)
GPIO.setup (Pin_X, GPIO.IN,)

last = time.time_ns()
prev = [0]


def do_Encoder(channel):
    global last
    if(time.time_ns() - last < 3000):
        print(f"last: {last}")
        print(f"time: {time.time_ns()}")
        print(f"diff: {last - time.time_ns()}")
        return
    last = time.time_ns()

    global Encodeer_count
    global prev
    if GPIO.input(pin_B) == 1:
        Encodeer_count += 1

    else:
        Encodeer_count -=1
    
    def do_Index(channel):
        global Encodeer_count
        Encodeer_count = 0
GPIO.add_event_detect (pin_A, GPIO.Falling, callback=do_Encoder)
GPIO.add_event_detect (pin_X, GPIO.Falling, callback=do_Index)

while(1):
    wdeg = (Encodeer_count/400)*360

    print ('count = ' + str(Encodeer_count))