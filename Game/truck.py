import pyxel
import constants

class Truck:
    def __init__(self, x: int = constants.TRUCK_X, y: int = 0):
        self.x = x
        self.y = y
        self.packages_count = 0
        self.is_leaving = False
        
        self.__sprites = constants.TRUCK_SPRITES
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("The x coordinate must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("The y coordinate must be an integer")
        self.__y = y

    @property
    def packages_count(self) -> int:
        return self.__packages_count

    @packages_count.setter
    def packages_count(self, value: int):
        if not isinstance(value, int):
            raise TypeError("The packages_count must be an integer")
        self.__packages_count = value
    
    @property
    def is_leaving(self) -> bool:
        return self.__is_leaving

    @is_leaving.setter
    def is_leaving(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("The is_leaving must be a boolean")
        self.__is_leaving = value

    def add_package(self):
        if self.packages_count < 8:
            self.packages_count += 1
            if self.packages_count == 8:
                self.is_leaving = True

    def update(self):
        if self.is_leaving:
            self.x -= 2

    def reset(self):
        self.x = constants.TRUCK_X
        self.packages_count = 0
        self.is_leaving = False

    def draw(self):
        if self.packages_count == 8:
            pyxel.blt(self.x, self.y, *constants.TRUCK_FULL)
        else:
            pyxel.blt(self.x, self.y, *self.__sprites[self.packages_count])