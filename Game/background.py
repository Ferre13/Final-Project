import pyxel
import constants

class GameObject:
    """
    A parent class for all static, non-interactive game objects.
    It provides base `x` and `y` properties.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value):
        if not isinstance(value, (int, float)): raise TypeError("x must be a number")
        self.__x = int(value)

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, value):
        if not isinstance(value, (int, float)): raise TypeError("y must be a number")
        self.__y = int(value)

class ExitSignal(GameObject):
    """A decorative 'EXIT' sign, usually placed near the truck."""
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.EXIT_SIGNAL_SPRITE)

class Machine(GameObject):
    """The large machine on the right side of the screen where packages originate."""
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.MACHINE_SPRITE)

class Window(GameObject):
    """A decorative window for the factory background."""
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.WINDOW_SPRITE)

class LevelSign(GameObject):
    """A sign in the bottom-left that displays the current difficulty."""
    def __init__(self, difficulty: str, x: int, y: int):
        super().__init__(x, y)
        self.difficulty = difficulty

    @property
    def __sprite(self):
        """Selects the correct sprite based on the difficulty string."""
        if self.difficulty == "EASY": return constants.LEVEL_EASY
        elif self.difficulty == "MEDIUM": return constants.LEVEL_MEDIUM
        elif self.difficulty == "EXTREME": return constants.LEVEL_EXTREME
        elif self.difficulty == "CRAZY": return constants.LEVEL_CRAZY
        return constants.LEVEL_EASY

    def draw(self):
        pyxel.blt(self.x, self.y, *self.__sprite)

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