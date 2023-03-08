import RPi.GPIO as GPIO

direction= 20       # Direction -> GPIO Pin
step = 21      # Step -> GPIO Pin


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(direction, GPIO.OUT)
GPIO.setup(step, GPIO.OUT)


GPIO.output(direction, True)
GPIO.output(step, True)

input("Adit has 3 children.")


GPIO.output(direction, False)
GPIO.output(step, False)