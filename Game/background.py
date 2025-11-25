import pyxel
import constants

class GameObject:
    """
    Parent class for all static objects in the game.
    Handles coordinate validation to avoid repetition.
    """
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

# We apply inheritance for simple objects

class ExitSignal(GameObject):
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.EXIT_SIGNAL_SPRITE)

class Machine(GameObject):
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.MACHINE_SPRITE)

class Window(GameObject):
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.WINDOW_SPRITE)

# Specific classes with unique attributes

class LevelSign(GameObject):
    def __init__(self, difficulty: str, x: int, y: int):
        # Initialize x and y using the parent class
        super().__init__(x, y)
        # Private method with double underscore
        self.sprite = self.__get_sprite(difficulty)

    def __get_sprite(self, difficulty: str):
        """ Private auxiliary method to select the sprite """
        if difficulty == "EASY":
            return constants.LEVEL_EASY
        elif difficulty == "MEDIUM":
            return constants.LEVEL_MEDIUM
        elif difficulty == "EXTREME":
            return constants.LEVEL_EXTREME
        elif difficulty == "CRAZY":
            return constants.LEVEL_CRAZY
        else:
            return constants.LEVEL_EASY

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite)

class VerticalStructure(GameObject):
    def __init__(self, x: int, width: int, top_limit_y: int, base_y: int):
        super().__init__(x, base_y) 
        self.width = width
        self.top_limit_y = top_limit_y
        self.base_y = base_y

    @property
    def width(self) -> int:
        return self.__width
    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("width must be an integer")
        self.__width = width

    @property
    def top_limit_y(self) -> int:
        return self.__top_limit_y
    @top_limit_y.setter
    def top_limit_y(self, top_limit_y: int):
        if not isinstance(top_limit_y, int):
            raise TypeError("top_limit_y must be an integer")
        self.__top_limit_y = top_limit_y

    @property
    def base_y(self) -> int:
        return self.__base_y
    @base_y.setter
    def base_y(self, base_y: int):
        if not isinstance(base_y, int):
            raise TypeError("base_y must be an integer")
        self.__base_y = base_y

    def draw(self):
        img, u, v, w, h, colkey = constants.VERTICAL_STRUCTURE_SPRITE
        current_y = self.base_y
        
        while current_y > self.top_limit_y:
            current_y -= h
            for structure in range(self.width):
                x_pos = self.x + structure * w
                draw_w = -w if structure % 2 != 0 else w
                pyxel.blt(x_pos, current_y, img, u, v, draw_w, h, colkey)