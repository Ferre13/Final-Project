import pyxel
from constants import EXIT_SIGNAL_SPRITE

class ExitSignal:
    """
    Represents the exit signal that appears when the truck is full.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the exit signal.
        :param x: The x-coordinate of the exit signal.
        :param y: The y-coordinate of the exit signal.
        """
        self._x = x
        self._y = y
        self.is_visible = False

    def draw(self):
        """
        Draws the exit signal on the screen if visible.
        """
        if self.is_visible:
            pyxel.blt(self._x, self._y, *EXIT_SIGNAL_SPRITE)
