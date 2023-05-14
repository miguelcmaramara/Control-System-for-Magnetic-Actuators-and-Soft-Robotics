from multiprocessing.connection import Connection
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QLabel, QPushButton, QApplication, QLineEdit, QMessageBox

from ..shared.machinestatus import MachineStatus
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
        self.UserInputs = UserInputs(self.conn, self.WindowMotorMovement)
        #self.UserInputs.MotorMovement = self.WindowMotorMovement

        
        layout1.addWidget(self.DrawWidget, 0, 0)
        layout1.addWidget(self.StartStop, 1, 0)
        layout1.addWidget(self.UserInputs, 0,1, -1,1)
    


        #set layout
        central_widget.setLayout(layout1)

        #find screen geometry
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
        #finds the proper scale for the widget that the bounds could fit properly based on the different moniter size
        scale = min(neww/350, newh/260)
        #set the draw widget to the proper scale and inform it able the scale
        self.DrawWidget.setMaximumSize(350*scale, 260*scale)
        self.DrawWidget.setMinimumSize(350*scale,260*scale)
        self.DrawWidget.setScale(scale)

        #self.StartStop.setMaximumSize(1080, 720)
        #self.StartStop.setMinimumSize(1080,720)
        self.setCentralWidget(central_widget)
        #creates a timer used to read if messages are being sent from the back end
        self.message = QTimer()
        self.message.timeout.connect(self.show_message)
        self.message.start(100)

    #function called at ever instance of the timer
    def show_message(self):
        #if a message is send from the back end
        if self.conn.poll():
                #read the message
                stat=self.conn.recv()
                #if it is any error message
                if stat==MachineStatus.ERROR:
                    #the next message would be a string containing message details
                    message =self.conn.recv()
                    msg = QMessageBox()
                    #display the message in a message box to have it pop up for the user
                    if message=="System is now home.":
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Information") 
                    else:
                        msg.setIcon(QMessageBox.Warning)
                        msg.setWindowTitle("Warning")
                    msg.setText(message)
                    msg.exec_()

    #if the window is closing, send a message to the back end so that process could end as well.
    def closeEvent(self, event):
        self.conn.send(MachineStatus.KILL)
        event.accept()

