import constants
import pyxel

class Conveyor:
    """ 
    This class represents the conveyor belt in the game. 
    """
    def __init__(self, x: int, y: int, length: int, speed: float, direction: int):
        self.x = x
        self.y = y
        # number of times the sprite repeats
        self.length = length
        self.speed = speed
        self.direction = direction

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

    @property
    def length(self) -> int:
        return self.__length
    @length.setter
    def length(self, length: int):
        if not isinstance(length, int):
            raise TypeError("length must be an integer")
        self.__length = length

    @property
    def speed(self) -> float:
        return self.__speed
    @speed.setter
    def speed(self, speed: float):
        if not isinstance(speed, (int, float)):
            raise TypeError("speed must be a number")
        self.__speed = speed

    @property
    def direction(self) -> int:
        return self.__direction
    @direction.setter
    def direction(self, value: int):
        if not isinstance(value, int) or value not in [-1, 1]:
            raise ValueError("Direction must be -1 or 1")
        self.__direction = value

    @property
    def width_px(self) -> int:
        """ Returns the total pixel width of the conveyor. """
        return self.length * constants.CONVEYOR_SPRITE[3]
    
    @property
    def end_x(self) -> int:
        """ Returns the X coordinate where the conveyor ends. """
        return self.x + self.width_px

    def draw(self):
        """
        Draws the conveyor belt.
        Left Side: Full Sprite + Left Half pixels left
        Right Side: Right Half pixels left + Full Sprite
        """
        sprite_width = constants.CONVEYOR_SPRITE[3]
        for conv in range(self.length):
            x_pos = self.x + (conv * sprite_width)
            pyxel.blt(x_pos, self.y, *constants.CONVEYOR_SPRITE)