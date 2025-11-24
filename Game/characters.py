import pyxel
import constants

class Character:
    """ 
    This class represents the characters in the game (Mario and Luigi). 
    """
    def __init__(self, name: str, x: int):
        """
        :param name: str - "Mario" or "Luigi"
        :param x: int - Fixed x-coordinate
        """
        self.name = name
        self.x = x
        self.y = 0

        # --- SETUP BASED ON CHARACTER ---
        if self.name == "Mario":
            self.sprite = constants.MARIO_WAIT
            self.key_up = pyxel.KEY_UP
            self.key_down = pyxel.KEY_DOWN
            # Mario starts on Floor 0 (The Ground)
            self.floor = 0
        else:
            self.sprite = constants.LUIGI_PCK
            self.key_up = pyxel.KEY_W
            self.key_down = pyxel.KEY_S
            # Luigi starts on Floor 1 (The first Conveyor)
            self.floor = 1

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("x must be an integer")
        self.__x = value

    @property
    def floor(self) -> int:
        return self.__floor
    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int):
            raise TypeError("floor must be an integer")
        self.__floor = value

    def move_up(self, max_floors: int):
        """ Move up 2 floors (Skip the other brother's floor) """
        next_floor = self.floor + 2
        if next_floor <= max_floors:
            self.floor = next_floor

    def move_down(self):
        """ Move down 2 floors """
        next_floor = self.floor - 2
        if next_floor >= 0:
            self.floor = next_floor

    def update(self, floors_list: list):
        """
        Updates character logic.
        :param floors_list: List of Y coordinates for the floors
        """
        # Handle Input
        if pyxel.btnp(self.key_up):
            self.move_up(len(floors_list))
        elif pyxel.btnp(self.key_down):
            self.move_down()

        sprite_h = self.sprite[4]
        if self.floor == 0:
            # SPECIAL CASE: GROUND
            # Ground Y is calculated as SCREEN_HEIGHT - 11 in board.py.
            # We recreate that logic here or pass it. 
            # Ground Top = 144 - 11 = 133.
            ground_top = constants.SCREEN_HEIGHT - 11
            self.y = ground_top - sprite_h
        elif self.floor > 0 and (self.floor - 1) < len(floors_list):
            # ELEVATED FLOORS
            # Floor 1 corresponds to floors_list[0]
            floor_y = floors_list[self.floor - 1]
            self.y = (floor_y +1) - sprite_h

    def draw(self):
        """ Draw the character sprite """
        pyxel.blt(self.x, self.y, *self.sprite)