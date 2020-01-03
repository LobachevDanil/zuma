import math
import random

from scipy import integrate, diff
import sympy as sym

from Point import Point
from ball import Ball
from colors import Colors
from sequence import Sequence
from level import Level


class Level0(Level):
    def __init__(self):
        """Движение по синусу"""
        size = 27
        start = 50
        end = 850
        normal_delta_length = 0.8
        fast_delta_length = 2
        func = lambda t: 300 * math.sin(t / 50) + 400
        delta_t = 0.1
        offset = Point(0, 200)
        calculator_x = lambda t: t
        calculator_y = lambda t: func(t) + offset.y
        integrator = lambda t: math.sqrt(1 + (6 * math.cos(t / 50)) ** 2)
        super().__init__(size, start, end, normal_delta_length, fast_delta_length,
                         func, delta_t, calculator_x, calculator_y, integrator)


class Level1(Level):
    def __init__(self):
        """Движение по спирали"""
        size = 30
        start = 2 * math.pi
        end = 9 * math.pi
        normal_delta_length = 0.3
        fast_delta_length = 3
        func = lambda t: 23 + 15 * t
        delta_t = 0.005
        offset = Point(500, 450)
        calculator_x = lambda t: func(t) * math.cos(t) + offset.x
        calculator_y = lambda t: func(t) * math.sin(t) + offset.y
        integrator = lambda t: math.sqrt(15 + 23 ** 2 + 225 * t * t + 46 * 15 * t)
        super().__init__(size, start, end, normal_delta_length, fast_delta_length,
                         func, delta_t, calculator_x, calculator_y, integrator)


class Level2(Level):
    def __init__(self):
        """Движение по окружности"""
        size = 2
        start = 0
        end = 3.5 * math.pi / 2
        normal_delta_length = 0.5
        fast_delta_length = 0.5
        func = lambda t: 400
        delta_t = 0.001
        offset = Point(450, 450)
        calculator_x = lambda t: func(t) * math.cos(t) + offset.x
        calculator_y = lambda t: func(t) * math.sin(t) + offset.y
        integrator = lambda t: 400
        super().__init__(size, start, end, normal_delta_length, fast_delta_length,
                         func, delta_t, calculator_x, calculator_y, integrator)


class Level3(Level):
    def __init__(self):
        """Движение по элиптической лемнискате"""
        size = 20
        start = math.pi / 10
        end = 2 * math.pi
        normal_delta_length = 0.5
        fast_delta_length = 1
        func = lambda t: math.sqrt((400 * math.cos(t)) ** 2 + (170 * math.sin(t)) ** 2)
        delta_t = 0.001
        offset = Point(450, 450)
        calculator_x = lambda t: func(t) * math.cos(t) + offset.x
        calculator_y = lambda t: func(t) * math.sin(t) + offset.y
        integrator = lambda t: math.sqrt(func(t) ** 2 + (115 * (math.sin(2 * t)) / func(t)) ** 2)
        super().__init__(size, start, end, normal_delta_length, fast_delta_length,
                         func, delta_t, calculator_x, calculator_y, integrator)


class Level4(Level):
    def __init__(self):
        """Движение по кривой, заданной параметрически"""
        size = 10
        start = -3 * math.pi / 4 + 2 * math.pi
        end = 3 * math.pi / 4 + 2 * math.pi
        normal_delta_length = 0.2
        fast_delta_length = 5
        func_x = lambda t: 400 * math.sin(t)
        func_y = lambda t: 400 * math.cos(3 * t)
        delta_t = 0.003
        offset = Point(450, 450)
        calculator_x = lambda t: func_x(t) + offset.x
        calculator_y = lambda t: func_y(t) + offset.y
        integrator = lambda t: 400 * math.sqrt(math.cos(t) ** 2 + 9 * math.sin(3 * t) ** 2)
        super().__init__(size, start, end, normal_delta_length, fast_delta_length,
                         None, delta_t, calculator_x, calculator_y, integrator)
