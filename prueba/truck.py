import pyxel
from constants import *

class Truck:
    """
    Represents the delivery truck.
    """

    def __init__(self, x: int, y: int, capacity: int = 8):
        """
        Initializes the truck.
        :param x: The x-coordinate of the truck.
        :param y: The y-coordinate of the truck.
        :param capacity: The number of packages the truck can hold.
        """
        self._x = x
        self._y = y
        self._capacity = capacity
        self._packages_loaded = 0
        self._is_away = False
        self._away_timer = 0

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def is_full(self) -> bool:
        return self._packages_loaded >= self._capacity

    @property
    def is_away(self) -> bool:
        return self._is_away

    @is_away.setter
    def is_away(self, value: bool):
        self._is_away = value
        if value:
            self._away_timer = TRUCK_AWAY_DURATION
        else:
            self._packages_loaded = 0

    def add_package(self) -> bool:
        """
        Adds a package to the truck. Returns True if the truck is now full.
        """
        if not self.is_full:
            self._packages_loaded += 1
        
        if self.is_full:
            self.is_away = True
            return True
        return False

    def update(self):
        """
        Updates the truck's state.
        """
        if self.is_away:
            self._away_timer -= 1
            if self._away_timer <= 0:
                self.is_away = False

    def draw(self):
        """
        Draws the truck on the screen.
        """
        if not self.is_away:
            pyxel.blt(self.x, self.y, *TRUCK_SPRITE)
