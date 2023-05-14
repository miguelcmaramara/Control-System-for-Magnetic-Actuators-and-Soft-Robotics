import time
import RPi.GPIO as GPIO
import math

# mode pins for controlling step size
MODE_STEP_TO_PIN_TMC2209 = {
        8: (0, 0),
        16: (1, 1),
        32: (1, 0),
        64: (0, 1)
        }
MODE_STEP_TO_PIN_TB67S128FTG = {
        1: (0, 0, 0),
        2: (1, 0, 0),
        4: (0, 1, 0),
        8: (1, 1, 0),
        16: (0, 0, 1),
        32: (1, 0, 1),
        64: (0, 1, 1),
        128: (1, 1, 1)
        }

class Stepper_motor:

    # initializes and starts all pins
    def __init__(self,
                 step_pin: int = -1,
                 dir_pin: int = -1,
                 en_pin: int = -1,
                 sb_pin: int = -1,
                 mode_0_pin: int = -1,
                 mode_1_pin: int = -1,
                 mode_2_pin: int = -1,
                 limit_switch: int =-1
                 ):
        # pins setup
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin
        self.sb_pin = sb_pin
        self.mode_0_pin = mode_0_pin
        self.mode_1_pin = mode_1_pin
        self.mode_2_pin = mode_2_pin
        self.limit_switch = limit_switch

        # current statuses
        self.dir = 1    # 1 = CCW, 0 = CW
        self.step = 0    # 1 = CCW, 0 = CW
        self.num_steps = 0
        self.enable = 0
        self.standby = 1
        
        self.active = 1     # active has nothing to do with the pins. it is a flag
                            # that determines whether or not the motor should write.
                            # typically changed by LIMIT SWITCH functions
        

        # timing variables
        self.delay = 100    # arbitrary initial value
        self.last = 0       # previous time delayed, set to 0

        self.step_size = 8
        
        # allows for empty Stepper_motor
        if step_pin < 0 and dir_pin < 0:
            return
        # setmode if not set already
        if(GPIO.getmode() is None):
            GPIO.setmode(GPIO.BOARD)

        # setup pins
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        
        if(mode_0_pin >= 0):
            GPIO.setup(mode_0_pin, GPIO.OUT)
        if(mode_1_pin >= 0):
            GPIO.setup(mode_1_pin, GPIO.OUT)
        if(mode_2_pin >= 0):
            GPIO.setup(mode_2_pin, GPIO.OUT)
        if(en_pin >= 0):
            GPIO.setup(en_pin, GPIO.OUT)
        if(sb_pin >= 0):
            GPIO.setup(sb_pin, GPIO.OUT)
        if(limit_switch >= 0):
            print(f"SETUP pin {limit_switch}")
            GPIO.setup(limit_switch, GPIO.IN, GPIO.PUD_DOWN)

        # tmc2209
        if(en_pin >= 0):
            self.write_modes(8)
            self.write_enable(self.enable)
        if(sb_pin >= 0):
            self.write_standby(self.standby)
            self.write_modes(4)


    # sets the value of the the active flag (used for controlling movement
    def set_active(self, val:int=1):
        print(f"HERE active = {self.active}, switch = {self.limit_switch}")
        print(f"HERE active = {self.active}, switch = {self.limit_switch}, state = {GPIO.input(self.limit_switch)}")
        self.active = val
        print("HERE")

    # returns the motors active flag
    def get_active(self):
        return self.active

    # adds an event detector for the limit switch
    def set_limit_action(self, set=1, fxn=None, sig_type=GPIO.RISING):
        print(f"HERE active = {self.active}, switch = {self.limit_switch}")

        callback = lambda channel:  self.set_active(val=0)       # default value of callback function
        if sig_type == GPIO.RISING:
            callback = lambda channel: self.set_active(val=1)   # second value of callback function

        if fxn is not None:
            callback = fxn
        if(set):
            GPIO.setup(self.limit_switch, GPIO.IN)
            GPIO.add_event_detect(self.limit_switch, sig_type, callback=callback)
        else:   # if not set, then unset
            GPIO.remove_event_detect(self.limit_switch)
        

    
    # writes a HIGH or LOW pulse to dir pin depending on the dir input
    def write_dir(self, dir:int = -2): 
        if self.active == 0: # don't write if inactive
            return
        if self.dir_pin < 0:
            return

        if dir < -1:     # if no arg provided, flip direction
            self.dir = 0 if self.dir == 1 else 1
        elif dir == 0 or dir==-1:
            self.dir = 0    # if 0, or negative 1 (to help make things more dynamic) set 0
        else:
            self.dir = 1    # if positive, set to 1

        GPIO.output(self.dir_pin, self.dir)

    # writes a HIGH or LOW pulse to step pin depending on the dir input
    def write_step(self, step:int = -1): 
        if self.step_pin < 0:
            return

        if step < 0:    # if no arg provided, write the opposite of previous step
            if self.step ==0:
                self.step=1 #when stepping 
                if self.dir==0:  #if direction is negative remove a step
                    self.num_steps-=1
                else: #otherwise add the step
                    self.num_steps+=1
            else:
                self.step=0
            #self.step = 0 if self.step == 1 else 1
        elif step == 0:
            self.step = 0    # if 0, set 0
        else:
            self.step = 1    # if positive, set to 1

            # increment number of steps for the pin number
        #if self.dir == 0:
        #    self.num_steps = self.num_steps - 1
        #else:
        #    self.num_steps = self.num_steps + 1
        
        GPIO.output(self.step_pin, self.step)

    #checks if it is time for the motors to step and steps when it is time
    def check_del(self, curr_time: int):
        if self.active == 0:
            return
        # if less then delay time has passed since last step just return
        if curr_time - self.last < self.delay:
            return
        #otherwise increment last by delay and write step
        self.last += self.delay
        self.write_step()
        # self.write_step()
    
    # writes enable pin value - should be low to run
    # if enable pin is not set (polulu drivers), then this does nothing
    def write_enable(self, enable:int = -1): 
        if self.en_pin < 0:
            return

        if enable < 0:    # if no arg provided, flip direction
            self.enable = 0 if self.enable == 1 else 1
        elif enable == 0:
            self.enable = 1    # if 0, set 0
        else:
            self.enable = 0    # if positive, set to 1

        
        GPIO.output(self.en_pin, self.enable)

    # writes standby pin value - should be low to run
    # if standby pin is not set (polulu drivers), then this does nothing
    def write_standby(self, standby:int = -1): 
        if self.sb_pin < 0:
            return

        if standby < 0:    # if no arg provided, flip direction
            self.standby = 0 if self.standby == 1 else 1
        elif standby == 0:
            self.standby = 0    # if 0, set 0
        else:
            self.standby = 1    # if positive, set to 1
        GPIO.output(self.sb_pin, self.standby)


    # write the stepper mode. pass in the step size dictionary.
    # this function determines the number of step size
    def write_modes(self, dict_Value:int): 
        self.step_size =dict_Value
        if self.en_pin >=0:
            # TMC2209
            #check if any pin has been initialized. If not, then resolution is fixed and nothing should happen
            if self.mode_0_pin == -1:
                pass
            else:
                mode_tup = MODE_STEP_TO_PIN_TMC2209[dict_Value]
                GPIO.output(self.mode_0_pin, mode_tup[0])
                GPIO.output(self.mode_1_pin, mode_tup[1])

        else:   
            # the bigger motor driver
            mode_tup = MODE_STEP_TO_PIN_TB67S128FTG[dict_Value]
            GPIO.output(self.mode_0_pin, mode_tup[0])
            GPIO.output(self.mode_1_pin, mode_tup[1])
            GPIO.output(self.mode_2_pin, mode_tup[2])
        return


    # last time that motor should have moved.
    # this should be called before a motion
    def reset_last(self):
        #self.num_steps=0
        self.last = 0
       # self.write_step()

    #resets the total number of steps the motor has moved
    #should be called when the system homes
    def set_home(self):
        self.num_steps=0

    #Gets the distance traveled (mm) for the linear motions
    #Using 1/8 step size and the pully with a 12mm diameter
    def dist_travel(self):
        return (self.num_steps/self.step_size)*(12*math.pi)*(1.8/360)
    
    #Gets the angled traveled for the  rotation
    #Using 1/8 step size
    def rot_travel(self):
        return (self.num_steps/self.step_size)*(12/20)*1.8 *-1