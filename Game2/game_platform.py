import pyxel
import constants
from game_object import GameObject

class Platform(GameObject):
    """
    Represents the platforms where characters stand, truck parks, boss appears...
    It is also used for the conveyor, since they are treated as platforms (using inheritance)
    """
    def __init__(self, x: int, y: int, width: int, sprite = constants.PLATFORM_SPRITE):
        """
        :param x: The starting x-coordinate of the platform.
        :param y: The y-coordinate of the platform.
        :param width: The number of times the sprite is repeated to form the platform's width.
        :param sprite: The sprite tuple to use for drawing. Defaults to the standard platform sprite.
        """
        super().__init__(x, y) # Inherit x and y from GameObject
        self.width = width
        self.sprite = sprite

    @property
    def width(self) -> int: 
        return self.__width
    @width.setter
    def width(self, width: int):
        """Sets the width of the platform in sprite tiles."""
        if not isinstance(width, int): 
            raise TypeError("width must be an integer")
        if width < 1: 
            raise ValueError("Width must be at least 1")
        self.__width = width

    def draw(self):
        """
        Draws the platform by tiling its sprite horizontally to match its width.
        """
        # Get the width of a single sprite tile from the sprite tuple
        sprite_width = self.sprite[3]
        
        # Draw the sprite repeatedly to create the full platform length
        for sprite in range(self.width):
            # Calculate the x position for the current platform segment
            x_position = self.x + (sprite * sprite_width)
            pyxel.blt(x_position, self.y, *self.sprite)