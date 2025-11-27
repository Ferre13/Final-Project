import pyxel
import constants

class Platform:
    """
    Represents a static platform in the game world.
    A platform is a horizontal surface composed of one or more repeating sprite tiles.
    """
    def __init__(self, x: int, y: int, width: int, sprite=constants.PLATFORM_SPRITE):
        """
        Initializes a platform.

        :param x: The starting x-coordinate of the platform.
        :param y: The y-coordinate of the platform.
        :param width: The number of sprite tiles the platform is wide.
        :param sprite: The sprite tuple to use for drawing. Defaults to the standard platform sprite.
        """
        self.x = x
        self.y = y
        self.width = width
        self.sprite = sprite

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, x: int):
        """Sets the x-coordinate of the platform."""
        if not isinstance(x, (int, float)): raise TypeError("x must be a number")
        self.__x = int(x)

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, y: int):
        """Sets the y-coordinate of the platform."""
        if not isinstance(y, (int, float)): raise TypeError("y must be a number")
        self.__y = int(y)

    @property
    def width(self) -> int: return self.__width
    @width.setter
    def width(self, width: int):
        """Sets the width of the platform in sprite tiles."""
        if not isinstance(width, int): raise TypeError("width must be an integer")
        if width < 1: raise ValueError("Width must be at least 1")
        self.__width = width

    def draw(self):
        """
        Draws the platform by tiling its sprite horizontally to match its width.
        """
        # Get the width of a single sprite tile from the sprite tuple.
        sprite_width = self.sprite[3]
        
        # Draw the sprite repeatedly to create the full platform length.
        for i in range(self.width):
            # Calculate the x position for the current tile.
            x_position = self.x + (i * sprite_width)
            pyxel.blt(x_position, self.y, *self.sprite)