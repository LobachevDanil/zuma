from ball import Ball
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
        self.is_ending = False

    def update(self, cursor_position):
        if self.level.end.get_distance(self.level.sequence.head.value.position) <= Ball.RADIUS / 10:
            self.is_ending = True
            print('Game Over! You lose')
            return
        self.level.update_balls_position()
        self.frog.transform_angle(cursor_position)

    def shoot(self):
        self.frog.get_next_ball()
