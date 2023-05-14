from enum import Enum
#List of possible statuses that would be sent between the front and back end
class MachineStatus(Enum):
    ERROR = -1
    OFF = 0
    SETUP = 1
    TEARDOWN = 2
    RUNNING = 3
    MANUAL = 4
    HOME = 5
    GOPOS = 6
    TOGGLEROT = 7
    DEBUG = 8
    KILL =9


