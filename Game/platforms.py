import pyxel
import constants

class Platform:
    """
    Represents static platforms. Strict encapsulation.
    """
    def __init__(self, x: int, y: int, width: int, sprite=constants.PLATFORM_SPRITE):
        self.x = x
        self.y = y
        self.width = width
        self.sprite = sprite

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, x):
        if not isinstance(x, (int, float)): raise TypeError("x must be number")
        self.__x = x

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, y):
        if not isinstance(y, (int, float)): raise TypeError("y must be number")
        self.__y = y

    @property
    def width(self) -> int: return self.__width
    @width.setter
    def width(self, width: int):
        if not isinstance(width, int): raise TypeError("width must be int")
        self.__width = width

    def draw(self):
        w = self.sprite[3]
        for sprite_idx in range(self.width):
            pyxel.blt(int(self.x) + (sprite_idx * w), int(self.y), *self.sprite)