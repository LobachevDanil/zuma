import enum

TEXTURE_PATH = "textures/new/"


class Colors(enum.Enum):
    red = TEXTURE_PATH + "red2.png"
    green = TEXTURE_PATH + "green2.png"
    blue = TEXTURE_PATH + "blue2.png"
    purple = TEXTURE_PATH + "purple2l.png"
    yellow = TEXTURE_PATH + "yellow2.png"
    frog = TEXTURE_PATH + "frog_ball2.png"


    @staticmethod
    def get_all_colors():
        return [Colors.red, Colors.green, Colors.blue, Colors.blue, Colors.purple, Colors.yellow]
