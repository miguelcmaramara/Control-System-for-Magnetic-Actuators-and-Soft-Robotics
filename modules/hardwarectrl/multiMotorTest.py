import time
import RPi.GPIO as GPIO
from multiprocessing.connection import Connection
from ..shared.machinestatus import MachineStatus
from .stepper_motor import Stepper_motor
import serial
import math
#from RpiMotorLib import RpiMotorLib
   



# 8 = 1/8 step size
class Motor_controller:
    
    def __init__(
            self, 
            h_mot_l: Stepper_motor,
            h_mot_h: Stepper_motor,
            v_mot: Stepper_motor,
            r_mot: Stepper_motor,
            conn: Connection,
            config
        ):
        self.h_mot_l = h_mot_l
        self.h_mot_h = h_mot_h
        self.v_mot = v_mot
        self.r_mot = r_mot
        self.conn =conn
        self.config=config
        self.canRead =True
        self.runpin = int(self.config['pi4.Misc.pins']['pico_run'])
        #resets the Pico run pin so that the Pico's code would reset
        GPIO.setup(self.runpin,GPIO.OUT)
        GPIO.output(self.runpin, 1)
        time.sleep(.5)
        GPIO.output(self.runpin,0)
        time.sleep(.5)
        GPIO.output(self.runpin,1)
        time.sleep(.5)
        #Set up the Serial port                                  
        self.encoder = serial.Serial('/dev/serial0',115200)
        #send an s to reset the encoder counts
        self.encoder.write(b's')
        print('b')
        #wait for response the pico should send an s back
        time.sleep(.5)
        #If something in the serial buffer
        if self.encoder.in_waiting>0:
            #Read the value
            response = self.encoder.read().decode()
            print(response)
            #if the value is not a s the pico did not connect and respond properly
            if(response!='s'):
                #Send error message to front end
                self.conn.send(MachineStatus.ERROR)
                self.conn.send("Encoder not connect.\n Movement might not be value.")
        else:
            #If there is nothing in the buffer, the pico did not connect and respond properly
            #Send error message to front end
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("Encoder not connect.\n Movement might not be value.")
        self.data=0
        self.error=[0,0,0,0,0]
        self.x=0
        self.y=0
        self.rot=0
        self.error_msg =False

    #Run the motion for all the motors
    #input should be a list of tuples to represent all the move commands
    #each tuple is a given command
    #tuples should start with either "Move" for a move command or "Dir" for a set or change direction command
    # for move cmds the tuple is("Move", h_mot_l_delay,h_mot_h_delay,v_mot_delay,r_mot_delay,time_of_command)
    # for direction cmds the tuple is "Dir" followed by 4 postive or negative 1s to represent the direction of each motor
    #all times are in nanoseconds
    def run(self, move_cmd: list[tuple]):
        #reset the last call before anything runs, this makes sure that time rolls over between commands
        self.h_mot_l.reset_last()
        self.h_mot_h.reset_last()
        self.v_mot.reset_last()
        self.r_mot.reset_last()
        motor_start =time.time_ns()
        #for every command
        for i in range(len(move_cmd)):
            #if it is a move command
            if move_cmd[i][0]=="Move":
                #print("Moving")
                delay_tup = move_cmd[i][1:]
                #PID CALCULATION
                #encoders currently inactive due to improper delay transmitions
                #if encoders are set properly
                #if self.canRead:
                    #find the error in motion of expected -actual
                    #self.data (message from pico) would be an int in from of AAABBBCCCDDD
                    #AAA represents the readings from encoder on h_mot_l
                    #BBB represents the readings from encoder on h_mot_h
                    #CCC represents the readings from encoder on v_mot
                    #DDD represents the readings from encoder on r_mot, the reading has an additional 100 to avoid sending
                    #negative numbers but the value for only r_mot could be a negative angle
                    #self.error[0]=self.h_mot_l.dist_travel()-self.find_distance(int(self.data/(1000**3)))
                    #self.error[1]=self.h_mot_h.dist_travel()-self.find_distance(int((self.data/(1000**2))%1000))
                    #self.error[2]=self.v_mot.dist_travel()-self.find_distance(int((self.data/1000)%1000))
                    #self.error[3]=self.r_mot.rot_travel()-self.find_rotation(int(self.data%1000-100))
                    #cacluate the PID values based on the error
                    #PID = self.find_PID()
                    #adjust the delays based on the PID values
                    #delay_tup = tuple(delay_tup[i]-PID[i] for i in range(len(delay_tup)))
                    #set the number of sets the motors think they went to the number of steps they would have actually 
                    #gone through based on the encoder readings
                    #self.h_mot_l.num_steps=int(self.data/(1000**3))*16
                    #self.h_mot_h.num_steps=int((self.data/(1000**2))%1000)*16
                    #self.v_mot.num_steps=int((self.data/1000)%1000)*16
                    #self.r_mot.num_steps=int(self.data%1000-100)*16
                #set the new delays and reset the start time
                start = time.time_ns()
                self.h_mot_l.delay = delay_tup[0]
                self.h_mot_h.delay = delay_tup[1]
                self.v_mot.delay = delay_tup[2]
                self.r_mot.delay = delay_tup[3]


                #print(delay_tup)
                #print(start)
                #runs movements
                while True:
                    #find the time it has been running
                    now = time.time_ns() - start
                    motor_now =time.time_ns()-motor_start
                    #if the time is greater than the time of the current command or if there is a error break out of the loop
                    if now > delay_tup[4] or self.error_msg:
                        break
                    #Each transmition from the encoder is expected to be 5 bytes so if there is more than 4 bytes wating and
                    #the encoders are set up properly to read
                    #read the data and convert it back to an int
                    if self.encoder.in_waiting>4 and self.canRead:
                        a=self.encoder.read_until(size=5)
                        #print(a)
                        self.data = int.from_bytes(a,"big")
                        print("test",self.data)
                

                    #check if enough time has passed for each motor to do the next step
                    self.h_mot_l.check_del(int(motor_now))
                    self.h_mot_h.check_del(int(motor_now))
                    self.v_mot.check_del(int(motor_now))
                    self.r_mot.check_del(int(motor_now))
            #if the command is "Dir" directions need to be adjusted
            elif move_cmd[i][0]=="Dir":
                #change the direction of each motor properly
                self.h_mot_h.write_dir(move_cmd[i][1])
                self.h_mot_l.write_dir(move_cmd[i][2])
                self.v_mot.write_dir(move_cmd[i][3])
                #rotation motor is always opposite since it is wired a different way due to how the order of the connection wires
                #are unadjustable
                self.r_mot.write_dir(-1*move_cmd[i][4])
            #after each cmd chceck if anything was sent from the front end
            if self.conn.poll():
                #if something was sent check what it was
                stat=self.conn.recv()
                #off cmds mean stop
                if stat==MachineStatus.OFF:
                    print("END")
                    #set error flag to true to avoid future movements
                    self.error_msg=True
                    #set actives to 0 to block all movements and force a rehome
                    self.set_actives(0)
                    #break out of the rest of the commands
                    break
                #Kill cmds mean the front end was closed
                if stat==MachineStatus.KILL:
                    #all close the back end process
                    print("Kill")
                    exit()
            #if there is an error
            if self.error_msg:
                #break out of the rest of the commands
                print("error")
                break
        #after all cmds were called check if anything is still in the buffer
        while self.encoder.in_waiting>0:
            #if something is in the buffer read it all to dump it out and not interfere with any other readings
            dump = self.encoder.read_all()
    
    #Displays how far the system believes all motors have traveled.
    def print_current_positions(self):
        print(f"h_mot_l position: {self.h_mot_l.dist_travel()}")
        print(f"h_mot_h position: {self.h_mot_h.dist_travel()}")
        print(f"v_mot position: {self.v_mot.dist_travel()}")
        print(f"r_mot position: {self.r_mot.rot_travel()}")

    #change the active flag for all the motors, used to control if the motors could move or not
    def set_actives(self, val:int=1):
        self.h_mot_l.set_active(val)
        self.h_mot_h.set_active(val)
        self.v_mot.set_active(val)
        self.r_mot.set_active(val)

    #gets the active flag for the first motor, since besides for homeing all the flags would be the same
    #so only looking at the first on is required
    def get_actives(self):
        return self.h_mot_l.get_active()

    # sets enable and standby on all the first value is for linear motors, the second is for the rotational one
    def set_en_sb(self, val:int=1,rot:int=1):
        #all linear motors have the same enable pin only 1 needs to be adjusted
        self.h_mot_l.write_enable(val)
        #self.h_mot_h.write_enable(val)
        #self.v_mot.write_enable(val)
        self.r_mot.write_enable(rot)

    #Set the entire system to its home position
    def set_home(self):
        #reset all the motor's step values
        self.h_mot_l.set_home()
        self.h_mot_h.set_home()
        self.v_mot.set_home()
        self.r_mot.set_home()
        #send the pico an s to reset the encoder readings
        self.encoder.write(b's')
        time.sleep(.5)
        #wait for a response which should be an S
        gotS = False
        #clear the buffer while searching the response
        while self.encoder.in_waiting>0:
            response = self.encoder.read(1)
            if response==b's':
                gotS=True
                break
        if not gotS:
            #if did not get a response back sent message to diplay in front end
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("Encoder readings did not reset properly at home.")
        #reset where the system believes it is
        self.x=0
        self.y=0
        self.rot=0

    #function used to convert linear encoder reading to mm traveled
    def find_distance(self, value:int):
        return value*(12*math.pi/100)
    
    #function used to convert rotation encoder readings to deg rotated
    def find_rotation(self, value:int):
        return value*360/100*(12/20)
    
    #get PID values based on the current error
    #Currently not fully implemented only does P and constant not tested fully
    def find_PID(self):
        return [i*10000 for i in self.error]
    
    #sets where the system is currently inputs are x distance in mm, y distance in mm, rotation in deg
    def set_position(self, x, y, rot):
        self.x = x
        self.y =y
        self.rot = rot

    #Function to send message to encoder for how often messages should be sent
    #input is a byte string of 1 or 2
    #this is used for when at faster speeds it would not send every change in the encoders
    #so that the pico could handle the speed of the data it needs to transmit
    def encoder_count(self, step):
        #sends the pico the message
        self.encoder.write(step)
        #waits for a response
        time.sleep(.5)
        if self.encoder.in_waiting>0:
            response = self.encoder.read()
            #The pico is expected to send the same thing back as a acknowledgement
            if response !=step:
                #if the response is not the same send message to the front end 
                # and set flag to not read encoders this time
                self.canRead = False
                self.conn.send(MachineStatus.ERROR)
                self.conn.send("Encoder readings not active for this motion.")
            else:
                #if the response is as expected set flag to read encoders
                self.canRead = True
        else:
            #if there is not response at all send same message to the front end
            #and set the flag to not read encoders
            self.canRead = False
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("Encoder readings not active for this motion.")

    




