import constants
import pyxel
import random

class Conveyor:
    """ 
    Represents a conveyor belt in the game. It is responsible for
    calculating its own speed based on the game's difficulty level
    and its position in the factory.
    """
    def __init__(self, x: int, y: int, length: int, direction: int, difficulty: str, level_index: int):
        """
        Initializes a conveyor belt.

        :param x: The starting x-coordinate.
        :param y: The y-coordinate.
        :param length: The number of sprite tiles the conveyor is long.
        :param direction: The direction of movement (-1 for left, 1 for right).
        :param difficulty: The current game difficulty string.
        :param level_index: The floor number of the conveyor.
        """
        self.x = x
        self.y = y
        self.length = length
        self.direction = direction
        
        self.__difficulty = difficulty
        self.__level_index = level_index
        
        # Speed is calculated once upon creation based on the game rules.
        self.speed = self.__calculate_speed()

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value: int):
        """Sets the x-coordinate."""
        if not isinstance(value, int):
            raise TypeError("x must be an integer")
        self.__x = value

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, value: int):
        """Sets the y-coordinate."""
        if not isinstance(value, int):
            raise TypeError("y must be an integer")
        self.__y = value

    @property
    def length(self) -> int: return self.__length
    @length.setter
    def length(self, value: int):
        """Sets the length of the conveyor in sprite tiles."""
        if not isinstance(value, int):
            raise TypeError("length must be an integer")
        self.__length = value

    @property
    def direction(self) -> int: return self.__direction
    @direction.setter
    def direction(self, value: int):
        """Sets the direction of the conveyor's movement."""
        if value not in [1, -1]:
            raise ValueError("Direction must be 1 (right) or -1 (left)")
        self.__direction = value

    @property
    def speed(self) -> float: return self.__speed
    @speed.setter
    def speed(self, value: float):
        """Sets the speed of the conveyor."""
        if not isinstance(value, (int, float)):
            raise TypeError("speed must be a number")
        self.__speed = float(value)

    @property
    def width_px(self) -> int:
        """Returns the total width of the conveyor in pixels."""
        return self.length * constants.CONVEYOR_SPRITE[3]

    @property
    def end_x(self) -> int:
        """Returns the X coordinate where the conveyor ends."""
        return self.x + self.width_px

    def __calculate_speed(self) -> float:
        """
        Determines the conveyor's speed based on game difficulty and its level.
        """
        # The first belt (level 0) where packages spawn is always slow.
        if self.__level_index == 0:
            return constants.SLOW_SPEED

        # In this game, odd-numbered floors (1, 3, 5...) are handled by Luigi
        # and even-numbered floors (2, 4, 6...) are handled by Mario.
        is_odd_belt = (self.__level_index % 2 != 0)

        if self.__difficulty == "EASY":
            return constants.SLOW_SPEED
            
        elif self.__difficulty == "MEDIUM":
            # Odd belts (Luigi's) are faster.
            if is_odd_belt: return constants.MEDIUM_SPEED
            else: return constants.SLOW_SPEED
            
        elif self.__difficulty == "EXTREME":
            # Both belts are faster, but odd belts (Luigi's) are fastest.
            if is_odd_belt: return constants.HIGH_SPEED
            else: return constants.MEDIUM_SPEED
            
        elif self.__difficulty == "CRAZY":
            # Speed is unpredictable.
            return random.uniform(constants.SLOW_SPEED, constants.HIGH_SPEED)
            
        return constants.SLOW_SPEED

    def draw(self):
        """Draws the conveyor by tiling its sprite horizontally."""
        sprite_width = constants.CONVEYOR_SPRITE[3]
        for i in range(self.length):
            x_pos = self.x + (i * sprite_width)
            pyxel.blt(x_pos, self.y, *constants.CONVEYOR_SPRITE)