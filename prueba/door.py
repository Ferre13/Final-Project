import pyxel
from constants import DOOR_CLOSED, DOOR_OPENING, DOOR_OPEN

class Door:
    """
    Represents the door for the boss to appear from.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the door.
        :param x: The x-coordinate of the door.
        :param y: The y-coordinate of the door.
        """
        self._x = x
        self._y = y
        self._state = "closed"
        self._animation_timer = 0
        self._current_sprite = DOOR_CLOSED

    def open(self):
        """
        Starts the door opening animation.
        """
        self._state = "opening"
        self._animation_timer = 30 # 0.5 seconds at 60fps

    def close(self):
        """
        Starts the door closing animation.
        """
        self._state = "closing"
        self._animation_timer = 30 # 0.5 seconds at 60fps

    def update(self):
        """
        Updates the door's animation.
        """
        if self._state == "opening":
            self._animation_timer -= 1
            if self._animation_timer > 15:
                self._current_sprite = DOOR_OPENING
            else:
                self._current_sprite = DOOR_OPEN
            if self._animation_timer <= 0:
                self._state = "open"
        elif self._state == "closing":
            self._animation_timer -= 1
            if self._animation_timer > 15:
                self._current_sprite = DOOR_OPENING
            else:
                self._current_sprite = DOOR_CLOSED
            if self._animation_timer <= 0:
                self._state = "closed"
    
    def draw(self):
        """
        Draws the door on the screen.
        """
        pyxel.blt(self._x, self._y, *self._current_sprite)
