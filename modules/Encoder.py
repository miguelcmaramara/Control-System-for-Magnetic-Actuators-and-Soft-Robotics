import RPi.GPIO as GPIO
import time

class encoder:
    def __init__(self, pin_A, pin_B, pin_X):
        # allows for empty Stepper_motor
        self.Encoder_Count = 0
        if pin_A< 0 and pin_B < 0 and pin_X is not None and pin_X < 0:
            return

        self.pin_A = pin_A
        self.pin_B = pin_B
        self.pin_X = pin_X
        # setmode if not set already
        if(GPIO.getmode() is None):
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_A, GPIO.IN)
        GPIO.setup(self.pin_B, GPIO.IN)
        GPIO.setup(self.pin_X, GPIO.IN)

        GPIO.add_event_detect (self.pin_A, GPIO.FALLING, callback=self.do_Encoder)   # Interrupt
        # GPIO.add_event_detect (self.pin_X, GPIO.FALLING, callback=self.do_Index)   # Index interrupt

    def do_Encoder(self, channel):

        global prev
        if GPIO.input(self.pin_B) == 1:
            self.Encoder_Count += 1
        else:
            self.Encoder_Count -= 1

        return self.Encoder_Count

    def do_Index(self, channel):
       # global Encoder_Count
       # self.Encoder_Count = 0
    #    print("x key reset")
        pass
        
    def get_steps(self):
        return self.Encoder_Count

    def reset_steps(self):
        print('encoder reset')
        self.Encoder_Count = 0




def main():
    pin_A = 37     # Channel A   
    pin_B = 38     # Channel B
    pin_X = 40     # Channel X 
    encoder(pin_A, pin_B, pin_X)




# last = time.time_ns()
# prev = [0]

# for i in range(100):
   # print(GPIO.input(pin_X), GPIO.input(pin_A), GPIO.input(pin_B))

   



# while(1):
    # # print(GPIO.input(pin_A), GPIO.input(pin_B), GPIO.input(pin_X))
    # wdeg = (Encoder_Count / 400) * 360
    # # if Encoder_Count < 1:
    # #    Encoder_Count = 512
    # # print ('Deg = '  + str(wdeg))
    # print ('count = '  + str(Encoder_Count))
   

   
