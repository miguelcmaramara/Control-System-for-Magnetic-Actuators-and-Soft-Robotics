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

        self.testinput = QLineEdit()

        
        layout1.addWidget(self.DrawWidget, 0, 0)
        layout1.addWidget(self.StartStop, 1, 0)
        layout1.addWidget(self.UserInputs, 0,1)

        layout1.addWidget(self.testinput, 1, 1)

        layout1.setColumnStretch(0, 2)
        layout1.setColumnStretch(1, 1)

        # layout1.setRowStretch(3, 1)



        central_widget.setLayout(layout1)
        # self.StartStop.show()s

        dim = QApplication.desktop().screenGeometry()

        neww = int(dim.width() *(1/2))
        newh = int(dim.height() *(1/2))

        print(neww)
        print(newh)

        #Connecting drawwdiget paint event to updating points displayed on the window
        self.DrawWidget.painted.connect(self.UserInputs.updateStart)

        #Connecting userninputs changing text field to draw widget self.update
        self.UserInputs.updateSignal.connect(self.DrawWidget.updateSelf)


        #Setting drawwidget size
        self.DrawWidget.setMaximumSize(neww, newh)
        self.DrawWidget.setMinimumSize(neww,newh)

        self.StartStop.setMaximumSize(1080, 720)
        self.StartStop.setMinimumSize(1080,720)
        self.setCentralWidget(central_widget)       


        # self.DrawWidget.move(100,100)
        # self.DrawWidget.resize(1080,720)

        # widget1 = StartStop()
        # widget2 = Widget2()

        # # Create a horizontal layout and add the two widgets to it
        # layout = QHBoxLayout()
        # layout.addWidget(widget1)
        # layout.addWidget(widget2)

        # # Create a central widget and set its layout
        # central_widget = QWidget()
        # central_widget.setLayout(layout)

        # # Set the central widget of the main window
        # self.setCentralWidget(central_widget)

