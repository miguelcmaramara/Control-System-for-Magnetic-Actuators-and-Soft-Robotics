from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QLineEdit

from .DrawWidget import DrawWidget
# from .Window import Window

class StartStop(QWidget):
    def __init__(self, parent= None):
        super().__init__(parent)


        # DrawWidget_instance = DrawWidget()
        
        self.startButton = QPushButton('START')
        self.stopButton = QPushButton('STOP')

        

        layout = QHBoxLayout()
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)

        # # Create the button
        # button = QPushButton("Button 1")

        # # Create a vertical layout and add the button to it
        # layout = QVBoxLayout()
        # layout.addWidget(button)

        # Set the widget's layout
        self.setLayout(layout)


        
    
    def mousePressEvent(self,event):
        print("Clicking in startstop")
        return
