from PyQt5.QtCore import QBasicTimer, Qt, QTimerEvent, QPoint, QSize
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QTransform, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QProgressBar, QWidget, QPushButton, \
    QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem

from player import Player


class Menu(QWidget):
    def __init__(self, parent):
        """
        Описывает главное окно
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
        self.output.move(500 - self.output.size().width() / 2, 320 - self.output.size().height() / 2)
        self.output.show()


class LevelsMenu(QWidget):
    def __init__(self, parent, levels):
        """Виджет меню выбора уровней"""
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
        """Описывает кнопки уровней"""
        super().__init__(str(parameter + 1), parent)
        self.clicked.connect(lambda: dad.close_level_menu(parameter))


class ResultTableWidget(QWidget):
    def __init__(self, table, parent, is_win):
        """
        Виджет окна результатов
        @type table: ResultTable
        """
        super().__init__(parent)
        self.setFixedSize(parent.size())
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green if is_win else Qt.red)
        self.setPalette(p)
        self.table = table

        qw = QWidget(self)

        result = QLabel('You Win!!!' if is_win else 'You Lose', self)
        result.setFixedSize(400, 50)
        result.move(370, 250)
        result.setFont(QFont("sefif", 40))
        result.show()

        players = self.table.get_table()
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(2)
        table_widget.setRowCount(5)
        table_widget.setHorizontalHeaderLabels(['Player', 'Scores'])
        table_widget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        i = 0
        for e in players:
            table_widget.setItem(i, 0, QTableWidgetItem(e.name))
            table_widget.setItem(i, 1, QTableWidgetItem(str(e.scores)))
            i += 1

        table_widget.setFixedSize(215, 185)
        table_widget.move(500 - 215 / 2, 450 - 185 / 2)
        qw.show()
