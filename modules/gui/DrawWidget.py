from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import  QImage, QPainter, QPen, QColor
from PyQt5.QtWidgets import  QWidget


class DrawWidget(QWidget):
    def __init__(self, parent=None):
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
