import os

import dill
import sys

from PyQt5.QtCore import QBasicTimer, Qt, QTimerEvent, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QTransform
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLabel, QProgressBar

from Point import Point
from ball import Ball
from bullet import Status
from frog import Frog
from game import Game
from level import Level
from levels import *
from menu import Menu, LevelsMenu, ResultTableWidget
from player import Player, ResultTable

FROG_SIZE = 100


class Graphics(QMainWindow):
    def __init__(self, size):
        """
        :type size: Point
        """
        super().__init__()
        self.game = None
        self.is_loading = False
        self.player = None
        self.pictures = dict()
        self.mouse_cursor = Point(size.x / 2, size.y - 1)
        self.size_vision = size

        self.setFixedSize(size.x, size.y)
        self.timer = QBasicTimer()
        self.initUi()
        self.menu = Menu(self)
        self.menu.show()
        self.levels_menu = LevelsMenu(self, LEVEL_DATA)

    def initUi(self):
        self.setWindowTitle('Zuma')
        self.setMouseTracking(True)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(700, 10, 250, 20)
        self.progress.setValue(0)
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

    def close_menu(self):
        if self.player is not None and self.game is not None:
            self.menu.hide()
            self.menu.lower()
            self.start_game()
        else:
            self.menu.print_message('Загрузите предыдущее сохранение')

    def change_level(self):
        self.player = self.menu.get_player()
        if self.player is not None:
            self.menu.hide()
            self.levels_menu.show()
        else:
            self.menu.print_message('Введите имя игрока')

    def close_level_menu(self, number):
        print('Выбран уровень: ' + str(number))
        self.levels_menu.hide()
        self.levels_menu.lower()
        self.game = Game(*LEVEL_DATA[number], self.player)
        self.start_game()

    def start_game(self):
        self.initialize_all()
        self.timer.start(30, self)
        self.setFocus()
        self.show()

    def save_game(self):
        with open('saves/' + self.game.player.name + '_save.txt', 'wb') as f:
            dill.dump(self.game, f)
            print('Ваша игра была сохранена')

    def load_past_game(self):
        self.player = self.menu.get_player()
        if self.player is None:
            self.menu.print_message('Введите имя игрока')
        elif os.path.exists(os.path.join('saves', self.player.name + '_save.txt')):
            with open('saves/' + self.player.name + '_save.txt', 'rb') as f:
                self.game = dill.load(f)
                self.is_loading = True
                self.player = self.game.player
                self.menu.print_message('Вы можете продолжить сохраненную игру, нажмите Play')
        else:
            self.menu.print_message('Сохранений не найдено, можете начать новую игру,\nвыберите уровень')

    def initialize_all(self):
        self.frog_bullet = self.initialize_bullet()
        self.frog_picture = self.initialize_frog()
        self.bullet_pictures = dict()
        self.data = self.initialize_level_data()

    def draw_level(self, qp):
        level = self.game.level
        offset = Ball.RADIUS / 2
        qp.drawEllipse(level.start.x - offset, level.start.y - offset, Ball.RADIUS, Ball.RADIUS)
        qp.drawEllipse(level.end.x - offset, level.end.y - offset, Ball.RADIUS, Ball.RADIUS)
        qp.drawEllipse(self.game.frog.position.x, self.game.frog.position.y, 4, 4)
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

        self.progress.setValue(self.game.level.released_balls / self.game.level.sequence_size * 100)

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
            if self.is_loading:
                path = os.path.join('saves', self.player.name + '_save.txt')
                print('Удалено сохранение: ' + path)
                os.remove(path)
            table = ResultTable('scores_table.txt')
            table.add_player(self.player)
            table.save_table()
            self.result_table = ResultTableWidget(table, self, self.game.is_win)
            self.result_table.show()
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
                # print(tmp.value.color, tmp.count)
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
        if self.game is None:
            return
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
            if self.game is not None:
                if not self.game.is_ending:
                    self.save_game()
            event.accept()
        else:
            event.ignore()


LEVEL_DATA = [
    (Frog(Point(700, 200)), Level0()),
    (Frog(Point(500, 450)), Level1()),
    (Frog(Point(500, 450)), Level2()),
    (Frog(Point(650, 450)), Level3()),
    (Frog(Point(450, 450)), Level4())]


def main():
    app = QApplication(sys.argv)
    game = Game(LEVEL_DATA[1][0], LEVEL_DATA[1][1], Player(''))
    g = Graphics(Point(1000, 1000))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
