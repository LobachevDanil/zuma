import math

from Point import Point


class Ball:
    RADIUS = 40

    def __init__(self, x, y, color):
        self.position = Point(x, y)
        self.color = color

    def change_position(self, position):
        """
        :type position: Point
        """
        self.position = position

    def is_collision(self, other):
        return self.position.get_distance(other.posotion) <= 2 * Ball.RADIUS

    def __str__(self):
        return "{0}: {1}".format(self.position, self.color)
