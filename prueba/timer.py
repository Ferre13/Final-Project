import pyxel
from constants import CLOCK_SPRITES

class Timer:
    """
    Represents the game timer.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the timer.
        :param x: The x-coordinate of the timer.
        :param y: The y-coordinate of the timer.
        """
        self._x = x
        self._y = y
        self._time = 0
        self._sprite_index = 0

    def update(self):
        """
        Updates the timer.
        """
        self._time += 1
        if self._time % 15 == 0:
            self._sprite_index = (self._sprite_index + 1) % len(CLOCK_SPRITES)

    def draw(self):
        """
        Draws the timer on the screen.
        """
        sprite = CLOCK_SPRITES[self._sprite_index]
        pyxel.blt(self._x, self._y, *sprite)
