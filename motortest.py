import RPi.GPIO as GPIO

from RpiMotorLib import RpiMotorLib

GPIO_pins = (14,15,18)
dir = 20
step = 21

mymotortest = RpiMotorLib.A4988Nema(dir, step, GPIO_pins, "A4988")

mymotortest.motor_go(False, "Full", 100, 0.01, False, 0.05)