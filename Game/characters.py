import pyxel
import constants

class Character:
    """
    Represents Mario or Luigi. 
    Handles input inversion for 'CRAZY' mode.
    """
    def __init__(self, name: str, x: int, difficulty: str):
        self.__name = name
        self.x = x
        self.__difficulty = difficulty
        
        self.y = 0
        self.state = constants.CHAR_STATE_STATIC
        self.original_x = x 
        self.rest_timer = 0
        self.floor = 0
        
        # Max floor derived from constants
        self.max_floor_index = len(constants.FLOOR_Y_LEVELS) - 1 
        self.__width = constants.MARIO_STATIC[3]
        self.__height = constants.MARIO_STATIC[4]

        if self.name == "Mario":
            self.__sprites = constants.MARIO_SPRITES
            self.key_up = pyxel.KEY_UP
            self.key_down = pyxel.KEY_DOWN
            self.floor = 0 
        else:
            self.__sprites = constants.LUIGI_SPRITES
            self.key_up = pyxel.KEY_W
            self.key_down = pyxel.KEY_S
            self.floor = 1 

    # --- GETTERS AND SETTERS ---
    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value):
        if not isinstance(value, int): raise TypeError("x must be int")
        self.__x = value

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, value):
        if not isinstance(value, int): raise TypeError("y must be int")
        self.__y = value

    @property
    def floor(self) -> int: return self.__floor
    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int): raise TypeError("floor must be int")
        self.__floor = value

    @property
    def name(self) -> str: return self.__name
    @property
    def width(self) -> int: return self.__width
    @property
    def height(self) -> int: return self.__height
    @property
    def state(self) -> int: return self.__state
    @state.setter
    def state(self, value: int):
        if not isinstance(value, int): raise TypeError("state must be int")
        self.__state = value

    # --- LOGIC ---
    def can_receive_package(self, package_floor: int) -> bool:
        if self.floor != package_floor: return False
        
        if self.name == "Mario": 
            return (package_floor % 2 == 0)
        else: 
            return (package_floor % 2 != 0)

    def move_up(self):
        next_floor = self.floor + 2
        if next_floor <= self.max_floor_index:
            self.floor = next_floor

    def move_down(self):
        next_floor = self.floor - 2
        if next_floor >= 0:
            self.floor = next_floor

    def enter_rest_mode(self):
        self.state = constants.CHAR_STATE_REST1
        self.rest_timer = 0

    def exit_rest_mode(self):
        self.state = constants.CHAR_STATE_STATIC
        self.update() 

    def enter_punishment_mode(self):
        self.state = constants.CHAR_STATE_BOSS
        if self.name == "Mario": self.x = constants.PUNISH_MARIO_X
        else: self.x = constants.PUNISH_LUIGI_X
        self.__update_physics_boss()

    def exit_punishment_mode(self):
        self.state = constants.CHAR_STATE_STATIC
        self.x = self.original_x
        self.update()

    # --- INTERNAL METHODS ---

    def __animate_rest(self):
        self.rest_timer += 1
        offset = (self.rest_timer // 15) % 2
        self.state = constants.CHAR_STATE_REST1 + offset

    def __handle_input(self):
        """ Handles keyboard input with difficulty logic. """
        if self.__difficulty == "CRAZY":
            # Inverted Controls
            if pyxel.btnp(self.key_up): 
                self.move_down()
            elif pyxel.btnp(self.key_down): 
                self.move_up()
        else:
            # Normal Controls
            if pyxel.btnp(self.key_up): 
                self.move_up()
            elif pyxel.btnp(self.key_down): 
                self.move_down()

    def __update_physics_floor(self):
        current_sprite = self.__sprites[self.state]
        sprite_h = current_sprite[4]
        safe_floor = min(self.floor, len(constants.FLOOR_Y_LEVELS) - 1)
        self.y = constants.FLOOR_Y_LEVELS[safe_floor] - sprite_h

    def __update_physics_boss(self):
        boss_sprite_h = self.__sprites[self.state][4]
        self.y = constants.BOSS_Y - boss_sprite_h

    def update(self):
        if self.state in [constants.CHAR_STATE_REST1, constants.CHAR_STATE_REST2]:
            self.__animate_rest()
        elif self.state != constants.CHAR_STATE_BOSS:
            self.__handle_input()

        if self.state == constants.CHAR_STATE_BOSS:
            self.__update_physics_boss()
        else:
            self.__update_physics_floor()

    def draw(self):
        img, u, v, w, h, colkey = self.__sprites[self.state]
        draw_w = w
        if self.name == "Mario" and self.floor == 0 and self.state == constants.CHAR_STATE_STATIC:
             draw_w = -w
        pyxel.blt(self.x, self.y, img, u, v, draw_w, h, colkey)