import pyxel
from constants import PLATFORM_SPRITE

class Platform:
    """
    Represents a platform for the characters to stand on.
    """

    def __init__(self, x: int, y: int, width: int):
        """
        Initializes a platform.
        :param x: The x-coordinate of the platform.
        :param y: The y-coordinate of the platform.
        :param width: The width of the platform in number of sprites.
        """
        self._x = x
        self._y = y
        self._width = width

    def draw(self):
        """
        Draws the platform on the screen.
        """
        sprite_width = PLATFORM_SPRITE[3]
        for i in range(self._width):
            pyxel.blt(self._x + i * sprite_width, self._y, *PLATFORM_SPRITE)
