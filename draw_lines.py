#
#__/\\\\\\\\\\\\__________/\\\\\_______/\\\\\_____/\\\__/\\\\__/\\\\\\\\\\\\\\\__
# _\/\\\////////\\\______/\\\///\\\____\/\\\\\\___\/\\\_\///\\_\///////\\\/////___
# _\/\\\______\//\\\___/\\\/__\///\\\__\/\\\/\\\__\/\\\__/\\/________\/\\\_________
#  _\/\\\_______\/\\\__/\\\______\//\\\_\/\\\//\\\_\/\\\_\//__________\/\\\_________
#   _\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\\//\\\\/\\\______________\/\\\_________
#    _\/\\\_______\/\\\_\//\\\______/\\\__\/\\\_\//\\\/\\\______________\/\\\_________
#     _\/\\\_______/\\\___\///\\\__/\\\____\/\\\__\//\\\\\\______________\/\\\_________
#      _\/\\\\\\\\\\\\/______\///\\\\\/_____\/\\\___\//\\\\\______________\/\\\_________
#       _\////////////__________\/////_______\///_____\/////_______________\///__________
# __/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\_____/\\\\\\\\\\\__/\\\\\\\\\\\\\\\__
#  _\/\\\///////////__\/\\\////////\\\__\/////\\\///__\///////\\\/////___
#  _\/\\\_____________\/\\\______\//\\\_____\/\\\___________\/\\\_________
#   _\/\\\\\\\\\\\_____\/\\\_______\/\\\_____\/\\\___________\/\\\_________
#    _\/\\\///////______\/\\\_______\/\\\_____\/\\\___________\/\\\_________
#     _\/\\\_____________\/\\\_______\/\\\_____\/\\\___________\/\\\_________
#      _\/\\\_____________\/\\\_______/\\\______\/\\\___________\/\\\_________
#       _\/\\\\\\\\\\\\\\\_\/\\\\\\\\\\\\/____/\\\\\\\\\\\_______\/\\\_________
#        _\///////////////__\////////////_____\///////////________\///__________
#__/\\\\\\\\\\\\\____/\\\_________________/\\\\\\\\\\\___       
# _\/\\\/////////\\\_\/\\\_______________/\\\/////////\\\_      
# _\/\\\_______\/\\\_\/\\\______________\//\\\______\///__      
#  _\/\\\\\\\\\\\\\/__\/\\\_______________\////\\\_________     
#   _\/\\\/////////____\/\\\__________________\////\\\______    
#    _\/\\\_____________\/\\\_____________________\////\\\___   
#     _\/\\\_____________\/\\\______________/\\\______\//\\\__  
#      _\/\\\_____________\/\\\\\\\\\\\\\\\_\///\\\\\\\\\\\/___ 
#       _\///______________\///////////////____\///////////_____
# 
# Thx -Miguel
# if u need to its ok, i get it

import sys

from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QGuiApplication, QImage, QPainter, QPen, QColor
from PyQt5.QtWidgets import  QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLabel, QLineEdit


