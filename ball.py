from Point import Point


class Ball:
    """Описыват шар  в игре"""
    RADIUS = 40

    def __init__(self, x, y, color):
        self.position = Point(x, y)
        self.color = color
        self.parameter = 0

    def change_position(self, position, parameter=0):
        """
        Обновляет позицию шара и его параметр
        :type position: Point
        :type parameter: float
        """
        self.position = position
        self.parameter = parameter

    def is_collision(self, other):
        """Проверка на столкновение шаров"""
        return self.position.get_distance(other.position) <= Ball.RADIUS

    def __str__(self):
        return "{0}: {1}".format(self.position, self.color)
