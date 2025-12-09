import constants
import random
from game_platform import Platform

class Conveyor(Platform):
    """Represents a conveyor belt that moves packages, inheriting from Platform."""
    def __init__(self, x: int, y: int, width: int, direction: int, difficulty: str, level_index: int):
        """
        :param x: The starting x-coordinate.
        :param y: The y-coordinate.
        :param width: The number of tiles for the conveyor's width.
        :param direction: The direction of movement (-1 for left, 1 for right).
        :param difficulty: The current game difficulty.
        :param level_index: The floor number of the conveyor.
        """
        super().__init__(x, y, width, sprite = constants.CONVEYOR_SPRITE)
        self.direction = direction
        self.__difficulty = difficulty
        self.__level_index = level_index
        self.speed = self.__calculate_speed()
        self.width_px = self.width * constants.CONVEYOR_SPRITE_W

    @property
    def direction(self) -> int:
        """The direction the conveyor moves (-1 for left, 1 for right)."""
        return self.__direction
    @direction.setter
    def direction(self, value: int):
        if value not in [1, -1]:
            raise ValueError("Direction must be 1 (right) or -1 (left)")
        self.__direction = value

    @property
    def speed(self) -> float:
        """The speed at which the conveyor moves packages."""
        return self.__speed
    @speed.setter
    def speed(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("speed must be a number")
        self.__speed = float(value)

    # Returns the x-coordinate where the conveyor ends. We use a read-only property for this.
    @property
    def end_x(self) -> int:
        """The x-coordinate where the conveyor ends."""
        return self.x + self.width_px

    def __calculate_speed(self) -> float:
        """Determines the conveyor's speed based on difficulty and level."""
        # The machine conveyor always has the slowest speed
        if self.__level_index == 0:
            return constants.SLOW_SPEED

        if self.__level_index % 2 != 0:
            is_odd_belt = True
        else:
            is_odd_belt = False

        if self.__difficulty == "EASY":
            return constants.SLOW_SPEED
        elif self.__difficulty == "MEDIUM":
            if is_odd_belt: 
                return constants.MEDIUM_SPEED
            else: 
                return constants.SLOW_SPEED
        elif self.__difficulty == "EXTREME":
            if is_odd_belt: 
                return constants.HIGH_SPEED
            else: 
                return constants.MEDIUM_SPEED
        elif self.__difficulty == "CRAZY":
            return random.uniform(constants.SLOW_SPEED, constants.HIGH_SPEED)