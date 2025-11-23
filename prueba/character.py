import pyxel
from constants import (
    MARIO_X, LUIGI_X, FLOOR_Y_POSITIONS,
    MARIO_STATIC, LUIGI_STATIC
)

class Character:
    """
    A class that represents a character in the game.
    This is a base class for Mario and Luigi.
    """

    def __init__(self, x: int, sprite: tuple, initial_floor: int):
        """
        Initialize the Character.
        :param x: The initial x-coordinate of the character.
        :param sprite: The initial sprite for the character.
        :param initial_floor: The initial floor index for the character.
        """
        self._x = x
        self._floor = initial_floor
        self._y = FLOOR_Y_POSITIONS[self._floor]
        self._current_sprite = sprite
        self._state = "static"

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def floor(self) -> int:
        return self._floor

    def move(self, direction: str):
        """
        Move the character up or down between floors.
        :param direction: The direction to move ("up" or "down").
        """
        if direction == "up":
            if self._floor < len(FLOOR_Y_POSITIONS) - 1:
                self._floor += 1
        elif direction == "down":
            if self._floor > 0:
                self._floor -= 1
        
        self._y = FLOOR_Y_POSITIONS[self._floor]

    def draw(self):
        """
        Draw the character on the screen.
        """
        pyxel.blt(self.x, self.y, *self._current_sprite)

class Mario(Character):
    """
    The Mario character.
    """
    def __init__(self):
        """
        Initialize Mario.
        """
        super().__init__(MARIO_X, MARIO_STATIC, initial_floor=1)

    def update(self):
        """
        Update Mario's state.
        """
        if pyxel.btnp(pyxel.KEY_UP):
            self.move("up")
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.move("down")

class Luigi(Character):
    """
    The Luigi character.
    """
    def __init__(self):
        """
        Initialize Luigi.
        """
        super().__init__(LUIGI_X, LUIGI_STATIC, initial_floor=1)

    def update(self):
        """
        Update Luigi's state.
        """
        if pyxel.btnp(pyxel.KEY_W):
            self.move("up")
        elif pyxel.btnp(pyxel.KEY_S):
            self.move("down")
