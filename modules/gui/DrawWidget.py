from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import  QImage, QPainter, QPen
from PyQt5.QtWidgets import  QWidget


class DrawWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        #my code

        self.firstclick = True
        self.firstpoint = QPoint()
        #my code

        self._drawing = False
        self.last_point = QPoint()

        self._image_layer = QImage(self.size(), QImage.Format_RGB32)
        self._image_layer.fill(Qt.gray)

        self.brushSize = 2
        self.brushColor = Qt.black

    def mousePressEvent(self, event):

        #mycode
        if self.firstclick == True:
            self.firstpoint = event.pos()
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
            self.update()

    def mouseReleaseEvent(self, event):
        self.firstclick = not self.firstclick

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(), self._image_layer)
        painter.end()
        

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
            qimg.fill(Qt.gray)
            painter = QPainter(qimg)
            painter.drawImage(QPoint(), self._image_layer)
            painter.end()
            self._image_layer = qimg
            self.update()