#deprecated
#original code to test motor speeds with different delays
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

#deprecated
#original method to run the test to determine if multiple motors can be controlled at different speeds
def main():
    #pins as specified in the fritzing diagram:
    # v_mot_a_dir_pin = 37
    # v_mot_a_step_pin = 35
    # v_mot_b_dir_pin = 28
    # v_mot_b_step_pin = 32
    # v_mot_mode0_pin = 36
    # v_mot_mode1_pin = 38
    # v_mot_mode2_pin = 40
    
    # h_mot_dir_pin = 24
    # h_mot_step_pin = 26
    # h_mot_mode0_pin = 7
    # h_mot_mode1_pin = 12
    # h_mot_mode2_pin = 22

    # r_mot_dir_pin = 33
    # r_mot_step_pin = 31
    
    

    h_mot_step_pin = 35
    h_mot_dir_pin = 36
    v_mot_step_pin = 37
    v_mot_dir_pin = 38

    h_mot = Stepper_motor(h_mot_step_pin, h_mot_dir_pin)
    v_mot_a = Stepper_motor(v_mot_step_pin, v_mot_dir_pin)
    v_mot_b = Stepper_motor()
    r_mot = Stepper_motor()

    mc = Motor_controller(h_mot, v_mot_a, v_mot_b, r_mot)

    controls = [
            (5000000, 250000, 5000, 5000, 3000000000),
            (250000, 5000000, 5000, 5000, 3000000000),
            (5000000, 250000, 5000, 5000, 3000000000),
            (250000, 5000000, 5000, 5000, 3000000000),
            (5000000, 250000, 5000, 5000, 3000000000),
            (250000, 5000000, 5000, 5000, 3000000000)
            ]

    mc.run(controls)
