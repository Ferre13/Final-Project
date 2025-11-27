import pyxel
import constants

class GameObject:
    """
    Parent class for all static objects.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self.__x
    
    @x.setter
    def x(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("x must be a number")
        self.__x = int(value)

    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("y must be a number")
        self.__y = int(value)

class ExitSignal(GameObject):
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.EXIT_SIGNAL_SPRITE)

class Machine(GameObject):
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.MACHINE_SPRITE)

class Window(GameObject):
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.WINDOW_SPRITE)

class LevelSign(GameObject):
    def __init__(self, difficulty: str, x: int, y: int):
        super().__init__(x, y)
        self.__sprite = self.__get_sprite(difficulty)

    def __get_sprite(self, difficulty: str):
        if difficulty == "EASY": return constants.LEVEL_EASY
        elif difficulty == "MEDIUM": return constants.LEVEL_MEDIUM
        elif difficulty == "EXTREME": return constants.LEVEL_EXTREME
        elif difficulty == "CRAZY": return constants.LEVEL_CRAZY
        return constants.LEVEL_EASY

    def draw(self):
        pyxel.blt(self.x, self.y, *self.__sprite)

class VerticalStructure(GameObject):
    def __init__(self, x: int, width: int, top_limit_y: int, base_y: int):
        super().__init__(x, base_y) 
        self.width = width
        self.top_limit_y = top_limit_y
        self.base_y = base_y

    @property
    def width(self) -> int: return self.__width
    @width.setter
    def width(self, value: int):
        if not isinstance(value, int): raise TypeError("width must be int")
        self.__width = value

    @property
    def top_limit_y(self) -> int: return self.__top_limit_y
    @top_limit_y.setter
    def top_limit_y(self, value: int):
        if not isinstance(value, int): raise TypeError("top_limit_y must be int")
        self.__top_limit_y = value

    @property
    def base_y(self) -> int: return self.__base_y
    @base_y.setter
    def base_y(self, value: int):
        if not isinstance(value, int): raise TypeError("base_y must be int")
        self.__base_y = value

    def draw(self):
        img, u, v, w, h, colkey = constants.VERTICAL_STRUCTURE_SPRITE
        current_y = self.base_y
        
        while current_y > self.top_limit_y:
            current_y -= h
            for structure in range(self.width):
                x_pos = self.x + (structure * w)
                
                # Removed Ternary Operator
                if structure % 2 != 0:
                    draw_w = -w
                else:
                    draw_w = w
                
                pyxel.blt(x_pos, current_y, img, u, v, draw_w, h, colkey)