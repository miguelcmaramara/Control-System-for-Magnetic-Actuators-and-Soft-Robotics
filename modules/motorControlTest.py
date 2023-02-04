import time
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
def main():
    # Microstep Resolution MS1-MS3 -> GPIO Pin , can be set to (-1,-1,-1) to turn off 
    GPIO_pins = (14, 15, 18)  
    direction= 20       # Direction -> GPIO Pin
    step = 21      # Step -> GPIO Pin
    
    # Declare an named instance of class pass GPIO-PINs
    # (self, direction_pin, step_pin, mode_pins , motor_type):
    mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
    # motor_go(clockwise, steptype", steps, stepdelay, verbose, initdelay)
    input("1/8 Step 360 degrees 0.005s/step 8 s total Press <Enter>")
    mymotortest.motor_go(False, "1/8" , 1600, .005, True, .05)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.001s/step, 1.6 s total. Press <Enter>")
    mymotortest.motor_go(False, "1/8" , 1600, .001, True, .05)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0005s/step, 0.8 s total. Press <Enter>")
    mymotortest.motor_go(False, "1/8" , 1600, .0005, True, .05)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.0002s/step, 0.32 s total. Press <Enter>")
    mymotortest.motor_go(False, "1/8" , 1600, .0002, True, .05)
    time.sleep(1)
    input("1/8 Step, 360 degrees, 0.00015s/step, 0.24 s total. Press <Enter>")
    mymotortest.motor_go(False, "1/8" , 1600, .00015, True, .05)
    time.sleep(1)