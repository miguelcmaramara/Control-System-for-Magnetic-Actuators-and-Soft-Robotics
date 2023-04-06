from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint
from .gui.Window import Window

"""
equivalent to: 
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
"""

def run(sysargs):
    app = QApplication(sysargs)
    window = Window()

    screen_geometry = app.desktop().screenGeometry()
    x = (screen_geometry.width()-window.width()) / 2
    y = (screen_geometry.height()-window.height()) / 2

    placement = QPoint(int(x),int(y))

    # print(screen_geometry)

    window.move(placement)

    window.show()
    app.exec()