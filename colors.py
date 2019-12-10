import enum
import os

TEXTURE_PATH = "textures/new/"
TEXTURE_PATH2 = os.path.join("./", "textures/", "new/")
print(TEXTURE_PATH2.join("/ab"))


class Colors(enum.Enum):
    red = TEXTURE_PATH + "red2.png"
    green = TEXTURE_PATH + "green2.png"
    blue = TEXTURE_PATH + "blue2.png"
    purple = TEXTURE_PATH + "purple2.png"
    yellow = TEXTURE_PATH + "yellow2.png"
    frog = TEXTURE_PATH + "frog_ball2.png"

    @staticmethod
    def get_all_colors():
        return [Colors.red, Colors.green, Colors.blue, Colors.blue, Colors.purple, Colors.yellow]


print(Colors.red.value)
