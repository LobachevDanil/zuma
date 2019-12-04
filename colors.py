import enum

TEXTURE_PATH = "textures/official/"


class Colors(enum.Enum):
    red = TEXTURE_PATH + "red_ball.png"
    green = TEXTURE_PATH + "green_ball.png"
    blue = TEXTURE_PATH + "blue_ball.png"
    purple = TEXTURE_PATH + "purple_ball.png"
    yellow = TEXTURE_PATH + "yellow_ball.png"
    frog = TEXTURE_PATH + "frog_ball.png"


    @staticmethod
    def get_all_colors():
        return [Colors.red, Colors.green, Colors.blue, Colors.blue, Colors.purple, Colors.yellow]
