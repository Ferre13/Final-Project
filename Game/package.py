import pyxel
import constants
from conveyor import Conveyor 

class Package:
    """
    Represents a package in the factory. It manages its own state (moving, falling),
    position, and visual appearance. Its update method returns a status code
    to the PackageLogic handler to signal important events.
    """
    def __init__(self, difficulty: str, start_conveyor: Conveyor, floor_index: int):
        """
        Initializes a package on a starting conveyor.

        :param difficulty: The current game difficulty.
        :param start_conveyor: The Conveyor object where the package will spawn.
        :param floor_index: The numerical index of the floor the package is on.
        """
        self.__difficulty = difficulty
        self.current_conveyor = start_conveyor
        self.floor_index = floor_index
        
        # Set initial position based on the conveyor's direction.
        # This ensures the package spawns at the "start" of the belt.
        if self.current_conveyor.direction == 1:
             self.x = self.current_conveyor.x
        else:
             self.x = self.current_conveyor.end_x - 10 
             
        self.y = self.current_conveyor.y - self.height
        
        self.state = constants.PKG_STATE_MOVING
        self.level_index = 0  # Used to determine which package sprite to show

    @property
    def x(self) -> float: return self.__x
    @x.setter
    def x(self, value: float): self.__x = float(value)

    @property
    def y(self) -> float: return self.__y
    @y.setter
    def y(self, value: float): self.__y = float(value)

    @property
    def width(self) -> int:
        """Returns the width of the package's sprite."""
        # Assumes all package sprites have a similar base width.
        return constants.PCK_LVL1[3]

    @property
    def height(self) -> int:
        """Returns the height of the package's sprite."""
        # Assumes all package sprites have a similar base height.
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
        if self.__difficulty == "EASY": return constants.PCK_EASY_SPRITES
        elif self.__difficulty == "MEDIUM": return constants.PCK_MEDIUM_SPRITES
        elif self.__difficulty == "EXTREME": return constants.PCK_EXTREME_SPRITES
        elif self.__difficulty == "CRAZY": return constants.PCK_CRAZY_SPRITES
        return constants.PCK_EASY_SPRITES

    def advance_to_conveyor(self, next_conveyor: Conveyor):
        """
        Moves the package to the next conveyor belt.

        :param next_conveyor: The conveyor object to move to.
        """
        self.current_conveyor = next_conveyor
        self.floor_index += 1
        
        # Position the package slightly over the edge to make the transition look smooth.
        if self.current_conveyor.direction == 1: 
            self.x = self.current_conveyor.x - constants.OVERHANG_LIMIT
        else: 
            self.x = self.current_conveyor.end_x + constants.OVERHANG_LIMIT - self.width

        self.y = self.current_conveyor.y - self.height
        self.state = constants.PKG_STATE_MOVING

    def fall(self):
        """Puts the package into the 'falling' state."""
        self.state = constants.PKG_STATE_FALLING

    def update(self) -> int:
        """
        Updates the package's state and position.
        
        :return: A status code (from constants) to inform the PackageLogic handler
                 of what action to take (e.g., package reached end, package fell).
        """
        # --- State 1: FALLING ---
        if self.state == constants.PKG_STATE_FALLING:
            self.y += constants.PACKAGE_FALL_SPEED
            
            # If the package is off the bottom of the screen, determine who is to blame.
            if self.y > constants.SCREEN_HEIGHT:
                # Blame is based on which character's "territory" the package was in.
                # Mario handles even floors (0, 2, ...), Luigi handles odd floors (1, 3, ...).
                if self.floor_index % 2 == 0:
                    return constants.PKG_STATUS_FALLEN_MARIO
                else:
                    return constants.PKG_STATUS_FALLEN_LUIGI
            return constants.PKG_STATUS_MOVING # Still falling, no special action needed yet.

        # --- State 2: MOVING ---
        elif self.state == constants.PKG_STATE_MOVING:
            speed = self.current_conveyor.speed
            direction = self.current_conveyor.direction
            
            prev_x = self.x
            self.x += speed * direction

            # Change the package's visual appearance (level) as it crosses the center.
            trigger_x = constants.CENTER_SCREEN
            if (direction == -1 and prev_x > trigger_x and self.x <= trigger_x) or \
               (direction == 1 and prev_x < trigger_x and self.x >= trigger_x):
                self.level_index += 1

            # Check if the package has reached the end of the conveyor.
            reached_end = False
            if direction == 1: # Moving right
                limit = self.current_conveyor.end_x + constants.OVERHANG_LIMIT
                if self.x + self.width >= limit:
                    self.x = limit - self.width 
                    reached_end = True
            else: # Moving left
                limit = self.current_conveyor.x - constants.OVERHANG_LIMIT
                if self.x <= limit:
                    self.x = limit 
                    reached_end = True
            
            if reached_end:
                return constants.PKG_STATUS_REACHED_END
            
            return constants.PKG_STATUS_MOVING # Still moving, no special action needed.

    def draw(self):
        """Draws the package with the correct sprite based on its level and state."""
        # Each "level" of a package has two sprites: normal and falling.
        # We find the base index for the current level.
        sprite_idx = self.level_index * 2
        
        # Ensure we don't go out of bounds of the sprite list.
        if sprite_idx >= len(self.__sprite_list): 
            sprite_idx = len(self.__sprite_list) - 2
        
        # If the package is falling, use the second sprite for the current level.
        if self.state == constants.PKG_STATE_FALLING:
             sprite_idx += 1 
             
        sprite = self.__sprite_list[sprite_idx]
        img, u, v, w, h, colkey = sprite
        pyxel.blt(int(self.x), int(self.y), img, u, v, w, h, colkey)