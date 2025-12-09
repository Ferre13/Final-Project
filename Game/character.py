import pyxel
import constants
from game_object import GameObject

class Character(GameObject):
    """A base class for characters, containing shared logic."""
    def __init__(self, x: int, difficulty: str, num_floors: int, initial_floor: int, 
                 sprites: list, key_up: int, key_down: int, punish_x: int):
        """
        :param x: The starting x-coordinate.
        :param difficulty: The current game difficulty.
        :param num_floors: The total number of floors in the level.
        :param initial_floor: The starting floor for the character.
        :param sprites: The list of sprites for the character.
        :param key_up: The key to move up.
        :param key_down: The key to move down.
        :param punish_x: The x-coordinate for the punishment position.
        """
        super().__init__(x, 0)
        self.difficulty = difficulty
        self.initial_floor = initial_floor
        self.punish_x = punish_x
        
        self.sprites = sprites
        self.key_up = key_up
        self.key_down = key_down

        self.state = constants.CHAR_STATE_STATIC
        self.original_x = x 
        self.rest_start_frame = 0
        self.floor = initial_floor
        self.transfer_pose_start_frame = 0
        self.max_floor_index = num_floors

    @property
    def floor(self) -> int:
        """The current floor number of the character."""
        return self.__floor
    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int): 
            raise TypeError("floor must be int")
        self.__floor = value

    @property
    def state(self) -> int:
        """The current state of the character (static, resting...)."""
        return self.__state
    @state.setter
    def state(self, value: int):
        if not isinstance(value, int): 
            raise TypeError("state must be int")
        self.__state = value

    def can_receive_package(self, package_floor: int) -> bool:
        """
        Checks if the character can receive a package, based on floor parity.
        :param package_floor: The floor index of the package.
        """
        # Check if the package floor has the same parity as the character's initial floor
        # This ensures characters only interact with packages on floors matching their starting parity
        is_correct_floor_type = (package_floor % 2 == self.initial_floor % 2)
        if self.state != constants.CHAR_STATE_STATIC:
            return False
        if self.floor != package_floor:
            return False
        if not is_correct_floor_type:
            return False
        return True

    def enter_punishment_mode(self):
        """Puts the character in their punishment state and position."""
        self.state = constants.CHAR_STATE_PUNISHED
        self.x = self.punish_x
        self.update_physics_boss()

    def reset(self):
        """Resets the character to its default state."""
        self.state = constants.CHAR_STATE_STATIC
        self.x = self.original_x
        self.floor = self.initial_floor
        self.update()

    def move_up(self):
        """Moves the character up by two floors."""
        next_floor = self.floor + 2
        if next_floor <= self.max_floor_index:
            self.floor = next_floor

    def move_down(self):
        """Moves the character down by two floors."""
        next_floor = self.floor - 2
        if next_floor >= 0:
            self.floor = next_floor

    def enter_rest_mode(self):
        """Puts the character into the resting state."""
        self.state = constants.CHAR_STATE_REST1
        self.rest_start_frame = pyxel.frame_count

    def exit_rest_mode(self):
        """Takes the character out of the resting state."""
        self.state = constants.CHAR_STATE_STATIC
        self.x = self.original_x
        self.update() 

    def exit_punishment_mode(self):
        """Takes the character out of the punishment state."""
        self.state = constants.CHAR_STATE_STATIC
        self.x = self.original_x
        self.update()

    def animate_rest(self):
        """Animates the character while resting."""
        # Calculate how many frames have passed since resting started
        elapsed_frames = pyxel.frame_count - self.rest_start_frame
        # Alternates between 0 and 1 because there are 2 rest sprites
        offset = (elapsed_frames // constants.REST_ANIMATION_SPEED) % 2
        self.state = constants.CHAR_STATE_REST1 + offset

    def show_transfer_pose(self):
        """Briefly shows the transfer pose."""
        if self.state == constants.CHAR_STATE_STATIC:
            self.state = constants.CHAR_STATE_TRANSFER_POSE
            self.transfer_pose_start_frame = pyxel.frame_count

    def update_transfer_pose(self):
        """Returns character to static state after transfer animation."""
        if pyxel.frame_count >= self.transfer_pose_start_frame + constants.TRANSFER_ANIMATION_TIME:
            self.state = constants.CHAR_STATE_STATIC

    def update_y_pos(self):
        """Calculates the character's y-position based on the current floor."""
        current_sprite = self.sprites[self.state]
        sprite_h = current_sprite[4]
        self.y = constants.FLOOR_Y_LEVELS[self.floor] - sprite_h

    def update_physics_boss(self):
        """Calculates the character's y-position when in the boss area."""
        boss_sprite_h = self.sprites[self.state][4]
        self.y = constants.BOSS_Y - boss_sprite_h

    def handle_player_input(self):
        """Handles player input for moving the character up or down."""
        up_pressed = pyxel.btnp(self.key_up)
        down_pressed = pyxel.btnp(self.key_down)
        if self.difficulty == "CRAZY":
            # In CRAZY mode, invert controls
            up_pressed, down_pressed = down_pressed, up_pressed

        if up_pressed:
            self.state = constants.CHAR_STATE_STATIC
            self.move_up()
        elif down_pressed:
            self.state = constants.CHAR_STATE_STATIC
            self.move_down()

    def update(self):
        """Updates the character's state and position."""
        if self.state == constants.CHAR_STATE_REST1 or self.state == constants.CHAR_STATE_REST2:
            self.animate_rest()
        elif self.state == constants.CHAR_STATE_TRANSFER_POSE:
            self.update_transfer_pose()
            # Allow movement during transfer pose, in case player wants to change floor
            self.handle_player_input()
        elif self.state != constants.CHAR_STATE_PUNISHED:
            self.handle_player_input()

        # Punished characters are the only ones that handle y-position differently
        if self.state == constants.CHAR_STATE_PUNISHED:
            self.update_physics_boss()
        else:
            self.update_y_pos()


# We create two subclasses for Mario and Luigi to define their specific attributes
class Mario(Character):
    """Represents the Mario character, providing his specific attributes."""
    def __init__(self, x: int, difficulty: str, num_floors: int):
        """
        :param x: The starting x-coordinate.
        :param difficulty: The current game difficulty.
        :param num_floors: The total number of floors in the level.
        """
        super().__init__(x, difficulty, num_floors, initial_floor = 0, sprites = constants.MARIO_SPRITES, key_up = pyxel.KEY_UP, 
                         key_down = pyxel.KEY_DOWN, punish_x = constants.PUNISH_MARIO_X)

    def draw(self):
        """Draws Mario on the screen."""
        sprite_index = self.state
        # Mario faces left when on the bottom floor
        img, u, v, w, h, colkey = self.sprites[sprite_index]
        if self.floor == 0 and self.state == constants.CHAR_STATE_STATIC:
            w = -w
        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)


class Luigi(Character):
    """Represents the Luigi character, providing his specific attributes."""
    def __init__(self, x: int, difficulty: str, num_floors: int):
        """
        Initializes Luigi.
        :param x: The starting x-coordinate.
        :param difficulty: The current game difficulty.
        :param num_floors: The total number of floors in the level.
        """
        super().__init__(x, difficulty, num_floors, initial_floor = 1, sprites = constants.LUIGI_SPRITES,
            key_up = pyxel.KEY_W, key_down = pyxel.KEY_S, punish_x = constants.PUNISH_LUIGI_X)

    def draw(self):
        """Draws Luigi on the screen."""
        sprite_index = self.state
        # Luigi faces left when on the top floor with a package
        img, u, v, w, h, colkey = self.sprites[sprite_index]
        if self.floor == self.max_floor_index and self.state == constants.CHAR_STATE_TRANSFER_POSE:
            w = -w
        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)