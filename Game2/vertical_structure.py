import pyxel
import constants
from game_object import GameObject

class VerticalStructure(GameObject):
    """The central vertical beam structure of the factory."""
    def __init__(self, x: int, width: int, top_limit_y: int, base_y: int):
        """
        Initializes the vertical structure.

        :param x: The starting x-coordinate.
        :param width: The width in number of sprite tiles.
        :param top_limit_y: The highest y-coordinate the structure should reach.
        :param base_y: The lowest y-coordinate where drawing should start.
        """
        super().__init__(x, base_y) 
        self.width = width
        self.top_limit_y = top_limit_y
        self.base_y = base_y

    @property
    def width(self) -> int: return self.__width
    @width.setter
    def width(self, value: int):
        if not isinstance(value, int): raise TypeError("width must be an integer")
        self.__width = value

    @property
    def top_limit_y(self) -> int: return self.__top_limit_y
    @top_limit_y.setter
    def top_limit_y(self, value: int):
        if not isinstance(value, int): raise TypeError("top_limit_y must be an integer")
        self.__top_limit_y = value

    @property
    def base_y(self) -> int: return self.__base_y
    @base_y.setter
    def base_y(self, value: int):
        if not isinstance(value, int): raise TypeError("base_y must be an integer")
        self.__base_y = value

    def draw(self):
        """Draws the structure by tiling sprites vertically and horizontally."""
        img, u, v, w, h, colkey = constants.VERTICAL_STRUCTURE_SPRITE
        current_y = self.base_y
        
        # Draw segments upwards from the base until the top limit is reached.
        while current_y > self.top_limit_y:
            current_y -= h
            for i in range(self.width):
                x_pos = self.x + (i * w)
                
                # Flip the sprite on alternating columns to create a symmetric pattern.
                if i % 2 != 0:
                    draw_w = -w
                else:
                    draw_w = w
                
                pyxel.blt(x_pos, current_y, img, u, v, draw_w, h, colkey)