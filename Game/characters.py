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
        self.__name = name
        self.x = x
        self.y = 0
        self.state = self.STATE_STATIC
        self.original_x = x 
        # New: Animation timer
        self.rest_timer = 0
        
        self.max_floor_index = 10 
        self.__width = 12
        self.__height = 16

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
        if not isinstance(value, (int, float)): raise TypeError("x must be a number")
        self.__x = value

    @property
    def floor(self) -> int: return self.__floor
    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int): raise TypeError("floor must be an integer")
        self.__floor = value

    @property
    def name(self) -> str: return self.__name
    @property
    def width(self) -> int: return self.__width
    @property
    def height(self) -> int: return self.__height

    def move_up(self):
        next_floor = self.floor + 2
        if next_floor <= self.max_floor_index:
            self.floor = next_floor

    def move_down(self):
        next_floor = self.floor - 2
        if next_floor >= 0:
            self.floor = next_floor

    def enter_rest_mode(self):
        self.state = self.STATE_REST1
        self.rest_timer = 0

    def exit_rest_mode(self):
        self.state = self.STATE_STATIC
        self.update()

    def enter_punishment_mode(self):
        self.state = self.STATE_BOSS
        
        if self.name == "Mario": 
            self.x = constants.PUNISH_MARIO_X
        else: 
            self.x = constants.PUNISH_LUIGI_X
            
        # We call the physics helper immediately to set the Y position
        self.__update_physics_boss()

    def exit_punishment_mode(self):
        self.state = self.STATE_STATIC
        self.x = self.original_x
        self.update()

    def __animate_rest(self):
        """ Private method to toggle rest sprites. """
        self.rest_timer += 1
        # Math: Toggles 0 or 1 every 15 frames
        offset = (self.rest_timer // 15) % 2
        self.state = self.STATE_REST1 + offset

    def __handle_input(self):
        """ Private: Handles keyboard input for movement. """
        if pyxel.btnp(self.key_up):
            self.move_up()
        elif pyxel.btnp(self.key_down):
            self.move_down()

    def __update_physics_floor(self):
        """ Private: Calculates Y position based on the current floor. """
        current_sprite = self.sprites[self.state]
        sprite_h = current_sprite[4]
        
        safe_floor = min(self.floor, len(constants.FLOOR_Y_LEVELS) - 1)
        target_floor_y = constants.FLOOR_Y_LEVELS[safe_floor]
        
        self.y = target_floor_y - sprite_h

    def __update_physics_boss(self):
        """ Private: Calculates Y position relative to the Boss platform. """
        boss_sprite_h = self.sprites[self.STATE_BOSS][4]
        self.y = (constants.BOSS_Y) - boss_sprite_h

    def update(self):
        # --- 1. LOGIC PHASE (State Behavior) ---
        if self.state == self.STATE_REST1 or self.state == self.STATE_REST2:
            self.__animate_rest()
            
        elif self.state != self.STATE_BOSS:
            # If not resting and not being punished, we handle input
            self.__handle_input()

        # --- 2. PHYSICS PHASE (Positioning) ---
        if self.state == self.STATE_BOSS:
            self.__update_physics_boss()
        else:
            self.__update_physics_floor()

    def draw(self):
        img, u, v, w, h, colkey = self.sprites[self.state]
        draw_w = w
        # Flip Mario if he is on ground and static (facing left default)
        if self.name == "Mario" and self.floor == 0 and self.state == self.STATE_STATIC:
             draw_w = -w
        pyxel.blt(int(self.x), int(self.y), img, u, v, draw_w, h, colkey)