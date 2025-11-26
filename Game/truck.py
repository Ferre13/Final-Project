import pyxel
import constants

class Truck:
    def __init__(self, x: int = constants.TRUCK_X, y: int = 0):
        self.x = x
        self.y = y
        self.packages_count = 0
        
        # Simple flag for the sprite (controlled by Board)
        self.is_closed = False
        
        self.__sprites = constants.TRUCK_SPRITES
        self.__width = 32
        self.__height = 16

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, x):
        if not isinstance(x, (int, float)): raise TypeError("x must be a number")
        self.__x = x

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, y):
        if not isinstance(y, (int, float)): raise TypeError("y must be a number")
        self.__y = y

    @property
    def width(self) -> int: return self.__width
    @property
    def height(self) -> int: return self.__height

    def receive_package(self):
        if self.packages_count < 8:
            self.packages_count += 1

    def update(self):
        # No internal logic needed. Board controls x.
        pass

    def empty_cargo(self):
        """ Resets cargo but keeps position (used when off-screen) """
        self.packages_count = 0
        self.is_closed = False

    def reset(self):
        """ Full reset to start position """
        self.x = constants.TRUCK_X
        self.packages_count = 0
        self.is_closed = False

    def draw(self):
        if self.packages_count == 8:
            # Board controls this flag to switch sprites
            if self.is_closed:
                pyxel.blt(int(self.x), int(self.y), *constants.TRUCK_FULL)
            else:
                pyxel.blt(int(self.x), int(self.y), *self.__sprites[8])
        else:
            pyxel.blt(int(self.x), int(self.y), *self.__sprites[self.packages_count])