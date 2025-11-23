import pyxel
from constants import (
    MARIO_X, LUIGI_X, FLOOR_Y_POSITIONS,
    MARIO_STATIC, LUIGI_STATIC,
    MARIO_REST1, MARIO_REST2,
    LUIGI_REST1, LUIGI_REST2
)

class Character:
    """
    A class that represents a character in the game.
    This is a base class for Mario and Luigi.
    """

    def __init__(self, x: int, sprite: tuple, initial_floor: int, character_type: str):
        """
        Initialize the Character.
        :param x: The initial x-coordinate of the character.
        :param sprite: The initial sprite for the character.
        :param initial_floor: The initial floor index for the character.
        :param character_type: The type of the character ("mario" or "luigi").
        """
        self._x = x
        self._floor = initial_floor
        self._y = FLOOR_Y_POSITIONS[self._floor]
        self._current_sprite = sprite
        self._state = "static"
        self.character_type = character_type
        self._animation_timer = 0

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
        Move the character up or down between floors, skipping floors.
        :param direction: The direction to move ("up" or "down").
        """
        if direction == "up":
            if self._floor < len(FLOOR_Y_POSITIONS) - 2:
                self._floor += 2
        elif direction == "down":
            if self._floor > 1:
                self._floor -= 2
        
        self._y = FLOOR_Y_POSITIONS[self._floor]

    def rest(self):
        """
        Sets the character's state to resting.
        """
        self._state = "resting"
        self._animation_timer = 60 # 1 second at 60fps

    def update(self):
        """
        Updates the character's state.
        """
        if self._state == "resting":
            self._animation_timer -= 1
            if self._animation_timer <= 0:
                self._state = "static"
    
    def draw(self):
        """
        Draws the character on the screen.
        """
        if self._state == "resting":
            if (self._animation_timer // 15) % 2 == 0:
                if self.character_type == "mario":
                    self._current_sprite = MARIO_REST1
                else:
                    self._current_sprite = LUIGI_REST1
            else:
                if self.character_type == "mario":
                    self._current_sprite = MARIO_REST2
                else:
                    self._current_sprite = LUIGI_REST2
        elif self._state == "static":
            if self.character_type == "mario":
                self._current_sprite = MARIO_STATIC
            else:
                self._current_sprite = LUIGI_STATIC
            
        pyxel.blt(self.x, self.y, *self._current_sprite)

class Mario(Character):
    """
    The Mario character.
    """
    def __init__(self):
        """
        Initialize Mario.
        """
        super().__init__(MARIO_X, MARIO_STATIC, initial_floor=1, character_type="mario")

    def update(self):
        """
        Update Mario's state.
        """
        super().update()
        if self._state != "resting":
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
        super().__init__(LUIGI_X, LUIGI_STATIC, initial_floor=1, character_type="luigi")

    def update(self):
        """
        Update Luigi's state.
        """
        super().update()
        if self._state != "resting":
            if pyxel.btnp(pyxel.KEY_W):
                self.move("up")
            elif pyxel.btnp(pyxel.KEY_S):
                self.move("down")
