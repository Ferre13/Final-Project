import pyxel
from constants import (
    TRUCK_EMPTY, TRUCK_1, TRUCK_2, TRUCK_3, TRUCK_4,
    TRUCK_5, TRUCK_6, TRUCK_7, TRUCK_8, TRUCK_FULL,
    TRUCK_AWAY_DURATION, TRUCK_X
)

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
        self._is_animating = False
        self._animation_timer = 0
        self._is_moving_away = False
        self._sprites = [
            TRUCK_EMPTY, TRUCK_1, TRUCK_2, TRUCK_3, TRUCK_4,
            TRUCK_5, TRUCK_6, TRUCK_7, TRUCK_8
        ]

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        
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
            if not self._is_moving_away:
                self.x = TRUCK_X
        else:
            self._packages_loaded = 0

    def add_package(self) -> bool:
        """
        Adds a package to the truck. Returns True if the truck is now full.
        """
        if not self.is_full:
            self._packages_loaded += 1
        
        if self.is_full:
            self._is_animating = True
            self._animation_timer = 180 # 3 seconds at 60fps
            return True
        return False

    def update(self):
        """
        Updates the truck's state.
        """
        if self._is_animating:
            self._animation_timer -= 1
            if self._animation_timer <= 0:
                self._is_animating = False
                self._is_moving_away = True
        
        if self._is_moving_away:
            self.x -= 2
            if self.x < -48:
                self._is_moving_away = False
                self.is_away = True

        if self.is_away:
            self._away_timer -= 1
            if self._away_timer <= 0:
                self.is_away = False

    def draw(self):
        """
        Draws the truck on the screen.
        """
        if not self.is_away or self._is_moving_away:
            sprite = self._sprites[self._packages_loaded]
            if self._is_animating:
                if (self._animation_timer // 30) % 2 == 0:
                    sprite = TRUCK_FULL
                else:
                    sprite = self._sprites[8]
            
            pyxel.blt(self.x, self.y, *sprite)
