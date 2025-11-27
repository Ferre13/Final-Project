import constants
import pyxel
import random

class Conveyor:
    """ 
    This class represents the conveyor belt in the game. 
    It manages its own speed calculation based on difficulty.
    """
    def __init__(self, x: int, y: int, length: int, direction: int, difficulty: str, level_index: int):
        self.x = x
        self.y = y
        self.length = length
        self.direction = direction
        
        # Private attributes for calculation
        self.__difficulty = difficulty
        self.__level_index = level_index
        
        # Calculate speed immediately
        self.speed = self.__calculate_speed()

    # --- GETTERS AND SETTERS ---

    @property
    def x(self) -> int:
        return self.__x
    
    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("x must be an integer")
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError("y must be an integer")
        self.__y = value

    @property
    def length(self) -> int:
        return self.__length

    @length.setter
    def length(self, value: int):
        if not isinstance(value, int):
            raise TypeError("length must be an integer")
        self.__length = value

    @property
    def direction(self) -> int:
        return self.__direction

    @direction.setter
    def direction(self, value: int):
        if value not in [1, -1]:
            raise ValueError("Direction must be 1 (right) or -1 (left)")
        self.__direction = value

    @property
    def speed(self) -> float:
        return self.__speed

    @speed.setter
    def speed(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("speed must be a number")
        self.__speed = float(value)

    # --- READ-ONLY CALCULATED PROPERTIES ---

    @property
    def width_px(self) -> int:
        """ Returns the total width of the conveyor in pixels """
        return self.length * constants.CONVEYOR_SPRITE[3]

    @property
    def end_x(self) -> int:
        """ Returns the X coordinate where the conveyor ends """
        return self.x + self.width_px

    # --- INTERNAL METHODS ---

    def __calculate_speed(self) -> float:
        """
        Determines speed based on the constants and rules.
        """
        # Machine belt (Level 0) is always slow
        if self.__level_index == 0:
            return constants.SLOW_SPEED

        # Odd/Even Logic (Note: Level 1 is Odd, Level 2 is Even)
        is_odd_belt = (self.__level_index % 2 != 0)

        if self.__difficulty == "EASY":
            return constants.SLOW_SPEED
            
        elif self.__difficulty == "MEDIUM":
            if is_odd_belt: return constants.MEDIUM_SPEED
            else: return constants.SLOW_SPEED
            
        elif self.__difficulty == "EXTREME":
            if is_odd_belt: return constants.HIGH_SPEED
            else: return constants.MEDIUM_SPEED
            
        elif self.__difficulty == "CRAZY":
            # Random speed between Slow and High
            return random.uniform(constants.SLOW_SPEED, constants.HIGH_SPEED)
            
        return constants.SLOW_SPEED

    # --- DRAWING ---

    def draw(self):
        sprite_width = constants.CONVEYOR_SPRITE[3]
        for conv in range(self.length):
            x_pos = self.x + (conv * sprite_width)
            pyxel.blt(x_pos, self.y, *constants.CONVEYOR_SPRITE)