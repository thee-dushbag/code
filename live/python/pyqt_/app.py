import sys

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


colors = (
    "red",
    "orange",
    "green",
    "blue",
    "yellow",
    "indigo",
    "purple",
    "orangered",
    "salmon",
    "wheat",
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)
        for _, color in colors:
            tabs.addTab(Color(color), color)
        self.setCentralWidget(tabs)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
