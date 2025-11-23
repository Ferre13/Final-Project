import pyxel
import constants

class ExitSignal:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("y must be an integer")
        self.__y = y

    def draw(self):
        pyxel.blt(self.x, self.y, *constants.EXIT_SIGNAL_SPRITE)

class Machine:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("y must be an integer")
        self.__y = y

    def draw(self):
        pyxel.blt(self.x, self.y, *constants.MACHINE_SPRITE)

class VerticalStructure:
    def __init__(self, x: int, width: int):
        self.x = x
        self.width = width
        # Changed to SCREEN_HEIGHT to start from the absolute bottom
        self.base_y = constants.SCREEN_HEIGHT 

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        self.__x = x

    @property
    def width(self) -> int:
        return self.__width
    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        self.__width = width

    def draw(self):
        sprite_width = constants.VERTICAL_STRUCTURE_SPRITE[3]
        sprite_height = constants.VERTICAL_STRUCTURE_SPRITE[4]
        
        num_rows = (self.base_y // sprite_height)

        for each in range(num_rows):
            y_pos = self.base_y - ((each + 1) * sprite_height)
            
            for structure in range(self.width):
                x_pos = self.x + structure * sprite_width
                pyxel.blt(x_pos, y_pos, *constants.VERTICAL_STRUCTURE_SPRITE)