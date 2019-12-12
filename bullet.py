import enum

from Point import Point


class Bullet:
    """Описывает класс шарика, которым выстрелили"""

    def __init__(self, delta_x, delta_y, ball):
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.ball = ball
        self.status = Status.FLY

    def update_position(self):
        """Обновляет позицию пули"""
        if self.status == Status.FLY:
            self.ball.change_position(Point(self.ball.position.x + self.delta_x, self.ball.position.y + self.delta_y))


class Status(enum.Enum):
    """Статус пули"""
    FLY = 0
    COLLISION = 1
    CAN_DELETE = 2
    DELETE = 3
