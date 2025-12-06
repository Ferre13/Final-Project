import pyxel
import constants
import random
from game_object import GameObject
from conveyor import Conveyor 

class Package(GameObject):
    """
    Represents a package in the factory. It manages its own state (moving, falling),
    position, and visual appearance. Its update method returns a status code
    to the PackageManager to signal important events.
    """
    def __init__(self, difficulty: str, start_conveyor: Conveyor, floor_index: int):
        """
        Initializes a package on a starting conveyor.

        :param difficulty: The current game difficulty.
        :param start_conveyor: The Conveyor object where the package will spawn.
        :param floor_index: The numerical index of the floor the package is on.
        """
        super().__init__(0.0, 0.0) # x and y will be set below
        self.__difficulty = difficulty
        self.current_conveyor = start_conveyor
        self.floor_index = floor_index
        
        # Set initial position based on the conveyor's direction.
        if self.current_conveyor.direction == 1:
             self.x = self.current_conveyor.x
        else:
             self.x = self.current_conveyor.end_x - 10 
             
        self.y = self.current_conveyor.y - self.height
        
        self.state = constants.PKG_STATE_MOVING
        self.level_index = 0
        self.last_direction = self.current_conveyor.direction

    @property
    def width(self) -> int:
        """Returns the width of the package's sprite."""
        return constants.PCK_LVL1[3]

    @property
    def height(self) -> int:
        """Returns the height of the package's sprite."""
        return constants.PCK_LVL1[4]

    @property
    def floor_index(self) -> int: return self.__floor_index
    @floor_index.setter
    def floor_index(self, value: int):
        if not isinstance(value, int): raise TypeError("Floor index must be an integer")
        self.__floor_index = value

    @property
    def current_conveyor(self) -> Conveyor: return self.__current_conveyor
    @current_conveyor.setter
    def current_conveyor(self, value: Conveyor):
        if not isinstance(value, Conveyor): raise TypeError("Must be a Conveyor object")
        self.__current_conveyor = value

    @property
    def __sprite_list(self) -> list:
        """Returns the appropriate list of package sprites based on difficulty."""
        return constants.DIFFICULTY_SPRITES.get(self.__difficulty, constants.PCK_EASY_SPRITES)

    def advance_to_conveyor(self, next_conveyor: Conveyor):
        """
        Moves the package to the next conveyor belt.

        :param next_conveyor: The conveyor object to move to.
        """
        self.current_conveyor = next_conveyor
        self.floor_index += 1
        
        if self.current_conveyor.direction == 1: # Moving right
            self.x = self.current_conveyor.x - constants.OVERHANG_LIMIT
        else: # Moving left
            self.x = self.current_conveyor.end_x + constants.OVERHANG_LIMIT - self.width

        self.y = self.current_conveyor.y - self.height
        self.state = constants.PKG_STATE_MOVING

    def fall(self):
        """Puts the package into the 'falling' state."""
        self.state = constants.PKG_STATE_FALLING

    def update(self) -> int:
        """
        Updates the package's state and position.
        
        :return: A status code to inform the PackageManager of what action to take.
        """
        if self.state == constants.PKG_STATE_FALLING:
            return self._update_falling_state()
        elif self.state == constants.PKG_STATE_MOVING:
            return self._update_moving_state()
        return constants.PKG_STATUS_MOVING # Default return if state is unknown or static

    def _update_falling_state(self) -> int:
        """Handles the logic when the package is in the 'falling' state."""
        self.y += constants.PACKAGE_FALL_SPEED
        if self.y > constants.SCREEN_HEIGHT:
            if self.floor_index % 2 == 0:
                return constants.PKG_STATUS_FALLEN_MARIO
            else:
                return constants.PKG_STATUS_FALLEN_LUIGI
        return constants.PKG_STATUS_MOVING

    def _update_moving_state(self) -> int:
        """Handles the logic when the package is in the 'moving' state."""
        speed = self.current_conveyor.speed
        direction = self.current_conveyor.direction
        self.last_direction = direction
        
        self._move_package_horizontally(speed, direction)
        
        if self._check_if_reached_conveyor_end(direction):
            return constants.PKG_STATUS_REACHED_END
        
        return constants.PKG_STATUS_MOVING

    def _move_package_horizontally(self, speed: float, direction: int):
        """Updates the package's x-position and level index based on movement."""
        prev_x = self.x
        self.x += speed * direction

        trigger_x = constants.CENTER_SCREEN
        if (direction == -1 and prev_x > trigger_x and self.x <= trigger_x) or \
           (direction == 1 and prev_x < trigger_x and self.x >= trigger_x):
            self.level_index += 1

    def _check_if_reached_conveyor_end(self, direction: int) -> bool:
        """Checks if the package has reached the end of the current conveyor."""
        if direction == 1: # Moving right
            return self.x + self.width >= self.current_conveyor.end_x + constants.OVERHANG_LIMIT
        else: # Moving left
            return self.x <= self.current_conveyor.x - constants.OVERHANG_LIMIT

    def draw(self):
        """Draws the package with the correct sprite based on its level and state."""
        sprite_idx = self.level_index * 2
        
        if sprite_idx >= len(self.__sprite_list):
            sprite_idx = len(self.__sprite_list) - 2
        
        if self.state == constants.PKG_STATE_FALLING:
             sprite_idx += 1 
             
        sprite = self.__sprite_list[sprite_idx]
        img, u, v, w, h, colkey = sprite

        # If falling and moving right, flip the sprite
        if self.state == constants.PKG_STATE_FALLING and self.last_direction == 1:
            w = -w

        pyxel.blt(int(self.x), int(self.y), img, u, v, w, h, colkey)
