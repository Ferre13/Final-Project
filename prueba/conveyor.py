import pyxel
from constants import *

class Conveyor:
    """
    Represents a conveyor belt in the factory.
    """

    def __init__(self, y: int, speed: float, length: int, direction: int):
        """
        Initializes a conveyor belt.
        :param y: The y-coordinate of the conveyor belt.
        :param speed: The speed at which packages move on the belt.
        :param length: The length of the conveyor belt.
        :param direction: The direction of the conveyor belt (-1 for left, 1 for right).
        """
        self._y = y
        self._speed = speed
        self._length = length
        self._direction = direction

    @property
    def y(self) -> int:
        return self._y

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float):
        self._speed = value
        
    @property
    def direction(self) -> int:
        return self._direction

    def draw(self):
        """
        Draws the conveyor belt.
        """
        # Draw the conveyor belt itself (a simple line for now)
        pyxel.rect(0, self.y, self._length, 2, 7) # Example color
