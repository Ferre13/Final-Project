import pyxel
from constants import VERTICAL_STRUCTURE_SPRITE

class VerticalStructure:
    """
    Represents the vertical structure in the center of the screen.
    """

    def __init__(self, x: int, height: int):
        """
        Initializes the vertical structure.
        :param x: The x-coordinate of the structure.
        :param height: The height of the structure in number of sprites.
        """
        self._x = x
        self._height = height

    def draw(self):
        """
        Draws the vertical structure on the screen.
        """
        sprite_height = VERTICAL_STRUCTURE_SPRITE[4]
        for i in range(self._height):
            pyxel.blt(self._x, i * sprite_height, *VERTICAL_STRUCTURE_SPRITE)
