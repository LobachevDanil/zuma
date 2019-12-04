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
        self.res2=sym.sqrt(1 + self.res)
        self.initialize_balls()

    def change_coordinates(self, ball):
        """
        :type t: int
        :type ball: Ball
        """
        delta_l = 0.5
        high = ball.position.x
        x = sym.Symbol('x')
        while sym.integrate(self.res2, (x, ball.position.x, high)) < delta_l:
            high += 0.1
        print("high=", high, self.path.evalf(6, subs={x: high}))
        ball.change_position(Point(high, self.path.evalf(6, subs={x: high})))

    def get_traectory(self, t):
        x = sym.Symbol('x')
        return self.path.evalf(6, subs={x: t})

    def get_offset(self):
        pass

    def update_balls_position(self):
        tmp = self.sequence.head
        while tmp.past is not None:
            self.change_coordinates(tmp.value)
            tmp = tmp.past

    def initialize_balls(self):
        for i in range(self.sequence_size - 1, -2, -1):
            color = random.randint(0, len(Colors.get_all_colors()) - 1)
            self.sequence.enqueue(Ball(self.start.x, self.start.y, Colors.get_all_colors()[color]))
