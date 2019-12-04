import math
import random

from scipy import integrate, diff
import sympy as sym

from Point import Point
from ball import Ball
from colors import Colors
from sequence import Sequence


class Level:
    def __init__(self, size, start, end):
        """
        :type size: int
        :type frog_position: Point
        :type start: Point
        :type end: Point
        """
        self.sequence = Sequence()
        self.sequence_size = size
        self.start = start
        self.end = end

        x = sym.Symbol('x')
        self.path = x ** 2 / 1000
        self.path_diff = sym.diff(self.path, x, 1)
        self.res = self.path_diff.powsimp(2)
        self.res2 = sym.sqrt(1 + self.res)
        self.delta_length = 0.5
        self.initialize_balls()
        self.end = Point(800, math.ceil(self.get_value(800)))

    def change_coordinates(self, ball):
        """
        :type ball: Ball
        """
        x = sym.Symbol('x')
        next_x = self.get_offset(ball)
        # print("high=", high, self.path.evalf(6, subs={x: high}))
        ball.change_position(Point(next_x, self.path.evalf(6, subs={x: next_x})))

    def get_value(self, t):
        x = sym.Symbol('x')
        return self.path.evalf(6, subs={x: t})

    def get_offset(self, ball):
        b = ball.position.x
        x = sym.Symbol('x')
        while sym.integrate(self.res2, (x, ball.position.x, b)) < self.delta_length:
            b += 0.1
        return b

    def update_balls_position(self):
        tmp = self.sequence.head
        while tmp.past is not None:
            self.change_coordinates(tmp.value)
            tmp = tmp.past

    def initialize_balls(self):
        for i in range(self.sequence_size - 1, -2, -1):
            color = random.randint(0, len(Colors.get_all_colors()) - 1)
            self.sequence.enqueue(Ball(self.start.x, self.start.y, Colors.get_all_colors()[color]))
