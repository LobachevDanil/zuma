from Point import Point
from bullet import Status


class Ball:
    RADIUS = 40

    def __init__(self, x, y, color):
        self.position = Point(x, y)
        self.color = color
        self.parameter = 0
        self.status = Status.ACTIVE

    def change_position(self, position, parameter=0):
        """
        Updates the position of the ball and its parameter
        :type position: Point
        :type parameter: float
        """
        self.position = position
        self.parameter = parameter

    def is_collision(self, other):
        """Check for collision of balls"""
        return self.position.get_distance(other.position) <= Ball.RADIUS

    def __str__(self):
        return "{0}: {1}".format(self.position, self.color)
