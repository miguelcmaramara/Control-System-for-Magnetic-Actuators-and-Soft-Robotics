from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QGridLayout, QWidget, QLabel, QLineEdit, QTabWidget, QVBoxLayout

from .DrawWidget import DrawWidget
from .MotorMovement import MotorMovement

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
        self.tabs.resize(300,200)


        #Adding tabs to tab screen
        self.tabs.addTab(self.inputTab1, "Distance-Angle Selection")
        self.tabs.addTab(self.inputTab2, "Start Point End Point Selection")
        
        #Setting layouts of tabs
        self.inputTab1.layout1 = QGridLayout(self)
        self.inputTab2.layout1 = QGridLayout(self)

        #Creating layout for the overall userinput section
        main_layout = QVBoxLayout()

        #Adding tabs to main layout
        main_layout.addWidget(self.tabs)

        
        self.startLabel = QLabel("Start")
        self.endLabel = QLabel("End")

        self.xLabel1 = QLabel("X:")
        self.yLabel1 = QLabel("Y:")

        self.xLabel2 = QLabel("X:")
        self.yLabel2 = QLabel("Y:")

        self.speedLabel = QLabel("Speed:")
        self.oscillationLabel = QLabel("Number of Oscillations:")    
        self.rotationLabel = QLabel("Rotations:")
        self.frequencyLabel = QLabel("Freqiuency (Hz):")

        # create a line edit to allow user input
        self.x1line_edit = QLineEdit()
        self.y1line_edit = QLineEdit()
        self.x2line_edit = QLineEdit()
        self.y2line_edit = QLineEdit()

        self.speedInput =  QLineEdit()
        self.oscillationInput = QLineEdit()
        self.rotationInput = QLineEdit()
        self.frequencyInput =  QLineEdit()
        #Adjusting layout within userinputs widget

        
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

        main_layout.addWidget(self.tabs)

        # layout2.addLayout(layout)
        # layout2.addWidget(self.tabs)
        self.setLayout(main_layout)
        # self.setLayout(layout)

        self.x1line_edit.editingFinished.connect(lambda: self.updateLine('x1'))
        self.y1line_edit.editingFinished.connect(lambda: self.updateLine('y1'))
        self.x2line_edit.editingFinished.connect(lambda: self.updateLine('x2'))
        self.y2line_edit.editingFinished.connect(lambda: self.updateLine('y2'))


    #Get show coordinates based on line drawn with mouse
    def updateStart(self):

        self.x1line_edit.setText(str(self.MotorMovement.getPoints()[0].x()))
        self.y1line_edit.setText(str(self.MotorMovement.getPoints()[0].y()))
        
        if len(self.MotorMovement.getPoints()) > 1:
            self.x2line_edit.setText(str(self.MotorMovement.getPoints()[1].x()))
            self.y2line_edit.setText(str(self.MotorMovement.getPoints()[1].y()))
    
    #Draw line based on coordinates typed into text field
    def updateLine(self,point):
        self.start = QPoint()
        self.end =  QPoint()
        
        if self.x1line_edit.text() != "":
            self.start.setX(int(self.x1line_edit.text()))

            if self.y1line_edit.text() != "":
                self.start.setY(int(self.y1line_edit.text()))
                
                if len(self.MotorMovement.getPoints()) > 1:
                    self.MotorMovement.setPoints([self.start, self.MotorMovement.getPoints()[1]])
                else:
                    self.MotorMovement.setPoints([self.start])
                
                self.updateSignal.emit()
                print(point)

        if self.y1line_edit.text() != "":
            self.start.setY(int(self.y1line_edit.text()))

            if self.x1line_edit.text() != "":
                self.start.setX(int(self.x1line_edit.text()))
                
                if len(self.MotorMovement.getPoints()) > 1:
                    self.MotorMovement.setPoints([self.start, self.MotorMovement.getPoints()[1]])
                else:
                    self.MotorMovement.setPoints([self.start])
                
                self.updateSignal.emit()
                print(point)

        if self.x2line_edit.text() != "":
            self.end.setX(int(self.x2line_edit.text()))

            if self.y2line_edit.text() != "":
                self.end.setY(int(self.y2line_edit.text()))
                self.MotorMovement.setPoints([self.MotorMovement.getPoints()[0], self.end])
                
                self.updateSignal.emit()
                print(point)

        if self.y2line_edit.text() != "":
            self.end.setY(int(self.y2line_edit.text()))

            if self.x2line_edit.text() != "":
                self.end.setX(int(self.x2line_edit.text()))
                self.MotorMovement.setPoints([self.MotorMovement.getPoints()[0], self.end])

                self.updateSignal.emit()
                print(point)
