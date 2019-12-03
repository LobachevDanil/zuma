import math

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
        ball.change_position(Point(ball.position.x + t, ball.position.y + t))

    def update_balls_position(self, t):
        tmp = self.sequence.head
        while tmp.past is not None:
            self.change_coordinates(tmp.value, t)
            tmp = tmp.past

    def initialize_balls(self):
        for i in range(self.sequence_size - 1, -2, -1):
            self.sequence.enqueue(Ball(self.start.x + i * 30, self.start.y + i * 30, Colors.blue))
