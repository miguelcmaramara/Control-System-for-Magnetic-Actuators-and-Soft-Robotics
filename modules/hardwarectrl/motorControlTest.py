import time
import RPi.GPIO as GPIO
#from RpiMotorLib import RpiMotorLib

def motorGoBrrr(dir:int, step:int, clockwise:bool, num:int,delay:float):
    if clockwise:
        GPIO.output(dir, True)
    else:
        GPIO.output(dir,False)
    for i in range(num):
        GPIO.output(step, True)
        time.sleep(delay)
        GPIO.output(step, False)
        time.sleep(delay)

def main():
    # Microstep Resolution MS1-MS3 -> GPIO Pin , can be set to (-1,-1,-1) to turn off 
    GPIO_pins = (14, 15, 18)  
    direction= 20       # Direction -> GPIO Pin
    step = 21      # Step -> GPIO Pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(direction, GPIO.OUT)
    GPIO.setup(step, GPIO.OUT)
    # Declare an named instance of class pass GPIO-PINs
    # (self, direction_pin, step_pin, mode_pins , motor_type):
    #mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
    # motor_go(clockwise, steptype", steps, stepdelay, verbose, initdelay)
    # input("1/8 Step 360 degrees 0.005s/step 8 s total Press <Enter>")
    # mymotortest.motor_go(False, "1/8" , 1600, .005, True, .05)
    # time.sleep(1)
    # input("1/8 Step, 360 degrees, 0.001s/step, 1.6 s total. Press <Enter>")
    # mymotortest.motor_go(False, "1/8" , 1600, .001, True, .05)
    # time.sleep(1)
    # input("1/8 Step, 360 degrees, 0.0005s/step, 0.8 s total. Press <Enter>")
    # mymotortest.motor_go(False, "1/8" , 1600, .0005, True, .05)
    # time.sleep(1)
    # input("1/8 Step, 360 degrees, 0.0002s/step, 0.32 s total. Press <Enter>")
    # mymotortest.motor_go(False, "1/8" , 1600, .0002, True, .05)
    # time.sleep(1)
    # input("1/8 Step, 360 degrees, 0.00015s/step, 0.24 s total. Press <Enter>")
    # mymotortest.motor_go(False, "1/8" , 1600, .00015, True, .05)
    # time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0016s/step, 2.56 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .0016)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0008s/step, 1.28 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .0008)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0004s/step, 0.64 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .0004)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0002s/step, 0.32 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .0002)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0001s/step, 0.16 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .0001)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.00005s/step, 0.08 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .00005)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.000025s/step, 0.04 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .000025)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0000125s/step, 0.02 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .0000125)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.00000625s/step, 0.01 s total. Press <Enter>")
    motorGoBrrr(20, 21, False, 1600, .00000625)
    time.sleep(1)
    GPIO.output(step, False)
    GPIO.output(direction, False)
