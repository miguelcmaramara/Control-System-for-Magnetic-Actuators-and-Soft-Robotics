from enum import Enum

class MachineStatus(Enum):
    ERROR = -1
    OFF = 0
    SETUP = 1
    TEARDOWN = 2
    RUNNING = 3
    MANUAL = 4
    


