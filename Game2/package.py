import pyxel
import constants
from game_object import GameObject
from conveyor import Conveyor 

class Package(GameObject):
    """Represents a package that moves along conveyors."""
    def __init__(self, difficulty: str, start_conveyor: Conveyor):
        """
        Initializes a package.
        :param difficulty: The current game difficulty.
        :param start_conveyor: The conveyor where the package will spawn.
        """
        super().__init__(0.0, 0.0)
        self.__difficulty = difficulty
        self.current_conveyor = start_conveyor
        self.floor_index = 0 # Always starts on floor 0
        self.sprites = constants.DIFFICULTY_SPRITES.get(self.__difficulty)
        self.width = constants.PCK_LVL1[3]
        self.height = constants.PCK_LVL1[4]
        self.x = self.current_conveyor.end_x - 10 # We know it always spawns on machine conveyor, which moves left
        self.y = self.current_conveyor.y - self.height
        
        self.state = constants.PKG_STATE_MOVING
        self.level_index = 0
        self.direction = -1 # Always starts moving left

    @property
    def current_conveyor(self) -> Conveyor:
        """The conveyor the package is currently on."""
        return self.__current_conveyor
    @current_conveyor.setter
    def current_conveyor(self, value: Conveyor):
        if not isinstance(value, Conveyor): 
            raise TypeError("Must be a Conveyor object")
        self.__current_conveyor = value

    def advance_to_conveyor(self, next_conveyor: Conveyor):
        """
        Moves the package to the next conveyor belt.
        :param next_conveyor: The conveyor object to move to.
        """
        self.current_conveyor = next_conveyor
        self.floor_index += 1
        if self.current_conveyor.direction == 1:
            self.x = self.current_conveyor.x - constants.OVERHANG_LIMIT
        else:
            self.x = self.current_conveyor.end_x + constants.OVERHANG_LIMIT - self.width
        self.y = self.current_conveyor.y - self.height
        self.state = constants.PKG_STATE_MOVING

    def fall(self):
        """Changes the package's state to falling."""
        self.state = constants.PKG_STATE_FALLING

    def update(self) -> int:
        """
        Updates the package's position and state.
        :return: A status code indicating the package's status.
        """
        if self.state == constants.PKG_STATE_FALLING:
            return self.__update_falling_state()
        elif self.state == constants.PKG_STATE_MOVING:
            return self.__update_moving_state()
        return constants.PKG_STATUS_MOVING

    def __update_falling_state(self) -> int:
        """Handles the package's logic while it is falling."""
        self.y += constants.PACKAGE_FALL_SPEED
        if self.y > constants.SCREEN_HEIGHT:
            return constants.PKG_STATUS_DELETE_ME
        # Package is still falling and visible, so return a generic 'active' status.
        return constants.PKG_STATUS_MOVING

    def __update_moving_state(self) -> int:
        """Handles the package's logic while it is on a conveyor."""
        speed = self.current_conveyor.speed
        direction = self.current_conveyor.direction
        self.direction = direction
        self.__move_package_horizontally(speed, direction)
        if self.__check_if_reached_conveyor_end(direction):
            return constants.PKG_STATUS_REACHED_END
        return constants.PKG_STATUS_MOVING

    def __move_package_horizontally(self, speed: float, direction: int):
        """
        Moves the package along the conveyor. Levels up when it crosses center screen.
        :param speed: The speed to move at.
        :param direction: The direction to move in (-1 or 1).
        """
        # It has to check both the previous and new x so that it just levels up once when it crosses center
        prev_x = self.x
        self.x += speed * direction
        trigger_x = constants.CENTER_SCREEN
        if (direction == -1 and prev_x > trigger_x and self.x <= trigger_x) or (direction == 1 and prev_x < trigger_x and self.x >= trigger_x):
            self.level_index += 1

    def __check_if_reached_conveyor_end(self, direction: int) -> bool:
        """
        Checks if the package has reached the end of its conveyor.
        :param direction: The direction the package is moving.
        """
        if direction == 1: # Moving right
            return self.x + self.width >= self.current_conveyor.end_x + constants.OVERHANG_LIMIT
        else: # Moving left
            return self.x <= self.current_conveyor.x - constants.OVERHANG_LIMIT

    def draw(self):
        """Draws the package on the screen."""
        # Multiply by 2 because each level has two sprites (normal and falling)
        sprite_idx = self.level_index * 2
        if self.state == constants.PKG_STATE_FALLING:
            sprite_idx += 1 
        sprite = self.sprites[sprite_idx]
        img, u, v, w, h, colkey = sprite
        if self.state == constants.PKG_STATE_FALLING and self.direction == 1:
            w = -w  # Flip sprite when the package falls and is moving right
        pyxel.blt(int(self.x), int(self.y), img, u, v, w, h, colkey)