import pyxel
import constants

class Platform:
    """
    This class represents the platforms created.
    """
    def __init__(self, x: int, y: int, width: int, sprite=constants.PLATFORM_SPRITE):
        self.x = x
        self.y = y
        self.width = width
        self.sprite = sprite

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def x(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError("The x coordinate must be a number")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y
    @y.setter
    def y(self, y):
        if not isinstance(y, (int, float)):
            raise TypeError("The y coordinate must be a number")
        self.__y = y

    @property
    def width(self) -> int:
        return self.__width
    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("The width must be an integer")
        self.__width = width

    def draw(self):
        w = self.sprite[3]
        for sprite in range(self.width):
            #Converting to int for drawing
            pyxel.blt(int(self.x) + (sprite * w), int(self.y), *self.sprite)