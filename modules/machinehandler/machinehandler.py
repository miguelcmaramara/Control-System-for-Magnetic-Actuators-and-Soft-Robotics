import typing
from multiprocessing.connection import Connection
from ..shared.machinestatus import MachineStatus
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




