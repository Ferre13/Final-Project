import pyxel
import constants

class Truck:
    """
    Represents the delivery truck. 
    Strict encapsulation and centralized constants.
    """
    def __init__(self, x: int = constants.TRUCK_X, y: int = 0):
        self.x = x
        self.y = y
        self.packages_count = 0
        self.is_delivering = False
        
        self.__sprites = constants.TRUCK_SPRITES
        self.__width = constants.TRUCK_1[3]
        self.__height = constants.TRUCK_1[4]
        
        self.__phase = 0 
        self.__timer = 0

    # --- GETTERS AND SETTERS ---
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
        if not isinstance(value, int): raise TypeError("Count must be int")
        self.__packages_count = value

    @property
    def is_delivering(self) -> bool: return self.__is_delivering
    @is_delivering.setter
    def is_delivering(self, value: bool):
        if not isinstance(value, bool): raise TypeError("Must be bool")
        self.__is_delivering = value

    # --- LOGIC ---
    def receive_package(self):
        if self.packages_count < constants.TRUCK_MAX_CAPACITY:
            self.packages_count += 1
            
        if self.packages_count == constants.TRUCK_MAX_CAPACITY:
            self.start_delivery()

    def start_delivery(self):
        self.is_delivering = True  
        self.__phase = 0
        self.__timer = constants.TRUCK_WAIT_TIME

    def reset(self):
        self.x = constants.TRUCK_X
        self.packages_count = 0
        self.is_delivering = False

    def update(self):
        if not self.is_delivering: return

        # PHASE 0: Wait
        if self.__phase == 0:
            self.__timer -= 1
            if self.__timer <= 0: self.__phase = 1

        # PHASE 1: Drive Left
        elif self.__phase == 1:
            self.x -= constants.TRUCK_SPEED
            if self.x < -self.width:
                self.__phase = 2
                self.__timer = constants.TRUCK_OFFSCREEN_TIME
                self.packages_count = 0

        # PHASE 2: Wait Off-screen
        elif self.__phase == 2:
            self.__timer -= 1
            if self.__timer <= 0:
                self.__phase = 3
                self.x = -self.width

        # PHASE 3: Drive Back
        elif self.__phase == 3:
            self.x += constants.TRUCK_SPEED
            if self.x >= constants.TRUCK_X:
                self.x = constants.TRUCK_X
                self.is_delivering = False 

    def draw(self):
        if self.is_delivering and self.packages_count > 0:
             pyxel.blt(int(self.x), int(self.y), *constants.TRUCK_FULL)
        else:
             idx = min(self.packages_count, len(self.__sprites) - 1)
             pyxel.blt(int(self.x), int(self.y), *self.__sprites[idx])