import math


class Point:
    """Описывает точку"""

    def __init__(self, x, y):
        """
            :type x: double
            :type y: double
        """
        self.x = x
        self.y = y

    def get_distance(self, other):
        """
        Расчитывает расстояние между точками
        :type other: Point
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self):
        return '({0},{1})'.format(self.x, self.y)
