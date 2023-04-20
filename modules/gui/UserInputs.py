from PyQt5.QtCore import QPoint, pyqtSignal, QPointF,QRegExp, QLocale
from PyQt5.QtGui import QGuiApplication, QDoubleValidator, QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import  QGridLayout, QWidget, QLabel, QLineEdit, QTabWidget, QVBoxLayout, QDoubleSpinBox, QSpinBox

from .DrawWidget import DrawWidget
from .MotorMovement import MotorMovement
from math import atan2, pi, cos, sin, tan

class UserInputs(QWidget):
    updateSignal = pyqtSignal()

    def __init__(self, parent= None):
        super().__init__(parent)

        self.MotorMovement = MotorMovement()

        #initialize tab object that will contain each tab
        self.tabs = QTabWidget()

        #Each tab will be its own widget with a layout and the input fields
        self.inputTab1 = QWidget()
        self.inputTab2 = QWidget()

        #adjusting tab size
        self.tabs.resize(50,50)


        #Adding tabs to tab screen
        self.tabs.addTab(self.inputTab1, "Start Point End Point Selection")
        self.tabs.addTab(self.inputTab2, "Distance-Angle Selection")
        
        #Setting layouts of tabs
        self.inputTab1.layout1 = QGridLayout(self)
        self.inputTab2.layout1 = QGridLayout(self)

        #Creating layout for the overall userinput section
        main_layout = QGridLayout()

        #Adding tabs to main layout
        #main_layout.addWidget(self.tabs)

        
        self.startLabel = QLabel("Start Point")
        self.startLabel2 = QLabel("Start Point")
        self.endLabel = QLabel("End Point")

        self.xLabel1 = QLabel("X (mm):")
        self.yLabel1 = QLabel("Y (mm):")

        self.xLabel2 = QLabel("X (mm):")
        self.yLabel2 = QLabel("Y (mm):")

        self.xLabel3 = QLabel("X (mm):")
        self.yLabel3 = QLabel("Y (mm):")

        self.speedLabel = QLabel("Speed (mm/s):")
        self.oscillationLabel = QLabel("Number of Oscillations:")    
        self.startRotationLabel = QLabel("Starting Angle: ")
        self.endRotationLabel = QLabel("Ending Angle: ")
        self.frequencyLabel = QLabel("Freqiuency (Hz):")

        self.distanceLabel = QLabel("Path Distance:")
        self.pathAngleLabel = QLabel("Path Angle:")

        # create a line edit to allow user input
        self.x1line_edit = QDoubleSpinBox()
        self.x1line_edit.setRange(0,350) 
        self.y1line_edit = QDoubleSpinBox()
        self.y1line_edit.setRange(0,275)  
        self.x2line_edit = QDoubleSpinBox()
        self.x2line_edit.setRange(0,350)  
        self.y2line_edit = QDoubleSpinBox()
        self.y2line_edit.setRange(0,275) 
        self.x3line_edit = QDoubleSpinBox()
        self.x3line_edit.setRange(0,350) 
        self.y3line_edit = QDoubleSpinBox()
        self.y3line_edit.setRange(0,275) 

        self.speedInput =  QDoubleSpinBox()
        self.speedInput.setRange(0,250) 
        self.oscillationInput = QSpinBox()
        self.oscillationInput.setRange(0,50)
        self.startRotationInput = QDoubleSpinBox() 
        self.startRotationInput.setRange(-90,90)
        self.endRotationInput = QDoubleSpinBox()
        self.endRotationInput.setRange(-90,90) 

        self.frequencyInput =  QDoubleSpinBox()
        self.frequencyInput.setRange(0,10) 
        
        self.distanceInput = QDoubleSpinBox()
        self.distanceInput.setRange(0,450) 
        self.pathAngleInput = QDoubleSpinBox()
        self.pathAngleInput.setRange(-360,360) 





        #Adjusting layout within tab1 
        self.inputTab1.layout1.addWidget(self.startLabel, 0, 0)
        self.inputTab1.layout1.addWidget(self.endLabel, 0, 2)

        self.inputTab1.layout1.addWidget(self.xLabel1, 1, 0)
        self.inputTab1.layout1.addWidget(self.x1line_edit, 1, 1)
        self.inputTab1.layout1.addWidget(self.yLabel1, 2, 0)
        self.inputTab1.layout1.addWidget(self.y1line_edit, 2, 1)

        self.inputTab1.layout1.addWidget(self.xLabel2, 1, 2)
        self.inputTab1.layout1.addWidget(self.x2line_edit, 1, 3)
        self.inputTab1.layout1.addWidget(self.yLabel2, 2, 2)
        self.inputTab1.layout1.addWidget(self.y2line_edit, 2, 3)



        
       
        self.inputTab1.setLayout(self.inputTab1.layout1)

        self.inputTab2.layout1.addWidget(self.startLabel2, 0, 0)
        self.inputTab2.layout1.addWidget(self.xLabel3, 1, 0)
        self.inputTab2.layout1.addWidget(self.x3line_edit, 1, 1)
        self.inputTab2.layout1.addWidget(self.yLabel3, 2, 0)
        self.inputTab2.layout1.addWidget(self.y3line_edit, 2, 1)
        self.inputTab2.layout1.addWidget(self.distanceLabel, 1, 2)
        self.inputTab2.layout1.addWidget(self.distanceInput, 1, 3)
        self.inputTab2.layout1.addWidget(self.pathAngleLabel, 2, 2)
        self.inputTab2.layout1.addWidget(self.pathAngleInput, 2, 3)

        self.inputTab2.setLayout(self.inputTab2.layout1)
        main_layout.addWidget(self.tabs,0,0,1,-1)
        main_layout.addWidget(self.startRotationLabel, 1, 0)
        main_layout.addWidget(self.startRotationInput, 1, 1)

        main_layout.addWidget(self.endRotationLabel, 1,2)
        main_layout.addWidget(self.endRotationInput, 1,3)
        main_layout.addWidget(self.speedLabel, 2, 0,1,1)
        main_layout.addWidget(self.speedInput, 2, 1,1,1)

        main_layout.addWidget(self.frequencyLabel, 2,2,1,1)
        main_layout.addWidget(self.frequencyInput, 2,3,1,1)

        main_layout.addWidget(self.oscillationLabel, 3, 0,1,1)
        main_layout.addWidget(self.oscillationInput, 3, 1,1,1)

    
        self.setLayout(main_layout)

        #when done editing update the path parameters and redraw the line
        self.x1line_edit.editingFinished.connect(lambda: self.updatePathParameters('points'))
        self.y1line_edit.editingFinished.connect(lambda: self.updatePathParameters('points'))
        self.x2line_edit.editingFinished.connect(lambda: self.updatePathParameters('points'))
        self.y2line_edit.editingFinished.connect(lambda: self.updatePathParameters('points'))

        self.x3line_edit.editingFinished.connect(lambda: self.updatePathParameters('distance'))
        self.y3line_edit.editingFinished.connect(lambda: self.updatePathParameters('distance'))
        self.distanceInput.editingFinished.connect(lambda: self.updatePathParameters("distance"))
        self.pathAngleInput.editingFinished.connect(lambda: self.updatePathParameters("distance"))

        self.startRotationInput.editingFinished.connect(lambda: self.MotorMovement.setRot([self.startRotationInput.value(),self.endRotationInput.value()]))
        self.endRotationInput.editingFinished.connect(lambda: self.MotorMovement.setRot([self.startRotationInput.value(),self.endRotationInput.value()]))


        self.speedInput.editingFinished.connect(lambda: self.updateSpeed('speed'))
        self.frequencyInput.editingFinished.connect(lambda: self.updateSpeed("freq"))

    #Get show coordinates based on line drawn with mouse
    def updateStart(self):

        self.x1line_edit.setValue((self.MotorMovement.getPoints()[0].x()))
        self.y1line_edit.setValue((self.MotorMovement.getPoints()[0].y()))
        self.x3line_edit.setValue((self.MotorMovement.getPoints()[0].x()))
        self.y3line_edit.setValue((self.MotorMovement.getPoints()[0].y()))
        
        if len(self.MotorMovement.getPoints()) > 1:
            self.x2line_edit.setValue((self.MotorMovement.getPoints()[1].x()))
            self.y2line_edit.setValue((self.MotorMovement.getPoints()[1].y()))
            distance = ((self.MotorMovement.getPoints()[0].x()-self.MotorMovement.getPoints()[1].x())**2+(self.MotorMovement.getPoints()[0].y()-self.MotorMovement.getPoints()[1].y())**2)**.5
            self.distanceInput.setValue((distance))
            angle = atan2((self.MotorMovement.getPoints()[0].y()-self.MotorMovement.getPoints()[1].y()),(self.MotorMovement.getPoints()[1].x()-self.MotorMovement.getPoints()[0].x()))*180/pi
            self.pathAngleInput.setValue((angle))
            self.updateSpeed("speed") 


    def updateSpeed(self,field):
        if(self.distanceInput.value()!=0):
            if(field=="speed"):
                self.frequencyInput.setValue((float(self.speedInput.text())/(2*float(self.distanceInput.text()))))
            elif(field=="freq"):
                self.speedInput.setValue((float(self.distanceInput.text())*float(self.frequencyInput.text())*2))
                self.frequencyInput.setValue((float(self.speedInput.text())/(2*float(self.distanceInput.text()))))
        self.MotorMovement.setSpeed(self.speedInput.value())

    #Draw line based on coordinates typed into text field
    def updatePathParameters(self,point):
        self.start = QPointF()
        self.end =  QPointF()
        if point=="points":
            self.start.setX(float(self.x1line_edit.text()))
            self.start.setY(float(self.y1line_edit.text()))
            self.end.setX(float(self.x2line_edit.text()))
            self.end.setY(float(self.y2line_edit.text()))   
        elif point=="distance":
            self.start.setX(float(self.x3line_edit.text()))
            self.start.setY(float(self.y3line_edit.text()))
            self.validateNum(self.distanceInput,0,self.getMaxDistance(self.start))
            x2 = self.start.x()+(self.distanceInput.value()*cos(self.pathAngleInput.value()*pi/180))
            y2 = self.start.y()-(self.distanceInput.value()*sin(self.pathAngleInput.value()*pi/180))
            self.end.setX(x2)
            self.end.setY(y2)
        self.MotorMovement.setPoints([self.start, self.end])
        self.updateSignal.emit()

    def getMaxDistance(self,point):
        x1=0
        y2=0
        x2=0
        y1=0
        angle = self.pathAngleInput.value()
        if ((angle>180)or(angle>-180 and angle<0)):
            y2=275
        if ((angle>-90 and angle<90)or (angle<-270)or(angle>270)):
            x1=350
        v2=800
        v1=800
        if(angle ==0 or angle ==360 or angle==-360):
            v1=350-point.x()
        elif (angle ==180 or angle ==-180):
            v1=point.x()
        elif (angle ==90 or angle ==-270):
            v2=point.y()
        elif (angle ==270 or angle ==-90):
            v2=275-point.y()
        else:
            x2=(point.y()-y2)/tan(angle*pi/180)
            v2= ((x2)**2+(point.y()-y2)**2)**.5
            y1=(point.x()-x1)*tan(angle*pi/180)
            v1= ((point.x()-x1)**2+(y1)**2)**.5
        return min(v1,v2)
    def validateNum(self, input, start, stop):
        value = float(input.text())
        if(value > stop):
            input.setValue((stop))
        elif(value<start):
            input.setValue((start))