import pyxel
import constants

class Platform:
    """
    This class represents the platforms for the characters to stand on.
    """
    def __init__(self, x: int, y: int, width: int, is_flipped: bool = False, sprite=constants.PLATFORM_SPRITE):
        self.x = x
        self.y = y
        self.width = width
        self.is_flipped = is_flipped
        self.sprite = sprite

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("The x coordinate must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("The y coordinate must be an integer")
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
        """
        Draws the platform on the screen using its assigned sprite.
        """
        img, u, v, w, h, colkey = self.sprite
        
        draw_w = -w if self.is_flipped else w

        for i in range(self.width):
            pyxel.blt(self.x + i * abs(w), self.y, img, u, v, draw_w, h, colkey)