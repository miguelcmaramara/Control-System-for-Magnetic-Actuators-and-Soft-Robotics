from multiprocessing.connection import Connection
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QLabel, QPushButton, QApplication, QLineEdit

from .DrawWidget import DrawWidget
from .StartStop import StartStop
from .UserInputs import UserInputs
from .MotorMovement import MotorMovement

import time

class Window(QMainWindow):
    def __init__(self, conn: Connection, parent=None):
        super().__init__(parent)

        #print(f"Machine status: {conn.recv()}")
        self.conn = conn
        # Testing multi-processing
        # start_time = time.time()
        # for i in range(1000000000):
            # pass
        # end_time = time.time()
        # print(f"Parent process finished in {end_time - start_time} seconds")


        #setting layout
        layout1 = QGridLayout()


        #initializing widgets
        central_widget = QWidget()
        self.WindowMotorMovement = MotorMovement()

        self.DrawWidget = DrawWidget()

        self.DrawWidget.MotorMovement = self.WindowMotorMovement
        self.StartStop = StartStop(self.conn, self.WindowMotorMovement)
        self.UserInputs = UserInputs()
        self.UserInputs.MotorMovement = self.WindowMotorMovement

        
        layout1.addWidget(self.DrawWidget, 0, 0)
        layout1.addWidget(self.StartStop, 1, 0)
        layout1.addWidget(self.UserInputs, 0,1, -1,1)
    


        #set layout
        central_widget.setLayout(layout1)

        
        dim = QApplication.desktop().screenGeometry()

        neww = int(dim.width() *(1/2))
        newh = int(dim.height() *(2/3))

        print(neww)
        print(newh)

        #Connecting drawwdiget paint event to updating points displayed on the window
        self.DrawWidget.painted.connect(self.UserInputs.updateStart)

        #Connecting userninputs changing text field to draw widget self.update
        self.UserInputs.updateSignal.connect(self.DrawWidget.updateSelf)


        #Setting drawwidget size
        #self.DrawWidget.setMaximumSize(neww, newh)
        #self.DrawWidget.setMinimumSize(neww,newh)
        scale = min(neww/350, newh/260)
        self.DrawWidget.setMaximumSize(350*scale, 260*scale)
        self.DrawWidget.setMinimumSize(350*scale,260*scale)
        self.DrawWidget.setScale(scale)

        #self.StartStop.setMaximumSize(1080, 720)
        #self.StartStop.setMinimumSize(1080,720)
        self.setCentralWidget(central_widget)       


