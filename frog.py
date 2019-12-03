import math
import random

from Point import Point
from ball import Ball
from colors import Colors


class Frog:
    next_ball: Ball
    current_ball: Ball

    def __init__(self, position):
        """
        :type position: Point
        """
        self.position = position
        self.color = Colors.frog
        self.current_ball = self.get_random_ball()
        self.next_ball = self.get_random_ball()
        self.angle = 0

    def get_next_ball(self):
        self.current_ball = self.next_ball
        self.next_ball = self.get_random_ball()

    def get_random_ball(self):
        all_colors = Colors.get_all_colors()
        number = random.randint(0, len(all_colors) - 1)
        return Ball(self.position.x, self.position.y, all_colors[number])

    def swap_balls(self):
        self.current_ball, self.next_ball = self.next_ball, self.current_ball

    def transform_angle(self, cursor_point):
        """
        :type cursor_point: Point
        """
        delta_x = cursor_point.x - self.position.x
        delta_y = cursor_point.y - self.position.y
        alpha = 0
        if delta_y != 0:
            alpha = math.atan(delta_x / delta_y)
        if delta_y < 0:
            alpha += math.pi
        self.angle = -math.degrees(alpha)
