from multiprocessing.connection import Connection
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QMainWindow, QPushButton, QWidget, QVBoxLayout, QGridLayout, QCheckBox, QLabel, QLineEdit
from ..shared.machinestatus import MachineStatus

from .DrawWidget import DrawWidget
# from .Window import Window

class StartStop(QWidget):
    def __init__(self, conn: Connection, motor_move=None, parent= None):
        super().__init__(parent)


        # DrawWidget_instance = DrawWidget()
        self.motor_movement = motor_move
        #creates all the buttons
        self.startButton = QPushButton('START')
        self.stopButton = QPushButton('STOP')
        self.conn = conn
        self.returnHomeButton = QPushButton('RETURN TO HOME')
        self.moveButton = QPushButton('GO TO START POSITION')
        #connect the button presses to an event
        self.startButton.clicked.connect(self.startPressEvent)
        self.stopButton.clicked.connect(self.stopPressEvent)
        self.returnHomeButton.clicked.connect(self.homePressEvent)
        self.moveButton.clicked.connect(self.returnStartPressEvent)
        

        layout = QGridLayout()
        #place the buttons in the grid layout
        layout.addWidget(self.startButton,0,0)
        layout.addWidget(self.stopButton,0,1)
        layout.addWidget(self.returnHomeButton,1,0)
        layout.addWidget(self.moveButton,1,1)

        # # Create the button
        # button = QPushButton("Button 1")

        # # Create a vertical layout and add the button to it
        # layout = QVBoxLayout()
        # layout.addWidget(button)

        # Set the widget's layout
        self.setLayout(layout)


        
    
    def mousePressEvent(self,event):
        #print("Clicking in startstop")
        # Trigger run function
        #self.conn.send(MachineStatus.RUNNING)
        return

    #tells the back end to start the motion and sends the motor movement objects
    #only sends if there are 2 points in the system
    def startPressEvent(self):
        if len(self.motor_movement.getPoints())==2:
            self.conn.send(MachineStatus.RUNNING)
            self.conn.send(self.motor_movement)
            pass
        #Trigger run function
        #self.conn.send(MachineStatus.DEBUG)
        return
    
    #sends a message to the back end to stop all motions
    def stopPressEvent(self):
        
        self.conn.send(MachineStatus.OFF)
        return
    
    #sends a message to the back end to home the system
    def homePressEvent(self):
        self.conn.send(MachineStatus.HOME)
        return
    
    #sends a message to the back end to got the the start postion and then sends the motor movement object
    #only sends if there is at least one point 
    def returnStartPressEvent(self):
        if len(self.motor_movement.getPoints())>0:
            self.conn.send(MachineStatus.GOPOS)
            self.conn.send(self.motor_movement)
        return