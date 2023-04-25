import typing
from multiprocessing.connection import Connection
from ..shared.machinestatus import MachineStatus
from ..hardwarectrl.multiMotorTest import Motor_controller, Stepper_motor
import time
import RPi.GPIO as GPIO

class MachineHandler:
    def __init__(self, config, conn: Connection):
        self.config = config
        self.conn = conn
        pass

    def run(self):
        # Setup
        self.conn.send(MachineStatus.SETUP)

        # Initialize all motors and encoders
        self.init_motors()

        self.home_axes()
        while(True):
            if(self.conn.recv() == MachineStatus.RUNNING):
                print("here")
                self.mc.run(self.controls)

    # initializes the motors and puts them into the motor control object
    def init_motors(self):
        # self.config ['pi4.pins.horizontal.light']['mot_step_pin']
        h_mot_l = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.horizontal.light']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.horizontal.light']['mot_dir']),
                 sb_pin=int(self.config['pi4.pins.horizontal.light']['mot_sb']),
                 mode_0_pin=int(self.config['pi4.pins.horizontal.light']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.horizontal.light']['mot_mode_1']),
                 mode_2_pin=int(self.config['pi4.pins.horizontal.light']['mot_mode_2']),
                 limit_switch=int(self.config['pi4.pins.horizontal.light']['limit_switch'])
                 )
        h_mot_h = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_dir']),
                 sb_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_sb']),
                 mode_0_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_mode_1']),
                 mode_2_pin=int(self.config['pi4.pins.horizontal.heavy']['mot_mode_2']),
                 limit_switch=int(self.config['pi4.pins.horizontal.heavy']['limit_switch'])
                 )
        v_mot = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.vertical']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.vertical']['mot_dir']),
                 sb_pin=int(self.config['pi4.pins.vertical']['mot_sb']),
                 mode_0_pin=int(self.config['pi4.pins.vertical']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.vertical']['mot_mode_1']),
                 mode_2_pin=int(self.config['pi4.pins.vertical']['mot_mode_2']),
                 limit_switch=int(self.config['pi4.pins.vertical']['limit_switch'])
                 )
        r_mot = Stepper_motor(
                 step_pin=int(self.config['pi4.pins.rotational']['mot_step']),
                 dir_pin=int(self.config['pi4.pins.rotational']['mot_dir']),
                 en_pin=int(self.config['pi4.pins.rotational']['mot_en']),
                 mode_0_pin=int(self.config['pi4.pins.rotational']['mot_mode_0']),
                 mode_1_pin=int(self.config['pi4.pins.rotational']['mot_mode_1']),
                 limit_switch=int(self.config['pi4.pins.rotational']['limit_switch'])
                 )

        self.mc = Motor_controller(h_mot_l, h_mot_h, v_mot, r_mot)

        self.controls = [
                (5000000, 250000, 5000000, 250000, 3000000000),
                (250000, 5000000, 250000, 5000000, 3000000000),
                (5000000, 250000, 5000000, 250000, 3000000000),
                (250000, 5000000, 250000, 5000000, 3000000000),
                (5000000, 250000, 5000000, 250000, 3000000000),
                (250000, 5000000, 250000, 5000000, 3000000000)
                ]

        # self.mc.run(self.controls)


    # home axes function
    def home_axes(self):
        self.controls = [
                (5000000, 250000, 5000000, 250000, 3000000000),
                (250000, 5000000, 250000, 5000000, 3000000000),
                (5000000, 250000, 5000000, 250000, 3000000000),
                (250000, 5000000, 250000, 5000000, 3000000000),
                (5000000, 250000, 5000000, 250000, 3000000000),
                (250000, 5000000, 250000, 5000000, 3000000000)
                ]

        # set a signal type
        self.mc.h_mot_l.set_limit_action(sig_type=GPIO.RISING)
        self.mc.h_mot_h.set_limit_action(sig_type=GPIO.RISING)
        self.mc.v_mot.set_limit_action(sig_type=GPIO.RISING)
        self.mc.r_mot.set_limit_action(sig_type=GPIO.RISING)

        self.mc.print_current_positions()   # print before the move

        self.mc.run(self.controls)          # run the controls program
        self.mc.set_actives(1)              # reactivate all of the motors
        self.mc.print_current_positions()   # print the positions after the move
        print("Finished Homing")






