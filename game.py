from ball import Ball
from bullet import Bullet
from colors import Colors
from frog import Frog
from level import Level


class Game:
    def __init__(self, frog, level):
        """
        :type frog: Frog
        :type level: Level
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
        self.cursor = cursor_position
        self.level.update_balls_position()
        self.frog.transform_angle(cursor_position)
        for bullet in self.bullets:
            bullet.update_position()

    def shoot(self):
        length = self.frog.position.get_distance(self.cursor)/8
        delta_x = (self.cursor.x - self.frog.position.x) / length
        delta_y = (self.cursor.y - self.frog.position.y) / length
        bullet = Bullet(delta_x, delta_y, self.frog.current_ball)
        self.bullets.append(bullet)
        self.frog.get_next_ball()
