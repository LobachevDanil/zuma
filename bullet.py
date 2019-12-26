import enum

from Point import Point


class Bullet:
    """Описывает класс шарика, которым выстрелили"""

    def __init__(self, delta_x, delta_y, ball):
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.ball = ball
        self.status = Status.ACTIVE

    def update_position(self):
        """Обновляет позицию пули"""
        if self.status == Status.ACTIVE:
            new_x = self.ball.position.x + self.delta_x
            new_y = self.ball.position.y + self.delta_y
            self.ball.change_position(Point(new_x, new_y))


class Status(enum.Enum):
    """Статус пули"""
    ACTIVE = 0
    CAN_DELETE = 1
    DELETE = 2
