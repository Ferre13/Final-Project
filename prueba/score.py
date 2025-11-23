import pyxel
from constants import NUMBER_SPRITES

class Score:
    """
    Represents the score display.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the score display.
        :param x: The x-coordinate of the score display.
        :param y: The y-coordinate of the score display.
        """
        self._x = x
        self._y = y

    def draw(self, score: int):
        """
        Draws the score on the screen using sprites.
        :param score: The score to display.
        """
        score_str = str(score)
        for i, digit in enumerate(score_str):
            digit_int = int(digit)
            pyxel.blt(self._x + i * 8, self._y, *NUMBER_SPRITES[digit_int])
