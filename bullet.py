from Point import Point


class Bullet:
    def __init__(self, delta_x, delta_y, ball):
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.ball = ball
        self.flag = True

    def update_position(self):
        if self.flag:
            self.ball.change_position(Point(self.ball.position.x + self.delta_x, self.ball.position.y + self.delta_y))
