import typing
from multiprocessing.connection import Connection
from ..shared.machinestatus import MachineStatus
from ..hardwarectrl.multiMotorTest import main
import time

class MachineHandler:
    def __init__(self, config, conn: Connection):
        self.config = config
        self.conn = conn
        pass

    def run(self):
        # Setup
        self.conn.send(MachineStatus.SETUP)

        # Initialize all motors and encoders
        while(True):
            print("here")
            if(self.conn.recv() == MachineStatus.RUNNING):
                print("here")
                main()
# def main():
    # h_mot_step_pin = 35
    # h_mot_dir_pin = 36
    # v_mot_step_pin = 37
    # v_mot_dir_pin = 38

    # h_mot = Stepper_motor(h_mot_step_pin, h_mot_dir_pin)
    # v_mot_a = Stepper_motor(v_mot_step_pin, v_mot_dir_pin)
    # v_mot_b = Stepper_motor()
    # r_mot = Stepper_motor()

    # mc = Motor_controller(h_mot, v_mot_a, v_mot_b, r_mot)

    # controls = [
            # (5000000, 250000, 5000, 5000, 3000000000),
            # (250000, 5000000, 5000, 5000, 3000000000),
            # (5000000, 250000, 5000, 5000, 3000000000),
            # (250000, 5000000, 5000, 5000, 3000000000),
            # (5000000, 250000, 5000, 5000, 3000000000),
            # (250000, 5000000, 5000, 5000, 3000000000)
            # ]

    # mc.run(controls)

        # initialize pi

        # while for while not in teardown mode




        # teardown the machineHandler, close pins gpio cleanup



        # testing multiprocessing
        # start_time = time.time()
        # for i in range(1000000000):
            # pass
        # end_time = time.time()
        # print(f"child process finished in {end_time - start_time} seconds")

        # while(True):
            # print(f"mot: {self.config ['pi4.pins.horizontal.light']['mot_step_pin']}")




