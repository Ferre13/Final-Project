import pyxel
import constants

class ExitSignal:
    """
    Represents the exit signal that appears when the truck is full.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the exit signal.
        :param x: The x-coordinate of the exit signal.
        :param y: The y-coordinate of the exit signal.
        """
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        """ Getter for x coordinate """
        return self.__x
    @x.setter
    def x(self, x: int):
        """ Setter for x coordinate """
        if not isinstance(x, int):
            raise TypeError("The x coordinate must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        """ Getter for y coordinate """
        return self.__y
    @y.setter
    def y(self, y: int):
        """ Setter for y coordinate """
        if not isinstance(y, int):
            raise TypeError("The y coordinate must be an integer")
        self.__y = y

    def draw(self):
        """
        Draws the exit signal on the screen.
        """
        pyxel.blt(self.x, self.y, *constants.EXIT_SIGNAL_SPRITE)

class Machine:
    """
    Represents a machine in the factory.
    """

    def __init__(self, x: int, y: int):
        """
        Initializes the machine.
        :param x: The x-coordinate of the machine.
        :param y: The y-coordinate of the machine.
        """
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        """ Getter for x coordinate """
        return self.__x
    @x.setter
    def x(self, x: int):
        """ Setter for x coordinate """
        if not isinstance(x, int):
            raise TypeError("The x coordinate must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        """ Getter for y coordinate """
        return self.__y
    @y.setter
    def y(self, y: int):
        """ Setter for y coordinate """
        if not isinstance(y, int):
            raise TypeError("The y coordinate must be an integer")
        self.__y = y

    def draw(self):
        """
        Draws the machine on the screen.
        """
        pyxel.blt(self.x, self.y, *constants.MACHINE_SPRITE)

class VerticalStructure:
    def __init__(self, x: int, width: int):
        self.x = x
        self.width = width
        self.base_y = constants.SCREEN_HEIGHT - 20 

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("The x coordinate must be an integer")
        self.__x = x

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("The width must be an integer")
        self.__width = width

    def draw(self):
        sprite_width = constants.VERTICAL_STRUCTURE_SPRITE[3]
        sprite_height = constants.VERTICAL_STRUCTURE_SPRITE[4]
        num_rows = (self.base_y // sprite_height)

        for each in range(num_rows):
            y_pos = self.base_y - (each + 1 * sprite_height)
            
            for structure in range(self.width):
                x_pos = self.x + structure * sprite_width
                pyxel.blt(x_pos, y_pos, *constants.VERTICAL_STRUCTURE_SPRITE)