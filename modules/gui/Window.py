from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLabel, QLineEdit

from .DrawWidget import DrawWidget

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


        central_widget = QWidget()
        self.DrawWidget = DrawWidget(central_widget)
       
        #The below code format the layout using the GridLayout class
        #I dont think we should use it because its annoying when you try to adjust the size of widget or the window.
        #going to proceed without it and see what happens
        # gridlay = QGridLayout()
        # gridlay.addWidget(self.DrawWidget, 1, 0)

        # gridlay.addItem(QSpacerItem(800,800), 1, 1)
        # gridlay.addItem(QSpacerItem(800, 800), 0, 1)
        # gridlay.addItem(QSpacerItem(800,800), 0, 0)

        # gridlay.setRowStretch(0,1)
        # gridlay.setColumnStretch(1,1)

        # central_widget.setLayout(gridlay)

        self.DrawWidget.move(100,800)
        self.DrawWidget.resize(1080,720)

        #Creating labels for text input fields
        self.startLabel = QLabel("Start", central_widget)
        self.endLabel = QLabel("End", central_widget)

        self.xLabel1 = QLabel("X:", central_widget)
        self.yLabel1 = QLabel("Y:", central_widget)

        self.xLabel2 = QLabel("X:", central_widget)
        self.yLabel2 = QLabel("Y:", central_widget)

        self.xLabel1.move (1200, 1150)
        self.yLabel1.move (1200, 1250)

        self.xLabel2.move (1470, 1150)
        self.yLabel2.move (1470, 1250)


        self.startLabel.move(1200, 1000)
        self.startLabel.resize(200, 160)

        self.endLabel.move(1500, 1000)
        self.endLabel.resize(200, 160)

        # create a line edit to allow user input
        self.x1line_edit = QLineEdit(central_widget)
        self.x1line_edit.move(1250, 1150)
        self.x1line_edit.resize(100, 70)

        self.y1line_edit = QLineEdit(central_widget)
        self.y1line_edit.move(1250, 1250)
        self.y1line_edit.resize(100, 70)


        self.x2line_edit = QLineEdit(central_widget)
        self.x2line_edit.move(1520, 1150)
        self.x2line_edit.resize(100, 70)

        self.y2line_edit = QLineEdit(central_widget)
        self.y2line_edit.move(1520, 1250)
        self.y2line_edit.resize(100, 70)


        # vlay.setContentsMargins(0, 0, 0, 0)
        # # vlay.addStretch(1)
        # vlay.addWidget(self.DrawWidget) #,stretch=0)


        # r = QGuiApplication.primaryScreen().availableGeometry()
        
        #set the central widget for the main window
        self.setCentralWidget(central_widget)

        #set the size and position of the main window
        self.setGeometry(0,0,2000, 1600)

        #connect paint signal to function that handles coordinate visualization
        self.DrawWidget.painted.connect(self.updateStart)

        #connect change in text field to function that handles redrawing drawWidget

        self.x1line_edit.textChanged.connect(lambda: self.updateLine('x1'))
        self.y1line_edit.textChanged.connect(lambda: self.updateLine('y1'))
        self.x2line_edit.textChanged.connect(lambda: self.updateLine('x2'))
        self.y1line_edit.textChanged.connect(lambda: self.updateLine('y2'))

    def updateStart(self):
        self.x1line_edit.setText(str(self.DrawWidget.points[0].x()))
        self.y1line_edit.setText(str(self.DrawWidget.points[0].y()))
        
        if len(self.DrawWidget.points) > 1:
            self.x2line_edit.setText(str(self.DrawWidget.points[1].x()))
            self.y2line_edit.setText(str(self.DrawWidget.points[1].y()))
        

    def updateLine(self, point):
        self.start = QPoint()
        self.end =  QPoint()
        
        if self.x1line_edit.text() != "" and self.y1line_edit.text() != "":
            self.start.setX(int(self.x1line_edit.text()))
            self.start.setY(int(self.y1line_edit.text()))
            if len(self.DrawWidget.points) > 0:
                self.DrawWidget.points[0] = self.start
            else:
                self.DrawWidget.points.append(self.start)
        
        if self.x2line_edit.text() != "" and self.y2line_edit.text() != "":
            self.end.setX(int(self.x2line_edit.text()))
            self.end.setY(int(self.y2line_edit.text()))
            if len(self.DrawWidget.points) > 1:
                self.DrawWidget.points[1] = self.end
            elif len(self.DrawWidget.points) == 1:
                self.DrawWidget.points.append(self.end)
        
        
        self.DrawWidget.update()
   