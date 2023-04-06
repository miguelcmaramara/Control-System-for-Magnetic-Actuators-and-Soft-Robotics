from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import  QGridLayout, QWidget, QLabel, QLineEdit

from .DrawWidget import DrawWidget
from .MotorMovement import MotorMovement

class UserInputs(QWidget):
    updateSignal = pyqtSignal()

    def __init__(self, parent= None):
        super().__init__(parent)



        self.MotorMovement = MotorMovement()
        layout = QGridLayout()
        
        self.startLabel = QLabel("Start")
        self.endLabel = QLabel("End")

        self.xLabel1 = QLabel("X:")
        self.yLabel1 = QLabel("Y:")

        self.xLabel2 = QLabel("X:")
        self.yLabel2 = QLabel("Y:")



        self.startLabel.resize(200, 160)

        #self.endLabel.resize(200, 160)

        # create a line edit to allow user input
        self.x1line_edit = QLineEdit()
        #self.x1line_edit.resize(100, 70)

        self.y1line_edit = QLineEdit()
        #self.y1line_edit.resize(100, 70)


        self.x2line_edit = QLineEdit()
        #self.x2line_edit.resize(100, 70)

        self.y2line_edit = QLineEdit()
        #self.y2line_edit.resize(100, 70)


        #Adjusting layout within userinputs widget

        
        layout.addWidget(self.startLabel, 0, 0)
        layout.addWidget(self.endLabel, 0, 2)
        layout.addWidget(self.xLabel1, 1, 0)
        layout.addWidget(self.x1line_edit, 1, 1)
        layout.addWidget(self.yLabel1, 2, 0)
        layout.addWidget(self.y1line_edit, 2, 1)

        layout.addWidget(self.xLabel2, 1, 2)
        layout.addWidget(self.x2line_edit, 1, 3)
        layout.addWidget(self.yLabel2, 2, 2)
        layout.addWidget(self.y2line_edit, 2, 3)

        self.setLayout(layout)


            
        # self.x1line_edit.textChanged.connect(lambda: self.updateLine('x1'))
        # self.y1line_edit.textChanged.connect(lambda: self.updateLine('y1'))
        # self.x2line_edit.textChanged.connect(lambda: self.updateLine('x2'))
        # self.y1line_edit.textChanged.connect(lambda: self.updateLine('y2'))

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


          

        # if self.x1line_edit.text() != "" and self.y1line_edit.text() != "":
        #     self.start.setX(int(self.x1line_edit.text()))
        #     self.start.setY(int(self.y1line_edit.text()))
        #     if len(self.MotorMovement.getPoints()) > 1:
        #         self.MotorMovement.setPoints([self.start, self.MotorMovement.getPoints()[1]])
        #     else:
        #         self.MotorMovement.setPoints([self.start])
        
        # if self.x2line_edit.text() != "" and self.y2line_edit.text() != "":
        #     self.end.setX(int(self.x2line_edit.text()))
        #     self.end.setY(int(self.y2line_edit.text()))
        #     self.MotorMovement.setPoints([self.MotorMovement.getPoints()[0], self.end])
        #     if len(self.MotorMovement.getPoints()) > 1:
        #         self.MotorMovement.setPoints([self.MotorMovement.getPoints()[0], self.end])
           

        # if self.x1line_edit.text() == "" or self.y1line_edit.text() == "":
        #     if len(self.MotorMovement.getPoints()) > 1:
        #         self.MotorMovement.setPoints([self.start, self.MotorMovement.getPoints()[1]])
        #     else:
        #         self.MotorMovement.setPoints([self.start])

        # if self.x2line_edit.text() == "" or self.y2line_edit.text() == "":
        #     if len(self.MotorMovement.getPoints()) > 1:
        #         self.MotorMovement.setPoints([self.start, self.MotorMovement.getPoints()[1]])
        #     else:
        #         self.MotorMovement.setPoints([self.start])
            
        
        # #Update drawer
        # self.updateSignal.emit()
        # self.DrawWidget_instance.update()