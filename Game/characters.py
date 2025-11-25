import pyxel
import constants

class Character:
    """ 
    This class represents the characters in the game (Mario and Luigi). 
    """
    STATE_STATIC = 0
    STATE_WAIT = 1
    STATE_PCK = 2
    STATE_BOSS = 3
    STATE_REST1 = 4
    STATE_REST2 = 5
    def __init__(self, name: str, x: int):
        """
        :param name: str - "Mario" or "Luigi"
        :param x: int - Fixed x-coordinate
        """
        self.name = name
        self.x = x
        self.y = 0
        self.state = self.STATE_STATIC

        # Character specific settings
        if self.name == "Mario":
            self.sprites = constants.MARIO_SPRITES
            self.key_up = pyxel.KEY_UP
            self.key_down = pyxel.KEY_DOWN
            # Mario starts on Floor 0 (The Ground)
            self.floor = 0
        else:
            self.sprites = constants.LUIGI_SPRITES
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

    def set_state_static(self):
        self.state = self.STATE_STATIC
        
    def set_state_wait(self):
        self.state = self.STATE_WAIT
        
    def set_state_pick(self):
        self.state = self.STATE_PCK

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

        current_sprite = self.sprites[self.state]
        sprite_h = current_sprite[4]
        if self.floor == 0:
            # SPECIAL CASE: GROUND
            # Ground Y is calculated as SCREEN_HEIGHT - 11 in board.py.
            # We recreate that logic here or pass it. 
            # Ground Top = 144 - 11 = 133.
            ground_top = constants.SCREEN_HEIGHT - 6
            self.y = ground_top - sprite_h
        elif self.floor > 0 and (self.floor - 1) < len(floors_list):
            # ELEVATED FLOORS
            # Floor 1 corresponds to floors_list[0]
            floor_y = floors_list[self.floor - 1]
            self.y = (floor_y + 2) - sprite_h

    def draw(self):
        """ Draw the character sprite """
        sprite = self.sprites[self.state]
        img, u, v, w, h, colkey = sprite
        
        # 2. Flipping Logic
        # Default draw width
        draw_w = w
        
        # Mario on Floor 0 Logic:
        # "floor0 (from Mario) has Mario_static but inverted (flipped horizontally)"
        if self.name == "Mario" and self.floor == 0:
             draw_w = -w
             
        # NOTE: If you need Mario to face Left on the other floors (since he is on the right),
        # you might need to add an 'else' here to set draw_w = -w for floors > 0 as well.
        # For now, I am strictly following the instruction "flipped on floor 0".

        pyxel.blt(self.x, self.y, img, u, v, draw_w, h, colkey)