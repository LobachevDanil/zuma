import math

from ball import Ball
from bullet import Bullet, Status
from colors import Colors
from frog import Frog
from level import Level


class Game:
    """Описывает игру"""

    def __init__(self, frog, level):
        """
        :type frog: Frog
        """
        self.frog = frog
        self.level = level
        self.bullets = []
        self.cursor = None
        self.is_ending = False

    def update(self, cursor_position):
        if self.level.sequence.size == 0:
            self.is_ending = True
            print('You win!!!')
            return
        if self.level.end.get_distance(self.level.sequence.head.value.position) <= Ball.RADIUS / 2:
            self.is_ending = True
            print('Game Over! You lose')
            return
        self.check_bullets_hits()
        self.cursor = cursor_position
        self.level.update_balls_position()
        self.frog.transform_angle(cursor_position)
        for bullet in self.bullets:
            bullet.update_position()

    def check_bullets_hits(self):
        must_remove = []
        for bullet in self.bullets:
            if bullet.status == Status.DELETE:
                must_remove.append(bullet)
                continue
            tmp = self.level.sequence.head
            if bullet.ball.is_collision(tmp.value) and bullet.status == Status.ACTIVE:
                bullet.status = Status.CAN_DELETE
                self.treat_head(bullet, tmp)
                self.level.offset_first_ball()
                break
            tmp = self.level.sequence.head.past
            while tmp.past is not None and bullet.status == Status.ACTIVE:
                if bullet.ball.is_collision(tmp.value):
                    # if not self.level.sequence.delete_similar(bullet.ball, tmp):
                    self.treat_body(bullet, tmp)
                    self.level.offset_first_ball()
                    bullet.status = Status.CAN_DELETE
                    self.level.sequence.delete_similar(bullet.ball, tmp)
                    break
                tmp = tmp.past
            if bullet.ball.is_collision(tmp.value) and bullet.status == Status.ACTIVE:
                bullet.status = Status.CAN_DELETE
                self.treat_tail(bullet, tmp)
                self.level.offset_first_ball()
        if len(must_remove) != 0:
            self.remove_bullets(must_remove)

    def calculate_angle(self, point1, point2, point3):
        a = point1.get_distance(point2)
        b = point2.get_distance(point3)
        c = point1.get_distance(point3)
        return math.acos((c ** 2 - a ** 2 - b ** 2) / (-2 * a * b))

    def treat_head(self, bullet, head):
        angle = self.calculate_angle(bullet.ball.position, head.value.position, head.past.value.position)
        if angle <= math.pi / 2:
            self.level.sequence.add_ball(bullet.ball, head.past)
        else:
            self.level.sequence.replace_head(bullet.ball)

    def treat_body(self, bullet, tmp):
        angle = self.calculate_angle(bullet.ball.position, tmp.value.position, tmp.past.value.position)
        if angle <= math.pi / 2:
            self.level.sequence.add_ball(bullet.ball, tmp)
        else:
            self.level.sequence.add_ball(bullet.ball, tmp.next)

    def treat_tail(self, bullet, tail):
        angle = self.calculate_angle(bullet.ball.position, tail.value.position, tail.next.value.position)
        if angle <= math.pi / 2:
            self.level.sequence.add_ball(bullet.ball, tail.next)
        else:
            self.level.sequence.replace_tail(bullet.ball)

    def remove_bullets(self, must_remove):
        for bullet in must_remove:
            self.bullets.remove(bullet)

    def shoot(self):
        length = self.frog.position.get_distance(self.cursor) / 8
        delta_x = (self.cursor.x - self.frog.position.x) / length
        delta_y = (self.cursor.y - self.frog.position.y) / length
        bullet = Bullet(delta_x, delta_y, self.frog.current_ball)
        self.bullets.append(bullet)
        self.frog.get_next_ball()
