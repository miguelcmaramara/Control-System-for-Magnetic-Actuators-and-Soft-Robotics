from machine import Pin
import time

class encoder:
    def __init__(self, pin_A, pin_B, pin_X = None):
        # allows for empty Stepper_motor
        self.Encoder_Count = 0
        if pin_A< 0 and pin_B < 0 and pin_X is not None and pin_X < 0:
            return
        
        self.pin_A = Pin(pin_A, mode=Pin.IN)
        self.pin_B = Pin(pin_B, mode=Pin.IN)
        
        if pin_X is not None:
            self.pin_X = Pin(pin_X, mode=Pin.IN)

        # # setmode if not set already
        # if(GPIO.getmode() is None):
        #     GPIO.setmode(GPIO.BOARD)
        
        self.pin_A.irq(trigger=self.pin_A.IRQ_FALLING, handler= self.do_Encoder) #Interrupt
        # self.pin_X.irq(trigger=self.pin_X.IRQ_FALLING, handler= self.do_Index)  #Index interrupt


    def do_Encoder(self, channel):
        # how global last
        # if(time.time_ns() - last < 3000):
            # return
        # self.last = time.time_ns()

        # global Encoder_Count
        global prev
        if self.pin_B.value() == 1:
            self.Encoder_Count += 1
        else:
            self.Encoder_Count -= 1

        return self.Encoder_Count

    # def do_Index(self, channel):
       # global Encoder_Count
       # self.Encoder_Count = 0
    #    print("x key reset")
    #    print(self.get_steps())
        return
            
    def get_steps(self):
        return self.Encoder_Count

    def reset_steps(self, pin= None):
        print("encoder_count reset")
        self.Encoder_Count = 0




# last = time.time_ns()
# prev = [0]

# for i in range(100):
   # print(GPIO.input(pin_X), GPIO.input(pin_A), GPIO.input(pin_B))

   



# while(1):
#     # print(GPIO.input(pin_A), GPIO.input(pin_B), GPIO.input(pin_X))
#     wdeg = (Encoder_Count / 400) * 360
#     # if Encoder_Count < 1:
#     #    Encoder_Count = 512
#     # print ('Deg = '  + str(wdeg))
#     print ('count = '  + str(Encoder_Count))
   

   
