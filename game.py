import math

from ball import Ball
from bullet import Bullet
from colors import Colors
from frog import Frog
from level import Level


class Game:
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
        if self.level.end.get_distance(self.level.sequence.head.value.position) <= Ball.RADIUS / 10:
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
        for bullet in self.bullets:
            tmp = self.level.sequence.head
            while tmp is not None:
                if bullet.ball.is_collision(tmp.value) and bullet.flag:
                    bullet.flag = False
                    s1 = self.calculate_area(bullet.ball.position, tmp.value.position, tmp.next.value.position)
                    s2 = self.calculate_area(bullet.ball.position, tmp.value.position, tmp.past.value.position)
                    if s1 <= s2:
                        self.level.sequence.add_ball(bullet.ball, tmp.next)
                    else:
                        self.level.sequence.add_ball(bullet.ball, tmp)
                    self.level.offset_first_ball()
                    break
                tmp = tmp.past

    def calculate_area(self, point1, point2, point3):
        a = point1.get_distance(point2)
        b = point1.get_distance(point3)
        c = point2.get_distance(point3)
        p = (a + b + c) / 2
        s = math.sqrt(p * (p - a) * (p - b) * (p - c))
        return s

    def shoot(self):
        length = self.frog.position.get_distance(self.cursor) / 8
        delta_x = (self.cursor.x - self.frog.position.x) / length
        delta_y = (self.cursor.y - self.frog.position.y) / length
        bullet = Bullet(delta_x, delta_y, self.frog.current_ball)
        self.bullets.append(bullet)
        self.frog.get_next_ball()
