import pyxel
from constants import SLOW_SPEED, PCK_LVL1

class Package:
    """
    Represents a package in the bottling factory.
    """

    def __init__(self, x: int, y: int, direction: int, is_full: bool = False):
        """
        Initializes a package.
        :param x: The initial x-coordinate.
        :param y: The initial y-coordinate.
        :param direction: The direction of movement (-1 for left, 1 for right).
        :param is_full: Whether the package is full or empty.
        """
        self._x = x
        self._y = y
        self._direction = direction
        self._is_full = is_full
        self._speed = SLOW_SPEED

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        
    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, value: int):
        self._direction = value

    @property
    def is_full(self) -> bool:
        return self._is_full

    @is_full.setter
    def is_full(self, value: bool):
        self._is_full = value

    def update(self):
        """
        Moves the package along a conveyor belt.
        """
        self.x += self._speed * self.direction

    def draw(self):
        """
        Draws the package on the screen.
        """
        pyxel.blt(self.x, self.y, *PCK_LVL1)
