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

        self.original_x = x 
        self.punishment_timer = 0

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

    def enter_punishment_mode(self):
        """ Moves character to boss platform and changes state """
        self.state = self.STATE_BOSS
        # Move to the Boss Platform X coordinate
        if self.name == "Mario":
            self.x = constants.PUNISH_MARIO_X
        else:
            self.x = constants.PUNISH_LUIGI_X
        
        # Set Y to the Boss Floor level
        # Boss floor is at constants.BOSS_Y + 2. Character stands on top.
        # Height logic: (Floor_Y) - Sprite_Height
        self.y = (constants.BOSS_Y + 2) - self.sprites[self.STATE_BOSS][4]

    def exit_punishment_mode(self, original_floors_list: list):
        """ Returns character to normal gameplay """
        self.state = self.STATE_STATIC
        self.x = self.original_x
        # Force a Y update to snap back to the correct floor height
        self.update(original_floors_list)


    def update(self, floors_list: list):
        """
        Updates character logic.
        :param floors_list: List of Y coordinates for the floors
        """
        if self.state == self.STATE_BOSS:
            return
        
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
        img, u, v, w, h, colkey = self.sprites[self.state]
        
        # Default orientation
        draw_w = w
        
        # Special Case: Mario on Ground Floor (Static Only)
        # We only flip him when he is waiting (Static), not when punished or moving
        is_mario_ground_static = (
            self.name == "Mario" and 
            self.floor == 0 and 
            self.state == self.STATE_STATIC
        )

        if is_mario_ground_static:
             draw_w = -w
             
        pyxel.blt(self.x, self.y, img, u, v, draw_w, h, colkey)