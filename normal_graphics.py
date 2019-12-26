import math
import sys

from PyQt5.QtCore import QBasicTimer, Qt, QTimerEvent, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QTransform
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel

from Point import Point
from ball import Ball
from bullet import Status
from frog import Frog
from game import Game
from level2 import Level2
from level4 import Level4
from level3 import Level3
from level5 import Level5

FROG_SIZE = 100


class Graphics(QMainWindow):
    def __init__(self, game, size):
        """
        :type game: Game
        :type size: Point
        """
        super().__init__()
        self.game = game
        self.pictures = dict()
        self.mouse_cursor = Point(size.x / 2, size.y - 1)
        self.size_vision = size

        self.setFixedSize(size.x, size.y)
        self.timer = QBasicTimer()
        self.initUi()

        self.frog_bullet = self.initialize_bullet()
        self.frog_picture = self.initialize_frog()
        self.bullet_pictures = dict()

        self.data = self.initialize_level_data()

    def initUi(self):
        self.setWindowTitle('Zuma')
        self.setMouseTracking(True)
        self.timer.start(30, self)
        self.show()

    def draw_ball(self, ql: QLabel, b: Ball):
        offset = Ball.RADIUS / 2
        ql.move(b.position.x - offset, b.position.y - offset)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.green)
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        self.draw_level(qp)
        self.update()
        qp.end()

    def draw_level(self, qp):
        level = self.game.level
        offset = Ball.RADIUS / 2
        qp.drawEllipse(level.start.x - offset, level.start.y - offset, Ball.RADIUS, Ball.RADIUS)
        qp.drawEllipse(level.end.x - offset, level.end.y - offset, Ball.RADIUS, Ball.RADIUS)
        qp.drawEllipse(self.game.frog.position.x, self.game.frog.position.y, 4, 4)
        # qp.drawLine(level.start.x, level.start.y, level.end.x, level.end.y)

        qp.drawPolyline(*self.initialize_level_data())

    def initialize_level_data(self):
        data = []
        for point in self.game.level.get_path():
            data.append(QPoint(point[0], point[1]))
        return data

    def update_graphic(self):
        self.refresh_textures()
        tmp = self.game.level.sequence.head
        while tmp is not None:
            self.draw_ball(self.pictures[tmp.value], tmp.value)
            tmp = tmp.past
        for bullet, picture in self.bullet_pictures.items():
            self.draw_ball(picture, bullet.ball)

    def rotate_frog(self):
        bullet_pm0 = QPixmap(self.game.frog.current_ball.color.value).scaled(FROG_SIZE, FROG_SIZE)
        self.frog_bullet[0].setPixmap(bullet_pm0)
        bullet_pm1 = QPixmap(self.game.frog.next_ball.color.value).scaled(FROG_SIZE / 6, FROG_SIZE / 6)
        self.frog_bullet[1].setPixmap(bullet_pm1)
        delta = FROG_SIZE / 4
        betta = math.radians(self.game.frog.angle + 90)
        self.frog_bullet[1].move(-delta * math.cos(betta) + self.game.frog.position.x - FROG_SIZE / 12,
                                 -delta * math.sin(betta) + self.game.frog.position.y - FROG_SIZE / 12)

        t = QTransform().rotate(self.game.frog.angle)
        pm = QPixmap(self.game.frog.color.value).scaled(FROG_SIZE, FROG_SIZE, Qt.KeepAspectRatio,
                                                        Qt.SmoothTransformation)
        self.frog_picture.setPixmap(pm.transformed(t, Qt.SmoothTransformation))

    def timerEvent(self, event: 'QTimerEvent'):
        self.game.update(self.mouse_cursor)
        self.update_graphic()
        if self.game.is_ending:
            self.timer.stop()
        self.rotate_frog()

    def initialize_ball(self, ball):
        ql = QLabel(self)
        ql.setFixedSize(Ball.RADIUS, Ball.RADIUS)
        ql.setPixmap(QPixmap(ball.color.value).scaled(Ball.RADIUS, Ball.RADIUS))
        ql.show()
        return ql

    def refresh_textures(self):
        sequence = self.game.level.sequence
        tmp = sequence.head
        actual = []
        while tmp is not None:
            if tmp.value not in self.pictures:
                self.pictures[tmp.value] = self.initialize_ball(tmp.value)
                # self.pictures[tmp.value].setText(str(tmp.count))
                print(tmp.value.color, tmp.count)
            actual.append(tmp.value)
            tmp = tmp.past
        most_delete = list(set(self.pictures.keys()) - set(actual))
        for ball in most_delete:
            ql = self.pictures[ball]
            del self.pictures[ball]
            ql.hide()
            ql.deleteLater()
            ball.status = Status.DELETE

        for bullet in self.game.bullets:
            if bullet not in self.bullet_pictures:
                self.bullet_pictures[bullet] = self.initialize_ball(bullet.ball)
            elif bullet.status == Status.CAN_DELETE or not self.is_visible(bullet):
                ql = self.bullet_pictures[bullet]
                del self.bullet_pictures[bullet]
                ql.hide()
                ql.deleteLater()
                bullet.status = Status.DELETE

    def is_visible(self, bullet):
        """
        Проверяет видна ли еще пуля
        @type bullet: Bullet
        """
        return 0 < bullet.ball.position.x < self.size_vision.x and 0 < bullet.ball.position.y < self.size_vision.y

    def initialize_frog(self):
        ql = QLabel(self)
        ql.setFixedSize(FROG_SIZE, FROG_SIZE)
        ql.setAlignment(Qt.AlignCenter)
        pm = QPixmap(self.game.frog.color.value).scaled(FROG_SIZE, FROG_SIZE, Qt.KeepAspectRatio,
                                                        Qt.SmoothTransformation)
        ql.setPixmap(pm)
        ql.move(self.game.frog.position.x - FROG_SIZE / 2, self.game.frog.position.y - FROG_SIZE / 2)
        ql.show()
        return ql

    def initialize_bullet(self):
        ql = QLabel(self)
        ql.setFixedSize(FROG_SIZE, FROG_SIZE)
        ql.setAlignment(Qt.AlignCenter)
        ql.setPixmap(QPixmap(self.game.frog.current_ball.color.value).scaled(FROG_SIZE, FROG_SIZE))
        ql.move(self.game.frog.position.x - FROG_SIZE / 2, self.game.frog.position.y - FROG_SIZE / 2)
        ql.show()
        ql1 = QLabel(self)
        ql1.setFixedSize(FROG_SIZE / 6, FROG_SIZE / 6)
        ql1.setAlignment(Qt.AlignCenter)
        ql1.setPixmap(QPixmap(self.game.frog.next_ball.color.value).scaled(FROG_SIZE / 6, FROG_SIZE / 6))
        ql1.move(self.game.frog.position.x - FROG_SIZE / 12, self.game.frog.position.y - FROG_SIZE / 12)
        ql1.show()
        return [ql, ql1]

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Shift:
            self.game.frog.swap_balls()
        if key == Qt.Key_Space:
            self.game.shoot()
        if key == Qt.Key_A:
            self.frog_picture.hide()
        if key == Qt.Key_D:
            self.frog_picture.show()

    def mouseMoveEvent(self, event):
        self.mouse_cursor = Point(event.x(), event.y())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    frog = Frog(Point(500, 450))
    level = Level5(30, 2 * math.pi, 9 * math.pi)
    game = Game(frog, level)
    g = Graphics(game, Point(1000, 1000))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

(0, 900)
(-1.5, 1.5)
(100, 850)
(2 * math.pi, 9 * math.pi)
