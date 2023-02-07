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

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QGuiApplication, QImage, QPainter, QPen, QColor
from PyQt5.QtWidgets import *# QApplication, QMainWindow, QVBoxLayout, QWidget


class Drawer(QWidget):
    def __init__(self, parent= None):
        super().__init__(parent)

        #creating variables and object to store coordinates of mouse click points and 
        #track where in the drawing process the user is
        self.firstclick = True
        self.firstpoint = QPoint()

        self._drawing = False
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
        if (
            self.size().width() > self._image_layer.width()
            or self.size().height() > self._image_layer.height()
        ):
            qimg = QImage(
                max(self.size().width(), self._image_layer.width()),
                max(self.size().height(), self._image_layer.height()),
                QImage.Format_RGB32,
            )
            qimg.fill(QColor("#D0d8dc"))
            painter = QPainter(qimg)
            painter.drawImage(QPoint(), self._image_layer)
            painter.end()
            self._image_layer = qimg
            self.update()



    def mousePressEvent(self, event):

        #on the first click, draw a circle showing where you clicked
        if self.firstclick == True:
            self.firstpoint = event.pos()
            painter = QPainter(self._image_layer)
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.circleBrushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawEllipse(self.firstpoint, 20, 20)
            self.update()

        #on the second click, draw line to endpoint
        else:
            self.last_point = event.pos()

            painter = QPainter(self._image_layer)
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawLine(self.firstpoint, self.last_point)

            painter.setPen(
                QPen(
                    self.brushColor,
                    self.circleBrushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawEllipse(self.last_point, 20, 20)

            self.update()
        
        #mycode
        self._drawing = True
        # self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self._drawing and event.buttons() & Qt.LeftButton:
            painter = QPainter(self._image_layer)
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawLine(self.firstpoint, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.firstclick = not self.firstclick


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(), self._image_layer)
        painter.end()
        


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


        central_widget = QWidget()
        self.drawer = Drawer(central_widget)
       
        #The below code format the layout using the GridLayout class
        #I dont think we should use it because its annoying when you try to adjust the size of widget or the window.
        #going to proceed without it and see what happens
        # gridlay = QGridLayout()
        # gridlay.addWidget(self.drawer, 1, 0)

        # gridlay.addItem(QSpacerItem(800,800), 1, 1)
        # gridlay.addItem(QSpacerItem(800, 800), 0, 1)
        # gridlay.addItem(QSpacerItem(800,800), 0, 0)

        # gridlay.setRowStretch(0,1)
        # gridlay.setColumnStretch(1,1)




        
        self.drawer.move(100,800)
        self.drawer.resize(700,500)

        # central_widget.setLayout(gridlay)

        self.setCentralWidget(central_widget)
        


        # vlay.setContentsMargins(0, 0, 0, 0)
        # # vlay.addStretch(1)
        # vlay.addWidget(self.drawer) #,stretch=0)


        # r = QGuiApplication.primaryScreen().availableGeometry()
        
        self.setGeometry(0,0,1500, 1500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()


    screen_geometry = app.desktop().screenGeometry()
    x = (screen_geometry.width()-window.width()) / 2
    y = (screen_geometry.height()-window.height()) / 2


    placement = QPoint(int(x),int(y))

    # print(screen_geometry)
    print(placement)
    print(window.width(), window.height())

    window.move(placement)
    window.show()


    sys.exit(app.exec())