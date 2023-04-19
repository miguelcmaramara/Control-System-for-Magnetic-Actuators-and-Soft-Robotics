from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QLabel, QPushButton, QApplication, QLineEdit

from .DrawWidget import DrawWidget
from .StartStop import StartStop
from .UserInputs import UserInputs
from .MotorMovement import MotorMovement


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


        layout1 = QGridLayout()
        central_widget = QWidget()


        self.WindowMotorMovement = MotorMovement()

        self.DrawWidget = DrawWidget()

        self.DrawWidget.MotorMovement = self.WindowMotorMovement
        self.StartStop = StartStop()
        self.UserInputs = UserInputs()
        self.UserInputs.MotorMovement = self.WindowMotorMovement

        


        
        layout1.addWidget(self.DrawWidget, 0, 0)
        layout1.addWidget(self.StartStop, 1, 0)
        layout1.addWidget(self.UserInputs, 0,1, -1,1)
    



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
        scale = min(neww/350, newh/275)
        self.DrawWidget.setMaximumSize(350*scale, 275*scale)
        self.DrawWidget.setMinimumSize(350*scale,275*scale)
        self.DrawWidget.setScale(scale)

        #self.StartStop.setMaximumSize(1080, 720)
        #self.StartStop.setMinimumSize(1080,720)
        self.setCentralWidget(central_widget)       


