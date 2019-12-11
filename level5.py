import math
import random

from scipy import integrate, diff
import sympy as sym

from Point import Point
from ball import Ball
from colors import Colors
from sequence import Sequence
from scipy import integrate


class Level5:
    def __init__(self, size, start, end):
        """
        :type size: int
        :type start: float
        :type end: float
        """
        self.sequence = Sequence()
        self.sequence_size = size
        self.delta_length = 3
        self.start_param = start
        self.end_param = end
        self.offset = Point(500, 400)

        self.func = lambda t: 23 + 15 * t
        self.calculator_x = lambda h: self.func(h) * math.cos(h) + self.offset.x
        self.calculator_y = lambda h: self.func(h) * math.sin(h) + self.offset.y
        self.integrator = lambda t: math.sqrt(15 + 23 ** 2 + 225 * t * t + 46 * 15 * t)

        self.start = Point(*self.translate_to_point(start))
        self.end = Point(*self.translate_to_point(end))

        self._add_ball()

    def _change_coordinates(self, ball):
        """
        :type ball: Ball
        """
        next_t = self._get_offset(ball)
        ball.parameter = next_t
        point = Point(*self.translate_to_point(next_t))
        ball.change_position(point, next_t)

    def get_path(self):
        delta = (self.end_param - self.start_param) / 1000
        t = self.start_param
        i = 0
        result = []
        while i < 1000:
            result.append(self.translate_to_point(t))
            t += delta
            i += 1
        return result

    def translate_to_point(self, t):
        return self.calculator_x(t), self.calculator_y(t)

    def _get_offset(self, ball):
        b = ball.parameter
        while integrate.quad(self.integrator, ball.parameter, b)[0] < self.delta_length:
            b += 0.005
        return b

    def update_balls_position(self):
        tmp = self.sequence.head
        self._change_coordinates(tmp.value)
        tmp = self.sequence.head.past
        while tmp is not None:
            new_position = tmp.value.position
            t = tmp.value.parameter
            while new_position.get_distance(tmp.next.value.position) > Ball.RADIUS:
                t = t + 0.005
                new_position = Point(*self.translate_to_point(t))
            tmp.value.change_position(new_position, t)
            tmp = tmp.past

        if self.sequence.size < self.sequence_size and self.start.get_distance(
                self.sequence.tail.value.position) >= Ball.RADIUS:
            self._add_ball()
        if self.sequence.size == self.sequence_size:
            self.delta_length = 0.3

    def _add_ball(self):
        color = random.randint(0, len(Colors.get_all_colors()) - 1)
        ball = Ball(self.start.x, self.start.y, Colors.get_all_colors()[color])
        ball.parameter = self.start_param
        self.sequence.enqueue(ball)

    def _init_length(self):
        a = 600
        t = sym.Symbol('t')
        x_t = 600 * (t * t - 1) / (1 + t * t) + 700
        y_t = 600 * t * (t * t - 1) / (1 + t * t) + 400
        diff_x = sym.diff(x_t, t, 1)
        diff_x3 = sym.simplify(diff_x)
        diff_y = sym.diff(y_t, t, 1)
        diff_y3 = sym.simplify(diff_y)
        diff_x2 = diff_x3 ** 2
        diff_y2 = diff_y3 ** 2
        result = sym.sqrt(diff_x2 + diff_y2)
        result = sym.simplify(result)
        return result
