import pyxel
import constants

class Character:
    STATE_STATIC = 0
    STATE_WAIT = 1
    STATE_PCK = 2
    STATE_BOSS = 3
    STATE_REST1 = 4
    STATE_REST2 = 5

    def __init__(self, name: str, x: int):
        # Name is private and read-only
        self.__name = name
        self.x = x
        self.y = 0
        self.state = self.STATE_STATIC
        self.original_x = x 
        self.punishment_timer = 0
        
        # Logical dimensions (Hitbox) - Read Only
        self.__width = 12
        self.__height = 16

        # Use the property self.name to check logic
        if self.name == "Mario":
            self.sprites = constants.MARIO_SPRITES
            self.key_up = pyxel.KEY_UP
            self.key_down = pyxel.KEY_DOWN
            self.floor = 0
        else:
            self.sprites = constants.LUIGI_SPRITES
            self.key_up = pyxel.KEY_W
            self.key_down = pyxel.KEY_S
            self.floor = 1

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value: int):
        if not isinstance(value, int): raise TypeError("x must be an integer")
        self.__x = value

    @property
    def floor(self) -> int: return self.__floor
    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int): raise TypeError("floor must be an integer")
        self.__floor = value

    # --- Read-Only Properties ---
    @property
    def name(self) -> str:
        return self.__name

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        """ Returns the logical hitbox height. """
        return self.__height

    def move_up(self, max_floors: int):
        next_floor = self.floor + 2
        if next_floor < max_floors:
            self.floor = next_floor

    def move_down(self):
        next_floor = self.floor - 2
        if next_floor >= 0:
            self.floor = next_floor

    def set_state_static(self): self.state = self.STATE_STATIC
    def set_state_wait(self): self.state = self.STATE_WAIT
    def set_state_pick(self): self.state = self.STATE_PCK

    def enter_punishment_mode(self):
        self.state = self.STATE_BOSS
        if self.name == "Mario": self.x = constants.PUNISH_MARIO_X
        else: self.x = constants.PUNISH_LUIGI_X
        
        # Here we use the specific sprite height for the boss state
        boss_sprite_h = self.sprites[self.STATE_BOSS][4]
        self.y = (constants.BOSS_Y) - boss_sprite_h

    def exit_punishment_mode(self, conveyors_list: list):
        self.state = self.STATE_STATIC
        self.x = self.original_x
        self.update(conveyors_list)

    def update(self, conveyors_list: list):
        if self.state == self.STATE_BOSS:
            return
        
        if pyxel.btnp(self.key_up):
            self.move_up(len(conveyors_list))
        elif pyxel.btnp(self.key_down):
            self.move_down()

        # Get the height of the CURRENT sprite to ensure perfect floor contact
        current_sprite = self.sprites[self.state]
        sprite_h = current_sprite[4]
        
        if self.floor == 0:
            ground_top = constants.SCREEN_HEIGHT - 6
            # Use visual sprite height
            self.y = ground_top - sprite_h
        else:
            conv_index = self.floor
            if 0 <= conv_index < len(conveyors_list):
                conveyor = conveyors_list[conv_index]
                # Use visual sprite height
                self.y = (conveyor.y + 2) - sprite_h

    def draw(self):
        img, u, v, w, h, colkey = self.sprites[self.state]
        draw_w = w
        is_mario_ground_static = (self.name == "Mario" and self.floor == 0 and self.state == self.STATE_STATIC)
        if is_mario_ground_static:
             draw_w = -w
        pyxel.blt(self.x, self.y, img, u, v, draw_w, h, colkey)