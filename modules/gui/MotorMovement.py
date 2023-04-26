class MotorMovement():
    def __init__(self, parent=None):

        self.points  = []
        self.speed = 0
        self.rotationAngle = []
        self.enableRot = True

    def getPoints(self):
        # print("getting points")
        return self.points
    
    
    def setPoints(self, point_array):
        # print("setting points")
        self.points = point_array
        return 
    
    def getSpeed(self):
        return self.speed
    def setSpeed(self, speed):
        self.speed = speed
        return

    def getRot(self):
        return self.rotationAngle
    def setRot(self, angle):
        self.rotationAngle = angle
        return
    
    def getEnableRot(self):
        return self.enableRot
    def toggleEnableRot(self):
        self.enableRot = not self.enableRot