from multiprocessing.connection import Connection
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QMainWindow, QPushButton, QWidget, QVBoxLayout, QGridLayout, QCheckBox, QLabel, QLineEdit
from ..shared.machinestatus import MachineStatus

from .DrawWidget import DrawWidget
# from .Window import Window

class StartStop(QWidget):
    def __init__(self, conn: Connection, parent= None):
        super().__init__(parent)


        # DrawWidget_instance = DrawWidget()
        
        self.startButton = QPushButton('START')
        self.stopButton = QPushButton('STOP')
        self.conn = conn
        self.returnHomeButton = QPushButton('RETURN TO HOME')
        self.moveButton = QPushButton('GO TO START POSITION')

        

        layout = QGridLayout()
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
        print("Clicking in startstop")
        # Trigger run function
        self.conn.send(MachineStatus.RUNNING)
        return
