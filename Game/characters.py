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
    def x(self, value):
        # Relaxed type check for physics
        if not isinstance(value, (int, float)): raise TypeError("x must be a number")
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

    def exit_punishment_mode(self):
        # Removed conveyors_list argument
        self.state = self.STATE_STATIC
        self.x = self.original_x
        self.update()

    def update(self):
        # Removed conveyors_list argument
        if self.state == self.STATE_BOSS:
            return
        
        # Input handling needs to know max floors. 
        # For simplicity in this decoupled version, we assume a safe max (e.g., 10) 
        # or we could pass just the INT limit, but logic is cleaner if Board checks limits.
        # However, to keep standard movement here:
        # We assume constants.FLOOR_Y_LEVELS has enough entries.
        if pyxel.btnp(self.key_up):
            # We use the length of the constant list as the limit
            self.move_up(len(constants.FLOOR_Y_LEVELS))
        elif pyxel.btnp(self.key_down):
            self.move_down()

        # Get the height of the CURRENT sprite to ensure perfect floor contact
        current_sprite = self.sprites[self.state]
        sprite_h = current_sprite[4]
        
        # --- NEW LOGIC: Use Constant List ---
        # Ensure we don't go out of index
        safe_floor = min(self.floor, len(constants.FLOOR_Y_LEVELS) - 1)
        target_floor_y = constants.FLOOR_Y_LEVELS[safe_floor]
        
        # Position is floor level minus the sprite height
        self.y = target_floor_y - sprite_h

    def draw(self):
        img, u, v, w, h, colkey = self.sprites[self.state]
        draw_w = w
        is_mario_ground_static = (self.name == "Mario" and self.floor == 0 and self.state == self.STATE_STATIC)
        if is_mario_ground_static:
             draw_w = -w
        
        # Cast to int for drawing
        pyxel.blt(int(self.x), int(self.y), img, u, v, draw_w, h, colkey)