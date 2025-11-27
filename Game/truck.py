import pyxel
import constants

class Truck:
    """
    Represents the delivery truck, which manages its own state machine for the
    package delivery sequence.
    """
    def __init__(self, x: int = constants.TRUCK_X, y: int = 0):
        """
        Initializes the truck at a given position.
        
        :param x: The initial x-coordinate.
        :param y: The initial y-coordinate.
        """
        self.x = x
        self.y = y
        self.packages_count = 0
        self.is_delivering = False
        
        self.__sprites = constants.TRUCK_SPRITES
        self.__width = constants.TRUCK_1[3]
        self.__height = constants.TRUCK_1[4]
        
        # Internal state machine for the delivery animation
        self.__phase = 0 
        self.__timer = 0

    @property
    def x(self) -> float: return self.__x
    @x.setter
    def x(self, x): self.__x = float(x)

    @property
    def y(self) -> float: return self.__y
    @y.setter
    def y(self, y): self.__y = float(y)

    @property
    def width(self) -> int: return self.__width
    @property
    def height(self) -> int: return self.__height

    @property
    def packages_count(self) -> int: return self.__packages_count
    @packages_count.setter
    def packages_count(self, value: int):
        if not isinstance(value, int): raise TypeError("Count must be an integer")
        self.__packages_count = value

    @property
    def is_delivering(self) -> bool: return self.__is_delivering
    @is_delivering.setter
    def is_delivering(self, value: bool):
        if not isinstance(value, bool): raise TypeError("Must be a boolean")
        self.__is_delivering = value

    def receive_package(self) -> bool:
        """
        Adds a package to the truck's count. If the truck becomes full,
        it automatically starts the delivery sequence.

        :return: True if the delivery sequence is starting, False otherwise.
        """
        if self.packages_count < constants.TRUCK_MAX_CAPACITY:
            self.packages_count += 1
            
        if self.packages_count == constants.TRUCK_MAX_CAPACITY:
            self.start_delivery()
            return True
        return False

    def start_delivery(self):
        """Kicks off the delivery animation sequence."""
        self.is_delivering = True  
        self.__phase = 0
        self.__timer = constants.TRUCK_WAIT_TIME

    def reset(self):
        """Resets the truck to its initial state and position."""
        self.x = constants.TRUCK_X
        self.packages_count = 0
        self.is_delivering = False

    def update(self):
        """
        Updates the truck's state machine for the delivery animation.
        This method only runs if `is_delivering` is True.
        """
        if not self.is_delivering: 
            return

        # Phase 0: A brief wait before the truck starts moving.
        if self.__phase == 0:
            self.__timer -= 1
            if self.__timer <= 0: 
                self.__phase = 1

        # Phase 1: Drive off the screen to the left.
        elif self.__phase == 1:
            self.x -= constants.TRUCK_SPEED
            if self.x < -self.width:
                self.__phase = 2
                self.__timer = constants.TRUCK_OFFSCREEN_TIME
                self.packages_count = 0  # Unload packages while off-screen

        # Phase 2: Wait for a short time while off-screen.
        elif self.__phase == 2:
            self.__timer -= 1
            if self.__timer <= 0:
                self.__phase = 3
                self.x = -self.width

        # Phase 3: Drive back to the starting position from the left.
        elif self.__phase == 3:
            self.x += constants.TRUCK_SPEED
            if self.x >= constants.TRUCK_X:
                self.x = constants.TRUCK_X
                self.is_delivering = False # End of delivery sequence

    def draw(self):
        """Draws the truck, choosing the sprite based on its fullness."""
        # If the truck is full and driving away, show the "full" sprite.
        if self.is_delivering and self.packages_count > 0:
             pyxel.blt(int(self.x), int(self.y), *constants.TRUCK_FULL)
        # Otherwise, show the sprite corresponding to the number of packages it holds.
        else:
             idx = min(self.packages_count, len(self.__sprites) - 1)
             pyxel.blt(int(self.x), int(self.y), *self.__sprites[idx])