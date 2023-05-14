class MotorMovement():
    #Class to store all the motor movements
    def __init__(self, parent=None):
        #initalize defaults for all the movements
        self.points  = []
        self.speed = 0
        self.rotationAngle = [0,0]
        self.oscNum=0
        self.enableRot = True

    #returns the list of start and end points with dimensions in mm
    def getPoints(self):
        # print("getting points")
        return self.points
    
    #sets the points to the given array, array should be at most 2 QPointF objects with dimensions in mm
    def setPoints(self, point_array):
        # print("setting points")
        self.points = point_array
        return 
    
    #returns the speed of the movement in mm/s
    def getSpeed(self):
        return self.speed
    
    #sets the speed of the movement to the given value which should be in mm/s
    def setSpeed(self, speed):
        self.speed = speed
        return

    #returns the list of start and end rotations, which are values in deg
    def getRot(self):
        return self.rotationAngle
    
    #sets the list of rotations to the given input, input must be a list of 2 numbers in deg
    def setRot(self, angle):
        self.rotationAngle = angle
        return
    
    #return if the rotation motor is enabled
    def getEnableRot(self):
        return self.enableRot
    #toggle if the rotation motor is enabled
    def toggleEnableRot(self):
        self.enableRot = not self.enableRot
    #return the number of oscillations, an int
    def getOsc(self):
        return self.oscNum
    #sets the number of oscillations to the given value, must be an int
    def setOsc(self,osc):
        self.oscNum =osc