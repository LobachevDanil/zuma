import enum
import os

TEXTURE_PATH2 = os.path.join(".", "textures", "new")


class Colors(enum.Enum):
    """Описывает виды шаров"""
    red = os.path.join(TEXTURE_PATH2, "red2.png")
    green = os.path.join(TEXTURE_PATH2, "green2.png")
    blue = os.path.join(TEXTURE_PATH2, "blue2.png")
    purple = os.path.join(TEXTURE_PATH2, "purple2.png")
    yellow = os.path.join(TEXTURE_PATH2, "yellow2.png")
    frog = os.path.join(TEXTURE_PATH2, "frog_ball_empty.png")

    bomb = os.path.join(TEXTURE_PATH2, "bomb.png")
    time = os.path.join(TEXTURE_PATH2, "time.png")
    pointer = os.path.join(TEXTURE_PATH2, "pointer.png")

    @staticmethod
    def get_all_colors():
        return [Colors.red, Colors.green, Colors.blue,
                Colors.blue, Colors.purple, Colors.yellow]

    @staticmethod
    def get_all_bonus():
        return [Colors.bomb, Colors.time, Colors.pointer]
