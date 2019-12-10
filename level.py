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
        self.calkulator = lambda t: t ** 2 / 1000
        self.path_diff = sym.diff(self.path, x, 1)
        self.res = self.path_diff.powsimp(2)
        self.res2 = sym.sqrt(1 + self.res)
        self.delta_length = 1
        self.initialize_balls()
        self.end = Point(800, math.ceil(self.get_value(800)))

    def change_coordinates(self, ball):
        """
        :type ball: Ball
        """
        x = sym.Symbol('x')
        next_x = self.get_offset(ball)
        ball.change_position(Point(next_x, self.calkulator(next_x)))

    def get_value(self, t):
        return self.calkulator(t)

    def get_offset(self, ball):
        b = ball.position.x
        x = sym.Symbol('x')
        while sym.integrate(self.res2, (x, ball.position.x, b)) < self.delta_length:
            b += 0.2
        return b

    def update_balls_position(self):
        tmp = self.sequence.head
        self.change_coordinates(tmp.value)
        tmp = self.sequence.head.past
        if tmp is not None:
            while tmp is not None:
                new_position = tmp.value.position
                while new_position.get_distance(tmp.next.value.position) > Ball.RADIUS:
                    t = new_position.x + 0.1
                    new_position = Point(t, self.calkulator(t))
                tmp.value.change_position(new_position)
                tmp = tmp.past

        if self.sequence.size < self.sequence_size and self.start.get_distance(
                self.sequence.tail.value.position) >= Ball.RADIUS:
            color = random.randint(0, len(Colors.get_all_colors()) - 1)
            self.sequence.enqueue(Ball(self.start.x, self.start.y, Colors.get_all_colors()[color]))

    def initialize_balls(self):
        color = random.randint(0, len(Colors.get_all_colors()) - 1)
        self.sequence.enqueue(Ball(self.start.x, self.start.y, Colors.get_all_colors()[color]))
        print('was')
        '''for i in range(self.sequence_size - 1, -2, -1):
            color = random.randint(0, len(Colors.get_all_colors()) - 1)
            self.sequence.enqueue(Ball(self.start.x, self.start.y, Colors.get_all_colors()[color]))'''
