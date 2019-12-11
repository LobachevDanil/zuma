import math
import random

from scipy import integrate, diff
import sympy as sym

from Point import Point
from ball import Ball
from colors import Colors
from sequence import Sequence


class Level4:
    def __init__(self, size, start, end):
        """
        :type size: int
        :type start: float
        :type end: float
        """
        self.sequence = Sequence()
        self.sequence_size = size

        x = sym.Symbol('x')
        self.path = x ** 2 / 1000
        self.calculator = lambda t: t ** 2 / 1000
        self.path_diff = sym.diff(self.path, x, 1)
        self.res = self.path_diff ** 2
        self.res2 = sym.sqrt(1 + self.res)
        self.integrator = lambda t: math.sqrt(t ** 2 / 250000 + 1)
        self.delta_length = 0.5

        self.start = Point(start, self.calculator(start))
        self.end = Point(end, self.calculator(end))
        self._add_ball()

    def _change_coordinates(self, ball):
        """
        :type ball: Ball
        """
        next_x = self._get_offset(ball)
        ball.change_position(Point(next_x, self.calculator(next_x)))

    def get_path(self):
        x = 0
        i = 0
        delta = (self.end.x - self.start.x) / 1000
        result = []
        while i < 1000:
            result.append(self.translate_to_point(x))
            x += delta
            i += 1
        return result

    def translate_to_point(self, t):
        return math.ceil(t), math.ceil(self.calculator(t))

    def _get_offset(self, ball):
        b = ball.position.x
        while integrate.quad(self.integrator, ball.position.x, b)[0] < self.delta_length:
            b += 0.2
        return b

    def update_balls_position(self):
        tmp = self.sequence.head
        self._change_coordinates(tmp.value)
        tmp = self.sequence.head.past
        while tmp is not None:
            new_position = tmp.value.position
            while new_position.get_distance(tmp.next.value.position) > Ball.RADIUS:
                t = new_position.x + 0.1
                new_position = Point(t, self.calculator(t))
            tmp.value.change_position(new_position)
            tmp = tmp.past

        if self.sequence.size < self.sequence_size and self.start.get_distance(
                self.sequence.tail.value.position) >= Ball.RADIUS:
            self._add_ball()

    def _add_ball(self):
        color = random.randint(0, len(Colors.get_all_colors()) - 1)
        ball = Ball(self.start.x, self.start.y, Colors.get_all_colors()[color])
        self.sequence.enqueue(ball)
