import pyxel
from constants import VERTICAL_STRUCTURE_SPRITE

class VerticalStructure:
    """
    Represents the vertical structure in the center of the screen.
    """

    def __init__(self, x: int, height: int, width: int):
        """
        Initializes the vertical structure.
        :param x: The x-coordinate of the structure.
        :param height: The height of the structure in number of sprites.
        :param width: The width of the structure in number of sprites.
        """
        self._x = x
        self._height = height
        self._width = width

    def draw(self):
        """
        Draws the vertical structure on the screen.
        """
        sprite_width = VERTICAL_STRUCTURE_SPRITE[3]
        sprite_height = VERTICAL_STRUCTURE_SPRITE[4]
        for i in range(self._height):
            for j in range(self._width):
                pyxel.blt(self._x + j * sprite_width, i * sprite_height, *VERTICAL_STRUCTURE_SPRITE)
