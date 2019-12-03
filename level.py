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
        self.initialize_balls()

    def change_coordinates(self, ball, t):
        """
        :type t: int
        :type ball: Ball
        """
        delta_l = 0.5
        high = ball.position.x
        func_lev = lambda x: x * x / 1000
        func = lambda x: math.sqrt(1 + x / 500)
        print(integrate.quad(func, ball.position.x, high))

        x = sym.Symbol('x')
        alpha = x
        alpha_deriv = sym.diff(alpha, x, 1)
        print(alpha_deriv)

        while sym.integrate(sym.sqrt(1 + alpha_deriv), (x, ball.position.x, high)) < delta_l:
            high += 0.1

        '''while integrate.quad(func, ball.position.x, high)[0] < delta_l:
            high += 0.1'''
        print("high", high, alpha.evalf(6, subs={x: high}))
        ball.change_position(Point(high, alpha.evalf(6, subs={x: high})))

    def update_balls_position(self, t):
        tmp = self.sequence.head
        while tmp.past is not None:
            self.change_coordinates(tmp.value, t)
            tmp = tmp.past

    def initialize_balls(self):
        for i in range(self.sequence_size - 1, -2, -1):
            color = random.randint(0, len(Colors.get_all_colors()) - 1)
            self.sequence.enqueue(Ball(self.start.x, self.start.y, Colors.get_all_colors()[color]))
