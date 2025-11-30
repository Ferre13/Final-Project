import pyxel
import constants

class Character:
    """
    Represents a player character (Mario or Luigi), responsible for its own state,
    movement, and drawing. It handles user input and character-specific logic
    like being in a "punished" or "resting" state.
    """
    def __init__(self, name: str, x: int, difficulty: str, num_floors: int):
        """
        Initializes a character.

        :param name: The name of the character ("Mario" or "Luigi").
        :param x: The initial x-coordinate.
        :param difficulty: The game difficulty, used for input handling.
        :param num_floors: The total number of floors in the level.
        """
        self.__name = name
        self.x = x
        self.__difficulty = difficulty
        
        self.y = 0
        self.state = constants.CHAR_STATE_STATIC
        self.original_x = x 
        self.rest_timer = 0
        self.floor = 0
        self.transfer_timer = 0
        
        # The maximum floor index the character can be on.
        self.max_floor_index = num_floors

        if self.name == "Mario":
            self.floor = 0
        else:
            self.floor = 1

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
    def width(self) -> int:
        """Returns the width of the character's static sprite."""
        return constants.MARIO_STATIC[3]

    @property
    def height(self) -> int:
        """Returns the height of the character's static sprite."""
        return constants.MARIO_STATIC[4]

    @property
    def state(self) -> int: return self.__state
    @state.setter
    def state(self, value: int):
        if not isinstance(value, int): raise TypeError("state must be int")
        self.__state = value

    @property
    def __sprites(self) -> list:
        """Returns the appropriate list of sprites based on the character's name."""
        if self.name == "Mario":
            return constants.MARIO_SPRITES
        else:
            return constants.LUIGI_SPRITES

    @property
    def key_up(self) -> int:
        """Returns the appropriate 'up' key based on the character's name."""
        if self.name == "Mario":
            return pyxel.KEY_UP
        else:
            return pyxel.KEY_W

    @property
    def key_down(self) -> int:
        """Returns the appropriate 'down' key based on the character's name."""
        if self.name == "Mario":
            return pyxel.KEY_DOWN
        else:
            return pyxel.KEY_S

    def can_receive_package(self, package_floor: int) -> bool:
        """
        Checks if the character is in the correct position and state to receive a package.
        
        :param package_floor: The floor index of the package.
        :return: True if the character can receive the package, False otherwise.
        """
        # A character can only start a transfer if they are standing still.
        if self.state != constants.CHAR_STATE_STATIC:
            return False
            
        if self.floor != package_floor: 
            return False
        
        # Mario handles even floors (0, 2, 4...), Luigi handles odd floors (1, 3, 5...)
        if self.name == "Mario": 
            return (package_floor % 2 == 0)
        else: 
            return (package_floor % 2 != 0)

    def move_up(self):
        """Moves the character up by two floors if possible."""
        next_floor = self.floor + 2
        if next_floor <= self.max_floor_index:
            self.floor = next_floor

    def move_down(self):
        """Moves the character down by two floors if possible."""
        next_floor = self.floor - 2
        if next_floor >= 0:
            self.floor = next_floor

    def enter_rest_mode(self):
        """Puts the character into the resting state (during truck sequence)."""
        self.state = constants.CHAR_STATE_REST1
        self.rest_timer = 0

    def exit_rest_mode(self):
        """Takes the character out of the resting state."""
        self.state = constants.CHAR_STATE_STATIC
        self.update() 

    def enter_punishment_mode(self):
        """Puts the character into the punishment state (after a failure)."""
        self.state = constants.CHAR_STATE_BOSS
        if self.name == "Mario": self.x = constants.PUNISH_MARIO_X
        else: self.x = constants.PUNISH_LUIGI_X
        self.__update_physics_boss()

    def exit_punishment_mode(self):
        """Takes the character out of the punishment state."""
        self.state = constants.CHAR_STATE_STATIC
        self.x = self.original_x
        self.update()

    def start_transfer_animation(self):
        """Starts the two-part package transfer animation."""
        # This can only be called when the character is static,
        # ensuring animations don't improperly interrupt each other.
        if self.state == constants.CHAR_STATE_STATIC:
            self.state = constants.CHAR_STATE_TRANSFER
            # Set the timer for the full two-part animation.
            self.transfer_timer = constants.TRANSFER_ANIMATION_TIME * 2

    def __animate_rest(self):
        """Animates the character while in the resting state."""
        self.rest_timer += 1
        offset = (self.rest_timer // 15) % 2
        self.state = constants.CHAR_STATE_REST1 + offset

    def __update_physics_floor(self):
        """Calculates the character's y-position based on their current floor."""
        # Determine which sprite to use for height calculation.
        sprite_index = self.state
        if self.state == constants.CHAR_STATE_TRANSFER:
            # For height calculation, assume the tallest possible sprite in the animation.
            sprite_index = constants.CHAR_STATE_PCK
            
        current_sprite = self.__sprites[sprite_index]
        sprite_h = current_sprite[4]
        safe_floor = min(self.floor, len(constants.FLOOR_Y_LEVELS) - 1)
        self.y = constants.FLOOR_Y_LEVELS[safe_floor] - sprite_h

    def __update_physics_boss(self):
        """Calculates the character's y-position when in the boss area."""
        boss_sprite_h = self.__sprites[self.state][4]
        self.y = constants.BOSS_Y - boss_sprite_h

    def update(self):
        """
        Main update method for the character. It prioritizes states and player input
        to determine the character's actions for the frame.
        """
        # States that cannot be interrupted by player input
        if self.state in [constants.CHAR_STATE_REST1, constants.CHAR_STATE_REST2]:
            self.__animate_rest()
        elif self.state == constants.CHAR_STATE_BOSS:
            # Physics are handled below, no other logic for this state
            pass
        
        # If not in a locked state, check for player input, which takes priority
        else:
            up_pressed = pyxel.btnp(self.key_up)
            down_pressed = pyxel.btnp(self.key_down)

            if self.__difficulty == "CRAZY":
                up_pressed, down_pressed = down_pressed, up_pressed

            if up_pressed:
                self.state = constants.CHAR_STATE_STATIC  # Interrupts transfer animation
                self.move_up()
            elif down_pressed:
                self.state = constants.CHAR_STATE_STATIC  # Interrupts transfer animation
                self.move_down()
            
            # If no input was detected, handle the transfer animation timer
            elif self.state == constants.CHAR_STATE_TRANSFER:
                self.transfer_timer -= 1
                if self.transfer_timer <= 0:
                    self.state = constants.CHAR_STATE_STATIC

        # --- Update Physics ---
        # Update vertical position based on the final state for this frame.
        if self.state == constants.CHAR_STATE_BOSS:
            self.__update_physics_boss()
        else:
            self.__update_physics_floor()

    def draw(self):
        """Draws the character's current sprite at its x, y position."""
        sprite_index = self.state
        draw_w_mod = 1 # Used to flip sprite horizontally

        # If in the transfer animation, choose the sprite based on the timer.
        if self.state == constants.CHAR_STATE_TRANSFER:
            # First half of animation: "getting ready" sprite (_WAIT)
            # The actual transfer happens at the midpoint of the animation.
            if self.transfer_timer > constants.TRANSFER_ANIMATION_TIME:
                # Special case for Mario on floor 0
                if self.name == "Mario" and self.floor == 0:
                    sprite_index = constants.CHAR_STATE_PCK # Use PCK sprite
                    draw_w_mod = -1 # And flip it
                else:
                    sprite_index = constants.CHAR_STATE_WAIT
            # Second half of animation: "has package" sprite (_PCK)
            else:
                sprite_index = constants.CHAR_STATE_PCK
        
        # Flip the static sprite for Mario on the ground floor
        elif self.name == "Mario" and self.floor == 0 and self.state == constants.CHAR_STATE_STATIC:
             draw_w_mod = -1
             
        img, u, v, w, h, colkey = self.__sprites[sprite_index]
        pyxel.blt(self.x, self.y, img, u, v, w * draw_w_mod, h, colkey)
