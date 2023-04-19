from PyQt5.QtCore import QPoint, Qt, pyqtSignal, QPointF
from PyQt5.QtGui import  QImage, QPainter, QPen, QColor
from PyQt5.QtWidgets import  QWidget

from .MotorMovement import MotorMovement


class DrawWidget(QWidget):
    #signal object allows for function in mainwindow to be triggered upon repainting
    #"painted.emit()"

   

    painted = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        

        #creating variables and object to store coordinates of mouse click points and 
        #track where in the drawing process the user is
        self.MotorMovement = MotorMovement()
        self.points = self.MotorMovement.getPoints()

        self.first_click = False
        self.last_click = False
        self.firstpoint = QPointF()
        self.last_point = QPointF()

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
        self.startColor = Qt.green
        self.endColor = Qt.red

    def updateSelf(self):
        self.points = self.MotorMovement.getPoints()
        print(self.points)
        self.update()   
        return
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
        
            self._image_layer = qimg
            self.update()




    def mousePressEvent(self, event):
        #on the first click, draw a circle showing where you clicked
        if len(self.points) == 0:
            self.points.append(event.pos()/self.scale)
            self.MotorMovement.setPoints(self.points)
            self.update()

        #on the second click, draw line to endpoint
        elif len(self.points) == 1:
            self.last_click = True
            self.points.append(event.pos()/self.scale)
            self.MotorMovement.setPoints(self.points)
            self.update()        

        #The following conditionals check if you are clicking wihtin a circle
        #This allows for easy line adjustment
        elif ( len(self.points)  == 2 and 
        self.points[1].x()*self.scale -20 <= event.pos().x() <= self.points[1].x()*self.scale + 20 
        and self.points[1].y()*self.scale -20 <= event.pos().y() <= self.points[1].y()*self.scale + 20 
        ):
            self.last_click = True
            self.points[1] = event.pos()/self.scale
            self.MotorMovement.setPoints(self.points)
            self.update() 

        elif ( len(self.points) == 2 and 
        self.points[0].x()*self.scale -20 <= event.pos().x() <= self.points[0].x()*self.scale + 20 
        and self.points[0].y()*self.scale -20 <= event.pos().y() <= self.points[0].y()*self.scale + 20 
        ):
            self.first_click = True
            self.last_point = event.pos()/self.scale
            self.points[0] = self.last_point
            self.MotorMovement.setPoints(self.points)
            self.update() 
        return

    def mouseMoveEvent(self, event):
        #Allows for the click and drag adjustment of the line
        if  self.last_click: #and event.pos().x()<350*self.scale and event.pos().y()<275*self.scale and event.pos().x()>0 and event.pos().y()>0:
            self.points[1] = event.pos()/self.scale
            if event.pos().x()>350*self.scale:
                self.points[1].setX(350)
            elif event.pos().x()<0:
                self.points[1].setX(0)
            if event.pos().y()>275*self.scale:
                self.points[1].setY(275)
            elif event.pos().y()<0:
                self.points[1].setY(0)
            self.MotorMovement.setPoints(self.points)
            self.update()

        elif self.first_click: #and event.pos().x()<350*self.scale and event.pos().y()<275*self.scale and event.pos().x()>0 and event.pos().y()>0:
            self.points[0] = event.pos()/self.scale
            if event.pos().x()>350*self.scale:
                self.points[0].setX(350)
            elif event.pos().x()<0:
                self.points[0].setX(0)
            if event.pos().y()>275*self.scale:
                self.points[0].setY(275)
            elif event.pos().y()<0:
                self.points[0].setY(0)
            self.MotorMovement.setPoints(self.points)
            self.update()

    def mouseReleaseEvent(self, event):
        self.last_click = False
        self.first_click = False


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPointF(), self._image_layer)

        #prevents painting on canvas before point specification
        if self.points == []:
            painter.end()
            return

        #draws starting point
        if len(self.points) == 1:
            painter.setPen(
                QPen(
                        self.startColor,
                        self.circleBrushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
            painter.drawEllipse(self.points[0]*self.scale, 20, 20)
            self.painted.emit()

        #draws remaining line and ending point
        if len(self.points) == 2:
            painter.drawImage(QPointF(), self._image_layer)
            painter.setPen(
                QPen(
                        self.startColor,
                        self.circleBrushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
            painter.drawEllipse(self.points[0]*self.scale, 20, 20)

            painter.setPen(
                QPen(
                        self.brushColor,
                        self.brushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
            painter.drawLine(self.points[0]*self.scale, self.points[1]*self.scale)

            painter.setPen(
                QPen(
                        self.endColor,
                        self.circleBrushSize,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin,
                    )
            )
            
            painter.drawEllipse(self.points[1]*self.scale, 20, 20)
            self.painted.emit()



        painter.end()
    def setScale(self,s):
        self.scale = s