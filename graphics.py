import math
import sys

from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui

from Point import Point
from ball import Ball
from colors import Colors
from frog import Frog
from game import Game
from level import Level


class MainGame(QMainWindow):
    def __init__(self, size_x, size_y, game):
        super().__init__()
        self.setFixedSize(size_x, size_y)
        self.game = game
        self.timer = QBasicTimer()
        self.pictures = dict()
        self.frog_picture = self.initialize_frog_picture()
        self.initialize_ball_pictures()
        self.mouse_cursor = Point(20, 20)
        self.offset = 1
        self.initUi()
        self.show()

    def initUi(self):
        self.setWindowTitle('Zuma')
        self.setMouseTracking(True)
        self.timer.start(30, self)

    def initialize_ball_pictures(self):
        tmp = self.game.level.sequence.head
        while tmp.past is not None:
            self.pictures[tmp.value] = self.create_QLable(tmp.value)
            self.pictures[tmp.value].show()
            tmp = tmp.past
        self.frog_picture.show()
        # print('balls is ok')

    def initialize_frog_picture(self):
        ql = QLabel(self)
        ql.setFixedSize(100, 100)
        pm = QPixmap(self.game.frog.color.value).scaled(100, 100)
        ql.setPixmap(pm)
        self.move_ball(ql, Ball(self.game.frog.position.x, self.game.frog.position.y, Colors.frog))
        # print('frog is ok')
        return ql

    def create_QLable(self, ball):
        ql = QLabel(self)
        qp = QPixmap(ball.color.value).scaled(Ball.RADIUS, Ball.RADIUS)
        ql.setPixmap(qp)
        ql.setFixedSize(Ball.RADIUS, Ball.RADIUS)
        # print('create ql')
        return ql

    def update_graphics(self):
        # print('go gog')
        tmp = self.game.level.sequence.head
        # print('start graph update')
        while tmp.past is not None:
            self.move_ball(self.pictures[tmp.value], tmp.value)
            tmp = tmp.past
        # print('was update')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.game.frog.swap_balls()
            print('space')

        t = QTransform().rotate(30)
        print('go')
        t.translate(self.frog_picture.width() / 2, self.frog_picture.height() / 2)
        self.frog_picture.setPixmap(QPixmap(self.game.frog.color.value).scaled(100, 100).transformed(t))
        self.show()

    def mouseMoveEvent(self, event):
        self.mouse_cursor = Point(event.x(), event.y())

    def move_ball(self, ql: QLabel, b: Ball):
        ql.move(b.position.x, b.position.y)

    def timerEvent(self, e):
        self.game.update(self.offset, self.mouse_cursor)
        # print('game was update')
        self.update_graphics()
        # print('graphics was update')
        if self.game.is_ending:
            self.timer.stop()
        """t = QTransform()
        t.translate(self.frog_picture.width() / 2, self.frog_picture.height() / 2)
        t.rotate(self.game.frog.angle * 180 / math.pi)
        self.frog_picture.setPixmap(QPixmap(Colors.frog.value).transformed(t))"""


def main():
    app = QApplication(sys.argv)
    frog = Frog(Point(900, 300))
    level = Level(5, Point(100, 100), Point(700, 700))
    game = Game(frog, level)
    a = MainGame(1700, 1000, game)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
