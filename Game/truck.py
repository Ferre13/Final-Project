import pyxel
import constants

class Truck:
    def __init__(self, x: int = constants.TRUCK_X, y: int = 0):
        self.x = x
        self.y = y
        self.packages_count = 0
        self.is_leaving = False
        self.departure_timer = 0

        # Private attributes, so that they are not modified directly
        self.__sprites = constants.TRUCK_SPRITES
        self.__width = 32
        self.__height = 16

    @property
    def x(self) -> int: 
        return self.__x
    @x.setter
    def x(self, x):
        if not isinstance(x, (int, float)): 
            raise TypeError("x must be a number")
        self.__x = x

    @property
    def y(self) -> int: 
        return self.__y
    @y.setter
    def y(self, y):
        if not isinstance(y, (int, float)): 
            raise TypeError("y must be a number")
        self.__y = y

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def receive_package(self):
        if self.packages_count < 8:
            self.packages_count += 1
            if self.packages_count == 8:
                self.departure_timer = 60
                self.is_leaving = False

    def update(self):
        if self.packages_count == 8 and self.departure_timer > 0:
            self.departure_timer -= 1
            # Once timer hits 0, we allow the truck to move
            if self.departure_timer == 0:
                self.is_leaving = True

        if self.is_leaving:
            self.x -= 1  # Truck speed when leaving

    def reset(self):
        self.x = constants.TRUCK_X
        self.packages_count = 0
        self.is_leaving = False
        self.departure_timer = 0

    def draw(self):
        # Casting to int for drawing
        if self.packages_count == 8:
            if self.departure_timer > 15:
                 pyxel.blt(int(self.x), int(self.y), *self.__sprites[8])
            else:
                 pyxel.blt(int(self.x), int(self.y), *constants.TRUCK_FULL)
        else:
            pyxel.blt(int(self.x), int(self.y), *self.__sprites[self.packages_count])