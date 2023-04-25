import time
import RPi.GPIO as GPIO
from .stepper_motor import Stepper_motor
#from RpiMotorLib import RpiMotorLib


# 8 = 1/8 step size
class Motor_controller:
    
    def __init__(
            self, 
            h_mot_l: Stepper_motor,
            h_mot_h: Stepper_motor,
            v_mot: Stepper_motor,
            r_mot: Stepper_motor,
        ):
        self.h_mot_l = h_mot_l
        self.h_mot_h = h_mot_h
        self.v_mot = v_mot
        self.r_mot = r_mot

    def run(self, move_cmd: list[tuple[int, int, int, int, int]]):
        # delay tuple is in following order: h_mot_l, h_mot_h, v_mot, r_mot time del
        # time del is the amount of time that it's active
        for delay_tup in move_cmd:
            start = time.time_ns()
            self.h_mot_l.delay = delay_tup[0]
            self.h_mot_h.delay = delay_tup[1]
            self.v_mot.delay = delay_tup[2]
            self.r_mot.delay = delay_tup[3]

            self.h_mot_l.reset_last()
            self.h_mot_h.reset_last()
            self.v_mot.reset_last()
            self.r_mot.reset_last()

            print(delay_tup)
            print(start)
            while True:
                now = time.time_ns() - start
                if now > delay_tup[4]:
                    break

                self.h_mot_l.check_del(int(now))
                self.h_mot_h.check_del(int(now))
                self.v_mot.check_del(int(now))
                self.r_mot.check_del(int(now))
    

    def print_current_positions(self):
        print(f"h_mot_l position: {self.h_mot_l.num_steps}")
        print(f"h_mot_h position: {self.h_mot_h.num_steps}")
        print(f"v_mot position: {self.v_mot.num_steps}")
        print(f"r_mot position: {self.r_mot.num_steps}")

    def set_actives(self, val:int=1):
        self.h_mot_l.set_active(val)
        self.h_mot_h.set_active(val)
        self.v_mot.set_active(val)
        self.r_mot.set_active(val)

    # sets enable and standby on all
    def set_en_sb(self, val:int=1):
        self.h_mot_l.write_standby(val)
        self.h_mot_h.write_standby(val)
        self.v_mot.write_standby(val)
        self.r_mot.write_enable(val)





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
