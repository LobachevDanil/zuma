import math
import random

from scipy import integrate, diff
import sympy as sym

from Point import Point
from ball import Ball
from colors import Colors
from sequence import Sequence
from scipy import integrate


class Level2:
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

        self.a = 600
        self.calculator_x = lambda h: self.a * (h ** 2 - 1) / (1 + h ** 2) + 700
        self.calculator_y = lambda h: self.a * h * (h ** 2 - 1) / (1 + h ** 2) + 400
        self.integrator = lambda x: 600 * math.sqrt(
            16 * x ** 2 / (x ** 2 + 1) ** 4 + (x ** 4 + 4 * x ** 2 - 1) ** 2 / (x ** 4 + 2 * x ** 2 + 1) ** 2)
        self.start = Point(math.ceil(self.calculator_x(-1.5)), math.ceil(self.calculator_y(-1.5)))
        self.delta_length = 0.7

        self._initialize_first_ball()
        print(self.sequence.head.value.parameter)
        self.end = Point(math.ceil(self.calculator_x(1.5)), math.ceil(self.calculator_y(1.5)))
        print('level_init')

    def change_coordinates(self, ball):
        """
        :type ball: Ball
        """
        print('run change')
        next_t = self.get_offset(ball)
        ball.parameter = next_t
        point = Point(*self.translate_to_point(next_t))
        print('parameter ', ball.parameter)
        print(point)
        ball.change_position(point, next_t)

    def get_path(self):
        delta = (1.5 + 1.5) / 1000
        t = -1.5
        i = 0
        result = []
        while i < 1000:
            result.append(self.translate_to_point(t))
            t += delta
            i += 1
        return result

    def translate_to_point(self, t):
        return self.calculator_x(t), self.calculator_y(t)

    def get_offset(self, ball):
        b = ball.parameter
        while integrate.quad(self.integrator, ball.parameter, b)[0] < self.delta_length:
            b += 0.0005
            print(b)
        return b

    def update_balls_position(self):
        tmp = self.sequence.head
        self.change_coordinates(tmp.value)
        tmp = self.sequence.head.past
        if tmp is not None:
            while tmp is not None:
                new_position = tmp.value.position
                t = tmp.value.parameter
                while new_position.get_distance(tmp.next.value.position) > Ball.RADIUS:
                    t = t + 0.0001
                    new_position = Point(*self.translate_to_point(t))
                tmp.value.change_position(new_position, t)
                tmp = tmp.past
        if self.sequence.size < self.sequence_size and self.start.get_distance(
                self.sequence.tail.value.position) >= Ball.RADIUS:
            color = random.randint(0, len(Colors.get_all_colors()) - 1)
            new_ball = Ball(self.start.x, self.start.y, Colors.get_all_colors()[color])
            new_ball.parameter = -1.5
            self.sequence.enqueue(new_ball)

    def _initialize_first_ball(self):
        color = random.randint(0, len(Colors.get_all_colors()) - 1)
        ball = Ball(self.start.x, self.start.y, Colors.get_all_colors()[color])
        ball.parameter = -1.5
        self.sequence.enqueue(ball)
        print(self.sequence.head.value.parameter)
        print('was_first')

    def init_length(self):
        self.a = 600
        t = sym.Symbol('t')
        self.x_t = 600 * (t * t - 1) / (1 + t * t) + 700
        self.y_t = 600 * t * (t * t - 1) / (1 + t * t) + 400
        self.diff_x = sym.diff(self.x_t, t, 1)
        self.diff_x3 = sym.simplify(self.diff_x)
        print(self.diff_x3)
        self.diff_y = sym.diff(self.y_t, t, 1)
        self.diff_y3 = sym.simplify(self.diff_y)
        print(self.diff_y3)
        self.diff_x2 = self.diff_x3 ** 2
        print(self.diff_x2)
        self.diff_y2 = self.diff_y3 ** 2
        print(self.diff_y2)
        result = sym.sqrt(self.diff_x2 + self.diff_y2)
        result = sym.simplify(result)
        print(result)
        return result


Level2(1, Point(0, 0), Point(0, 0))
