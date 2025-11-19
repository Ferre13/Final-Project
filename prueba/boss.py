import pyxel
from constants import *

class Boss:
    """
    Represents the boss character who appears when players make a mistake.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the Boss.
        :param x: The x-coordinate for the boss to appear at.
        :param y: The y-coordinate for the boss to appear at.
        """
        self._x = x
        self._y = y
        self._is_visible = False
        self._timer = 0

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    def appear(self, duration: int):
        """
        Makes the boss appear for a specific duration.
        :param duration: The number of frames the boss should be visible.
        """
        self._is_visible = True
        self._timer = duration

    def update(self):
        """
        Updates the boss's visibility timer.
        """
        if self._is_visible:
            self._timer -= 1
            if self._timer <= 0:
                self._is_visible = False

    def draw(self):
        """
        Draws the boss on the screen if visible.
        """
        if self.is_visible:
            pyxel.blt(self._x, self._y, *BOSS_SPRITE)