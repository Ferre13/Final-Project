import pyxel
import constants
from game_object import GameObject

class Truck(GameObject):
    """Represents the delivery truck, which drives away when full."""
    def __init__(self, x: float = constants.TRUCK_X, y: float = 0):
        """
        Initializes the truck.
        :param x: The starting x-coordinate.
        :param y: The starting y-coordinate.
        """
        super().__init__(x, y)
        self.packages_count = 0
        self.is_delivering = False
        self.__sprites = constants.TRUCK_SPRITES
        self.__phase = 0
        self.__event_start_frame = 0

    # Read-only properties for truck dimensions
    @property
    def width(self) -> int:
        """The width of the truck's sprite."""
        return constants.TRUCK_1[3]
    @property
    def height(self) -> int:
        """The height of the truck's sprite."""
        return constants.TRUCK_1[4]

    @property
    def packages_count(self) -> int:
        """The number of packages currently in the truck."""
        return self.__packages_count
    @packages_count.setter
    def packages_count(self, value: int):
        if not isinstance(value, int): 
            raise TypeError("Count must be an integer")
        self.__packages_count = value

    @property
    def is_delivering(self) -> bool:
        """True if the truck is currently in its delivery animation sequence."""
        return self.__is_delivering
    @is_delivering.setter
    def is_delivering(self, value: bool):
        if not isinstance(value, bool): 
            raise TypeError("Must be a boolean")
        self.__is_delivering = value

    def receive_package(self) -> bool:
        """
        Adds a package to the truck. Returns True if the truck is now full and starts delivery.
        """
        if self.packages_count < constants.TRUCK_MAX_CAPACITY:
            self.packages_count += 1
            
        if self.packages_count == constants.TRUCK_MAX_CAPACITY:
            self.start_delivery()
            return True
        return False

    def start_delivery(self):
        """Starts the delivery animation sequence."""
        self.is_delivering = True  
        self.__phase = 0
        self.__event_start_frame = pyxel.frame_count

    def reset(self):
        """Resets the truck to its default state and position."""
        self.x = constants.TRUCK_X
        self.packages_count = 0
        self.is_delivering = False

    def update(self):
        """Updates the truck's delivery animation state machine."""
        # If not delivering, no update needed
        if not self.is_delivering: 
            return
        
        if self.__phase == 0:
            self.__update_phase_0_wait()
        elif self.__phase == 1:
            self.__update_phase_1_drive_off()
        elif self.__phase == 2:
            self.__update_phase_2_wait_offscreen()
        elif self.__phase == 3:
            self.__update_phase_3_drive_back()

    def __update_phase_0_wait(self):
        """Initial waiting phase before the truck drives off."""
        if pyxel.frame_count >= self.__event_start_frame + constants.TRUCK_WAIT_TIME:
            self.__phase = 1

    def __update_phase_1_drive_off(self):
        """Handles the truck driving off the screen."""
        self.x -= constants.TRUCK_SPEED
        if self.x < -self.width:
            self.__phase = 2
            self.__event_start_frame = pyxel.frame_count
            self.packages_count = 0

    def __update_phase_2_wait_offscreen(self):
        """Handles the truck waiting while off-screen."""
        if pyxel.frame_count >= self.__event_start_frame + constants.TRUCK_OFFSCREEN_TIME:
            self.__phase = 3
            self.x = -self.width

    def __update_phase_3_drive_back(self):
        """Handles the truck driving back to its starting position."""
        self.x += constants.TRUCK_SPEED
        if self.x >= constants.TRUCK_X:
            self.x = constants.TRUCK_X
            self.is_delivering = False

    def draw(self):
        """Draws the truck sprite based on how full it is."""
        if self.is_delivering and self.packages_count > 0:
            pyxel.blt(int(self.x), int(self.y), *constants.TRUCK_FULL)
        else:
            idx = min(self.packages_count, len(self.__sprites) - 1)
            pyxel.blt(int(self.x), int(self.y), *self.__sprites[idx])