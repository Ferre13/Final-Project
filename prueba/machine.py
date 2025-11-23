import pyxel
from constants import MACHINE_SPRITE

class Machine:
    """
    Represents the machine that creates the packages.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the machine.
        :param x: The x-coordinate of the machine.
        :param y: The y-coordinate of the machine.
        """
        self._x = x
        self._y = y

    def draw(self):
        """
        Draws the machine on the screen.
        """
        pyxel.blt(self._x, self._y, *MACHINE_SPRITE)
