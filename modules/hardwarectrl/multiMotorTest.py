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
            conn: Connection
        ):
        self.h_mot_l = h_mot_l
        self.h_mot_h = h_mot_h
        self.v_mot = v_mot
        self.r_mot = r_mot
        self.conn =conn
        self.runpin = 11
        GPIO.setup(self.runpin,GPIO.OUT)
        GPIO.output(self.runpin, 1)
        time.sleep(.5)
        GPIO.output(self.runpin,0)
        time.sleep(.5)
        GPIO.output(self.runpin,1)
        time.sleep(.5)                                  
        self.encoder = serial.Serial('/dev/serial0',115200)
        self.encoder.write(b's')
        print('b')
        time.sleep(.5)
        if self.encoder.in_waiting>0:
            response = self.encoder.read().decode()
            print(response)
            if(response!='s'):
                self.conn.send(MachineStatus.ERROR)
                self.conn.send("Encoder not connect.\n Movement might not be value.")
        else:
            self.conn.send(MachineStatus.ERROR)
            self.conn.send("Encoder not connect.\n Movement might not be value.")
        self.data=0
        self.error=[0,0,0,0,0]
        self.x=0
        self.y=0
        self.rot=0
        self.error_msg =False

    def run(self, move_cmd: list[tuple]):
        # delay tuple is in following order: h_mot_l, h_mot_h, v_mot, r_mot time del
        # time del is the amount of time that it's active

        self.h_mot_l.reset_last()
        self.h_mot_h.reset_last()
        self.v_mot.reset_last()
        self.r_mot.reset_last()
        motor_start =time.time_ns()
        for i in range(len(move_cmd)):
            if move_cmd[i][0]=="Move":
                #print("Moving")
                delay_tup = move_cmd[i][1:]
                #PID CALCULATION 
                PID = self.find_PID()
                delay_tup = tuple(delay_tup[i]-PID[i] for i in range(len(delay_tup)))
                self.h_mot_l.num_steps=int(self.data/(1000**3))*16
                self.h_mot_h.num_steps=int((self.data/(1000**2))%1000)*16
                self.v_mot.num_steps=int((self.data/1000)%1000)*16
                self.r_mot.num_steps=int(self.data%1000)*16
                start = time.time_ns()
                self.h_mot_l.delay = delay_tup[0]
                self.h_mot_h.delay = delay_tup[1]
                self.v_mot.delay = delay_tup[2]
                self.r_mot.delay = delay_tup[3]


                #print(delay_tup)
                #print(start)
                while True:
                    now = time.time_ns() - start
                    motor_now =time.time_ns()-motor_start
                    if now > delay_tup[4] or self.error_msg:
                        break
                    if self.encoder.in_waiting>0:
                        self.data = int.from_bytes(self.encoder.read(5),"big")
                        print("test",self.data)
                
                    self.error[0]=self.h_mot_l.dist_travel()-self.find_distance(int(self.data/(1000**3)))
                    self.error[1]=self.h_mot_h.dist_travel()-self.find_distance(int((self.data/(1000**2))%1000))
                    self.error[2]=self.v_mot.dist_travel()-self.find_distance(int((self.data/1000)%1000))
                    self.error[3]=self.r_mot.rot_travel()-self.find_rotation(int(self.data%1000))

                    self.h_mot_l.check_del(int(motor_now))
                    self.h_mot_h.check_del(int(motor_now))
                    self.v_mot.check_del(int(motor_now))
                    self.r_mot.check_del(int(motor_now))

            elif move_cmd[i][0]=="Dir":
                self.h_mot_h.write_dir(move_cmd[i][1])
                self.h_mot_l.write_dir(move_cmd[i][2])
                self.v_mot.write_dir(move_cmd[i][3])
                self.r_mot.write_dir(-1*move_cmd[i][4])
            if self.conn.poll():
                stat=self.conn.recv()
                if stat==MachineStatus.OFF:
                    print("END")
                    self.error_msg=True
                    break
                if stat==MachineStatus.KILL:
                    print("Kill")
                    exit()
            if self.error_msg:
                print("error")
                break
    

    def print_current_positions(self):
        print(f"h_mot_l position: {self.h_mot_l.dist_travel()}")
        print(f"h_mot_h position: {self.h_mot_h.dist_travel()}")
        print(f"v_mot position: {self.v_mot.dist_travel()}")
        print(f"r_mot position: {self.r_mot.rot_travel()}")

    def set_actives(self, val:int=1):
        self.h_mot_l.set_active(val)
        self.h_mot_h.set_active(val)
        self.v_mot.set_active(val)
        self.r_mot.set_active(val)

    def get_actives(self):
        return self.h_mot_l.get_active()

    # sets enable and standby on all
    def set_en_sb(self, val:int=1,rot:int=1):
        self.h_mot_l.write_enable(val)
        #self.h_mot_h.write_enable(val)
        #self.v_mot.write_enable(val)
        self.r_mot.write_enable(rot)

    def set_home(self):
        self.h_mot_l.set_home()
        self.h_mot_h.set_home()
        self.v_mot.set_home()
        self.r_mot.set_home()
        self.encoder.write(b's')
        self.x=0
        self.y=0
        self.rot=0

    def find_distance(self, value:int):
        return value*(12*math.pi/100)
        
    def find_rotation(self, value:int):
        return value*360/100*(12/20)
    
    def find_PID(self):
        return [i*50000 for i in self.error]
    
    def set_position(self, x, y, rot):
        self.x = x
        self.y =y
        self.rot = rot
    

    





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
