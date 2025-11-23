import pyxel
from constants import WINDOW_SPRITE

class Window:
    """
    Represents a window in the background.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the window.
        :param x: The x-coordinate of the window.
        :param y: The y-coordinate of the window.
        """
        self._x = x
        self._y = y

    def draw(self):
        """
        Draws the window on the screen.
        """
        pyxel.blt(self._x, self._y, *WINDOW_SPRITE)
