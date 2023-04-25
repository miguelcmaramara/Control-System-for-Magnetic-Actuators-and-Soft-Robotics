import time
import RPi.GPIO as GPIO
#from RpiMotorLib import RpiMotorLib



class Stepper_motor:
    def __init__(self, step_pin:int = -1, dir_pin: int = -1):
        # running logistics varibles
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.dir = 1    # 1 = CCW, 0 = CW
        self.step = 0    # 1 = CCW, 0 = CW

        # timing variables
        self.delay = 100    # arbitrary initial value
        self.last = 0

        
        # allows for empty Stepper_motor
        if step_pin < 0 and dir_pin < 0:
            return
        # setmode if not set already
        if(GPIO.getmode() is None):
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
    
    def write_dir(self, dir:int = -1): 
        if self.dir_pin < 0:
            return

        if dir < 0:     # if no arg provided, flip direction
            self.dir = 0 if self.dir == 1 else 1
        elif dir == 0:
            self.dir = 0    # if 0, set 0
        else:
            self.dir = 1    # if positive, set to 1

        GPIO.output(self.dir_pin, self.dir)

    def write_step(self, step:int = -1): 
        if self.step_pin < 0:
            return

        if step < 0:    # if no arg provided, flip direction
            self.step = 0 if self.step == 1 else 1
        elif step == 0:
            self.step = 0    # if 0, set 0
        else:
            self.step = 1    # if positive, set to 1
        GPIO.output(self.step_pin, self.step)

    def check_del(self, curr_time: int):
        if curr_time - self.last < self.delay:
            return

        self.last += self.delay
        self.write_step()
        # self.write_step()

    def reset_last(self):
        self.last = 0

class Motor_controller:
    
    def __init__(
            self, 
            h_mot: Stepper_motor,
            v_mot_A: Stepper_motor,
            v_mot_B: Stepper_motor,
            r_mot: Stepper_motor,
        ):
        self.h_mot = h_mot
        self.v_mot_A = v_mot_A
        self.v_mot_B = v_mot_B
        self.r_mot = r_mot

    def run(self, move_cmd: list[tuple[int, int, int, int, int]]):
        # delay tuple is in following order: h_mot, v_mot_A, v_mot_B, r_mot time del
        # time del is the amount of time that it's active
        for delay_tup in move_cmd:
            start = time.time_ns()
            self.h_mot.delay = delay_tup[0]
            self.v_mot_A.delay = delay_tup[1]
            self.v_mot_B.delay = delay_tup[2]
            self.r_mot.delay = delay_tup[3]

            self.h_mot.reset_last()
            self.v_mot_A.reset_last()
            self.v_mot_B.reset_last()
            self.r_mot.reset_last()

            print(delay_tup)
            # print(start)
            while True:
                now = time.time_ns() - start
                if now > delay_tup[4]:
                    break

                self.h_mot.check_del(int(now))
                self.v_mot_A.check_del(int(now))
                self.v_mot_B.check_del(int(now))
                self.r_mot.check_del(int(now))





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
    h_mot_step_pin = 35
    h_mot_dir_pin = 36
    # v_mot_step_pin = 37
    # v_mot_dir_pin = 38

    h_mot = Stepper_motor(h_mot_step_pin, h_mot_dir_pin)
    # v_mot_a = Stepper_motor(v_mot_step_pin, v_mot_dir_pin)
    v_mot_a = Stepper_motor()
    v_mot_b = Stepper_motor()
    r_mot = Stepper_motor()

    mc = Motor_controller(h_mot, v_mot_a, v_mot_b, r_mot)

    controls = [
            (10000000, 250000, 5000, 5000, 3000000000),
            (250000, 10000000, 5000, 5000, 3000000000),
            (10000000, 250000, 5000, 5000, 3000000000),
            (250000, 10000000, 5000, 5000, 3000000000),
            (10000000, 250000, 5000, 5000, 3000000000),
            (250000, 10000000, 5000, 5000, 3000000000)
            ]

    mc.run(controls)
