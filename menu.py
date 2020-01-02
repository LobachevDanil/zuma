import sys
import copy
import time

from PyQt5.QtCore import QBasicTimer, Qt, QTimerEvent, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QTransform, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QProgressBar, QWidget, QPushButton, \
    QLineEdit

from player import Player


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

        ql_text = QLabel('ZUMA', self)
        # ql_text.textFormat(Qt.Text)
        ql_text.setFont(QFont("sefif", 40))
        ql_text.move(420, 250)

        self.player = None
        qle = QLineEdit(self)
        qle.move(420, 350)
        qle.textChanged[str].connect(self.update_player)

        self.output = QLabel(self)
        self.output.move(420, 320)

        self.play_btn = QPushButton("Play", self)
        self.play_btn.resize(400, 80)
        self.play_btn.clicked.connect(parent.close_menu)
        self.play_btn.move(300, 400)

        self.play_btn = QPushButton("Levels", self)
        self.play_btn.resize(400, 80)
        self.play_btn.clicked.connect(parent.change_level)
        self.play_btn.move(300, 480)

        self.play_btn = QPushButton("Saves", self)
        self.play_btn.resize(200, 50)
        self.play_btn.clicked.connect(parent.load_past_game)
        self.play_btn.move(300, 560)

        self.close_btn = QPushButton("Quit", self)
        self.close_btn.resize(200, 50)
        self.close_btn.clicked.connect(parent.close)
        self.close_btn.move(500, 560)

    def update_player(self, name):
        self.player = name

    def get_player(self):
        if self.player is not None:
            return Player(self.player)
        else:
            return None

    def print_message(self, text):
        self.output.setText(text)
        self.output.adjustSize()
        self.output.show()


class LevelsMenu(QWidget):
    def __init__(self, parent, levels):
        super().__init__(parent)
        self.setFixedSize(parent.size())
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)
        ql_text = QLabel('Уровни', self)
        ql_text.move(400, 100)
        btns = []
        for i in range(0, len(levels)):
            btns.append(LevelButton(i, self, parent))
            btns[i].resize(50, 50)
            btns[i].move(50 + 100 * i, 200)


class LevelButton(QPushButton):
    def __init__(self, parameter, parent, dad):
        super().__init__(str(parameter + 1), parent)
        self.clicked.connect(lambda: dad.close_level_menu(parameter))
