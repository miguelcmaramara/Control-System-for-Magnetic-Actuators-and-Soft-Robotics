from machine import Pin, UART
from time import sleep
# from Encoder import encoder
# from write import writeSteps

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

        
        self.pin_A.irq(trigger=self.pin_A.IRQ_FALLING, handler= self.do_Encoder) #Interrupt
        # self.pin_X.irq(trigger=self.pin_X.IRQ_FALLING, handler= self.do_Index)  #Index interrupt


    def do_Encoder(self, channel= None):
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

    

# pin = Pin("LED", Pin.OUT)
pin = Pin(25, Pin.OUT)
# readpin = Pin(16, Pin.IN)
run_state = False#True  #make false
# method = ''

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

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
arr = []
#random pin i use to reset the encounder step count **temporary**
statePin = Pin(16, mode=Pin.IN)

encoder_x1 = encoder(ex1_pinA, ex1_pinB)
encoder_x2 = encoder(ex2_pinA, ex2_pinB )
encoder_y = encoder(ey_pinA, ey_pinB)
encoder_r = encoder(er_pinA, er_pinB)

encoder_list = [encoder_x1, encoder_x2, encoder_y, encoder_r]

counter = 0
counter2 = 0
def writeSteps(pin, ex1, ex2, ey, er, es):
    if run_state == True:
        global counter
        global counter2
        es.do_Encoder()
        if counter %1 == 0:
            #message = str(encoder_x1.get_steps()) + ',' + str(encoder_x2.get_steps()) + ',' + str(encoder_y.get_steps()) + ',' +  str(encoder_r.get_steps()) + '\n'       
            #arr.append(message)
            #uart.write(message.encode())
            print(encoder_x1.get_steps(),encoder_x2.get_steps(), encoder_y.get_steps(), encoder_r.get_steps())
            et = abs(encoder_x1.get_steps())*(1000**3) + abs(encoder_x2.get_steps())*(1000**2) + abs(encoder_y.get_steps())*(1000) + abs(encoder_r.get_steps())
            # arr.append(et)

            uart.write(et.to_bytes(5, 'big'))
            counter2 += 1
        
        counter +=1

        if counter ==2:
            counter = 0
    
  
    
    
# #send data to mama pi when there is a step
# # encoder_x1.pin_A.irq(trigger=encoder_x1.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1,))
encoder_x1.pin_A.irq(trigger=encoder_x1.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r, encoder_x1 ))
encoder_x2.pin_A.irq(trigger=encoder_x2.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r, encoder_x2 ))
encoder_y.pin_A.irq(trigger=encoder_y.pin_A.IRQ_FALLING, handler= lambda pin : writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r, encoder_y ))
encoder_r.pin_A.irq(trigger=encoder_r.pin_A.IRQ_FALLING, handler= lambda pin: writeSteps(pin, encoder_x1, encoder_x2, encoder_y, encoder_r, encoder_r))



while True:     
    if uart.any()>0:
        data_bytes = uart.read()
        if data_bytes is not None:
            # pass
            # print(data_bytes)
            # data_str = data_bytes.decode('utf-8')
            
            if (data_bytes[0]) == ord('s'):
                print('nsnsdf')
                pin.value(1)
                # method = data_str[1]
                # rate = data_str[1:]
                for enc in encoder_list:
                    enc.reset_steps()

                uart.write(b's')
                print('s')
                run_state = True
            #     pin.value(0)

            # if data_str[0] == 'e':
            #     pin.value(1)
            #     for enc in encoder_list:
            #         enc.reset_steps()
            #     uart.write('e'.encode())
            #     print('e')
            #     run_state = False
            #     pin.value(0)
    


