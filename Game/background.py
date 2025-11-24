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
    def __init__(self, x: int, width: int, top_limit_y: int, base_y: int = constants.SCREEN_HEIGHT):
        self.x = x
        self.width = width
        self.top_limit_y = top_limit_y
        self.base_y = base_y 

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
        img, u, v, w, h, colkey = constants.VERTICAL_STRUCTURE_SPRITE

        # Start from the base (ground level)
        current_draw_y = self.base_y
        
        # Keep adding segments upwards until we are ABOVE the top conveyor limit
        # The loop runs at least once, and continues as long as the current top is below the limit
        while current_draw_y > self.top_limit_y:
            # Move cursor up for the next segment
            current_draw_y -= h
            
            for structure in range(self.width):
                x_pos = self.x + structure * w
                if structure % 2 != 0:
                    draw_w = -w
                else:
                    draw_w = w

                pyxel.blt(x_pos, current_draw_y, img, u, v, draw_w, h, colkey)

class Window:
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
        pyxel.blt(self.x, self.y, *constants.WINDOW_SPRITE)

class LevelSign:
    def __init__(self, difficulty: str, x: int, y: int):
        self.x = x
        self.y = y
        self.sprite = self._get_sprite(difficulty)

    def _get_sprite(self, difficulty: str):
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