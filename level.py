import math
import random

from scipy import integrate, diff
import sympy as sym

from Point import Point
from ball import Ball
from colors import Colors
from sequence import Sequence
from scipy import integrate


class Level:
    def __init__(self, size, start, end, normal_delta_length, fast_delta_length,
                 func, delta_t, calculator_x, calculator_y, integrator):
        """
        Описывает уровень
        :type size: int
        :type start: float
        :type end: float
        :type normal_delta_length: float
        :type fast_delta_length: float
        :type func: lambda
        :type delta_t: float
        :type calculator_x: lambda
        :type calculator_y: lambda
        :type integrator: lambda
        """
        self.sequence = Sequence()
        self.sequence_size = size
        self.released_balls = 0
        self.delta_length = fast_delta_length
        self.start_param = start
        self.end_param = end
        self.normal_delta_length = normal_delta_length

        self.func = func
        self.delta_t = delta_t
        self.calculator_x = calculator_x
        self.calculator_y = calculator_y
        self.integrator = integrator

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
            b += self.delta_t
        return b

    def update_balls_position(self):
        tmp = self.sequence.head
        if tmp is None:
            return
        self._change_coordinates(tmp.value)
        tmp = self.sequence.head.past
        while tmp is not None:
            new_position = tmp.value.position
            t = tmp.value.parameter
            while new_position.get_distance(tmp.next.value.position) > Ball.RADIUS:
                t += self.delta_t
                new_position = Point(*self.translate_to_point(t))
            tmp.value.change_position(new_position, t)
            tmp = tmp.past

        if self.released_balls < self.sequence_size and self.start.get_distance(
                self.sequence.tail.value.position) >= Ball.RADIUS:
            self._add_ball()
        if self.released_balls >= self.sequence_size:
            self.delta_length = self.normal_delta_length

    def _add_ball(self):
        color = random.randint(0, len(Colors.get_all_colors()) - 1)
        ball = Ball(self.start.x, self.start.y, Colors.get_all_colors()[color])
        ball.parameter = self.start_param
        self.sequence.enqueue(ball)
        self.released_balls += 1

    def offset_first_ball(self):
        if self.sequence.head is None:
            return
        first = self.sequence.head.value
        second = None if self.sequence.head.past is None else self.sequence.head.past.value
        if second is not None:
            while second.is_collision(first) or second.parameter > first.parameter:
                first.parameter += self.delta_t
                first.change_position(Point(*self.translate_to_point(first.parameter)), first.parameter)
        if first.parameter >= self.end_param:
            self.sequence.size = -1
