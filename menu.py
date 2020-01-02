import sys

from PyQt5.QtCore import QBasicTimer, Qt, QTimerEvent, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QTransform
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QProgressBar, QWidget, QPushButton


class Menu(QWidget):
    def __init__(self, parent):
        """

        @type parent: QMainWindow
        """
        super().__init__(parent)
        self.setFixedSize(parent.size())
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)

        self.play_btn = QPushButton("Play", self)
        self.play_btn.resize(400, 80)
        self.play_btn.clicked.connect(parent.close_menu)
        self.play_btn.move(300, 400)

        self.play_btn = QPushButton("Levels", self)
        self.play_btn.resize(400, 80)
        self.play_btn.clicked.connect(self.hide)
        self.play_btn.move(300, 480)

        self.play_btn = QPushButton("Saves", self)
        self.play_btn.resize(200, 50)
        self.play_btn.clicked.connect(self.hide)
        self.play_btn.move(300, 560)

        self.close_btn = QPushButton("Quit", self)
        self.close_btn.resize(200, 50)
        self.close_btn.clicked.connect(parent.close)
        self.close_btn.move(500, 560)


class LevelsMenu(QWidget):
    def __init__(self, parent, levels):
        super().__init__(parent)
        self.setFixedSize(parent.size())
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)
        ql_text=QLabel('Уровни', self)
        ql_text.move(400, 100)

        for i in range(0,len(levels)):
            btn=QPushButton('i+1', self)
            btn.resize(20,20)