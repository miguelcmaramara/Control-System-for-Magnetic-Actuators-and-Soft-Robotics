from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .DrawWidget import DrawWidget

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


        central_widget = QWidget()
        self.drawWidget = DrawWidget(central_widget)
       
        #The below code format the layout using the GridLayout class
        #I dont think we should use it because its annoying when you try to adjust the size of widget or the window.
        #going to proceed without it and see what happens
        # gridlay = QGridLayout()
        # gridlay.addWidget(self.drawWidget, 1, 0)

        # gridlay.addItem(QSpacerItem(800,800), 1, 1)
        # gridlay.addItem(QSpacerItem(800, 800), 0, 1)
        # gridlay.addItem(QSpacerItem(800,800), 0, 0)

        # gridlay.setRowStretch(0,1)
        # gridlay.setColumnStretch(1,1)




        
        self.drawWidget.move(100,800)
        self.drawWidget.resize(700,500)

        # central_widget.setLayout(gridlay)

        self.setCentralWidget(central_widget)
        


        # vlay.setContentsMargins(0, 0, 0, 0)
        # # vlay.addStretch(1)
        # vlay.addWidget(self.drawer) #,stretch=0)


        # r = QGuiApplication.primaryScreen().availableGeometry()
        
        self.setGeometry(0,0,1500, 1500)