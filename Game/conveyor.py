import constants
import pyxel

class Conveyor:
    """ 
    This class represents the conveyor belt in the game. 
    """
    def __init__(self, speed: float, length: int, y_pos: int, direction: int):
        """ This is the magic method we must use to declare the attributes of our objects.
        :param speed: int - The speed of the conveyor belt
        :param y_pos: The y-coordinate of the conveyor belt.
        :param length: The length of the conveyor belt.
        :param direction: The direction of the conveyor belt (-1 for left, 1 for right).

        """
        # Attributes must always start by self.
        self.speed = speed
        self.length = length
        self.y_pos = y_pos
        self.direction = direction

    @property
    def speed(self) -> float:
        """ This is the getter method for the speed attribute """
        return self.__speed
    
    @speed.setter
    def speed(self, speed: float):
        """ This is the setter method for the speed attribute """
        if not isinstance(speed, float):
            raise TypeError("The speed must be an integer")
        self.__speed = speed

    @property
    def length(self) -> int:
        """ This is the getter method for the length attribute """
        return self.__length
    
    @length.setter
    def length(self, length: int):
        """ This is the setter method for the length attribute """
        if not isinstance(length, int):
            raise TypeError("The length must be an integer")
        self.__length = length

    @property
    def y_pos(self) -> int:
        """ This is the getter method for the y_pos attribute """
        return self.__y_pos
    
    @y_pos.setter
    def y_pos(self, y_pos: int):
        """ This is the setter method for the y_pos attribute """
        if not isinstance(y_pos, int):
            raise TypeError("The y position must be an integer")
        self.__y_pos = y_pos

    @property
    def direction(self) -> int:
        return self.__direction
    
    @direction.setter
    def direction(self, value: int):
        if not isinstance(value, int) or value not in [-1, 1]:
            raise ValueError("Direction must be -1 (left) or 1 (right)")
        self.__direction = value

    def draw(self):
        """
        Draws the conveyor belt on the screen.
        """
        sprite_width = constants.CONVEYOR_SPRITE[3]
        num_sprites = self.length // sprite_width
        for conv in range(num_sprites):
            x = constants.CONVEYOR_X_LEFT + conv * sprite_width
            pyxel.blt(x, self.y_pos, *constants.CONVEYOR_SPRITE)