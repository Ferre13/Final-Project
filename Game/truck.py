import pyxel
import constants

class Truck:
    def __init__(self, x: int = constants.TRUCK_X, y: int = 0):
        self.x = x
        self.y = y
        self.packages_count = 0
        self.is_leaving = False
        
        self.__sprites = constants.TRUCK_SPRITES
        
        # Read-Only attributes (Private with __)
        self.__width = 32
        self.__height = 16

    # ... [Keep x and y properties] ...
    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int): raise TypeError("x must be integer")
        self.__x = x

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int): raise TypeError("y must be integer")
        self.__y = y

    # --- NEW: Read-Only Properties (No Setters) ---
    @property
    def width(self) -> int:
        """ The width is fixed and cannot be changed. """
        return self.__width

    @property
    def height(self) -> int:
        """ The height is fixed and cannot be changed. """
        return self.__height

    def receive_package(self):
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