import pyxel
import constants

class Platform:
    """
    This class represents the platforms for the characters to stand on.
    """
    def __init__(self, x: int, y: int, width: int):
        """
        This is the magic method we must use to declare the attributes of our objects.
        :param x: The x-coordinate of the platform.
        :param y: The y-coordinate of the platform.
        :param width: The width of the platform in number of sprites.
        """
        self.x = x
        self.y = y
        self.width = width

    @property
    def x(self) -> int:
        """ This is the getter method for the x attribute """
        return self.__x
    @x.setter
    def x(self, x: int):
        """ This is the setter method for the x attribute """
        if not isinstance(x, int):
            raise TypeError("The x coordinate must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        """ This is the getter method for the y attribute """
        return self.__y
    @y.setter
    def y(self, y: int):
        """ This is the setter method for the y attribute """
        if not isinstance(y, int):
            raise TypeError("The y coordinate must be an integer")
        self.__y = y

    @property
    def width(self) -> int:
        """ This is the getter method for the width attribute """
        return self.__width
    @width.setter
    def width(self, width: int):
        """ This is the setter method for the width attribute """
        if not isinstance(width, int):
            raise TypeError("The width must be an integer")
        self.__width = width

    def draw(self):
        """
        Draws the platform on the screen.
        """
        sprite_width = constants.PLATFORM_SPRITE[3]
        for platform in range(self.width):
            pyxel.blt(self.x + platform * sprite_width, self.y, *constants.PLATFORM_SPRITE)