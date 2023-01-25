from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .DrawWidget import DrawWidget

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.drawWidget = DrawWidget()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vlay = QVBoxLayout(central_widget)
        vlay.setContentsMargins(0, 0, 0, 0)
        vlay.addStretch(1)
        vlay.addWidget(self.drawWidget, stretch=1)

        r = QGuiApplication.primaryScreen().availableGeometry()
        self.setGeometry(r)