class Drawer(QWidget):
    painted = pyqtSignal()

    def __init__(self, parent= None):
        super().__init__(parent)

        #creating variables and object to store coordinates of mouse click points and 
        #track where in the drawing process the user is
        self.points = []
        self.first_click = False
        self.last_click = False
        self.firstpoint = QPoint()
        self.last_point = QPoint()

        #creating Qcolor object in order to assign specific colors to widget
        color = QColor("#D0d8dc")

        #creating an image oject that drawing will be done on.
        #self.size() makes it the size of the Drawer object 
        self._image_layer = QImage(self.size(), QImage.Format_RGB32)
        self._image_layer.fill(color)

        #specifying brush settings for the drawing of the line
        self.brushSize = 7
        self.circleBrushSize = 3
        self.brushColor = Qt.black

    def resizeEvent(self, event):
        
        #This function allows for the resizing of the image layer whenever the drawing widget is resized (no real purpose as of now, comeback to this later)
        if (
            self.size().width() > self._image_layer.width()
            or self.size().height() > self._image_layer.height() or self.size().width() < self._image_layer.width()
            or self.size().height() < self._image_layer.height()
        ):
            qimg = QImage(
                max(self.size().width(), self._image_layer.width()),
                max(self.size().height(), self._image_layer.height()),
                QImage.Format_RGB32,
            )
            qimg.fill(QColor("#D0d8dc"))
            painter = QPainter(qimg)
            # painter.drawImage(QPoint(), self._image_layer)

            # painter.end()
            self._image_layer = qimg
            self.update()



    def mousePressEvent(self, event):
        #on the first click, draw a circle showing where you clicked
        if len(self.points) == 0:
            self.points.append(event.pos())
            self.update()

        #on the second click, draw line to endpoint
        elif len(self.points) == 1:
            self.last_click = True
            self.points.append(event.pos())
            self.update()        

        elif ( len(self.points)  == 2 and 
        self.points[1].x() -20 <= event.pos().x() <= self.points[1].x() + 20 
        and self.points[1].y() -20 <= event.pos().y() <= self.points[1].y() + 20 
        ):
            self.last_click = True
            self.points[1] = event.pos()
            self.update() 

        elif ( len(self.points) == 2 and 
        self.points[0].x() -20 <= event.pos().x() <= self.points[0].x() + 20 
        and self.points[0].y() -20 <= event.pos().y() <= self.points[0].y() + 20 
        ):
            self.first_click = True
            self.last_point = event.pos()
        
            self.points[0] = self.last_point
            self.update() 
        return
     

        
    

    def mouseMoveEvent(self, event):
        if  self.last_click:
            self.points[1] = event.pos()
            self.update()

        elif self.first_click:
            self.points[0] = event.pos()
            self.update()



    def mouseReleaseEvent(self, event):
        self.last_click = False
        


    def paintEvent(self, event):
        painter = QPainter(self)
        # img_painter = QPainter(self._image_layer)
        painter.drawImage(QPoint(), self._image_layer)


        if self.points == []:
            return

        if len(self.points) == 1:
            painter.setPen(
                QPen(
                        self.brushColor,
                        self.circleBrushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
        
            painter.drawEllipse(self.points[0], 20, 20)
            self.painted.emit()


        if len(self.points) == 2:

            painter.drawImage(QPoint(), self._image_layer)
            # img_painter = QPainter(self._image_layer)
            painter.setPen(
                QPen(
                        self.brushColor,
                        self.circleBrushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
            painter.drawEllipse(self.points[0], 20, 20)


            painter.setPen(
                QPen(
                        self.brushColor,
                        self.brushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
            painter.drawLine(self.points[0], self.points[1])

            painter.setPen(
                QPen(
                        self.brushColor,
                        self.circleBrushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
            
            painter.drawEllipse(self.points[1], 20, 20)
            self.painted.emit()



        painter.end()
        
        


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


        central_widget = QWidget()
        self.drawer = Drawer(central_widget)
       
    
        self.drawer.move(100,800)
        self.drawer.resize(1080,720)


        # self.setCentralWidget(central_widget)
        # # self.setGeometry(0,0,2330, 1770)
        # self.setGeometry(0,0,2000, 1600)

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
        
        # set the central widget for the main window
        self.setCentralWidget(central_widget)

        # set the size and position of the main window
        self.setGeometry(0, 0, 2000, 1600)

        self.drawer.painted.connect(self.updateStart)
        
        self.x1line_edit.textChanged.connect(lambda: self.updateLine('x1'))
        self.y1line_edit.textChanged.connect(lambda: self.updateLine('y1'))
        self.x2line_edit.textChanged.connect(lambda: self.updateLine('x2'))
        self.y1line_edit.textChanged.connect(lambda: self.updateLine('y2'))


    def updateStart(self):
        self.x1line_edit.setText(str(self.drawer.points[0].x()))
        self.y1line_edit.setText(str(self.drawer.points[0].y()))
        
        if len(self.drawer.points) > 1:
            self.x2line_edit.setText(str(self.drawer.points[1].x()))
            self.y2line_edit.setText(str(self.drawer.points[1].y()))
        
        print(self.drawer.points)
        return
    
    #/////////////////////////////////////////////////////////////////////////////////////////////////////
    #Important: as of right now, user must put start coordinates before end cooridinates if starting from 
    #empty start and end fields. Will revise this soon
    #////////////////////////////////////////////////////////////////////////////////////////////////////

    def updateLine(self, point):
        self.start = QPoint()
        self.end =  QPoint()
        
        if self.x1line_edit.text() != "" and self.y1line_edit.text() != "":
            self.start.setX(int(self.x1line_edit.text()))
            self.start.setY(int(self.y1line_edit.text()))
            if len(self.drawer.points) > 0:
                self.drawer.points[0] = self.start
            else:
                self.drawer.points.append(self.start)
        
        if self.x2line_edit.text() != "" and self.y2line_edit.text() != "":
            self.end.setX(int(self.x2line_edit.text()))
            self.end.setY(int(self.y2line_edit.text()))
            if len(self.drawer.points) > 1:
                self.drawer.points[1] = self.end
            elif len(self.drawer.points) == 1:
                self.drawer.points.append(self.end)
        
        
        self.drawer.update()
   
        if point == 'x1':
            print ('x1 changed')
        if point == 'y1':
            print ('y1 changed')
        if point == 'x2':
            print ('x2 changed')
        if point == 'y2':
            print ('y2 changed')





       


    def resizeEvent(self, event):
        # print(self.size())
        pass
    
    def mousePressEvent(self, event):
        return
        print(type(event.pos().x()))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()


    screen_geometry = app.desktop().screenGeometry()
    x = (screen_geometry.width()-window.width()) / 2
    y = (screen_geometry.height()-window.height()) / 2


    placement = QPoint(int(x),int(y))

    # print(screen_geometry)
    # print(placement)
    # print(window.width(), window.height())

    window.move(placement)
    window.show()


    sys.exit(app.exec())





 #****The below code format the layout using the GridLayout class****
        # central_widget.setLayout(gridlay)
        #I dont think we should use it because its annoying when you try to adjust the size of widget or the window.
        #going to proceed without it and see what happens
        # gridlay = QGridLayout()
        # gridlay.addWidget(self.drawer, 1, 0)

        # gridlay.addItem(QSpacerItem(800,800), 1, 1)
        # gridlay.addItem(QSpacerItem(800, 800), 0, 1)
        # gridlay.addItem(QSpacerItem(800,800), 0, 0)

        # gridlay.setRowStretch(0,1)
        # gridlay.setColumnStretch(1,1)

        
        # vlay.setContentsMargins(0, 0, 0, 0)
        # # vlay.addStretch(1)
        # vlay.addWidget(self.drawer) #,stretch=0)


        # r = QGuiApplication.primaryScreen().availableGeometry()

        #**************************************************************************************************************