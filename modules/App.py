from PyQt5.QtWidgets import QApplication
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
    window.show()
    app.exec()